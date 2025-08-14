#!/usr/bin/env python3
"""
Seq80x25 - A retro-inspired, terminal-based music sequencer
Built to run in an 80x25 terminal grid with ASCII-based visuals
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple
import pygame
import numpy as np
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Label
from textual.widgets import DataTable, Input, Select
from textual.reactive import reactive
from textual import events
from textual.binding import Binding


class NoteGrid(Static):
    """The main note grid widget for the sequencer"""
    
    current_position = reactive((0, 0))
    notes = reactive({})
    tempo = reactive(120)
    is_playing = reactive(False)
    
    def __init__(self):
        super().__init__()
        self.grid_width = 16
        self.grid_height = 12
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.octaves = [4, 5, 6, 7, 8]
        self.notes = {}
        self.current_position = (0, 0)
        self.tempo = 120
        self.is_playing = False
        self.playhead = 0
        
    def compose(self) -> ComposeResult:
        """Create the note grid layout"""
        with Container(id="grid-container"):
            yield Label("Seq80x25 - Retro Music Sequencer", id="title")
            with Horizontal(id="controls"):
                yield Button("Play", id="play-btn", variant="primary")
                yield Button("Stop", id="stop-btn", variant="error")
                yield Button("Clear", id="clear-btn")
                yield Label(f"Tempo: {self.tempo} BPM", id="tempo-label")
                yield Button("+", id="tempo-up")
                yield Button("-", id="tempo-down")
            
            with Horizontal(id="grid-layout"):
                # Note labels (vertical)
                with Vertical(id="note-labels"):
                    for octave in reversed(self.octaves):
                        for note in reversed(self.note_names):
                            yield Label(f"{note}{octave}", classes="note-label")
                
                # The main grid
                with Container(id="main-grid"):
                    for row in range(self.grid_height):
                        with Horizontal(classes="grid-row"):
                            for col in range(self.grid_width):
                                cell = Button(" ", id=f"cell-{row}-{col}", classes="grid-cell")
                                cell.styles.width = "3"
                                cell.styles.height = "1"
                                yield cell
                
                # Step labels (horizontal)
                with Vertical(id="step-labels"):
                    for step in range(self.grid_width):
                        yield Label(f"{step+1:02d}", classes="step-label")
            
            with Horizontal(id="info-panel"):
                yield Label("Use arrow keys to navigate, Enter to place notes", id="help-text")
                yield Label(f"Current: {self.get_note_name(self.current_position)}", id="current-note")
    
    def get_note_name(self, pos: Tuple[int, int]) -> str:
        """Convert grid position to note name"""
        if not pos or pos[0] >= self.grid_height or pos[1] >= self.grid_width:
            return "---"
        
        note_idx = (self.grid_height - 1 - pos[0]) % len(self.note_names)
        octave_idx = (self.grid_height - 1 - pos[0]) // len(self.note_names)
        
        if octave_idx < len(self.octaves):
            return f"{self.note_names[note_idx]}{self.octaves[octave_idx]}"
        return "---"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        
        if button_id == "play-btn":
            self.start_playback()
        elif button_id == "stop-btn":
            self.stop_playback()
        elif button_id == "clear-btn":
            self.clear_grid()
        elif button_id == "tempo-up":
            self.tempo = min(200, self.tempo + 10)
        elif button_id == "tempo-down":
            self.tempo = max(60, self.tempo - 10)
        elif button_id.startswith("cell-"):
            self.toggle_note(event.button)
    
    def toggle_note(self, cell: Button) -> None:
        """Toggle a note on/off in the grid"""
        # Extract position from cell ID
        parts = cell.id.split("-")
        row, col = int(parts[1]), int(parts[2])
        
        if (row, col) in self.notes:
            del self.notes[(row, col)]
            cell.label = " "
            cell.styles.background = "default"
        else:
            note_name = self.get_note_name((row, col))
            if note_name != "---":
                self.notes[(row, col)] = note_name
                cell.label = "♪"
                cell.styles.background = "green"
    
    def start_playback(self) -> None:
        """Start playing the sequence"""
        if not self.notes:
            return
        
        self.is_playing = True
        self.playhead = 0
        asyncio.create_task(self.play_sequence())
    
    def stop_playback(self) -> None:
        """Stop playing the sequence"""
        self.is_playing = False
    
    async def play_sequence(self) -> None:
        """Play the sequence with the current tempo"""
        step_duration = 60.0 / self.tempo / 4  # 16th note duration
        
        while self.is_playing:
            # Play notes at current step
            for (row, col), note_name in self.notes.items():
                if col == self.playhead:
                    self.play_note(note_name)
            
            # Update playhead
            self.playhead = (self.playhead + 1) % self.grid_width
            
            # Highlight current step
            self.highlight_step(self.playhead)
            
            await asyncio.sleep(step_duration)
    
    def highlight_step(self, step: int) -> None:
        """Highlight the current step in playback"""
        # Reset all step highlights
        for i in range(self.grid_width):
            cell = self.query_one(f"#cell-0-{i}", Button)
            if cell:
                cell.styles.border = ("none", "default")
        
        # Highlight current step
        if step < self.grid_width:
            cell = self.query_one(f"#cell-0-{step}", Button)
            if cell:
                cell.styles.border = ("solid", "yellow")
    
    def play_note(self, note_name: str) -> None:
        """Play a note using pygame audio"""
        try:
            # Simple square wave generation
            frequency = self.note_to_frequency(note_name)
            if frequency > 0:
                self.generate_tone(frequency, 0.1)
        except Exception as e:
            # Silently fail if audio isn't available
            pass
    
    def note_to_frequency(self, note_name: str) -> float:
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
    
    def generate_tone(self, frequency: float, duration: float) -> None:
        """Generate a simple square wave tone"""
        try:
            sample_rate = 44100
            samples = int(sample_rate * duration)
            
            # Generate square wave
            t = np.linspace(0, duration, samples, False)
            tone = np.sin(2 * np.pi * frequency * t) * 0.3
            
            # Convert to 16-bit integers
            tone = (tone * 32767).astype(np.int16)
            
            # Play the tone
            pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
            sound = pygame.sndarray.make_sound(tone)
            sound.play()
            
        except Exception:
            # Silently fail if pygame audio isn't available
            pass
    
    def clear_grid(self) -> None:
        """Clear all notes from the grid"""
        self.notes = {}
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                cell = self.query_one(f"#cell-{row}-{col}", Button)
                if cell:
                    cell.label = " "
                    cell.styles.background = "default"
    
    def on_key(self, event: events.Key) -> None:
        """Handle keyboard navigation"""
        if event.key == "up":
            self.current_position = (max(0, self.current_position[0] - 1), self.current_position[1])
        elif event.key == "down":
            self.current_position = (min(self.grid_height - 1, self.current_position[0] + 1), self.current_position[1])
        elif event.key == "left":
            self.current_position = (self.current_position[0], max(0, self.current_position[1] - 1))
        elif event.key == "right":
            self.current_position = (self.current_position[0], min(self.grid_width - 1, self.current_position[1] + 1))
        elif event.key == "enter":
            # Place note at current position
            cell = self.query_one(f"#cell-{self.current_position[0]}-{self.current_position[1]}", Button)
            if cell:
                self.toggle_note(cell)
        
        # Update current note display
        current_note_label = self.query_one("#current-note", Label)
        if current_note_label:
            current_note_label.update(f"Current: {self.get_note_name(self.current_position)}")
        
        # Update tempo display
        tempo_label = self.query_one("#tempo-label", Label)
        if tempo_label:
            tempo_label.update(f"Tempo: {self.tempo} BPM")


class Seq80x25App(App):
    """Main application class for Seq80x25"""
    
    CSS_PATH = "seq80x25.css"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("h", "help", "Help"),
        Binding("space", "play_pause", "Play/Pause"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create the main app layout"""
        yield Header()
        yield NoteGrid()
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the app when mounted"""
        self.title = "Seq80x25 - Retro Music Sequencer"
        self.sub_title = "Compose in Code: Retro Beats in 80x25 Glory!"
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()
    
    def action_help(self) -> None:
        """Show help information"""
        # Simple help overlay
        help_text = """
        Seq80x25 Controls:
        
        Navigation:
        - Arrow keys: Move cursor
        - Enter: Place/remove note
        - Space: Play/Pause
        
        Playback:
        - P: Play sequence
        - S: Stop sequence
        - +/-: Adjust tempo
        
        Other:
        - H: This help
        - Q: Quit
        
        Create chiptune magic in your terminal!
        """
        self.notify(help_text, severity="information")
    
    def action_play_pause(self) -> None:
        """Toggle play/pause"""
        note_grid = self.query_one(NoteGrid)
        if note_grid.is_playing:
            note_grid.stop_playback()
        else:
            note_grid.start_playback()


def main():
    """Main entry point"""
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Run the app
        app = Seq80x25App()
        app.run()
        
    except Exception as e:
        print(f"Error starting Seq80x25: {e}")
        print("Make sure you have the required dependencies installed:")
        print("pip install textual pygame numpy")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
