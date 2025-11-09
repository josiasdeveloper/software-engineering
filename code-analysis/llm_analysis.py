#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from file_reader import FileReader
from llm_manager import LLMManager

def create_simple_prompt(code):
    return f"""Analyze this Python code and identify design patterns. Respond ONLY with: SINGLETON, FACTORY, DECORATOR, OBSERVER, STRATEGY, ADAPTER, BUILDER, MVC, REPOSITORY, COMMAND or NONE.

EXAMPLES:
Code: 
class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
Response: SINGLETON

Code:
def log_function(f):
    def wrapper(*args, **kwargs):
        print("Calling function")
        return f(*args, **kwargs)
    return wrapper
Response: DECORATOR

Code:
class PaymentProcessor:
    def process(self, amount):
        pass
class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        print("Processing credit card")
Response: NONE

CODE TO ANALYZE:
{code}

RESPONSE:"""

def analyze_with_llm(llm_manager, code_content, filename):
    code_sample = code_content[:800]
    prompt = create_simple_prompt(code_sample)
    
    try:
        # Generate LLM response
        response = llm_manager.generate(prompt, max_new_tokens=50)
        
        # Clean response
        response = response.replace('"', '').replace("'", "").replace("`", "").replace("\n", " ").strip()

        print(f"Resposta do LLM para {filename}: '{response}'")
        
        # Check if response contains Python code (indicates model repeated code)
        python_keywords = ["def ", "class ", "import ", "print(", "return ", "if ", "for "]
        if any(keyword in response for keyword in python_keywords):
            print(f"  AVISO: LLM repetiu código em vez de analisar")
            response = "NONE"
        
        # Extract patterns from response
        patterns_found = []
        known_patterns = ['SINGLETON', 'FACTORY', 'OBSERVER', 'STRATEGY', 'DECORATOR', 
                         'ADAPTER', 'BUILDER', 'MVC', 'REPOSITORY', 'COMMAND']
        
        response_upper = response.upper()
        
        # Search for known patterns
        for pattern in known_patterns:
            if pattern in response_upper:
                patterns_found.append(pattern)
                print(f"  Padrão encontrado: {pattern}")
                break  # Stop at first occurrence
        
        # If no patterns found, check if it's "NONE" or equivalent
        if not patterns_found:
            none_indicators = [
                "NONE", "NO PATTERN", "NO PATTERNS", "NONE PATTERN",
                "NO PATTERN IDENTIFIED", "NONE IDENTIFIED", "NONE DETECTED",
                "NO DESIGN PATTERN", "NONE FOUND"
            ]
            
            if any(indicator in response_upper for indicator in none_indicators):
                patterns_found = ["NONE"]
                print(f"  NONE identificado na resposta")
            else:
                # If not recognized, force NONE
                patterns_found = ["NONE"]
                response = f"NONE (forçado - resposta: '{response}')"
                print(f"  Resposta não reconhecida, forçando NONE")
        
        result = {
            "llm_raw_response": response,
            "patterns_detected": patterns_found,
            "total_patterns": len(patterns_found),
            "analysis_method": "LLM Expert"
        }
        
        return result
        
    except Exception as e:
        error_msg = f"Erro na geração: {str(e)}"
        print(f"  ERRO NO LLM: {error_msg}")
        return {
            "llm_raw_response": error_msg,
            "patterns_detected": ["NONE"],
            "total_patterns": 0,
            "analysis_method": "LLM Generation (Error)"
        }

