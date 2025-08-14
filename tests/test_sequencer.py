#!/usr/bin/env python3
"""
Tests for Seq80x25 sequencer functionality
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import seq80x25
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seq80x25 import NoteGrid


class TestNoteGrid:
    """Test the NoteGrid class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.grid = NoteGrid()
    
    def test_initialization(self):
        """Test that the grid initializes correctly"""
        assert self.grid.grid_width == 16
        assert self.grid.grid_height == 12
        assert self.grid.tempo == 120
        assert not self.grid.is_playing
        assert len(self.grid.notes) == 0
    
    def test_note_names(self):
        """Test that note names are correctly defined"""
        expected_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        assert self.grid.note_names == expected_notes
    
    def test_octaves(self):
        """Test that octaves are correctly defined"""
        expected_octaves = [4, 5, 6, 7, 8]
        assert self.grid.octaves == expected_octaves
    
    def test_get_note_name_valid_position(self):
        """Test getting note names for valid positions"""
        # Test C4 (bottom-left)
        note = self.grid.get_note_name((11, 0))
        assert note == "C4"
        
        # Test A5 (middle)
        note = self.grid.get_note_name((6, 0))
        assert note == "A5"
        
        # Test B8 (top-right)
        note = self.grid.get_note_name((0, 15))
        assert note == "B8"
    
    def test_get_note_name_invalid_position(self):
        """Test getting note names for invalid positions"""
        # Out of bounds
        note = self.grid.get_note_name((20, 0))
        assert note == "---"
        
        note = self.grid.get_note_name((0, 20))
        assert note == "---"
        
        # Negative positions
        note = self.grid.get_note_name((-1, 0))
        assert note == "---"
    
    def test_note_to_frequency(self):
        """Test note to frequency conversion"""
        # A4 should be 440Hz
        freq = self.grid.note_to_frequency("A4")
        assert abs(freq - 440.0) < 0.1
        
        # C4 should be 261.63Hz
        freq = self.grid.note_to_frequency("C4")
        assert abs(freq - 261.63) < 0.1
        
        # Invalid notes should return 0
        freq = self.grid.note_to_frequency("X5")
        assert freq == 0
        
        freq = self.grid.note_to_frequency("C")
        assert freq == 0
    
    def test_tempo_limits(self):
        """Test tempo adjustment limits"""
        # Test upper limit
        self.grid.tempo = 200
        self.grid.tempo = 210  # Should be capped at 200
        assert self.grid.tempo == 200
        
        # Test lower limit
        self.grid.tempo = 60
        self.grid.tempo = 50  # Should be capped at 60
        assert self.grid.tempo == 60
    
    def test_clear_grid(self):
        """Test clearing the grid"""
        # Add some notes
        self.grid.notes[(0, 0)] = "C4"
        self.grid.notes[(5, 5)] = "F5"
        assert len(self.grid.notes) == 2
        
        # Clear the grid
        self.grid.clear_grid()
        assert len(self.grid.notes) == 0
    
    def test_playback_control(self):
        """Test playback start/stop"""
        # Start playback
        self.grid.start_playback()
        assert self.grid.is_playing
        assert self.grid.playhead == 0
        
        # Stop playback
        self.grid.stop_playback()
        assert not self.grid.is_playing


class TestAudioGeneration:
    """Test audio generation functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.grid = NoteGrid()
    
    def test_frequency_calculation(self):
        """Test frequency calculations for various notes"""
        # Test octave relationships (each octave doubles frequency)
        c4_freq = self.grid.note_to_frequency("C4")
        c5_freq = self.grid.note_to_frequency("C5")
        assert abs(c5_freq - (c4_freq * 2)) < 0.1
        
        # Test semitone relationships
        c4_freq = self.grid.note_to_frequency("C4")
        c_sharp4_freq = self.grid.note_to_frequency("C#4")
        # C# should be approximately 1.0595 times C frequency
        assert abs(c_sharp4_freq - (c4_freq * 1.0595)) < 1.0


if __name__ == "__main__":
    pytest.main([__file__])
