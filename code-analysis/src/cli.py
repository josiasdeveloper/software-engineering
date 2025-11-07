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
@click.argument('repository_url')
@click.option('--keep-repo', is_flag=True, help='Keep cloned repository after analysis')
@click.option('--keep-summaries', is_flag=True, help='Keep generated summaries JSON')
@click.option('--target-dir', default='./target_repo', help='Directory to clone repository into')
@click.option('--skip-summaries', is_flag=True, help='Skip summary generation (faster, for testing)')
def analyze(repository_url, keep_repo, keep_summaries, target_dir, skip_summaries):
    """Analyze a repository to detect design patterns."""
    
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
        
        if not skip_summaries:
            print_section("PHASE 1: Load Language Model")
            analyzer.phase_1_load_model()
            
            print_section("PHASE 2: Generate File Summaries (Indexer)")
            summaries_path = analyzer.phase_2_generate_summaries()
            click.echo(f"\nIndexing complete! Summaries saved to: {summaries_path}")
            
            print_section("PHASE 3: Documentation Analysis (Not Implemented)")
            click.echo("Agent 1 will analyze documentation for architectural patterns.")
            
            print_section("PHASE 4: Code Investigation (Not Implemented)")
            click.echo("Agent 2 will investigate code using RAG.")
            
            print_section("PHASE 5: Evidence Collection (Not Implemented)")
            click.echo("Agent 3 will collect code evidence for detected patterns.")
        else:
            click.echo("\nSkipping summary generation (--skip-summaries flag set)")
        
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

