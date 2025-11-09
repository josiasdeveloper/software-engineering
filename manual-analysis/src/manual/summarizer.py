from manual.llm_manager import llm_manager
from manual.config import MAX_CONTEXT_TOKENS


SUMMARIZE_PROMPT = """You are tasked with summarizing a conversation between a developer and an AI assistant to maintain context within token limits.

Create a concise summary that preserves:
1. Key technical topics discussed
2. Important code snippets or file references
3. Decisions made or conclusions reached
4. Any ongoing tasks or open questions
5. Context needed for future messages

Focus on facts and technical details. Omit pleasantries and redundant information.

Format the summary as:
**Context Summary:**
[Your summary here]

**Key Points:**
- Point 1
- Point 2
...

Conversation to summarize:
---"""


class ConversationSummarizer:
    """Handles conversation summarization for context management."""
    
    def __init__(self):
        self.llm_manager = llm_manager
        self.summarize_prompt = SUMMARIZE_PROMPT
    
    def summarize(self, conversation_text: str, max_tokens: int = None) -> str:
        """
        Summarize a conversation to reduce token usage.
        
        Args:
            conversation_text: The full conversation text to summarize
            max_tokens: Maximum tokens for summary (default: 1/4 of context window)
            
        Returns:
            The summarized conversation
        """
        if max_tokens is None:
            max_tokens = min(1024, MAX_CONTEXT_TOKENS // 4)
        
        print("Summarizing conversation to manage context...")
        
        
        summary_prompt = f"{self.summarize_prompt}\n{conversation_text}\n---\n\nSummary:"
        
        summary = self.llm_manager.generate(
            prompt=summary_prompt,
            max_new_tokens=max_tokens,
            temperature=0.3,  # Lower temperature for more focused summary
            do_sample=True
        )
        
        print("Conversation summarized successfully\n")
        
        return summary


# Export singleton instance
summarizer = ConversationSummarizer()

