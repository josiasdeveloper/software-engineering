#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from file_reader import FileReader
from llm_manager import LLMManager

def create_simple_prompt(code):
    return f"""Você é um especialista em arquitetura de software. Analise o código e responda APENAS no formato exato solicitado.

Código:
{code}

Responda EXATAMENTE assim (sem explicações):
- "Padrão Singleton identificado."
- "Padrão Factory identificado."
- "Vários padrões identificados: Factory, Decorator."
- "Nenhum padrão identificado."

Sua resposta:"""

def analyze_with_llm(llm_manager, code_content, filename):
    code_sample = code_content[:800]
    prompt = create_simple_prompt(code_sample)
    
    try:
        # Gerar resposta do LLM
        response = llm_manager.generate(prompt, max_new_tokens=80)
        
        # Limpar resposta
        response = response.strip()
        
        # Extrair padrões da resposta
        patterns_found = []
        known_patterns = ['Singleton', 'Factory', 'Observer', 'Strategy', 'Decorator', 
                         'Adapter', 'Builder', 'MVC', 'Repository', 'Command']
        
        for pattern in known_patterns:
            if pattern in response:
                patterns_found.append(pattern)
        
        # Status é exatamente o que o LLM respondeu
        result = {
            "llm_raw_response": response,
            "patterns_detected": patterns_found,
            "total_patterns": len(patterns_found),
            "analysis_method": "LLM Especialista",
        }
        
        return result
        
    except Exception as e:
        return {
            "llm_raw_response": f"Erro: {str(e)}",
            "patterns_detected": [],
            "total_patterns": 0,
            "analysis_method": "LLM Generation (Error)",
            "status": f"Erro na análise: {str(e)}"
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
    
    # Selecionar arquivos para análise
    files_to_analyze = py_files[:5]  
    print(f"Analisando {len(files_to_analyze)} arquivos com LLM...")
    
    results = {}
    total_patterns = 0
    files_with_patterns = 0
    
    for i, file_path in enumerate(files_to_analyze, 1):
        try:
            relative_path = str(file_path.relative_to(repo_path))
            print(f"\\n[{i}/{len(files_to_analyze)}] {relative_path}")
            
            # Ler arquivo
            content = FileReader.read_source_file(file_path)
            if not content or len(content.strip()) < 50:
                results[relative_path] = {
                    "status": "Arquivo muito pequeno",
                    "patterns_detected": [],
                    "llm_raw_response": "Arquivo vazio ou muito pequeno"
                }
                print(" Arquivo muito pequeno, pulando...")
                continue
            
            # Analisar com LLM
            print("  Analisando com LLM...")
            analysis = analyze_with_llm(llm_manager, content, relative_path)
            results[relative_path] = analysis
            
            # Mostrar resultado
            print(f"  LLM Resposta: {analysis['status']}")
            
            if analysis['patterns_detected']:
                files_with_patterns += 1
                total_patterns += analysis['total_patterns']
                print(f"  PADRÕES EXTRAÍDOS: {', '.join(analysis['patterns_detected'])}")
            else:
                print(f"  Nenhum padrão extraído")
            
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            results[str(file_path.relative_to(repo_path))] = {
                "status": error_msg,
                "patterns_detected": [],
                "llm_raw_response": error_msg
            }
            print(f"  ERRO: {error_msg}")
    
    # Consolidar padrões encontrados
    all_patterns = {}
    for file_result in results.values():
        if isinstance(file_result, dict) and "patterns_detected" in file_result:
            for pattern in file_result["patterns_detected"]:
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
    
    output_file = "analise_llm_real.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Relatório final
    print(f"\\n" + "=" * 60)
    print("RELATÓRIO FINAL - ANÁLISE COM LLM")
    print("=" * 60)
    
    print(f"Arquivos analisados: {len(files_to_analyze)}")
    print(f"Arquivos com padrões detectados: {files_with_patterns}")
    print(f"Total de padrões detectados: {total_patterns}")
    
    if all_patterns:
        print(f"\\nPadrões detectados pelo LLM:")
        for pattern, count in sorted(all_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {pattern}: {count} ocorrências")
    else:
        print(f"\\nNenhum padrão foi detectado pelo LLM")
    
    print(f"\\nEfetividade do LLM: {(files_with_patterns/len(files_to_analyze)*100):.1f}%")
    print(f"Resultados salvos em: {output_file}")
    
    # Descarregar modelo
    llm_manager.unload_model()
    print(f"\\nAnálise com LLM concluída!")

if __name__ == "__main__":
    main()