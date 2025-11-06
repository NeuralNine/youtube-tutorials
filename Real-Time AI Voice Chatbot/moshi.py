import asyncio

import modal

from .common import app

model_path = '/models'
volume = modal.Volume.from_name('model_cache', create_if_missing=True)

image = modal.Image.debian_slim(python_version='3.11')
image = image.pip_install('moshi', 'sphn', 'fastapi', 'huggingface_hub')
image = image.env({'HF_HUB_CACHE': model_path})


with image.imports():
    import torch
    import numpy as np

    import sphn
    import sentencepiece

    from huggingface_hub import hf_hub_download
    from moshi.models import loaders, LMGen


@app.cls(image=image, gpu='A10G', timeout=600, volumes={model_path: volume})
class Moshi:

    @modal.enter()
    def setup(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        mimi_weights = hf_hub_download(loaders.DEFAULT_REPO, loaders.MIMI_NAME)

        self.mimi = loaders.get_mimi(mimi_weights, device=self.device)
        self.mimi.set_num_codebooks(8)
        self.frame_size = int(self.mimi.sample_rate / self.mimi.frame_rate)

        moshi_weights = hf_hub_download(loaders.DEFAULT_REPO, loaders.MOSHI_NAME)

        self.moshi = loaders.get_moshi_lm(moshi_weights, device=self.device)
        self.lm_gen = LMGen(self.moshi, temp=0.8, top_k=250)

        self.mimi.streaming_forever(1)
        self.lm_gen.streaming_forever(1)

        tokenizer_path = hf_hub_download(loaders.DEFAULT_REPO, loaders.TEXT_TOKENIZER_NAME)
        self.text_tokenizer = sentencepiece.SentencePieceProcessor(tokenizer_path)

        for _ in range(4):
            chunk = torch.zeros(1, 1, self.frame_size, dtype=torch.float32, device=self.device)
            codes = self.mimi.encode(chunk)

            for c in range(codes.shape[-1]):
                output_tokens = self.lm_gen.step(codes[:, :, c:c+1])

                if output_tokens is not None:
                    self.mimi.decode(output_tokens[:, 1:])

        torch.cuda.synchronize()

    @modal.asgi_app()
    def web(self):
        from fastapi import FastAPI, WebSocket

        web_app = FastAPI()

        @web_app.websocket('/ws')
        async def websocket(ws: WebSocket):
            await ws.accept()

            self.mimi.reset_streaming()
            self.lm_gen.reset_streaming()

            opus_in = sphn.OpusStreamReader(self.mimi.sample_rate)
            opus_out = sphn.OpusStreamWriter(self.mimi.sample_rate)

            async def recieve():
                while True:
                    data = await ws.receive_bytes()

                    if isinstance(data, bytes) and len(data) > 0:
                        opus_in.append_bytes(data)

            async def process():
                pcm_buffer = None

                while True:
                    await asyncio.sleep(0.001)
                    pcm = opus_in.read_pcm()

                    if pcm is None or len(pcm) == 0:
                        continue

                    pcm_buffer = pcm if pcm_buffer is None else np.concatenate([pcm_buffer, pcm])

                    while pcm_buffer.shape[-1] >= self.frame_size:
                        chunk = torch.from_numpy(pcm_buffer[:self.frame_size]).to(self.device)[None, None]

                        pcm_buffer = pcm_buffer[self.frame_size:]

                        codes = self.mimi.encode(chunk)

                        for c in range(codes.shape[-1]):
                            output_tokens = self.lm_gen.step(codes[:, :, c:c+1])

                            if output_tokens is not None:
                                audio = self.mimi.decode(output_tokens[:, 1:])
                                opus_out.append_pcm(audio[0,0].cpu().numpy())

                                text_token = output_tokens[0,0,0].item()
                                if text_token not in (0, 3):
                                    text = self.text_tokenizer.id_to_piece(text_token).replace('▁', ' ')

                                    await ws.send_bytes(b'\x02' + text.encode('utf-8'))

            async def send():
                while True:
                    await asyncio.sleep(0.001)

                    audio = opus_out.read_bytes()

                    if audio and len(audio) > 0:
                        await ws.send_bytes(b'\x01' + audio)

            try:
                with torch.no_grad():
                    tasks = [asyncio.create_task(recieve()), asyncio.create_task(process()), asyncio.create_task(send())]
                    await asyncio.gather(*tasks)
            except Exception as e:
                print(f'Error {e}, {str(e)}')
                for task in tasks:
                    task.cancel()

        return web_app


