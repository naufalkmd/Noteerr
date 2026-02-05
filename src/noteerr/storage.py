"""Storage backend for noteerr using JSON."""
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import ErrorEntry


class Storage:
    """Handles persistent storage of error entries."""
    
    def __init__(self, data_file: Optional[Path] = None):
        """Initialize storage with a data file path."""
        if data_file is None:
            # Default to user's home directory
            home = Path.home()
            data_dir = home / ".noteerr"
            data_dir.mkdir(exist_ok=True)
            self.data_file = data_dir / "errors.json"
        else:
            self.data_file = data_file
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not self.data_file.exists():
            self._write_data({"entries": [], "next_id": 1})
    
    def _read_data(self) -> Dict[str, Any]:
        """Read data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"entries": [], "next_id": 1}
    
    def _write_data(self, data: Dict[str, Any]) -> None:
        """Write data to JSON file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_entry(self, command: str, error: str, exit_code: int, 
                  directory: str, notes: str = "", tags: List[str] = None, 
                  project: str = "") -> ErrorEntry:
        """Add a new error entry."""
        data = self._read_data()
        
        entry = ErrorEntry(
            id=data["next_id"],
            timestamp=datetime.now().isoformat(),
            command=command,
            error=error,
            exit_code=exit_code,
            directory=directory,
            notes=notes,
            tags=tags or [],
            project=project
        )
        
        data["entries"].append(entry.to_dict())
        data["next_id"] += 1
        self._write_data(data)
        
        return entry
    
    def get_all_entries(self) -> List[ErrorEntry]:
        """Get all error entries."""
        data = self._read_data()
        return [ErrorEntry.from_dict(e) for e in data["entries"]]
    
    def get_entry_by_id(self, entry_id: int) -> Optional[ErrorEntry]:
        """Get a specific entry by ID."""
        entries = self.get_all_entries()
        for entry in entries:
            if entry.id == entry_id:
                return entry
        return None
    
    def update_entry(self, entry_id: int, notes: Optional[str] = None, 
                    tags: Optional[List[str]] = None) -> bool:
        """Update an existing entry."""
        data = self._read_data()
        
        for entry_data in data["entries"]:
            if entry_data["id"] == entry_id:
                if notes is not None:
                    entry_data["notes"] = notes
                if tags is not None:
                    entry_data["tags"] = tags
                self._write_data(data)
                return True
        
        return False
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID."""
        data = self._read_data()
        original_count = len(data["entries"])
        
        data["entries"] = [e for e in data["entries"] if e["id"] != entry_id]
        
        if len(data["entries"]) < original_count:
            self._write_data(data)
            return True
        
        return False
    
    def search_entries(self, query: str) -> List[ErrorEntry]:
        """Search entries by command, error text, or notes."""
        entries = self.get_all_entries()
        query_lower = query.lower()
        
        return [
            entry for entry in entries
            if query_lower in entry.command.lower()
            or query_lower in entry.error.lower()
            or query_lower in entry.notes.lower()
            or any(query_lower in tag.lower() for tag in entry.tags)
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about stored errors."""
        entries = self.get_all_entries()
        
        if not entries:
            return {
                "total_errors": 0,
                "most_common_command": None,
                "most_recent": None,
                "tags": {}
            }
        
        # Count commands
        command_counts = {}
        tag_counts = {}
        
        for entry in entries:
            cmd = entry.command.split()[0] if entry.command else "unknown"
            command_counts[cmd] = command_counts.get(cmd, 0) + 1
            
            for tag in entry.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        most_common = max(command_counts.items(), key=lambda x: x[1]) if command_counts else (None, 0)
        
        return {
            "total_errors": len(entries),
            "most_common_command": most_common[0],
            "most_common_count": most_common[1],
            "most_recent": entries[-1],
            "tags": tag_counts
        }
    
    def find_similar_entries(self, entry: ErrorEntry, threshold: float = 0.85) -> List[ErrorEntry]:
        """
        Find entries similar to the given entry.
        
        Args:
            entry: The entry to compare against
            threshold: Similarity threshold (0.0 to 1.0)
            
        Returns:
            List of similar entries
        """
        all_entries = self.get_all_entries()
        similar = []
        
        for existing in all_entries:
            if entry.is_similar_to(existing, threshold):
                similar.append(existing)
        
        return similar
    
    def get_entries_by_project(self, project: str) -> List[ErrorEntry]:
        """Get all entries for a specific project."""
        entries = self.get_all_entries()
        return [e for e in entries if e.project.lower() == project.lower()]
    
    def get_all_projects(self) -> List[str]:
        """Get a list of all unique project names."""
        entries = self.get_all_entries()
        projects = set()
        for entry in entries:
            if entry.project:
                projects.add(entry.project)
        return sorted(list(projects))
    
    def clear_all(self) -> int:
        """Clear all entries and return count of deleted entries."""
        data = self._read_data()
        count = len(data["entries"])
        self._write_data({"entries": [], "next_id": 1})
        return count
