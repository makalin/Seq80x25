#!/usr/bin/env python3
"""
Export Tools for Seq80x25
Export sequences to various formats including MIDI, WAV, and text
"""

import json
import wave
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import os


class SequenceExporter:
    """Export sequences to various formats"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def export_to_json(self, sequence_data: Dict, filename: str) -> bool:
        """Export sequence to JSON format"""
        try:
            export_data = {
                "metadata": {
                    "name": sequence_data.get("name", "Untitled"),
                    "tempo": sequence_data.get("tempo", 120),
                    "grid_width": sequence_data.get("grid_width", 16),
                    "grid_height": sequence_data.get("grid_height", 12),
                    "export_date": str(np.datetime64('now')),
                    "version": "1.0"
                },
                "notes": sequence_data.get("notes", {}),
                "settings": sequence_data.get("settings", {})
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def export_to_wav(self, sequence_data: Dict, filename: str, 
                      duration_per_step: float = 0.25) -> bool:
        """Export sequence to WAV format"""
        try:
            notes = sequence_data.get("notes", {})
            tempo = sequence_data.get("tempo", 120)
            
            # Calculate step duration
            step_duration = 60.0 / tempo / 4  # 16th note duration
            
            # Generate audio for each step
            all_audio = []
            for step in range(16):  # 16 steps
                step_notes = []
                for (row, col), note_name in notes.items():
                    if col == step:
                        freq = self._note_to_frequency(note_name)
                        if freq > 0:
                            audio = self._generate_tone(freq, step_duration)
                            step_notes.append(audio)
                
                if step_notes:
                    # Mix notes at this step
                    step_audio = np.sum(step_notes, axis=0)
                    # Normalize to prevent clipping
                    if np.max(np.abs(step_audio)) > 0:
                        step_audio = step_audio / np.max(np.abs(step_audio)) * 0.7
                else:
                    # Silence for this step
                    step_audio = np.zeros(int(step_duration * self.sample_rate))
                
                all_audio.append(step_audio)
            
            # Concatenate all steps
            if all_audio:
                final_audio = np.concatenate(all_audio)
                
                # Convert to 16-bit integers
                final_audio = (final_audio * 32767).astype(np.int16)
                
                # Save as WAV
                with wave.open(filename, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(final_audio.tobytes())
                
                return True
            else:
                print("No notes to export")
                return False
                
        except Exception as e:
            print(f"Error exporting to WAV: {e}")
            return False
    
    def export_to_midi(self, sequence_data: Dict, filename: str) -> bool:
        """Export sequence to MIDI format (simplified)"""
        try:
            # This is a simplified MIDI export
            # In a full implementation, you'd use a proper MIDI library
            notes = sequence_data.get("notes", {})
            tempo = sequence_data.get("tempo", 120)
            
            # Create a simple MIDI-like text representation
            midi_data = {
                "format": "MIDI-like",
                "tempo": tempo,
                "ticks_per_beat": 480,
                "tracks": [
                    {
                        "name": "Seq80x25 Track",
                        "notes": []
                    }
                ]
            }
            
            # Convert grid notes to MIDI events
            for (row, col), note_name in notes.items():
                freq = self._note_to_frequency(note_name)
                if freq > 0:
                    midi_note = self._frequency_to_midi_note(freq)
                    if midi_note is not None:
                        event = {
                            "time": col * 120,  # 120 ticks per step
                            "note": midi_note,
                            "velocity": 100,
                            "duration": 120
                        }
                        midi_data["tracks"][0]["notes"].append(event)
            
            # Save as JSON (simplified MIDI representation)
            midi_filename = filename.replace('.mid', '_midi.json')
            with open(midi_filename, 'w') as f:
                json.dump(midi_data, f, indent=2)
            
            print(f"MIDI-like data saved to {midi_filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting to MIDI: {e}")
            return False
    
    def export_to_text(self, sequence_data: Dict, filename: str) -> bool:
        """Export sequence to human-readable text format"""
        try:
            notes = sequence_data.get("notes", {})
            tempo = sequence_data.get("tempo", 120)
            
            with open(filename, 'w') as f:
                f.write("Seq80x25 Sequence Export\n")
                f.write("=" * 30 + "\n\n")
                f.write(f"Tempo: {tempo} BPM\n")
                f.write(f"Total Notes: {len(notes)}\n\n")
                
                f.write("Step-by-step breakdown:\n")
                f.write("-" * 25 + "\n")
                
                for step in range(16):
                    step_notes = []
                    for (row, col), note_name in notes.items():
                        if col == step:
                            step_notes.append(note_name)
                    
                    if step_notes:
                        f.write(f"Step {step+1:2d}: {', '.join(step_notes)}\n")
                    else:
                        f.write(f"Step {step+1:2d}: (rest)\n")
                
                f.write("\nNote positions:\n")
                f.write("-" * 15 + "\n")
                for (row, col), note_name in sorted(notes.items(), key=lambda x: x[1]):
                    f.write(f"({row:2d}, {col:2d}) -> {note_name}\n")
            
            return True
        except Exception as e:
            print(f"Error exporting to text: {e}")
            return False
    
    def export_to_csv(self, sequence_data: Dict, filename: str) -> bool:
        """Export sequence to CSV format for analysis"""
        try:
            notes = sequence_data.get("notes", {})
            
            with open(filename, 'w') as f:
                f.write("Step,Row,Column,Note,Frequency\n")
                
                for step in range(16):
                    step_notes = []
                    for (row, col), note_name in notes.items():
                        if col == step:
                            freq = self._note_to_frequency(note_name)
                            f.write(f"{step+1},{row},{col},{note_name},{freq:.1f}\n")
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def _note_to_frequency(self, note_name: str) -> float:
        """Convert note name to frequency"""
        if len(note_name) < 2:
            return 0
        
        note = note_name[:-1]
        octave = int(note_name[-1])
        
        note_values = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 
                      'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        
        if note not in note_values:
            return 0
        
        # A4 = 440Hz
        semitones = note_values[note] + (octave - 4) * 12
        return 440 * (2 ** (semitones / 12))
    
    def _frequency_to_midi_note(self, frequency: float) -> Optional[int]:
        """Convert frequency to MIDI note number"""
        if frequency <= 0:
            return None
        
        # A4 = 440Hz = MIDI note 69
        midi_note = 69 + 12 * np.log2(frequency / 440)
        return int(round(midi_note))
    
    def _generate_tone(self, frequency: float, duration: float) -> np.ndarray:
        """Generate a tone with the given frequency and duration"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples, False)
        
        # Generate sine wave with slight harmonics for richer sound
        tone = np.sin(2 * np.pi * frequency * t) * 0.5
        tone += np.sin(2 * np.pi * frequency * 2 * t) * 0.25  # 2nd harmonic
        tone += np.sin(2 * np.pi * frequency * 3 * t) * 0.125  # 3rd harmonic
        
        # Apply simple envelope
        envelope = np.exp(-t * 2)  # Decay
        tone = tone * envelope
        
        return tone


