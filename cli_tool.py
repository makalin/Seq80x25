#!/usr/bin/env python3
"""
Command Line Interface for Seq80x25
Provides command-line access to Seq80x25 functionality
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from patterns import PatternLibrary
    from export_tools import SequenceExporter
    from audio_effects import AudioEffects
    from project_manager import ProjectManager
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required modules are available")
    sys.exit(1)


class Seq80x25CLI:
    """Command-line interface for Seq80x25"""
    
    def __init__(self):
        self.pattern_lib = PatternLibrary()
        self.exporter = SequenceExporter()
        self.effects = AudioEffects()
        self.project_mgr = ProjectManager()
    
    def list_patterns(self, category: Optional[str] = None):
        """List available patterns"""
        if category:
            patterns = self.pattern_lib.list_patterns(category)
            print(f"Patterns in category '{category}':")
        else:
            patterns = self.pattern_lib.list_patterns()
            print("All available patterns:")
        
        for pattern_name in patterns:
            pattern = self.pattern_lib.get_pattern(pattern_name)
            print(f"  {pattern_name}: {pattern['name']} - {pattern['description']}")
    
    def show_pattern(self, pattern_name: str):
        """Show details of a specific pattern"""
        pattern = self.pattern_lib.get_pattern(pattern_name)
        if not pattern:
            print(f"Pattern '{pattern_name}' not found")
            return
        
        print(f"Pattern: {pattern['name']}")
        print(f"Description: {pattern['description']}")
        print(f"Category: {pattern['category']}")
        print(f"Tempo: {pattern['tempo']} BPM")
        print(f"Notes: {' '.join(pattern['notes'])}")
    
    def create_pattern(self, name: str, notes: list, description: str = "", 
                      category: str = "custom", tempo: int = 120):
        """Create a custom pattern"""
        pattern = {
            "name": name,
            "description": description,
            "notes": notes,
            "tempo": tempo,
            "category": category
        }
        
        if self.pattern_lib.save_custom_pattern(name, pattern):
            print(f"Pattern '{name}' created successfully")
        else:
            print(f"Error creating pattern '{name}'")
    
    def export_sequence(self, input_file: str, output_format: str, 
                       output_file: Optional[str] = None):
        """Export a sequence to various formats"""
        if not os.path.exists(input_file):
            print(f"Input file '{input_file}' not found")
            return
        
        try:
            with open(input_file, 'r') as f:
                import json
                sequence_data = json.load(f)
        except Exception as e:
            print(f"Error reading input file: {e}")
            return
        
        if not output_file:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.{output_format}"
        
        success = False
        if output_format == "json":
            success = self.exporter.export_to_json(sequence_data, output_file)
        elif output_format == "wav":
            success = self.exporter.export_to_wav(sequence_data, output_file)
        elif output_format == "midi":
            success = self.exporter.export_to_midi(sequence_data, output_file)
        elif output_format == "txt":
            success = self.exporter.export_to_text(sequence_data, output_file)
        elif output_format == "csv":
            success = self.exporter.export_to_csv(sequence_data, output_file)
        else:
            print(f"Unsupported output format: {output_format}")
            return
        
        if success:
            print(f"Sequence exported to {output_file}")
        else:
            print(f"Error exporting sequence to {output_file}")
    
    def apply_effects(self, input_file: str, output_file: str, effects: list):
        """Apply audio effects to a WAV file"""
        if not os.path.exists(input_file):
            print(f"Input file '{input_file}' not found")
            return
        
        try:
            import wave
            with wave.open(input_file, 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                audio_data = wav_file.readframes(wav_file.getnframes())
                
            # Convert to numpy array
            import numpy as np
            audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32767
            
            # Apply effects
            processed_audio = self.effects.apply_multiple_effects(audio, effects)
            
            # Save processed audio
            processed_audio = (processed_audio * 32767).astype(np.int16)
            with wave.open(output_file, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(processed_audio.tobytes())
            
            print(f"Effects applied and saved to {output_file}")
            
        except Exception as e:
            print(f"Error applying effects: {e}")
    
    def project_commands(self, command: str, *args):
        """Handle project-related commands"""
        if command == "list":
            projects = self.project_mgr.list_projects()
            if projects:
                print("Available projects:")
                for project in projects:
                    info = self.project_mgr.get_project_info(project)
                    print(f"  {project}: {info['description']}")
            else:
                print("No projects found")
        
        elif command == "create":
            if len(args) < 1:
                print("Usage: project create <name> [description] [author]")
                return
            name = args[0]
            description = args[1] if len(args) > 1 else ""
            author = args[2] if len(args) > 2 else ""
            self.project_mgr.create_project(name, description, author)
        
        elif command == "open":
            if len(args) < 1:
                print("Usage: project open <name>")
                return
            self.project_mgr.open_project(args[0])
        
        elif command == "close":
            self.project_mgr.close_project()
        
        elif command == "sequences":
            sequences = self.project_mgr.list_sequences()
            if sequences:
                print("Sequences in current project:")
                for seq in sequences:
                    print(f"  {seq}")
            else:
                print("No sequences in current project")
        
        else:
            print(f"Unknown project command: {command}")
            print("Available commands: list, create, open, close, sequences")
    
    def run(self):
        """Run the CLI"""
        parser = argparse.ArgumentParser(
            description="Seq80x25 Command Line Interface",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s patterns list
  %(prog)s patterns show c_major_scale
  %(prog)s export sequence.json wav output.wav
  %(prog)s project create "My Project" "A test project"
  %(prog)s project open "My_Project"
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Patterns subcommand
        patterns_parser = subparsers.add_parser('patterns', help='Pattern management')
        patterns_parser.add_argument('action', choices=['list', 'show', 'create', 'categories'],
                                   help='Action to perform')
        patterns_parser.add_argument('--category', help='Filter by category')
        patterns_parser.add_argument('--name', help='Pattern name')
        patterns_parser.add_argument('--notes', nargs='+', help='Note sequence')
        patterns_parser.add_argument('--description', help='Pattern description')
        patterns_parser.add_argument('--tempo', type=int, default=120, help='Tempo in BPM')
        
        # Export subcommand
        export_parser = subparsers.add_parser('export', help='Export sequences')
        export_parser.add_argument('input', help='Input sequence file')
        export_parser.add_argument('format', choices=['json', 'wav', 'midi', 'txt', 'csv'],
                                 help='Output format')
        export_parser.add_argument('--output', help='Output file path')
        
        # Effects subcommand
        effects_parser = subparsers.add_parser('effects', help='Audio effects')
        effects_parser.add_argument('input', help='Input WAV file')
        effects_parser.add_argument('output', help='Output WAV file')
        effects_parser.add_argument('--reverb', type=float, help='Reverb room size')
        effects_parser.add_argument('--delay', type=float, help='Delay time in seconds')
        effects_parser.add_argument('--distortion', type=float, help='Distortion amount')
        
        # Project subcommand
        project_parser = subparsers.add_parser('project', help='Project management')
        project_parser.add_argument('action', choices=['list', 'create', 'open', 'close', 'sequences'],
                                  help='Project action')
        project_parser.add_argument('args', nargs='*', help='Additional arguments')
        
        # Parse arguments
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            if args.command == 'patterns':
                if args.action == 'list':
                    self.list_patterns(args.category)
                elif args.action == 'show':
                    if not args.name:
                        print("Pattern name required for 'show' action")
                        return
                    self.show_pattern(args.name)
                elif args.action == 'create':
                    if not args.name or not args.notes:
                        print("Pattern name and notes required for 'create' action")
                        return
                    self.create_pattern(args.name, args.notes, args.description or "", 
                                     tempo=args.tempo)
                elif args.action == 'categories':
                    categories = self.pattern_lib.get_categories()
                    print("Available categories:")
                    for category in categories:
                        print(f"  {category}")
            
            elif args.command == 'export':
                self.export_sequence(args.input, args.format, args.output)
            
            elif args.command == 'effects':
                effects = []
                if args.reverb:
                    effects.append({
                        'type': 'reverb',
                        'params': {'room_size': args.reverb, 'damping': 0.5}
                    })
                if args.delay:
                    effects.append({
                        'type': 'delay',
                        'params': {'delay_time': args.delay, 'feedback': 0.3}
                    })
                if args.distortion:
                    effects.append({
                        'type': 'distortion',
                        'params': {'amount': args.distortion, 'type_': 'soft'}
                    })
                
                if effects:
                    self.apply_effects(args.input, args.output, effects)
                else:
                    print("No effects specified")
            
            elif args.command == 'project':
                self.project_commands(args.action, *args.args)
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point"""
    cli = Seq80x25CLI()
    cli.run()


if __name__ == "__main__":
    main()
