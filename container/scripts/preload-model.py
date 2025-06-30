from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer

def main():
    # download model
    model = AutoModelForCausalLM.from_pretrained("hugohrban/progen2-small", trust_remote_code=True)
    tokenizer = Tokenizer.from_pretrained("hugohrban/progen2-small")
    
if __name__ == "__main__":
    main()