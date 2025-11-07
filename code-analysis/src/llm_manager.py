import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_NAME, MAX_CONTEXT_TOKENS


class LLMManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
    
    def load_model(self):
        if self.model is not None:
            return
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading model: {MODEL_NAME}")
        print(f"Device: {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        
        self.model.eval()
        
        print("Model loaded successfully")
    
    def generate(self, prompt, max_new_tokens=256):
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_CONTEXT_TOKENS)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        response = generated_text[len(prompt):].strip()
        
        return response
    
    def unload_model(self):
        if self.model is not None:
            del self.model
            del self.tokenizer
            if self.device == "cuda":
                torch.cuda.empty_cache()
            self.model = None
            self.tokenizer = None
            print("Model unloaded")