def main():
    """Test the export tools"""
    exporter = SequenceExporter()
    
    # Sample sequence data
    sample_sequence = {
        "name": "Test Sequence",
        "tempo": 120,
        "grid_width": 16,
        "grid_height": 12,
        "notes": {
            (11, 0): "C4",
            (10, 1): "D4", 
            (9, 2): "E4",
            (8, 3): "F4",
            (7, 4): "G4",
            (6, 5): "A4",
            (5, 6): "B4",
            (4, 7): "C5"
        },
        "settings": {
            "waveform": "sine",
            "volume": 0.7
        }
    }
    
    print("Seq80x25 Export Tools Test")
    print("=" * 30)
    
    # Test JSON export
    if exporter.export_to_json(sample_sequence, "test_sequence.json"):
        print("✓ JSON export successful")
    
    # Test WAV export
    if exporter.export_to_wav(sample_sequence, "test_sequence.wav"):
        print("✓ WAV export successful")
    
    # Test text export
    if exporter.export_to_text(sample_sequence, "test_sequence.txt"):
        print("✓ Text export successful")
    
    # Test CSV export
    if exporter.export_to_csv(sample_sequence, "test_sequence.csv"):
        print("✓ CSV export successful")
    
    # Test MIDI export
    if exporter.export_to_midi(sample_sequence, "test_sequence.mid"):
        print("✓ MIDI export successful")
    
    print("\nAll export tests completed!")


if __name__ == "__main__":
    main()
