import torch
import torch.optim as optim
from model import BigramLanguageModel
from data import load_data, get_batch
import os

# Hyperparameters
batch_size = 16
block_size = 128
max_iters = 50
eval_interval = 500
#learning_rate = 3e-4
learning_rate = 0.9
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
n_embd = 384
n_head = 6
n_layer = 6
dropout = 0.2
save_path = 'model_weights.pth'

def train():
    # Load data
    data, vocab_size, stoi, itos, encode, decode = load_data('data.txt')
    n = int(0.9 * len(data))
    train_data = data[:n]
    val_data = data[n:]

    @torch.no_grad()
    def estimate_loss(model):
        out = {}
        model.eval()
        for split in ['train', 'val']:
            losses = torch.zeros(eval_iters)
            for k in range(eval_iters):
                X, Y = get_batch(train_data if split == 'train' else val_data, block_size, batch_size, device)
                logits, loss = model(X, Y)
                losses[k] = loss.item()
            out[split] = losses.mean()
        model.train()
        return out

    # Initialize model
    model = BigramLanguageModel(vocab_size, n_embd, n_layer, n_head, block_size, dropout).to(device)
    if os.path.exists(save_path):
        model.load_state_dict(torch.load(save_path))

    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
    best_val_loss = float('inf')

    for iter in range(max_iters):
        #if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss(model)
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
        if losses['val'] < best_val_loss:
            best_val_loss = losses['val']
            torch.save(model.state_dict(), save_path)
            print(f"Validation loss improved. Model weights saved.")

        xb, yb = get_batch(train_data, block_size, batch_size, device)
        logits, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
