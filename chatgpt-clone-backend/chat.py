import torch
from model import BigramLanguageModel
from data import load_data

device = 'cuda' if torch.cuda.is_available() else 'cpu'
block_size = 128
save_path = 'model_weights.pth'

# Load data
_, vocab_size, stoi, itos, encode, decode = load_data('data.txt')

# Initialize model
model = BigramLanguageModel(vocab_size, 384, 6, 6, block_size, 0.2).to(device)
model.load_state_dict(torch.load(save_path))
model.eval()

def chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        context = torch.tensor(encode(user_input), dtype=torch.long, device=device).unsqueeze(0)
        response = decode(model.generate(context, max_new_tokens=100, block_size=block_size)[0].tolist())
        print(f"Response: {response}")

if __name__ == "__main__":
    chat()
