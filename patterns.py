#!/usr/bin/env python3
"""
Pattern Library for Seq80x25
Contains preset musical patterns for quick composition
"""

from typing import Dict, List, Tuple, Optional
import json
import os


class PatternLibrary:
    """Library of preset musical patterns"""
    
    def __init__(self):
        self.patterns = self._load_default_patterns()
        self.custom_patterns = self._load_custom_patterns()
    
    def _load_default_patterns(self) -> Dict[str, Dict]:
        """Load built-in musical patterns"""
        return {
            "c_major_scale": {
                "name": "C Major Scale",
                "description": "Ascending C major scale",
                "notes": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
                "tempo": 120,
                "category": "scales"
            },
            "c_major_arpeggio": {
                "name": "C Major Arpeggio",
                "description": "C major chord arpeggio",
                "notes": ["C4", "E4", "G4", "C5", "G4", "E4", "C4"],
                "tempo": 120,
                "category": "arpeggios"
            },
            "blues_lick": {
                "name": "Blues Lick",
                "description": "Classic blues phrase in C",
                "notes": ["C4", "E4", "F4", "F#4", "G4", "A4", "B4", "C5"],
                "tempo": 100,
                "category": "blues"
            },
            "pentatonic": {
                "name": "C Pentatonic",
                "description": "C major pentatonic scale",
                "notes": ["C4", "D4", "E4", "G4", "A4", "C5"],
                "tempo": 120,
                "category": "scales"
            },
            "bass_line": {
                "name": "Walking Bass",
                "description": "Walking bass line in C",
                "notes": ["C3", "E3", "F3", "G3", "A3", "B3", "C4"],
                "tempo": 140,
                "category": "bass"
            },
            "drum_pattern": {
                "name": "Basic Beat",
                "description": "Simple 4/4 drum pattern",
                "notes": ["Kick", "Snare", "Kick", "Snare"],
                "tempo": 120,
                "category": "drums"
            },
            "chiptune_melody": {
                "name": "Chiptune Melody",
                "description": "8-bit style melody",
                "notes": ["C5", "D5", "E5", "G5", "A5", "G5", "E5", "C5"],
                "tempo": 150,
                "category": "melodies"
            },
            "ambient_pad": {
                "name": "Ambient Pad",
                "description": "Slow ambient progression",
                "notes": ["C4", "F4", "A4", "C5"],
                "tempo": 80,
                "category": "ambient"
            }
        }
    
    def _load_custom_patterns(self) -> Dict[str, Dict]:
        """Load custom patterns from file"""
        custom_file = "custom_patterns.json"
        if os.path.exists(custom_file):
            try:
                with open(custom_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_custom_pattern(self, name: str, pattern: Dict) -> bool:
        """Save a custom pattern"""
        try:
            self.custom_patterns[name] = pattern
            with open("custom_patterns.json", 'w') as f:
                json.dump(self.custom_patterns, f, indent=2)
            return True
        except Exception:
            return False
    
    def get_pattern(self, name: str) -> Optional[Dict]:
        """Get a pattern by name"""
        return self.patterns.get(name) or self.custom_patterns.get(name)
    
    def list_patterns(self, category: Optional[str] = None) -> List[str]:
        """List available patterns, optionally filtered by category"""
        all_patterns = {**self.patterns, **self.custom_patterns}
        if category:
            return [name for name, pattern in all_patterns.items() 
                   if pattern.get('category') == category]
        return list(all_patterns.keys())
    
    def get_categories(self) -> List[str]:
        """Get list of available categories"""
        all_patterns = {**self.patterns, **self.custom_patterns}
        categories = set(pattern.get('category', 'other') 
                        for pattern in all_patterns.values())
        return sorted(list(categories))
    
    def convert_to_grid(self, pattern_name: str) -> Dict[Tuple[int, int], str]:
        """Convert a pattern to grid coordinates"""
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            return {}
        
        grid_notes = {}
        notes = pattern['notes']
        
        # Map notes to grid positions (simplified mapping)
        note_to_pos = {
            'C4': (11, 0), 'D4': (10, 0), 'E4': (9, 0), 'F4': (8, 0),
            'G4': (7, 0), 'A4': (6, 0), 'B4': (5, 0), 'C5': (4, 0),
            'D5': (3, 0), 'E5': (2, 0), 'F5': (1, 0), 'G5': (0, 0),
            'A5': (0, 1), 'B5': (0, 2), 'C6': (0, 3), 'D6': (0, 4)
        }
        
        for i, note in enumerate(notes):
            if note in note_to_pos:
                pos = note_to_pos[note]
                grid_notes[pos] = note
        
        return grid_notes
    
    def create_pattern_from_grid(self, grid_notes: Dict[Tuple[int, int], str], 
                                name: str, description: str = "", 
                                category: str = "custom") -> Dict:
        """Create a pattern from grid notes"""
        notes = []
        for pos in sorted(grid_notes.keys(), key=lambda x: x[1]):  # Sort by column
            notes.append(grid_notes[pos])
        
        pattern = {
            "name": name,
            "description": description,
            "notes": notes,
            "tempo": 120,
            "category": category
        }
        
        return pattern


def main():
    """Test the pattern library"""
    lib = PatternLibrary()
    
    print("Seq80x25 Pattern Library")
    print("=" * 40)
    
    # List all categories
    print("Available categories:")
    for category in lib.get_categories():
        print(f"  - {category}")
    print()
    
    # List patterns by category
    for category in lib.get_categories():
        print(f"{category.title()} patterns:")
        patterns = lib.list_patterns(category)
        for pattern_name in patterns:
            pattern = lib.get_pattern(pattern_name)
            print(f"  - {pattern['name']}: {pattern['description']}")
        print()
    
    # Test pattern conversion
    print("Testing pattern conversion:")
    grid_notes = lib.convert_to_grid("c_major_scale")
    print(f"C Major Scale grid positions: {grid_notes}")
    
    # Test custom pattern creation
    custom_grid = {(11, 0): "C4", (10, 1): "D4", (9, 2): "E4"}
    custom_pattern = lib.create_pattern_from_grid(
        custom_grid, "My Pattern", "A custom pattern", "custom"
    )
    print(f"Custom pattern: {custom_pattern}")


if __name__ == "__main__":
    main()
