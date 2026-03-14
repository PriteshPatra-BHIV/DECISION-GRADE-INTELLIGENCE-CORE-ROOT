"""Configuration management for DGIC reasoning layer."""

from dataclasses import dataclass
from typing import Optional
import os
import json
import logging


@dataclass
class ReasoningConfig:
    """Production configuration for reasoning engine."""
    
    confidence_threshold: float = 0.85
    entropy_floor: float = 0.2
    dominance_gap: float = 0.25
    support_confidence_boost: float = 0.1
    support_entropy_reduction: float = 0.1
    contradict_confidence_penalty: float = 0.15
    contradict_entropy_increase: float = 0.1
    neutral_entropy_increase: float = 0.05
    compatible_confidence_boost: float = 0.03
    compatible_entropy_reduction: float = 0.02
    conflict_confidence_penalty: float = 0.04
    conflict_entropy_increase: float = 0.02
    min_confidence: float = 0.0
    max_confidence: float = 1.0
    min_entropy: float = 0.0
    max_entropy: float = 1.0
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError(f"confidence_threshold must be [0,1], got {self.confidence_threshold}")
        if not (0.0 <= self.entropy_floor <= 1.0):
            raise ValueError(f"entropy_floor must be [0,1], got {self.entropy_floor}")
        if not (0.0 <= self.dominance_gap <= 1.0):
            raise ValueError(f"dominance_gap must be [0,1], got {self.dominance_gap}")
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log_level: {self.log_level}")
    
    @classmethod
    def from_file(cls, filepath: str) -> "ReasoningConfig":
        """Load configuration from JSON file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Config file not found: {filepath}")
        with open(filepath, 'r') as f:
            data = json.load(f)
        config = cls(**data)
        config.validate()
        return config
    
    @classmethod
    def from_env(cls) -> "ReasoningConfig":
        """Load configuration from environment variables."""
        config = cls()
        if val := os.getenv("DGIC_CONFIDENCE_THRESHOLD"):
            config.confidence_threshold = float(val)
        if val := os.getenv("DGIC_ENTROPY_FLOOR"):
            config.entropy_floor = float(val)
        if val := os.getenv("DGIC_LOG_LEVEL"):
            config.log_level = val
        if val := os.getenv("DGIC_LOG_FILE"):
            config.log_file = val
        config.validate()
        return config


_default_config = ReasoningConfig()


def get_config() -> ReasoningConfig:
    """Get current configuration."""
    return _default_config


def set_config(config: ReasoningConfig) -> None:
    """Set global configuration."""
    global _default_config
    config.validate()
    _default_config = config
