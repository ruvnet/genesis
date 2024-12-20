import time
import threading
from typing import List, Optional

class ConsoleLogger:
    def __init__(self, max_messages: int = 100):
        self.messages: List[str] = []
        self.max_messages = max_messages
        self.lock = threading.Lock()
        
    def add_message(self, message: str, message_type: str = "info") -> str:
        """Add a message to the console output with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        with self.lock:
            self.messages.append(f"[{timestamp}] [{message_type.upper()}] {message}")
            # Keep only last N messages
            if len(self.messages) > self.max_messages:
                self.messages.pop(0)
        return self.get_messages()
    
    def clear(self) -> None:
        """Clear all messages."""
        with self.lock:
            self.messages.clear()
    
    def get_messages(self) -> str:
        """Get all messages as a single string."""
        with self.lock:
            return "\n".join(self.messages)

# Global console logger instance
console = ConsoleLogger()
