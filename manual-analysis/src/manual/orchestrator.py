from manual.llm_manager import llm_manager
from manual.summarizer import summarizer
from manual.config import (
    MAX_CONTEXT_TOKENS, 
    SUMMARIZE_THRESHOLD, 
    MAX_HISTORY_BEFORE_SUMMARY,
    RESERVED_TOKENS_FOR_RESPONSE
)

SYSTEM_PROMPT = """You are an expert AI assistant specialized in software architecture and design pattern analysis.

Your primary task is to help developers identify, understand, and analyze design patterns in codebases. The user will provide:
- Code snippets
- Documentation
- GitHub issues or technical specifications
- Questions about architectural decisions

Your responses should:
- Accurately identify design patterns (Gang of Four, architectural patterns, domain patterns)
- Explain how patterns are implemented in the given code
- Point out code smells, anti-patterns, or misused patterns
- Provide clear reasoning for your analysis
- Reference specific code elements (classes, functions, files) in your explanations

Analysis approach:
1. Examine code structure and relationships between components
2. Identify behavioral, creational, and structural patterns
3. Consider context: language idioms, framework conventions, domain requirements
4. Be precise: distinguish between similar patterns (e.g., Strategy vs State)
5. Support conclusions with evidence from the code

Respond as a knowledgeable colleague conducting a thorough code review.

"""


class Orchestrator:
    def __init__(self):
        self.llm_manager = llm_manager
        self.summarizer = summarizer
        self.conversation_history = []  # List of {"role": "user"/"assistant", "content": str}
        self.summary = None 
        self.system_prompt = SYSTEM_PROMPT
        
    def _count_tokens(self, text: str) -> int:
        """Estimate token count for text."""
    
        if self.llm_manager._tokenizer is None:
            self.llm_manager.load_model()
        
        tokens = self.llm_manager._tokenizer.encode(text, truncation=False)
        return len(tokens)
    
    def _build_conversation_text(self) -> str:
        
        parts = []
        
        if self.summary:
            parts.append(f"[Previous conversation summary]\n{self.summary}\n")
        
        for msg in self.conversation_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            parts.append(f"{role}: {msg['content']}")
        
        return "\n\n".join(parts)
    
    def _get_current_context_size(self) -> int:
        """Calculate current total token count."""
        system_tokens = self._count_tokens(self.system_prompt)
        conversation_text = self._build_conversation_text()
        conversation_tokens = self._count_tokens(conversation_text)
        return system_tokens + conversation_tokens
    
    def _should_summarize(self) -> bool:
        """Check if conversation should be summarized."""
        current_tokens = self._get_current_context_size()
        token_threshold = int(MAX_CONTEXT_TOKENS * SUMMARIZE_THRESHOLD) - RESERVED_TOKENS_FOR_RESPONSE
        

        return (current_tokens > token_threshold or 
                len(self.conversation_history) > MAX_HISTORY_BEFORE_SUMMARY)
    
    def _summarize_conversation(self):
        """Summarize the conversation and reset history."""
        if not self.conversation_history:
            return
        
        conversation_text = self._build_conversation_text()
        self.summary = self.summarizer.summarize(conversation_text)
        self.conversation_history = []
    
    def orchestrate(self, user_input: str, max_new_tokens: int = 512) -> str:
        """
        Process user input and generate response with full conversation context.
        
        Args:
            user_input: The user's message
            max_new_tokens: Maximum tokens for the response
            
        Returns:
            The assistant's response
        """
        self.llm_manager.load_model()
        
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        
        if self._should_summarize():
            self._summarize_conversation()
        
        
        conversation_text = self._build_conversation_text()
        full_prompt = f"{self.system_prompt}\n\n{conversation_text}\n\nAssistant:"
                
        response = self.llm_manager.generate(
            prompt=full_prompt,
            max_new_tokens=max_new_tokens
        )
        

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def get_history(self) -> list:
        """Return the conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history and summary."""
        self.conversation_history = []
        self.summary = None
        print("Conversation history cleared")
    
    def restart(self):
        """Restart by clearing everything including model from memory."""
        self.conversation_history = []
        self.summary = None
        self.llm_manager._model = None
        self.llm_manager._tokenizer = None
        print("Model and conversation restarted. Model will reload on next message.")
    
    def save_history(self, filepath: str = None) -> str:
        """
        Save conversation history to a text file.
        
        Args:
            filepath: Path to save the history (default: auto-generated with timestamp)
            
        Returns:
            Confirmation message with filepath
        """
        from datetime import datetime
        
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"conversation_{timestamp}.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("Design Pattern Analysis - Conversation History\n")
            f.write(f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            if self.summary:
                f.write("[PREVIOUS CONVERSATION SUMMARY]\n")
                f.write("-"*70 + "\n")
                f.write(self.summary + "\n")
                f.write("-"*70 + "\n\n")
            
            if not self.conversation_history:
                f.write("No messages in current history.\n")
            else:
                for i, msg in enumerate(self.conversation_history, 1):
                    role = "USER" if msg["role"] == "user" else "ASSISTANT"
                    f.write(f"{role} (Message {i}):\n")
                    f.write(msg["content"] + "\n")
                    f.write("\n" + "-"*70 + "\n\n")
            
            context_info = self.get_context_info()
            f.write("\n" + "="*70 + "\n")
            f.write("CONTEXT INFORMATION\n")
            f.write("="*70 + "\n")
            f.write(f"Total messages: {context_info['messages_count']}\n")
            f.write(f"Current tokens: {context_info['current_tokens']}\n")
            f.write(f"Max tokens: {context_info['max_tokens']}\n")
            f.write(f"Usage: {context_info['usage_percent']:.1f}%\n")
            f.write(f"Has summary: {context_info['has_summary']}\n")
        
        return f"History saved to: {filepath}"
    
    def get_context_info(self) -> dict:
        """Get information about current context usage."""
        current_tokens = self._get_current_context_size()
        return {
            "current_tokens": current_tokens,
            "max_tokens": MAX_CONTEXT_TOKENS,
            "usage_percent": (current_tokens / MAX_CONTEXT_TOKENS) * 100,
            "messages_count": len(self.conversation_history),
            "has_summary": self.summary is not None
        }

