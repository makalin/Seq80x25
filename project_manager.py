#!/usr/bin/env python3
"""
Project Manager for Seq80x25
Manages multiple sequences and project organization
"""

import json
import os
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import shutil


class ProjectManager:
    """Manages Seq80x25 projects and sequences"""
    
    def __init__(self, projects_dir: str = "projects"):
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(exist_ok=True)
        self.current_project = None
        self.projects = self._load_projects()
    
    def _load_projects(self) -> Dict[str, Dict]:
        """Load existing projects"""
        projects = {}
        
        if self.projects_dir.exists():
            for project_dir in self.projects_dir.iterdir():
                if project_dir.is_dir():
                    project_file = project_dir / "project.json"
                    if project_file.exists():
                        try:
                            with open(project_file, 'r') as f:
                                project_data = json.load(f)
                                projects[project_dir.name] = project_data
                        except (json.JSONDecodeError, FileNotFoundError):
                            continue
        
        return projects
    
    def create_project(self, name: str, description: str = "", 
                      author: str = "") -> bool:
        """Create a new project"""
        try:
            # Sanitize project name
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            
            if not safe_name:
                print("Invalid project name")
                return False
            
            project_path = self.projects_dir / safe_name
            if project_path.exists():
                print(f"Project '{safe_name}' already exists")
                return False
            
            # Create project directory structure
            project_path.mkdir()
            (project_path / "sequences").mkdir()
            (project_path / "exports").mkdir()
            (project_path / "samples").mkdir()
            
            # Create project metadata
            project_data = {
                "name": name,
                "description": description,
                "author": author,
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "sequences": [],
                "settings": {
                    "default_tempo": 120,
                    "grid_width": 16,
                    "grid_height": 12,
                    "sample_rate": 44100
                }
            }
            
            # Save project file
            with open(project_path / "project.json", 'w') as f:
                json.dump(project_data, f, indent=2)
            
            # Add to projects list
            self.projects[safe_name] = project_data
            print(f"Project '{name}' created successfully")
            return True
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False
    
    def open_project(self, name: str) -> bool:
        """Open an existing project"""
        if name not in self.projects:
            print(f"Project '{name}' not found")
            return False
        
        self.current_project = name
        print(f"Opened project: {name}")
        return True
    
    def close_project(self):
        """Close the current project"""
        if self.current_project:
            print(f"Closed project: {self.current_project}")
            self.current_project = None
        else:
            print("No project is currently open")
    
    def save_sequence(self, sequence_name: str, sequence_data: Dict) -> bool:
        """Save a sequence to the current project"""
        if not self.current_project:
            print("No project is currently open")
            return False
        
        try:
            project_path = self.projects_dir / self.current_project
            sequences_dir = project_path / "sequences"
            
            # Add metadata
            sequence_data["saved"] = datetime.now().isoformat()
            sequence_data["project"] = self.current_project
            
            # Save sequence file
            sequence_file = sequences_dir / f"{sequence_name}.json"
            with open(sequence_file, 'w') as f:
                json.dump(sequence_data, f, indent=2)
            
            # Update project metadata
            if sequence_name not in self.projects[self.current_project]["sequences"]:
                self.projects[self.current_project]["sequences"].append(sequence_name)
            
            self.projects[self.current_project]["modified"] = datetime.now().isoformat()
            
            # Update project file
            with open(project_path / "project.json", 'w') as f:
                json.dump(self.projects[self.current_project], f, indent=2)
            
            print(f"Sequence '{sequence_name}' saved to project '{self.current_project}'")
            return True
            
        except Exception as e:
            print(f"Error saving sequence: {e}")
            return False
    
    def load_sequence(self, sequence_name: str) -> Optional[Dict]:
        """Load a sequence from the current project"""
        if not self.current_project:
            print("No project is currently open")
            return None
        
        try:
            project_path = self.projects_dir / self.current_project
            sequence_file = project_path / "sequences" / f"{sequence_name}.json"
            
            if not sequence_file.exists():
                print(f"Sequence '{sequence_name}' not found")
                return None
            
            with open(sequence_file, 'r') as f:
                sequence_data = json.load(f)
            
            print(f"Sequence '{sequence_name}' loaded from project '{self.current_project}'")
            return sequence_data
            
        except Exception as e:
            print(f"Error loading sequence: {e}")
            return None
    
    def list_sequences(self) -> List[str]:
        """List all sequences in the current project"""
        if not self.current_project:
            print("No project is currently open")
            return []
        
        return self.projects[self.current_project].get("sequences", [])
    
    def delete_sequence(self, sequence_name: str) -> bool:
        """Delete a sequence from the current project"""
        if not self.current_project:
            print("No project is currently open")
            return False
        
        try:
            project_path = self.projects_dir / self.current_project
            sequence_file = project_path / "sequences" / f"{sequence_name}.json"
            
            if sequence_file.exists():
                sequence_file.unlink()
                
                # Update project metadata
                if sequence_name in self.projects[self.current_project]["sequences"]:
                    self.projects[self.current_project]["sequences"].remove(sequence_name)
                
                self.projects[self.current_project]["modified"] = datetime.now().isoformat()
                
                # Update project file
                with open(project_path / "project.json", 'w') as f:
                    json.dump(self.projects[self.current_project], f, indent=2)
                
                print(f"Sequence '{sequence_name}' deleted from project '{self.current_project}'")
                return True
            else:
                print(f"Sequence '{sequence_name}' not found")
                return False
                
        except Exception as e:
            print(f"Error deleting sequence: {e}")
            return False
    
    def export_project(self, export_format: str = "zip") -> Optional[str]:
        """Export the current project"""
        if not self.current_project:
            print("No project is currently open")
            return None
        
        try:
            project_path = self.projects_dir / self.current_project
            export_dir = project_path / "exports"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_name = f"{self.current_project}_{timestamp}"
            
            if export_format == "zip":
                import zipfile
                zip_path = export_dir / f"{export_name}.zip"
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in project_path.rglob("*"):
                        if file_path.is_file() and not file_path.name.startswith('.'):
                            arcname = file_path.relative_to(project_path)
                            zipf.write(file_path, arcname)
                
                print(f"Project exported to {zip_path}")
                return str(zip_path)
            
            else:
                print(f"Export format '{export_format}' not supported")
                return None
                
        except Exception as e:
            print(f"Error exporting project: {e}")
            return None
    
    def list_projects(self) -> List[str]:
        """List all available projects"""
        return list(self.projects.keys())
    
    def get_project_info(self, name: str) -> Optional[Dict]:
        """Get information about a specific project"""
        return self.projects.get(name)
    
    def delete_project(self, name: str) -> bool:
        """Delete a project and all its contents"""
        if name not in self.projects:
            print(f"Project '{name}' not found")
            return False
        
        try:
            project_path = self.projects_dir / name
            
            if self.current_project == name:
                self.close_project()
            
            # Remove project directory
            shutil.rmtree(project_path)
            
            # Remove from projects list
            del self.projects[name]
            
            print(f"Project '{name}' deleted successfully")
            return True
            
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False
    
    def backup_project(self, name: str) -> Optional[str]:
        """Create a backup of a project"""
        if name not in self.projects:
            print(f"Project '{name}' not found")
            return None
        
        try:
            project_path = self.projects_dir / name
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{name}_backup_{timestamp}"
            backup_path = backup_dir / backup_name
            
            # Copy project directory
            shutil.copytree(project_path, backup_path)
            
            print(f"Project '{name}' backed up to {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            print(f"Error backing up project: {e}")
            return None


def main():
    """Test the project manager"""
    pm = ProjectManager()
    
    print("Seq80x25 Project Manager Test")
    print("=" * 30)
    
    # List existing projects
    print("Existing projects:")
    for project in pm.list_projects():
        print(f"  - {project}")
    print()
    
    # Create a test project
    if pm.create_project("Test Project", "A test project for Seq80x25", "Test User"):
        print("✓ Test project created")
        
        # Open the project
        if pm.open_project("Test_Project"):
            print("✓ Test project opened")
            
            # Create a sample sequence
            sample_sequence = {
                "name": "Test Sequence",
                "tempo": 120,
                "grid_width": 16,
                "grid_height": 12,
                "notes": {
                    (11, 0): "C4",
                    (10, 1): "D4",
                    (9, 2): "E4"
                }
            }
            
            # Save the sequence
            if pm.save_sequence("test_sequence", sample_sequence):
                print("✓ Test sequence saved")
                
                # List sequences
                sequences = pm.list_sequences()
                print(f"✓ Sequences in project: {sequences}")
                
                # Load the sequence
                loaded_sequence = pm.load_sequence("test_sequence")
                if loaded_sequence:
                    print("✓ Test sequence loaded")
                
                # Export project
                export_path = pm.export_project()
                if export_path:
                    print(f"✓ Project exported to {export_path}")
            
            # Close project
            pm.close_project()
            print("✓ Test project closed")
    
    print("\nAll project manager tests completed!")


if __name__ == "__main__":
    main()
