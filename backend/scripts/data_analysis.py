#!/usr/bin/env python3
"""
Data Analysis Script for Legal Data Reorganization

This script analyzes the current data structure and generates a comprehensive
report of the existing organization, dependencies, and files that need to be
moved or merged during the reorganization process.

Requirements addressed: 1.1, 2.1, 3.1
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Set
from datetime import datetime
import argparse


class DataStructureAnalyzer:
    """Analyzes the current data structure and generates reorganization reports."""
    
    def __init__(self, data_root: str = "backend/app/data"):
        self.data_root = Path(data_root)
        self.analysis_results = {
            "metadata": {
                "analysis_date": datetime.now().isoformat(),
                "data_root": str(self.data_root),
                "total_files": 0,
                "total_directories": 0,
                "total_size_bytes": 0
            },
            "directory_structure": {},
            "file_inventory": {},
            "dependencies": {},
            "migration_plan": {
                "files_to_move": [],
                "files_to_merge": [],
                "directories_to_create": [],
                "directories_to_remove": [],
                "index_files_to_update": []
            },
            "issues_identified": [],
            "recommendations": []
        }
    
    def analyze_structure(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of the current data structure."""
        print("Starting data structure analysis...")
        
        # Analyze directory structure
        self._analyze_directories()
        
        # Inventory all files
        self._inventory_files()
        
        # Analyze dependencies
        self._analyze_dependencies()
        
        # Generate migration recommendations
        self._generate_migration_plan()
        
        # Identify issues
        self._identify_issues()
        
        print(f"Analysis complete. Found {self.analysis_results['metadata']['total_files']} files in {self.analysis_results['metadata']['total_directories']} directories.")
        
        return self.analysis_results
    
    def _analyze_directories(self):
        """Analyze the directory structure and categorize directories."""
        print("Analyzing directory structure...")
        
        for root, dirs, files in os.walk(self.data_root):
            rel_path = os.path.relpath(root, self.data_root)
            if rel_path == ".":
                rel_path = "root"
            
            self.analysis_results["metadata"]["total_directories"] += 1
            
            # Categorize directory
            category = self._categorize_directory(rel_path, files)
            
            self.analysis_results["directory_structure"][rel_path] = {
                "absolute_path": str(root),
                "category": category,
                "subdirectories": dirs.copy(),
                "file_count": len(files),
                "files": files.copy()
            }
    
    def _categorize_directory(self, path: str, files: List[str]) -> str:
        """Categorize a directory based on its path and contents."""
        path_lower = path.lower()
        
        if "case_documents" in path_lower:
            return "cases_index"
        elif path_lower in ["ai", "al"] or path_lower.startswith("ai/") or path_lower.startswith("al/"):
            return "analysis_data"
        elif "legal_corpus" in path_lower:
            return "corpus_data"
        elif "embeddings" in path_lower:
            return "ml_data"
        elif "demo" in path_lower or any("demo" in f.lower() for f in files):
            return "demo_data"
        elif any(f.endswith("_index.json") for f in files):
            return "index_data"
        else:
            return "other"
    
    def _inventory_files(self):
        """Create detailed inventory of all files."""
        print("Creating file inventory...")
        
        for root, dirs, files in os.walk(self.data_root):
            for file in files:
                file_path = Path(root) / file
                rel_path = os.path.relpath(file_path, self.data_root)
                
                # Get file stats
                try:
                    stat = file_path.stat()
                    file_size = stat.st_size
                    modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    # Calculate file hash for integrity checking
                    file_hash = self._calculate_file_hash(file_path)
                    
                    self.analysis_results["file_inventory"][rel_path] = {
                        "absolute_path": str(file_path),
                        "size_bytes": file_size,
                        "modified_time": modified_time,
                        "file_hash": file_hash,
                        "extension": file_path.suffix,
                        "category": self._categorize_file(rel_path, file),
                        "migration_action": self._determine_migration_action(rel_path, file)
                    }
                    
                    self.analysis_results["metadata"]["total_files"] += 1
                    self.analysis_results["metadata"]["total_size_bytes"] += file_size
                    
                except (OSError, IOError) as e:
                    self.analysis_results["issues_identified"].append({
                        "type": "file_access_error",
                        "file": rel_path,
                        "error": str(e)
                    })
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file for integrity checking."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except (OSError, IOError):
            return "hash_calculation_failed"
    
    def _categorize_file(self, rel_path: str, filename: str) -> str:
        """Categorize a file based on its path and name."""
        path_lower = rel_path.lower()
        filename_lower = filename.lower()
        
        if filename_lower.endswith("_index.json") or filename_lower.endswith("index.json"):
            return "index_file"
        elif "demo" in filename_lower:
            return "demo_file"
        elif filename_lower.endswith(".json") and ("analysis" in filename_lower or "ai/" in path_lower or "al/" in path_lower):
            return "analysis_file"
        elif "case_documents" in path_lower and filename_lower.endswith(".txt"):
            return "case_document"
        elif "legal_corpus" in path_lower:
            return "corpus_file"
        elif "embeddings" in path_lower:
            return "embedding_file"
        else:
            return "other_file"
    
    def _determine_migration_action(self, rel_path: str, filename: str) -> str:
        """Determine what migration action is needed for this file."""
        path_lower = rel_path.lower()
        filename_lower = filename.lower()
        
        if "case_documents" in path_lower:
            return "move_to_cases"
        elif path_lower.startswith("ai/") or path_lower.startswith("al/"):
            return "merge_to_analysis"
        elif "demo" in filename_lower and not path_lower.startswith("demo"):
            return "move_to_demo"
        elif filename_lower.endswith("_index.json"):
            return "update_index"
        else:
            return "no_action"
    
    def _analyze_dependencies(self):
        """Analyze dependencies between files and directories."""
        print("Analyzing file dependencies...")
        
        # Look for JSON files that might reference other files
        for rel_path, file_info in self.analysis_results["file_inventory"].items():
            if file_info["extension"] == ".json":
                try:
                    full_path = Path(file_info["absolute_path"])
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                    
                    # Find references to other files
                    references = self._find_file_references(content, rel_path)
                    if references:
                        self.analysis_results["dependencies"][rel_path] = references
                        
                except (json.JSONDecodeError, OSError, IOError) as e:
                    self.analysis_results["issues_identified"].append({
                        "type": "dependency_analysis_error",
                        "file": rel_path,
                        "error": str(e)
                    })
    
    def _find_file_references(self, data: Any, current_file: str) -> List[str]:
        """Recursively find file references in JSON data."""
        references = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and (
                    value.endswith('.txt') or 
                    value.endswith('.json') or 
                    'doc-' in value or
                    'case-' in value
                ):
                    references.append(value)
                else:
                    references.extend(self._find_file_references(value, current_file))
        elif isinstance(data, list):
            for item in data:
                references.extend(self._find_file_references(item, current_file))
        
        return references
    
    def _generate_migration_plan(self):
        """Generate detailed migration plan based on analysis."""
        print("Generating migration plan...")
        
        migration_plan = self.analysis_results["migration_plan"]
        
        # Files to move
        for rel_path, file_info in self.analysis_results["file_inventory"].items():
            action = file_info["migration_action"]
            
            if action == "move_to_cases":
                new_path = rel_path.replace("case_documents", "cases")
                migration_plan["files_to_move"].append({
                    "source": rel_path,
                    "destination": new_path,
                    "reason": "Consolidate case documents"
                })
            
            elif action == "move_to_demo":
                new_path = f"demo/{os.path.basename(rel_path)}"
                migration_plan["files_to_move"].append({
                    "source": rel_path,
                    "destination": new_path,
                    "reason": "Organize demo content"
                })
            
            elif action == "merge_to_analysis":
                migration_plan["files_to_merge"].append({
                    "source": rel_path,
                    "destination": f"analysis/{os.path.basename(rel_path)}",
                    "reason": "Merge AI analysis data"
                })
            
            elif action == "update_index":
                migration_plan["index_files_to_update"].append({
                    "file": rel_path,
                    "reason": "Update paths after reorganization"
                })
        
        # Directories to create
        migration_plan["directories_to_create"] = [
            "cases",
            "analysis", 
            "demo"
        ]
        
        # Directories to remove (after migration)
        migration_plan["directories_to_remove"] = [
            "case_documents",
            "ai",
            "al"
        ]
    
    def _identify_issues(self):
        """Identify potential issues with the current structure."""
        print("Identifying structural issues...")
        
        issues = self.analysis_results["issues_identified"]
        recommendations = self.analysis_results["recommendations"]
        
        # Check for duplicate analysis directories
        if "ai" in self.analysis_results["directory_structure"] and "al" in self.analysis_results["directory_structure"]:
            issues.append({
                "type": "duplicate_directories",
                "description": "Both 'ai' and 'al' directories exist with similar content",
                "severity": "high"
            })
            recommendations.append("Merge 'ai' and 'al' directories into single 'analysis' directory")
        
        # Check for demo files mixed with production data
        demo_files_in_root = [f for f in self.analysis_results["file_inventory"] 
                             if f.startswith("demo_") and "/" not in f]
        if demo_files_in_root:
            issues.append({
                "type": "mixed_demo_content",
                "description": f"Found {len(demo_files_in_root)} demo files in root data directory",
                "files": demo_files_in_root,
                "severity": "medium"
            })
            recommendations.append("Move all demo files to dedicated demo/ directory")
        
        # Check for missing index files
        if "cases" not in [d["category"] for d in self.analysis_results["directory_structure"].values()]:
            if not any("cases_index.json" in f for f in self.analysis_results["file_inventory"]):
                issues.append({
                    "type": "missing_index",
                    "description": "No cases index file found",
                    "severity": "medium"
                })
                recommendations.append("Create cases_index.json after reorganization")
        
        # Check for inconsistent naming
        case_dirs = [d for d, info in self.analysis_results["directory_structure"].items() 
                    if info["category"] == "cases_index" and d.startswith("case_documents/case-")]
        if case_dirs:
            recommendations.append("Rename 'case_documents' to 'cases' for consistency")
    
    def generate_report(self, output_file: str = "data_analysis_report.json"):
        """Generate and save the analysis report."""
        print(f"Generating report: {output_file}")
        
        # Add summary statistics
        self.analysis_results["summary"] = {
            "total_files": self.analysis_results["metadata"]["total_files"],
            "total_directories": self.analysis_results["metadata"]["total_directories"],
            "files_by_category": {},
            "migration_actions_needed": {},
            "issues_by_severity": {"high": 0, "medium": 0, "low": 0}
        }
        
        # Count files by category
        for file_info in self.analysis_results["file_inventory"].values():
            category = file_info["category"]
            self.analysis_results["summary"]["files_by_category"][category] = \
                self.analysis_results["summary"]["files_by_category"].get(category, 0) + 1
            
            action = file_info["migration_action"]
            self.analysis_results["summary"]["migration_actions_needed"][action] = \
                self.analysis_results["summary"]["migration_actions_needed"].get(action, 0) + 1
        
        # Count issues by severity
        for issue in self.analysis_results["issues_identified"]:
            severity = issue.get("severity", "low")
            self.analysis_results["summary"]["issues_by_severity"][severity] += 1
        
        # Save report
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"Report saved to: {output_path.absolute()}")
        return output_path
    
    def print_summary(self):
        """Print a human-readable summary of the analysis."""
        print("\n" + "="*60)
        print("DATA STRUCTURE ANALYSIS SUMMARY")
        print("="*60)
        
        metadata = self.analysis_results["metadata"]
        print(f"Analysis Date: {metadata['analysis_date']}")
        print(f"Data Root: {metadata['data_root']}")
        print(f"Total Files: {metadata['total_files']}")
        print(f"Total Directories: {metadata['total_directories']}")
        print(f"Total Size: {metadata['total_size_bytes']:,} bytes")
        
        print(f"\nFILES BY CATEGORY:")
        if "summary" in self.analysis_results:
            for category, count in self.analysis_results["summary"]["files_by_category"].items():
                print(f"  {category}: {count}")
        
        print(f"\nMIGRATION ACTIONS NEEDED:")
        if "summary" in self.analysis_results:
            for action, count in self.analysis_results["summary"]["migration_actions_needed"].items():
                print(f"  {action}: {count}")
        
        print(f"\nISSUES IDENTIFIED:")
        for issue in self.analysis_results["issues_identified"]:
            severity = issue.get("severity", "unknown")
            print(f"  [{severity.upper()}] {issue.get('type', 'unknown')}: {issue.get('description', 'No description')}")
        
        print(f"\nRECOMMENDATIONS:")
        for i, rec in enumerate(self.analysis_results["recommendations"], 1):
            print(f"  {i}. {rec}")
        
        print("="*60)


def main():
    """Main function to run the data analysis."""
    parser = argparse.ArgumentParser(description="Analyze legal data structure for reorganization")
    parser.add_argument("--data-root", default="backend/app/data", 
                       help="Root directory of data to analyze")
    parser.add_argument("--output", default="data_analysis_report.json",
                       help="Output file for analysis report")
    parser.add_argument("--summary", action="store_true",
                       help="Print summary to console")
    
    args = parser.parse_args()
    
    # Create analyzer and run analysis
    analyzer = DataStructureAnalyzer(args.data_root)
    results = analyzer.analyze_structure()
    
    # Generate report
    report_path = analyzer.generate_report(args.output)
    
    # Print summary if requested
    if args.summary:
        analyzer.print_summary()
    
    print(f"\nAnalysis complete! Report saved to: {report_path}")
    return results


if __name__ == "__main__":
    main()