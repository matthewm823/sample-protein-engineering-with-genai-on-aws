
import logging
import os
import json  
from transformers import AutoModel, AutoTokenizer
import torch

logging.basicConfig(level=logging.INFO)

def model_fn(model_dir):
    logging.info("[custom] model_fn: Starting the model loading process...")

    try:
        model_id = os.getenv('AMPLIFY_MODEL_ID', 'chandar-lab/AMPLIFY_120M')
        logging.info(f"[custom] model_fn: Model id is {model_id}")

        model = AutoModel.from_pretrained(model_id, trust_remote_code=True)
        logging.info(f"[custom] model_fn: Successfully loaded the model: {model}")

        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        logging.info(f"[custom] model_fn: Successfully loaded the tokenizer: {tokenizer}")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(device)
        logging.info(f"[custom] model_fn: Moved model to {device} device")

        return model, tokenizer, device

    except Exception as e:        
        logging.error(f"[custom] model_fn: Error occurred while loading the model and tokenizer: {str(e)}", exc_info=True)
        raise e

def input_fn(request_body, content_type='application/json'):
    logging.info("input_fn: Received input")
    if content_type == 'application/json':
        input_data = json.loads(request_body)  
        sequence = input_data['sequence']
        mode = input_data.get('mode','logits')
        return sequence, mode
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

def predict_fn(input_data, model_artifacts):
    logging.info("predict_fn: Running inference")
    sequence, mode = input_data
    model, tokenizer, device = model_artifacts
    
    inputs = tokenizer.encode(sequence, return_tensors="pt")
    inputs = inputs.to(device)

    with torch.no_grad():
        if mode == 'logits':
            output = model(inputs)
        elif mode == 'embeddings':
            output = model(inputs, output_hidden_states=True)
        else:
            raise ValueError(f"Unknown mode: {mode}")            

    return output, mode

def output_fn(prediction, accept='application/json'):
    logging.info("output_fn: Formatting output")
    output, mode = prediction
    
    if accept == 'application/json':
        if mode == 'logits':
            if hasattr(output, 'logits'):
                result = output.logits
            else:
                raise ValueError(f"Unknown prediction format: {type(output)}")
        elif mode == 'embeddings':
            if hasattr(output, 'hidden_states'):
                result = output.hidden_states[-1]
            else:
                raise ValueError(f"Unknown prediction format: {type(output)}")
        else:
            raise ValueError(f"Unknown mode: {mode}")
        return json.dumps({mode: result.tolist()}), accept
    else:
        raise ValueError(f"Unsupported accept type: {accept}")
