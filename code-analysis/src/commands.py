#!/usr/bin/env python3

import click
from analyzer import PatternAnalyzer
from tree_builder import DirectoryTreeBuilder


def print_section(title):
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}\n")


@click.group()
def cli():
    """Design Pattern Detection Tool - Analyzes codebases to identify design patterns."""
    pass


@cli.command()
@click.option('--model', help='Model name (overrides LLM_MODEL env var)')
def load_model(model):
    """Load the LLM model into memory (GPU/CPU)."""
    
    print_section("Loading Language Model")
    
    from llm_manager import LLMManager
    import os
    
    if model:
        os.environ['LLM_MODEL'] = model
        click.echo(f"Using custom model: {model}")
    
    from config import MODEL_NAME
    click.echo(f"Model: {MODEL_NAME}")
    
    llm_manager = LLMManager()
    llm_manager.load_model()
    
    click.echo("\nModel loaded successfully!")
    click.echo("\nNext steps:")
    click.echo("  1. Run 'analyze clone <repo-url>' to clone and map a repository")
    click.echo("  2. Run 'analyze index' to generate summaries")


@cli.command()
@click.argument('repository_url')
@click.option('--target-dir', default='./target_repo', help='Directory to clone repository into')
def clone(repository_url, target_dir):
    """Clone repository and generate directory tree."""
    
    print_section("PHASE 0: Clone and Map Repository")
    
    analyzer = PatternAnalyzer(target_dir)
    
    repo_path = analyzer.phase_0_clone_and_map(repository_url)
    click.echo(f"Repository cloned to: {repo_path}")
    
    click.echo(f"\nDirectory structure ({len(analyzer.source_files)} source files found):\n")
    click.echo(analyzer.directory_tree)
    
    if analyzer.doc_files:
        click.echo(f"\nFound {len(analyzer.doc_files)} documentation file(s):")
        for doc_path in analyzer.doc_files.keys():
            click.echo(f"  - {doc_path}")
    
    click.echo(f"\nRepository ready for analysis at: {repo_path}")


@cli.command()
@click.option('--target-dir', default='./target_repo', help='Directory containing cloned repository')
def index(target_dir):
    """Generate file summaries (loads model automatically if needed)."""
    
    print_section("PHASE 2: Generate File Summaries (Indexer)")
    
    analyzer = PatternAnalyzer(target_dir)
    
    click.echo("Loading repository information...")
    tree_builder = DirectoryTreeBuilder(analyzer.repo_manager.target_dir)
    analyzer.directory_tree, analyzer.source_files = tree_builder.build()
    analyzer.repo_path = analyzer.repo_manager.target_dir
    
    if not analyzer.source_files:
        click.echo("Error: No source files found. Did you run 'analyze clone' first?")
        return
    
    click.echo(f"Found {len(analyzer.source_files)} source files")
    
    click.echo("\nLoading model (if not already loaded)...")
    analyzer.phase_1_load_model()
    
    summaries_path = analyzer.phase_2_generate_summaries()
    
    click.echo(f"\nIndexing complete! Summaries saved to: {summaries_path}")


@cli.command()
@click.argument('repository_url')
@click.option('--keep-repo', is_flag=True, help='Keep cloned repository after analysis')
@click.option('--keep-summaries', is_flag=True, help='Keep generated summaries JSON')
@click.option('--target-dir', default='./target_repo', help='Directory to clone repository into')
def analyze(repository_url, keep_repo, keep_summaries, target_dir):
    """Full analysis pipeline: clone and generate summaries (requires model loaded)."""
    
    analyzer = PatternAnalyzer(target_dir)
    
    try:
        print_section("PHASE 0: Clone and Map Repository")
        
        repo_path = analyzer.phase_0_clone_and_map(repository_url)
        click.echo(f"Repository cloned to: {repo_path}")
        
        click.echo(f"\nDirectory structure ({len(analyzer.source_files)} source files found):\n")
        click.echo(analyzer.directory_tree)
        
        if analyzer.doc_files:
            click.echo(f"\nFound {len(analyzer.doc_files)} documentation file(s):")
            for doc_path in analyzer.doc_files.keys():
                click.echo(f"  - {doc_path}")
        
        print_section("PHASE 2: Generate File Summaries (Indexer)")
        summaries_path = analyzer.phase_2_generate_summaries()
        click.echo(f"\nIndexing complete! Summaries saved to: {summaries_path}")
        
        print_section("PHASE 3: Documentation Analysis (Not Implemented)")
        click.echo("Agent 1 will analyze documentation for architectural patterns.")
        
        print_section("PHASE 4: Code Investigation (Not Implemented)")
        click.echo("Agent 2 will investigate code using RAG.")
        
        print_section("PHASE 5: Evidence Collection (Not Implemented)")
        click.echo("Agent 3 will collect code evidence for detected patterns.")
        
    finally:
        analyzer.cleanup(keep_summaries=keep_summaries)
        
        if not keep_repo:
            click.echo("\nCleanup completed.")
        else:
            click.echo(f"\nRepository kept at: {repo_path}")


@cli.command()
@click.argument('directory')
def tree(directory):
    """Generate directory tree for a local repository."""
    
    tree_builder = DirectoryTreeBuilder(directory)
    directory_tree, source_files = tree_builder.build()
    
    click.echo(f"Directory structure ({len(source_files)} source files found):\n")
    click.echo(directory_tree)


if __name__ == "__main__":
    cli()

