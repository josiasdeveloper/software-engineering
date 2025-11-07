import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import MODEL_NAME, MAX_CONTEXT_TOKENS


class LLMManager:
    _instance = None
    _model = None
    _tokenizer = None
    _device = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
        return cls._instance
    
    @property
    def model(self):
        return self._model
    
    @property
    def tokenizer(self):
        return self._tokenizer
    
    @property
    def device(self):
        return self._device
    
    def is_loaded(self):
        return self._model is not None
    
    def load_model(self):
        if self._model is not None:
            return
        
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading model: {MODEL_NAME}")
        print(f"Device: {self._device}")
        
        if self._device == "cpu":
            print("ERROR: No GPU (cuda) detected.")
            print("This model requires GPU to run efficiently.")
            print("In Colab: Runtime -> Change runtime type -> T4 GPU")
            raise Exception("No CUDA device found")
        
        self._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        self._model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        self._model.eval()
        
        print("Model loaded successfully")
    
    def generate(self, prompt, max_new_tokens=256):
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        inputs = self._tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_CONTEXT_TOKENS)
        inputs = {k: v.to(self._device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
                repetition_penalty=1.2,
                pad_token_id=self._tokenizer.eos_token_id
            )
        
        generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        response = generated_text[len(prompt):].strip()
        
        return response
    
    def unload_model(self):
        if self._model is not None:
            del self._model
            del self._tokenizer
            if self._device == "cuda":
                torch.cuda.empty_cache()
            self._model = None
            self._tokenizer = None
            self._device = None
            print("Model unloaded")
