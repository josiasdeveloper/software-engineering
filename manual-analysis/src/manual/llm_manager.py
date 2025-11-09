import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from manual.config import MODEL_NAME, MAX_CONTEXT_TOKENS

class LLMManager:
    _instance = None
    _model = None
    _tokenizer = None
    _device = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
        return cls._instance
    
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

    def generate(self, prompt, max_new_tokens=512, temperature=0.7, top_p=0.95, 
                 repetition_penalty=1.15, do_sample=True):
        """
        Generate text from prompt with configurable parameters.
        
        Args:
            prompt: Input prompt
            max_new_tokens: Maximum new tokens to generate (default: 512)
            temperature: Controls randomness (0.0-1.0). Higher = more creative (default: 0.7)
            top_p: Nucleus sampling threshold (default: 0.95)
            repetition_penalty: Penalize repetition (default: 1.15)
            do_sample: Whether to use sampling or greedy decoding (default: True)
        """
        inputs = self._tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=MAX_CONTEXT_TOKENS
        )
        inputs = {k: v.to(self._device) for k, v in inputs.items()}
        
        gen_config = {
            "max_new_tokens": max_new_tokens,
            "pad_token_id": self._tokenizer.eos_token_id,
            "eos_token_id": self._tokenizer.eos_token_id,
            "repetition_penalty": repetition_penalty,
        }
        
        
        if do_sample:
            gen_config.update({
                "do_sample": True,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": 50,  # Consider top 50 tokens
            })
        else:
            gen_config["do_sample"] = False
        
        with torch.no_grad():
            outputs = self._model.generate(**inputs, **gen_config)
        
        generated_text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        
        response = generated_text[len(prompt):].strip()
        
        return response



llm_manager = LLMManager() # export singleton instance