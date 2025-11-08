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
    
    def is_loaded(self):
        return self._model is not None
    
    def load_model(self):
        if self._model is not None:
            return
        
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Carregando modelo: {MODEL_NAME}")
        print(f"Device: {self._device}")
        
        try:
            # Carregar tokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(
                MODEL_NAME,
                trust_remote_code=True
            )
            
            # Configurar padding token
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            
            # Carregar modelo
            self._model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                trust_remote_code=True,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            
            self._model = self._model.to(self._device)
            self._model.eval()
            print("Modelo carregado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self._load_fallback()
    
    def _load_fallback(self):
        """Fallback para modelo de código mais simples"""
        try:
            print("Usando fallback: codeparrot/codeparrot-small")
            self._tokenizer = AutoTokenizer.from_pretrained("codeparrot/codeparrot-small")
            self._tokenizer.pad_token = self._tokenizer.eos_token
            
            self._model = AutoModelForCausalLM.from_pretrained(
                "codeparrot/codeparrot-small",
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            self._model = self._model.to(self._device)
            self._model.eval()
            print("Fallback codeparrot carregado!")
        except Exception as e:
            print(f"Erro no fallback: {e}")
            raise
    
    def generate(self, prompt, max_new_tokens=400):
        if not self.is_loaded():
            self.load_model()
        
        try:
            # Tokenização simples
            inputs = self._tokenizer.encode(prompt, return_tensors="pt")
            inputs = inputs.to(self._device)
            
            # Geração com parâmetros otimizados para análise
            with torch.no_grad():
                outputs = self._model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.3,  # Mais baixo para análise mais consistente
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self._tokenizer.eos_token_id,
                    eos_token_id=self._tokenizer.eos_token_id,
                    early_stopping=True
                )
            
            # Decodificar resposta
            response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(prompt):].strip()
            
            # Limpar resposta
            if not response:
                response = "No patterns identified."
                
            return response
            
        except Exception as e:
            return f"Generation error: {str(e)}"
    
    def unload_model(self):
        if self._model is not None:
            del self._model
            if self._tokenizer:
                del self._tokenizer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self._model = None
            self._tokenizer = None
            print("Modelo descarregado")