# Seq80x25 Usage Guide

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Sequencer**:
   ```bash
   python seq80x25.py
   ```

   Or use the launcher scripts:
   - **Unix/macOS**: `./launch.sh`
   - **Windows**: `launch.bat`

## Interface Overview

The Seq80x25 interface is designed to fit in an 80x25 terminal grid, featuring:

- **16-step sequencer** (horizontal)
- **5 octaves** of notes (vertical)
- **Retro DOS-style** color scheme
- **Real-time playback** with visual feedback

## Controls

### Navigation
- **Arrow Keys**: Move cursor around the grid
- **Enter**: Place/remove note at current position
- **Space**: Play/Pause current sequence

### Playback
- **Play Button**: Start sequence playback
- **Stop Button**: Stop playback
- **Clear Button**: Clear all notes from grid
- **+/- Buttons**: Adjust tempo (60-200 BPM)

### Global Shortcuts
- **H**: Show help information
- **Q**: Quit the application

## Creating Music

### 1. Navigate the Grid
- Use arrow keys to move the cursor
- The current note is displayed at the bottom
- Grid positions map to specific notes (C4, D#5, etc.)

### 2. Place Notes
- Move to desired position
- Press Enter to place a note (♪ symbol appears)
- Press Enter again to remove the note

### 3. Set Tempo
- Use +/- buttons to adjust BPM
- Range: 60-200 BPM
- Default: 120 BPM

### 4. Play Your Sequence
- Click Play or press Space
- Watch the playhead move across the grid
- Current step is highlighted in yellow

## Note Layout

The vertical grid represents musical notes:

```
Row 0:  B8  B#8  C9  C#9  D9  D#9  E9  F9  F#9  G9  G#9  A9
Row 1:  A8  A#8  B8  C8   C#8 D8   D#8 E8   F8   F#8 G8   G#8
Row 2:  G7  G#7  A7  A#7  B7  C7   C#7 D7   D#7  E7   F7   F#7
...
Row 11: C4  C#4  D4  D#4  E4  F4   F#4 G4   G#4 A4   A#4  B4
```

## Tips for Better Music

### 1. Start Simple
- Begin with a basic melody using 4-8 steps
- Use notes from the same scale (e.g., C major: C, D, E, F, G, A, B)

### 2. Rhythm Patterns
- Place notes on beats 1, 3, 5, 7 for a basic rhythm
- Experiment with syncopation (off-beat notes)

### 3. Melodic Contour
- Create ascending/descending patterns
- Use repetition for memorable melodies
- Vary note lengths by leaving some steps empty

### 4. Chiptune Style
- Focus on strong, simple melodies
- Use the full range of octaves
- Keep patterns relatively short (8-16 steps)

## Example Patterns

### Basic C Major Scale (Ascending)
```
Step:  1  2  3  4  5  6  7  8
Note:  C4 D4 E4 F4 G4 A4 B4 C5
```

### Simple Rhythm Pattern
```
Step:  1  2  3  4  5  6  7  8
Note:  C4 -  E4 -  G4 -  C5 -
```

### Bass Line
```
Step:  1  2  3  4  5  6  7  8
Note:  C3 -  C3 -  G3 -  G3 -
```

## Troubleshooting

### Audio Issues
- **No Sound**: Check system volume and audio drivers
- **Crackling**: Try reducing tempo or closing other audio applications
- **Lag**: Ensure pygame is properly installed

### Display Issues
- **Grid Not Visible**: Ensure terminal supports 80x25 or larger
- **Colors Wrong**: Check terminal color support
- **Layout Broken**: Try resizing terminal window

### Performance Issues
- **Slow Playback**: Reduce tempo or simplify patterns
- **High CPU Usage**: Close other applications
- **Memory Issues**: Clear grid and restart application

## Advanced Features

### Custom Patterns
- Create your own musical patterns
- Experiment with different scales and modes
- Try creating bass lines and melodies

### Tempo Changes
- Adjust tempo during playback
- Use different tempos for different sections
- Create dynamic performances

### Grid Management
- Use the full 16-step grid for longer compositions
- Create multiple patterns and switch between them
- Use empty steps for rests and rhythm variation

## Keyboard Shortcuts Reference

| Action | Key | Description |
|--------|-----|-------------|
| Move Up | ↑ | Move cursor up one row |
| Move Down | ↓ | Move cursor down one row |
| Move Left | ← | Move cursor left one step |
| Move Right | → | Move cursor right one step |
| Place Note | Enter | Toggle note at current position |
| Play/Pause | Space | Start/stop playback |
| Help | H | Show help information |
| Quit | Q | Exit application |

## Getting Help

- **In-App Help**: Press H for quick reference
- **Demo Script**: Run `python demo.py` for basic functionality
- **Documentation**: Check README.md for detailed information
- **Issues**: Report bugs on GitHub

## Contributing

Want to improve Seq80x25? Check out the contributing guidelines in the main README and consider:

- Adding new features
- Improving the UI
- Creating preset patterns
- Enhancing audio quality
- Adding export functionality

Happy sequencing! 🎵
