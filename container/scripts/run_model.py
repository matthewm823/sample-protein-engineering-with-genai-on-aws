import json
import argparse
from transformers import AutoModelForCausalLM
from tokenizers import Tokenizer
import torch
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO


def run_model(
        model_id,
        params_file,
        batch_id,
        batch_size,
        batch_number,
        output_file
    ):
    
    # Load model and tokenizer 
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    tokenizer = Tokenizer.from_pretrained(model_id)
    tokenizer.no_padding()

    # put model on cuda or cpu
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    # load prompts with parameters and identify a subset of prompts to be processed
    with open(params_file, 'r') as f:
        inference_configurations = json.load(f)['inference-params']

    start_idx = batch_size*batch_number
    end_idx = min(start_idx +  batch_size, len(inference_configurations))
    
    
    # Generate sequences
    fasta_records = []
    for i in range(start_idx, end_idx):
        inf_config = inference_configurations[i]
        prompt_id = inf_config['prompt_id']
        prompt = inf_config['prompt']
        temperature = inf_config['temperature']
        max_length = inf_config['max_length']
        top_k = inf_config['top_k']
        top_p = inf_config['top_p']
        
        # Tokenize input
        input_ids = torch.tensor(tokenizer.encode(prompt).ids).to(device)
                
        # Generate sequence
        pad_token_id = tokenizer.encode('<|pad|>').ids[0]
        output = model.generate(
            input_ids.unsqueeze(0),
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            top_k=int(top_k),
            num_return_sequences=1,
            do_sample=True,
            pad_token_id=pad_token_id
        )

        # Decode sequence and add to fasta records
        sequence = tokenizer.decode(output[0].tolist())
        print(f'Prompt id: {prompt_id}, Generated sequence: {sequence}')
    
        fasta_record = SeqRecord(
            Seq(sequence), 
            id=prompt_id, 
            description=','.join([
                f'max_len:{max_length}',
                f'temp:{temperature}',
                f'top_k:{top_k}',
                f'top_p:{top_p}',
                f'prompt:{prompt}'
            ])
        )
                
        fasta_records.append(fasta_record)


    # Save all generated sequences to FASTA file
    with open(output_file, "w") as f:
        SeqIO.write(fasta_records, f, "fasta")



def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Entrypoint"
    )
    parser.add_argument("--model_id",
                        help="Hugging Face model id", default="hugohrban/progen2-small")
    parser.add_argument("--params_file",
                        help="Path to json file with prompts and parameters to generate protein sequences")
    parser.add_argument("--batch_id",
                        help="ID of batch job")
    parser.add_argument("--batch_size", help="number of pormts per batch job", type=int, default=10)
    parser.add_argument("--batch_number",
                        help="batch number", type=int, default=0)
    parser.add_argument("--output_file",
                        help="Paht to FASTA file with generated seuqneces")
                    
                        
    return parser.parse_args()


def main():
    args = parse_arguments()
    run_model(
        model_id=args.model_id,
        params_file=args.params_file,
        batch_id=args.batch_id,
        batch_size=args.batch_size,
        batch_number=args.batch_number,
        output_file=args.output_file
    )
    
if __name__ == "__main__":
    main()    