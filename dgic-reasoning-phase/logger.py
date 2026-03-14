"""Logging infrastructure for DGIC reasoning layer."""

import logging
import sys
from typing import Optional
from config import get_config


class ReasoningLogger:
    """Centralized logging for reasoning engine."""
    
    _instance: Optional["ReasoningLogger"] = None
    
    def __init__(self):
        self.logger = logging.getLogger("dgic.reasoning")
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configure logging based on config."""
        config = get_config()
        level = getattr(logging, config.log_level)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if configured
        if config.log_file:
            file_handler = logging.FileHandler(config.log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get singleton logger instance."""
        if cls._instance is None:
            cls._instance = ReasoningLogger()
        return cls._instance.logger


def get_logger() -> logging.Logger:
    """Get logger instance."""
    return ReasoningLogger.get_logger()
