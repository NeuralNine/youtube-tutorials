const { useRef, useEffect, useState } = React;

const getWebSocketURL = () => {
	const url = new URL(window.location.href);
	const hostname = url.hostname.replace('-web', '-moshi-web');
	const protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';

	return `${protocol}//${hostname}/ws`;
}

const App = () => {
	const [audioContext] = useState(() => new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 48000 }));
	const [text, setText] = useState('');

	const socketRef = useRef(null);
	const decoderRef = useRef(null);
	const scheduledEndRef = useRef(null);

	const startRecording = async () => {
		const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

		const rec = new Recorder({
			encoderPath: "https://cdn.jsdelivr.net/npm/opus-recorder@latest/dist/encoderWorker.min.js",
			streamPages: true,
			encoderApplication: 2049,
			encoderFrameSize: 80,
			encoderSampleRate: 24000,
			maxFramesPerPage: 1,
			numberOfChannels: 1,
		});

		rec.ondataavailable = async (data) => {
			if (socketRef.current?.readyState === WebSocket.OPEN) {
				await socketRef.current.send(data);
			}
		};

		await rec.start();
	};

	useEffect(() => {
		const init = async () => {
			const decoder = new window['ogg-opus-decoder'].OggOpusDecoder();
			await decoder.ready;

			decoderRef.current = decoder;
		};
		init();
		return () => decoderRef.current?.free();
	}, []);

	const playAudio = (audioData)=> {
		const buffer = audioContext.createBuffer(1, audioData.length, audioContext.sampleRate);
		buffer.copyToChannel(audioData, 0);

		const source = audioContext.createBufferSource();
		source.buffer = buffer;
		source.connect(audioContext.destination);

		const startTime = Math.max(scheduledEndRef.current, audioContext.currentTime);
		source.start(startTime);
		scheduledEndRef.current = startTime + buffer.duration;
	};

	useEffect(() => {
		const socket = new WebSocket(getWebSocketURL());
		socketRef.current = socket;

		socket.onopen = () => startRecording();

		socket.onmessage = async (event) => {
			const buffer = await event.data.arrayBuffer();
			const tag = new Uint8Array(buffer)[0];
			const payload = buffer.slice(1);

			if (tag === 1) {
				const { channelData, samplesDecoded } = await decoderRef.current.decode(new Uint8Array(payload));
				if (samplesDecoded > 0) playAudio(channelData[0]);
			} else if (tag === 2) {
				const newText = new TextDecoder().decode(payload);
				setText(prev => prev + newText);
			}
		};

		return () => socket.close();
	}, []);

	return (
		<div className="bg-gray-900 text-white min-h-screen flex items-center justify-center p-4">
			<div className="bg-gray-800 rounded-lg shadow-lg w-full max-w-xl p-6">
				<p className="text-gray-300 break-words">
					{text || 'Connecting...'}
				</p>
			</div>
		</div>
	);

};

ReactDOM.createRoot(document.getElementById("react")).render(<App />);
