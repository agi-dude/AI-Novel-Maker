import json
import pickle
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import os

from config import SAVE_DIR

@dataclass
class StyleGuide:
    tone: str = ""
    language: str = ""
    narrative_style: str = ""
    pov: str = ""
    tense: str = ""
    themes: List[str] = field(default_factory=list)

@dataclass
class WorldLore:
    setting: str = ""
    history: str = ""
    culture: str = ""
    rules: str = ""
    locations: Dict[str, str] = field(default_factory=dict)

@dataclass
class Plot:
    main_plot: str = ""
    subplots: List[str] = field(default_factory=list)
    arcs: List[str] = field(default_factory=list)

@dataclass
class Character:
    name: str = ""
    description: str = ""
    background: str = ""
    motivation: str = ""
    arc: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)

@dataclass
class ChapterPlan:
    title: str = ""
    summary: str = ""
    scenes: List[str] = field(default_factory=list)
    pov_character: str = ""
    goals: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    resolutions: List[str] = field(default_factory=list)

@dataclass
class Chapter:
    number: int
    title: str = ""
    plan: Optional[ChapterPlan] = None
    content: str = ""
    status: str = "planned"  # planned, writing, completed

@dataclass
class Novel:
    title: str
    idea: str
    style_guide: Optional[StyleGuide] = None
    world_lore: Optional[WorldLore] = None
    plot: Optional[Plot] = None
    characters: Dict[str, Character] = field(default_factory=dict)
    chapters: List[Chapter] = field(default_factory=list)
    status: str = "idea"  # idea, planning, writing, reviewing, completed
    
    def save(self) -> str:
        """Save the novel to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.title.replace(' ', '_')}_{timestamp}.pkl"
        save_path = SAVE_DIR / filename
        
        with open(save_path, 'wb') as f:
            pickle.dump(self, f)
        
        return str(save_path)
    
    @staticmethod
    def load(filepath: str) -> 'Novel':
        """Load a novel from a file"""
        with open(filepath, 'rb') as f:
            novel = pickle.load(f)
        
        return novel
    
    @staticmethod
    def list_saves() -> List[Path]:
        """List all saved novels"""
        return sorted(Path(SAVE_DIR).glob("*.pkl"))
    
    def to_json(self) -> str:
        """Convert the novel to JSON string"""
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)
    
    def export_to_markdown(self, output_path: Optional[str] = None) -> str:
        """Export the novel to a Markdown file"""
        if output_path is None:
            output_path = SAVE_DIR / f"{self.title.replace(' ', '_')}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.title}\n\n")
            
            for chapter in self.chapters:
                f.write(f"## Chapter {chapter.number}: {chapter.title}\n\n")
                f.write(f"{chapter.content}\n\n")
        
        return str(output_path)
