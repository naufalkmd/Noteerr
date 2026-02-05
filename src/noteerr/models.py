"""Data models for noteerr."""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ErrorEntry:
    """Represents a command error entry."""
    id: int
    timestamp: str
    command: str
    error: str
    exit_code: int
    directory: str
    notes: str = ""
    tags: list = None
    project: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        # Ensure project is always a string
        if self.project is None:
            self.project = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorEntry':
        """Create an ErrorEntry from a dictionary."""
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ErrorEntry to dictionary."""
        return asdict(self)
    
    @property
    def formatted_timestamp(self) -> str:
        """Return a human-readable timestamp."""
        dt = datetime.fromisoformat(self.timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def short_date(self) -> str:
        """Return a short date format."""
        dt = datetime.fromisoformat(self.timestamp)
        return dt.strftime("%Y-%m-%d")
    
    def is_similar_to(self, other: 'ErrorEntry', threshold: float = 0.85) -> bool:
        """
        Check if this error is similar to another error.
        
        Args:
            other: Another ErrorEntry to compare against
            threshold: Similarity threshold (0.0 to 1.0), default 0.85
            
        Returns:
            True if errors are similar enough to be considered duplicates
        """
        # Same command and error message (case-insensitive)
        if (self.command.lower() == other.command.lower() and 
            self.error.lower() == other.error.lower()):
            return True
        
        # Same command and similar error (fuzzy match)
        if self.command.lower() == other.command.lower():
            # Simple word-based similarity
            error1_words = set(self.error.lower().split())
            error2_words = set(other.error.lower().split())
            if len(error1_words) == 0 or len(error2_words) == 0:
                return False
            
            intersection = error1_words & error2_words
            union = error1_words | error2_words
            similarity = len(intersection) / len(union)
            
            if similarity >= threshold:
                return True
        
        return False
