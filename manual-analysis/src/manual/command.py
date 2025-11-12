import sys
from manual.orchestrator import Orchestrator
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

console = Console()
last_response = ""


def print_banner():
    banner_text = """
# Design Pattern Analysis Assistant

## Commands:
- `/help`       - Show this help message
- `/clear`      - Clear conversation history
- `/restart`    - Restart model and clear all context
- `/save`       - Save conversation history to file
- `/raw`        - Show last response in plain text (easy to copy)
- `/context`    - Show context usage information
- `/exit`       - Exit the assistant

## Tips:
- **Paste code directly**: Just paste! Multi-line is fully supported
- **Submit**: Press `Alt+Enter` or `Esc` then `Enter` to submit
- **New line**: Press `Enter` to add a new line
- **Cancel**: Press `Ctrl+C` to cancel

Start analyzing your codebase by pasting code snippets, documentation, 
or asking questions about design patterns.
"""
    console.print(Panel(Markdown(banner_text), 
                       title="[bold cyan]Welcome[/bold cyan]", 
                       border_style="cyan"))
    console.print()


def print_help():
    help_text = """
## Available Commands

- `/help`       - Show this help message
- `/clear`      - Clear conversation history (keeps model loaded)
- `/restart`    - Restart model and clear all context
- `/save`       - Save conversation history to file
- `/raw`        - Show last response in plain text (easy to copy)
- `/context`    - Display current context usage (tokens, messages)
- `/exit`       - Exit the assistant

## Input Tips

### Multi-line Input
- **Paste directly**: Just paste your code - multi-line works!
- **Submit**: Press `Alt+Enter` or `Esc` then `Enter` to send
- **New line**: Press `Enter` to add a new line while typing
- **Single line**: Type your question and press `Alt+Enter`

### Usage Examples
1. **Ask questions**: "What design patterns are used in this code?"
2. **Paste code**: Just paste directly - multi-line is supported
3. **Reference specifics**: Mention file paths, class names for better analysis
4. **Continue conversation**: The assistant remembers context automatically

### Auto-summarization
The assistant will automatically summarize when context is full, 
preserving the most important information.
"""
    console.print(Panel(Markdown(help_text), 
                       title="[bold yellow]Help[/bold yellow]", 
                       border_style="yellow"))
    console.print()


def print_context_info(orchestrator: Orchestrator):
    info = orchestrator.get_context_info()
    
    usage = info['usage_percent']
    bar_length = 40
    filled = int(bar_length * usage / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if usage < 60:
        color = "green"
    elif usage < 85:
        color = "yellow"
    else:
        color = "red"
    
    context_text = f"""
**Current Context Usage**

Token Usage: [{color}]{bar}[/{color}] {usage:.1f}%
- Current: {info['current_tokens']:,} tokens
- Maximum: {info['max_tokens']:,} tokens

Messages: {info['messages_count']}
Has Summary: {'Yes' if info['has_summary'] else 'No'}
"""
    
    console.print(Panel(Markdown(context_text), 
                       title="[bold blue]Context Info[/bold blue]", 
                       border_style="blue"))
    console.print()


def get_user_input():
    console.print("[bold green]You:[/bold green]")
    console.print("[dim](Press Alt+Enter or Esc then Enter to submit)[/dim]")
    
    try:
        bindings = KeyBindings()
        
        @bindings.add('escape', 'enter')
        def _(event):
            event.current_buffer.validate_and_handle()
        
        user_input = prompt(
            '',
            multiline=True,
            key_bindings=bindings,
            mouse_support=True
        )
        
        return user_input.strip()
    
    except KeyboardInterrupt:
        return None
    except EOFError:
        return None


def print_response(response: str):
    global last_response
    last_response = response
    
    md = Markdown(response)
    
    console.print()
    console.print(Panel(
        md,
        title="[bold magenta]Assistant[/bold magenta]",
        border_style="magenta",
        padding=(1, 2)
    ))
    console.print("[dim]Tip: Use /raw to see plain text version[/dim]")
    console.print()


def print_raw_response():
    global last_response
    if not last_response:
        console.print("[yellow]No response to show yet[/yellow]\n")
        return
    
    console.print("\n" + "="*70)
    console.print("RAW TEXT (easy to copy):")
    console.print("="*70)
    print(last_response)
    console.print("="*70 + "\n")


def run_interactive_chat():
    orchestrator = Orchestrator()
    
    print_banner()
    
    try:
        with console.status("[bold green]Loading model...[/bold green] (this may take a moment)", 
                           spinner="dots"):
            orchestrator.llm_manager.load_model()
        
        console.print("[bold green]Model loaded successfully![/bold green]\n")
        
        while True:
            try:
                user_input = get_user_input()
                
                if user_input is None:
                    console.print("\n[yellow]Interrupted. Type /exit to quit or continue chatting.[/yellow]\n")
                    continue
                
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    command_parts = user_input.split(maxsplit=1)
                    command = command_parts[0].lower()
                    
                    if command == "/exit":
                        console.print("\n[bold cyan]Exiting Design Pattern Analysis Assistant. Goodbye![/bold cyan]\n")
                        sys.exit(0)
                    
                    elif command == "/help":
                        print_help()
                        continue
                    
                    elif command == "/clear":
                        orchestrator.clear_history()
                        console.print("[bold green]Conversation history cleared[/bold green]\n")
                        continue
                    
                    elif command == "/restart":
                        with console.status("[bold yellow]Restarting...[/bold yellow]", spinner="dots"):
                            orchestrator.restart()
                        console.print("[bold green]Model and conversation restarted. Model will reload on next message.[/bold green]\n")
                        continue
                    
                    elif command == "/save":
                        try:
                            with console.status("[bold blue]Saving conversation...[/bold blue]", spinner="dots"):
                                message = orchestrator.save_history()
                            console.print(f"[bold green]{message}[/bold green]\n")
                        except Exception as e:
                            console.print(f"[bold red]Error saving history: {e}[/bold red]\n")
                        continue
                    
                    elif command == "/context":
                        print_context_info(orchestrator)
                        continue
                    
                    elif command == "/raw":
                        print_raw_response()
                        continue
                    
                    else:
                        console.print(f"[bold red]Unknown command: {command}[/bold red]")
                        console.print("[dim]Type /help for available commands.[/dim]\n")
                        continue
                
                with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
                    response = orchestrator.orchestrate(user_input)
                
                print_response(response)
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Use /exit to quit or continue chatting.[/yellow]")
                continue
            
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {e}")
                console.print("[dim]Please try again or use /clear to reset.[/dim]\n")
                continue
    
    except KeyboardInterrupt:
        console.print("\n\n[bold cyan]Exiting Design Pattern Analysis Assistant. Goodbye![/bold cyan]\n")
        sys.exit(0)
    
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {e}\n")
        sys.exit(1)


def main():
    run_interactive_chat()


if __name__ == "__main__":
    main()
