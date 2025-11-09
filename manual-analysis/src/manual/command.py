import sys
from manual.orchestrator import Orchestrator


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print("  Design Pattern Analysis Assistant")
    print("="*70)
    print("\nCommands:")
    print("  /help         - Show this help message")
    print("  /clear        - Clear conversation history")
    print("  /restart      - Restart model and clear all context")
    print("  /save         - Save conversation history to file")
    print("  /context      - Show context usage information")
    print("  /exit         - Exit the assistant")
    print("\nStart analyzing your codebase by pasting code snippets,")
    print("documentation, or asking questions about design patterns.")
    print("="*70 + "\n")


def print_help():
    """Print help message."""
    print("\nAvailable commands:")
    print("  /help         - Show this help message")
    print("  /clear        - Clear conversation history (keeps model loaded)")
    print("  /restart      - Restart model and clear all context")
    print("  /save         - Save conversation history to file")
    print("  /context      - Display current context usage (tokens, messages)")
    print("  /exit         - Exit the assistant")
    print("\nTips:")
    print("  - Paste code snippets directly")
    print("  - Ask about specific design patterns")
    print("  - Reference file paths and class names for better analysis")
    print("  - The assistant will auto-summarize when context is full")
    print()


def print_context_info(orchestrator: Orchestrator):
    """Print context usage information."""
    info = orchestrator.get_context_info()
    print(f"\n{'='*70}")
    print("Context Information:")
    print(f"  Current tokens: {info['current_tokens']}")
    print(f"  Max tokens: {info['max_tokens']}")
    print(f"  Usage: {info['usage_percent']:.1f}%")
    print(f"  Messages in history: {info['messages_count']}")
    print(f"  Has summary: {'Yes' if info['has_summary'] else 'No'}")
    print(f"{'='*70}\n")


def run_interactive_chat():
    """Run the interactive chat loop."""
    orchestrator = Orchestrator()
    
    print_banner()
    
    try:
        # Load model at startup
        print("Loading model... (this may take a moment)")
        orchestrator.llm_manager.load_model()
        print("Model loaded successfully!\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    command_parts = user_input.split(maxsplit=1)
                    command = command_parts[0].lower()
                    
                    if command == "/exit":
                        print("\nExiting Design Pattern Analysis Assistant. Goodbye!")
                        sys.exit(0)
                    
                    elif command == "/help":
                        print_help()
                        continue
                    
                    elif command == "/clear":
                        orchestrator.clear_history()
                        continue
                    
                    elif command == "/restart":
                        orchestrator.restart()
                        continue
                    
                    elif command == "/save":
                        try:
                            message = orchestrator.save_history()
                            print(message)
                        except Exception as e:
                            print(f"Error saving history: {e}")
                        continue
                    
                    elif command == "/context":
                        print_context_info(orchestrator)
                        continue
                    
                    else:
                        print(f"Unknown command: {command}")
                        print("Type /help for available commands.\n")
                        continue
                
                
                response = orchestrator.orchestrate(user_input)
                
                
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nUse /exit to quit or continue chatting.")
                continue
            
            except Exception as e:
                print(f"\nError processing request: {e}")
                print("Please try again or use /clear to reset.\n")
                continue
    
    except KeyboardInterrupt:
        print("\n\nExiting Design Pattern Analysis Assistant. Goodbye!")
        sys.exit(0)
    
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    run_interactive_chat()


if __name__ == "__main__":
    main()

