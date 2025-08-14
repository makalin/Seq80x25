#!/usr/bin/env python3
"""
Demo script for Seq80x25 - shows basic functionality without the full UI
"""

import time
import numpy as np

def note_to_frequency(note_name):
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

def generate_tone(frequency, duration, sample_rate=44100):
    """Generate a simple sine wave tone"""
    samples = int(sample_rate * duration)
    
    # Generate sine wave
    t = np.linspace(0, duration, samples, False)
    tone = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Convert to 16-bit integers
    tone = (tone * 32767).astype(np.int16)
    
    return tone, sample_rate

def play_sequence(notes, tempo=120):
    """Play a sequence of notes"""
    print(f"Playing sequence at {tempo} BPM...")
    
    # Calculate step duration (16th notes)
    step_duration = 60.0 / tempo / 4
    
    for i, note in enumerate(notes):
        if note is None:
            print(f"Step {i+1:02d}: Rest")
        else:
            freq = note_to_frequency(note)
            print(f"Step {i+1:02d}: {note} ({freq:.1f} Hz)")
            
            # Generate and save tone (instead of playing)
            tone, sr = generate_tone(freq, step_duration)
            
            # Save as WAV file for this demo
            import wave
            import os
            
            # Ensure samples directory exists
            os.makedirs("samples", exist_ok=True)
            
            filename = os.path.join("samples", f"step_{i+1:02d}_{note}.wav")
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sr)
                wav_file.writeframes(tone.tobytes())
            
            print(f"  Saved: {filename}")
        
        time.sleep(step_duration)
    
    print("Sequence complete!")

def main():
    """Main demo function"""
    print("Seq80x25 - Retro Music Sequencer Demo")
    print("=" * 40)
    
    # Demo sequence: C major scale
    demo_sequence = [
        "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5",
        "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4"
    ]
    
    print("Demo sequence: C major scale (ascending and descending)")
    print("Notes:", " ".join(demo_sequence))
    print()
    
    # Show frequency calculations
    print("Note frequencies:")
    for note in demo_sequence:
        freq = note_to_frequency(note)
        print(f"  {note}: {freq:.1f} Hz")
    print()
    
    # Play the sequence
    try:
        play_sequence(demo_sequence, tempo=120)
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error during demo: {e}")
        print("This demo generates WAV files instead of playing audio")
        print("You can play the generated WAV files with any audio player")

if __name__ == "__main__":
    main()
