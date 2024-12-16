from typing import List, Optional
from .base import BaseResponseGenerator

class TransformerResponseGenerator(BaseResponseGenerator):
    """Response generator that uses transformer models"""
    
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
    
    def _load_model(self):
        """Lazy loading of the model"""
        if self.model is None:
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                import torch
                
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
                self.model.to(self.device)
            except ImportError:
                raise ImportError(
                    "transformers package is required for TransformerResponseGenerator. "
                    "Install it with: pip install transformers torch"
                )
    
    def generate_responses(self, message: str, num_responses: int = 3) -> List[str]:
        """Generate responses using the transformer model"""
        try:
            self._load_model()
            
            inputs = self.tokenizer.encode(message, return_tensors="pt").to(self.device)
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
            # Fallback to simple responses if model fails
            from .simple import SimpleResponseGenerator
            generator = SimpleResponseGenerator()
            return generator.generate_responses(message, num_responses)