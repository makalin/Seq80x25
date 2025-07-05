# Seq80x25

A retro-inspired, terminal-based music sequencer that brings the nostalgic charm of DOS-style interfaces to modern music creation. Built to run in an 80x25 terminal grid, Seq80x25 lets you compose chiptune-style music with a simple, text-based interface.

## Features

- **Retro UI**: 80x25 terminal grid with ASCII-based visuals, mimicking classic DOS aesthetics.
- **Music Sequencing**: Create melodies and rhythms using a grid-based note editor.
- **Chiptune Sounds**: Generate square-wave and basic waveforms via `pygame` for that authentic 8-bit feel.
- **Cross-Platform**: Runs on Windows, macOS, and Linux with Python.
- **Browser Demo**: Play sequences in the browser using Pyodide (no local file I/O).
- **Customizable**: Adjust tempo, note duration, and instrument types within the terminal.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/frangedev/seq80x25.git
   cd seq80x25
   ```

2. **Install Dependencies**:
   Ensure Python 3.8+ is installed, then run:
   ```bash
   pip install textual pygame numpy
   ```

3. **Run the Sequencer**:
   ```bash
   python seq80x25.py
   ```

## Usage

- Launch the sequencer to enter the 80x25 terminal interface.
- Use arrow keys to navigate the note grid.
- Press `Enter` to place or edit notes (e.g., C4, D#5).
- Adjust tempo with `+/-` keys.
- Press `P` to play your sequence, `S` to stop.
- Save sequences as text-based patterns (no file I/O for browser mode).
- Check `HELP` (press `H`) for full keybindings.

## Browser Demo

Run Seq80x25 in your browser using Pyodide! Visit `https://github.com/frangedev/Seq80x25/` (TBD) to try it without installation. Note: Browser mode uses `pygame` with NumPy arrays for sound, avoiding local file access.

## Tech Stack

- **Python**: Core language for simplicity and cross-platform support.
- **Textual**: Reactive terminal UI framework for retro-styled interface.
- **pygame**: Audio synthesis for chiptune-style sounds.
- **NumPy**: Waveform generation for custom sounds.
- **Pyodide**: Enables browser-based execution.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m "Add YourFeature"`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and report issues via [GitHub Issues](https://github.com/frangedev/seq80x25/issues).

## Roadmap

- Add support for multiple tracks (e.g., melody, bass, drums).
- Implement export to MIDI or WAV (desktop only).
- Enhance ASCII visuals with customizable themes.
- Add preset patterns for quick chiptune composition.

## License

MIT License. See [LICENSE](LICENSE) for details.

Compose in Code: Retro Beats in 80x25 Glory!
