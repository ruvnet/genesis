import unittest
import threading
import time
from ui.utils.console_logger import ConsoleLogger

class TestConsoleLogger(unittest.TestCase):
    def setUp(self):
        self.logger = ConsoleLogger(max_messages=3)
    
    def test_add_message(self):
        """Test basic message addition."""
        msg = self.logger.add_message("Test message")
        self.assertIn("Test message", msg)
        self.assertIn("[INFO]", msg)
    
    def test_message_types(self):
        """Test different message types."""
        msg = self.logger.add_message("Error test", "error")
        self.assertIn("[ERROR]", msg)
        
        msg = self.logger.add_message("System test", "system")
        self.assertIn("[SYSTEM]", msg)
    
    def test_max_messages(self):
        """Test message limit enforcement."""
        self.logger.add_message("Message 1")
        self.logger.add_message("Message 2")
        self.logger.add_message("Message 3")
        final_msg = self.logger.add_message("Message 4")
        
        # Should only contain last 3 messages
        self.assertNotIn("Message 1", final_msg)
        self.assertIn("Message 4", final_msg)
    
    def test_thread_safety(self):
        """Test concurrent message addition."""
        def add_messages():
            for i in range(50):
                self.logger.add_message(f"Thread message {i}")
                time.sleep(0.01)
        
        threads = [
            threading.Thread(target=add_messages)
            for _ in range(3)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # Verify no messages were lost due to race conditions
        messages = self.logger.get_messages()
        self.assertEqual(len(messages.split("\n")), 3)  # max_messages=3
    
    def test_clear(self):
        """Test message clearing."""
        self.logger.add_message("Test message")
        self.logger.clear()
        self.assertEqual(self.logger.get_messages(), "")

if __name__ == '__main__':
    unittest.main()
