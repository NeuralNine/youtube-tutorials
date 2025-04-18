import random

import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('shakespeare.txt', 'r') as f:
    text = f.read().lower()[:50000]

chars = sorted(set(text))
vocab_size = len(chars)

char2idx = {c: i for i, c in enumerate(chars)}
idx2char = {i: c for c, i in char2idx.items()}

seq_length = 100
step_size = 1
data = [(text[i:i+seq_length], text[i+seq_length]) for i in range(0, len(text)-seq_length, step_size)]

X = torch.tensor([[char2idx[c] for c in seq] for seq, _ in data]).to(device)
y = torch.tensor([char2idx[c] for _, c in data]).to(device)


class CharLSTM(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers=1):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embed(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out[:, -1, :])

        return out, hidden


model = CharLSTM(vocab_size, hidden_size=256).to(device)
optimizer = optim.Adam(model.parameters(), lr=0.0003)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    model.train()
    running_loss = 0.0

    for i in range(0, len(X), 64):
        x_batch = X[i:i+64].to(device)
        y_batch = y[i:i+64].to(device)

        if len(x_batch) == 0:
            continue

        optimizer.zero_grad()
        output, _ = model(x_batch)
        loss = criterion(output, y_batch)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f'Epoch {epoch+1}/20, Loss: {running_loss:.4f}')


def generate_text(model, start_seq, length=200):
    model.eval()

    input_seq = torch.tensor([[char2idx[c] for c in start_seq]]).to(device)
    hidden = None

    result = start_seq

    for _ in range(length):
        output, hidden = model(input_seq, hidden)
        probs = torch.softmax(output, dim=-1).squeeze()
        next_idx = torch.multinomial(probs, 1).item()
        next_char = idx2char[next_idx]
        result += next_char

        input_seq = torch.tensor([[next_idx]]).to(device)

    return result


print(generate_text(model, 'he was going with'))
print(generate_text(model, 'why is it'))
print(generate_text(model, 'we must all'))

torch.save(model.state_dict(), 'lstm_model.pth')