def main():
    """Executa análise com LLM real"""
    
    print("ANÁLISE DE PADRÕES COM LLM")
    print("=" * 60)
    
    # Verificar repositório
    repo_path = Path("./target_repo")
    if not repo_path.exists():
        print("Repositório não encontrado!")
        return
    
    # Inicializar LLM
    print("Inicializando LLM...")
    llm_manager = LLMManager()
    llm_manager.load_model()
    
    # Encontrar arquivos Python
    py_files = list(repo_path.rglob("*.py"))
    print(f"Encontrados {len(py_files)} arquivos Python")
    
    # Selecionar TODOS os arquivos para análise
    files_to_analyze = py_files  # Todos os arquivos
    print(f"Analisando {len(files_to_analyze)} arquivos com LLM...")
    
    results = {}
    total_patterns = 0
    files_with_patterns = 0
    
    for i, file_path in enumerate(files_to_analyze, 1):
        try:
            relative_path = str(file_path.relative_to(repo_path))
            print(f"\n[{i}/{len(files_to_analyze)}] {relative_path}")
            
            # Ler arquivo
            content = FileReader.read_source_file(file_path)
            if not content or len(content.strip()) < 50:
                results[relative_path] = {
                    "llm_raw_response": "Arquivo vazio ou muito pequeno",
                    "patterns_detected": ["NONE"],
                    "total_patterns": 0,
                    "analysis_method": "Skip - Arquivo pequeno"
                }
                print("  Arquivo muito pequeno, pulando...")
                continue
            
            # Analisar com LLM
            print("  Analisando com LLM...")
            analysis = analyze_with_llm(llm_manager, content, relative_path)
            results[relative_path] = analysis
            
            # Mostrar resultado
            print(f"  Resposta do LLM: {analysis['llm_raw_response']}")
            
            if analysis['patterns_detected'] and analysis['patterns_detected'] != ["NONE"]:
                files_with_patterns += 1
                total_patterns += analysis['total_patterns']
                print(f"  ✅ PADRÕES EXTRAÍDOS: {', '.join(analysis['patterns_detected'])}")
            else:
                print(f"  ❌ Nenhum padrão extraído")
            
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            results[str(file_path.relative_to(repo_path))] = {
                "llm_raw_response": error_msg,
                "patterns_detected": ["NONE"],
                "total_patterns": 0,
                "analysis_method": "Error"
            }
            print(f"  🚨 ERRO: {error_msg}")
    
    # Consolidar padrões encontrados (ignorar "NONE")
    all_patterns = {}
    for file_result in results.values():
        if isinstance(file_result, dict) and "patterns_detected" in file_result:
            for pattern in file_result["patterns_detected"]:
                if pattern != "NONE":
                    all_patterns[pattern] = all_patterns.get(pattern, 0) + 1
    
    # Salvar resultados
    output_data = {
        "repositorio": "https://github.com/vanna-ai/vanna",
        "metodo_analise": "LLM Especialista em Arquitetura",
        "arquivos_analisados": len(files_to_analyze),
        "estatisticas": {
            "arquivos_com_padroes": files_with_patterns,
            "total_padroes_detectados": total_patterns,
            "padroes_por_frequencia": all_patterns
        },
        "resultados_detalhados": results
    }
    
    output_file = "analise_llm_completa.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Relatório final
    print(f"\n" + "=" * 60)
    print("RELATÓRIO FINAL - ANÁLISE COMPLETA COM LLM")
    print("=" * 60)
    
    print(f"Modelo LLM usado: microsoft/CodeGPT-small-py")
    print(f"Total de arquivos analisados: {len(files_to_analyze)}")
    print(f"Arquivos com padrões detectados: {files_with_patterns}")
    print(f"Total de padrões detectados: {total_patterns}")
    
    if all_patterns:
        print(f"\n✅ Padrões detectados pelo LLM:")
        for pattern, count in sorted(all_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {pattern}: {count} ocorrências")
    else:
        print(f"\n❌ Nenhum padrão foi detectado pelo LLM")
    
    if len(files_to_analyze) > 0:
        print(f"\n📊 Efetividade do LLM: {(files_with_patterns/len(files_to_analyze)*100):.1f}%")
    print(f"💾 Resultados salvos em: {output_file}")
    
    # Descarregar modelo
    llm_manager.unload_model()
    print(f"\n🎯 Análise com LLM concluída!")

if __name__ == "__main__":
    main()