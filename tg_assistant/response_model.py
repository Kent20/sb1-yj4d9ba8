from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List
import logging

class ResponseGenerator:
    def __init__(self, model_name: str = "gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
    def generate_responses(self, message: str, num_responses: int = 3) -> List[str]:
        """
        Generate multiple response suggestions for a given message
        """
        try:
            inputs = self.tokenizer.encode(message, return_tensors="pt").to(self.device)
            
            # Generate multiple responses with different sampling parameters
            responses = []
            for _ in range(num_responses):
                outputs = self.model.generate(
                    inputs,
                    max_length=50,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    temperature=0.7,
                )
                
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                responses.append(response)
            
            return responses
            
        except Exception as e:
            logging.error(f"Error generating responses: {str(e)}")
            return []