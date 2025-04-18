import random

import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('shakespeare.txt', 'r') as f:
    text = f.read().lower()[:200000]


words = text.split()
vocab = sorted(set(words))

word2idx = {w: i for i, w in enumerate(vocab)}
idx2word = {i: w for w, i in word2idx.items()}

vocab_size = len(vocab)

seq_length = 5
data = [(words[i:i+seq_length], words[i+seq_length]) for i in range(0, len(words) - seq_length)]

X = torch.tensor([[word2idx[w] for w in seq] for seq, _ in data]).to(device)
y = torch.tensor([word2idx[w] for _, w in data]).to(device)


class CharRNNAttention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim, batch_first=True)
        self.attention = nn.Linear(hidden_dim, 1)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embed(x)
        out, _ = self.rnn(x)
        attn_weights = nn.functional.softmax(self.attention(out).squeeze(2), dim=1)

        context = torch.sum(attn_weights.unsqueeze(2) * out, dim=1)
        out = self.fc(context)

        return out


model = CharRNNAttention(vocab_size, 128, 256).to(device)

optimizer = optim.Adam(model.parameters(), lr=0.003)
criterion = nn.CrossEntropyLoss()

for epoch in range(20):
    model.train()
    running_loss = 0.0

    for i in range(0, len(X), 64):
        x_batch = X[i:i+64].to(device)
        y_batch = y[i:i+64].to(device)

        if len(x_batch) == 0:
            continue

        optimizer.zero_grad()
        outputs = model(x_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f'Epoch {epoch+1}/20, Loss: {running_loss:.4f}')


def generate_text(model, start_words, num_words=20):
    model.eval()
    generated = start_words[:]
    
    for _ in range(num_words):
        current_seq = generated[-seq_length:] if len(generated) >= seq_length else generated

        if len(current_seq) < seq_length:
            current_seq = [""] * (seq_length - len(current_seq)) + current_seq

        idx_seq = [word2idx[w] if w in word2idx else 0 for w in current_seq]
        input_seq = torch.tensor([idx_seq], dtype=torch.long).to(device)

        with torch.no_grad():
            logits = model(input_seq)
            probs = torch.softmax(logits, dim=-1).squeeze(0)
            next_idx = torch.multinomial(probs, 1).item()

        next_word = idx2word[next_idx]
        generated.append(next_word)

    return ' '.join(generated)

print(generate_text(model, ['he', 'was', 'going', 'with'], num_words=30))
print(generate_text(model, ['why', 'is', 'it'], num_words=30))
print(generate_text(model, ['we', 'must', 'all'], num_words=30))

torch.save(model.state_dict(), 'attention_model.pth')
