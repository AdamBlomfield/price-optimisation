import logging
import os
from datetime import datetime
import glob

class LoggerManager:
    def __init__(self, script_name, max_log_files=3, log_dir='logs'):
        """
        Initialize a logger for a specific script.
        
        Args:
            script_name (str): Name of the script using the logger
            max_log_files (int, optional): Maximum number of log files to keep. Defaults to 3.
            log_dir (str, optional): Directory to store log files. Defaults to 'logs'.
        """
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Generate unique log filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_filename = os.path.join(log_dir, f"{script_name}-{timestamp}.log")
        
        # Clean up old log files
        self._cleanup_old_logs(script_name, log_dir, max_log_files)
        
        # Configure logging
        self.logger = logging.getLogger(script_name)
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _cleanup_old_logs(self, script_name, log_dir, max_log_files):
        """
        Remove old log files, keeping only the most recent ones.
        
        Args:
            script_name (str): Name of the script
            log_dir (str): Directory containing log files
            max_log_files (int): Maximum number of log files to keep
        """
        # Find all log files for this script
        log_pattern = os.path.join(log_dir, f"{script_name}-*.log")
        existing_logs = sorted(glob.glob(log_pattern))
        
        # Remove older log files if more than max_log_files
        while len(existing_logs) >= max_log_files:
            oldest_log = existing_logs.pop(0)
            try:
                os.remove(oldest_log)
            except OSError as e:
                print(f"Error removing log file {oldest_log}: {e}")
    
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)

# Convenience function to create logger
def create_logger(script_name):
    """
    Create and return a logger for a specific script.
    
    Args:
        script_name (str): Name of the script
    
    Returns:
        LoggerManager: Configured logger instance
    """
    return LoggerManager(script_name)