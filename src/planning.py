import logging
import re
from typing import Dict, List, Optional

from src.ollama_client import OllamaClient
from src.novel import Novel, StyleGuide, WorldLore, Plot, Character
from prompts.planning import (
    STYLE_GUIDE_SYSTEM,
    WORLD_LORE_SYSTEM,
    PLOT_SYSTEM,
    CHARACTER_SYSTEM
)

logger = logging.getLogger(__name__)

class PlanningStage:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        
    def develop_style_guide(self, novel: Novel) -> StyleGuide:
        """Develop the style guide for the novel"""
        prompt = STYLE_GUIDE_SYSTEM.format(idea=novel.idea)
        style_guide_str = self.ollama_client.generate(prompt)
        
        # Parse the generated style guide
        try:
            # Try to directly parse JSON
            style_guide_data = eval(style_guide_str) # Dangerous, should be improved
            style_guide = StyleGuide(**style_guide_data)
        except (SyntaxError, TypeError):
            # If JSON parsing fails, try to extract information manually
            logger.warning("JSON parsing failed, trying to extract style guide information manually")
            style_guide = self._extract_style_guide(style_guide_str)
            
        return style_guide
    
    def _extract_style_guide(self, text: str) -> StyleGuide:
        """Extract style guide information from text"""
        # Example: Use regex to extract information, adjust as needed
        tone_match = re.search(r"Tone:\s*([^\n]+)", text)
        language_match = re.search(r"Language:\s*([^\n]+)", text)
        narrative_style_match = re.search(r"Narrative Style:\s*([^\n]+)", text)
        pov_match = re.search(r"POV:\s*([^\n]+)", text)
        tense_match = re.search(r"Tense:\s*([^\n]+)", text)
        themes_match = re.search(r"Themes:\s*([^\n]+)", text)
        
        tone = tone_match.group(1).strip() if tone_match else "Undefined"
        language = language_match.group(1).strip() if language_match else "Undefined"
        narrative_style = narrative_style_match.group(1).strip() if narrative_style_match else "Undefined"
        pov = pov_match.group(1).strip() if pov_match else "Undefined"
        tense = tense_match.group(1).strip() if tense_match else "Undefined"
        themes = [t.strip() for t in themes_match.group(1).split(",")] if themes_match else []
        
        return StyleGuide(tone=tone, language=language, narrative_style=narrative_style, pov=pov, tense=tense, themes=themes)
    
    def develop_world_lore(self, novel: Novel) -> WorldLore:
        """Develop the world lore for the novel"""
        prompt = WORLD_LORE_SYSTEM.format(idea=novel.idea, style_guide=novel.style_guide)
        world_lore_str = self.ollama_client.generate(prompt)
        
        try:
            world_lore_data = eval(world_lore_str)
            world_lore = WorldLore(**world_lore_data)
        except (SyntaxError, TypeError):
            logger.warning("JSON parsing failed, trying to extract world lore information manually")
            world_lore = self._extract_world_lore(world_lore_str)
        
        return world_lore
    
    def _extract_world_lore(self, text: str) -> WorldLore:
        """Extract world lore information from text"""
        setting_match = re.search(r"Setting:\s*([^\n]+)", text)
        history_match = re.search(r"History:\s*([^\n]+)", text)
        culture_match = re.search(r"Culture:\s*([^\n]+)", text)
        rules_match = re.search(r"Rules:\s*([^\n]+)", text)
        locations_match = re.search(r"Locations:\s*([^\n]+)", text)
        
        setting = setting_match.group(1).strip() if setting_match else "Undefined"
        history = history_match.group(1).strip() if history_match else "Undefined"
        culture = culture_match.group(1).strip() if culture_match else "Undefined"
        rules = rules_match.group(1).strip() if rules_match else "Undefined"
        
        locations_str = locations_match.group(1).strip() if locations_match else ""
        locations = {}
        for location_pair in locations_str.split(","):
            try:
                location_name, location_desc = location_pair.split(":")
                locations[location_name.strip()] = location_desc.strip()
            except ValueError:
                pass
        
        return WorldLore(setting=setting, history=history, culture=culture, rules=rules, locations=locations)
    
    def develop_plot(self, novel: Novel) -> Plot:
        """Develop the plot for the novel"""
        prompt = PLOT_SYSTEM.format(idea=novel.idea, world_lore=novel.world_lore, style_guide=novel.style_guide)
        plot_str = self.ollama_client.generate(prompt)
        
        try:
            plot_data = eval(plot_str)
            plot = Plot(**plot_data)
        except (SyntaxError, TypeError):
            logger.warning("JSON parsing failed, trying to extract plot information manually")
            plot = self._extract_plot(plot_str)
        
        return plot
    
    def _extract_plot(self, text: str) -> Plot:
        """Extract plot information from text"""
        main_plot_match = re.search(r"Main Plot:\s*([^\n]+)", text)
        subplots_match = re.search(r"Subplots:\s*\[(.*?)\]", text, re.DOTALL)
        arcs_match = re.search(r"Character Arcs:\s*\[(.*?)\]", text, re.DOTALL)
        
        main_plot = main_plot_match.group(1).strip() if main_plot_match else "Undefined"
        subplots_str = subplots_match.group(1).strip() if subplots_match else ""
        subplots = [s.strip() for s in subplots_str.split(",") if s.strip()]
        arcs_str = arcs_match.group(1).strip() if arcs_match else ""
        arcs = [a.strip() for a in arcs_str.split(",") if a.strip()]
        
        return Plot(main_plot=main_plot, subplots=subplots, arcs=arcs)
    
    def develop_characters(self, novel: Novel) -> Dict[str, Character]:
        """Develop the characters for the novel"""
        characters: Dict[str, Character] = {}
        prompt = CHARACTER_SYSTEM.format(idea=novel.idea, plot=novel.plot, world_lore=novel.world_lore, style_guide=novel.style_guide)
        characters_str = self.ollama_client.generate(prompt)
        
        try:
            characters_data = eval(characters_str)
            for char_name, char_data in characters_data.items():
                characters[char_name] = Character(**char_data)
        except (SyntaxError, TypeError):
            logger.warning("JSON parsing failed, trying to extract character information manually")
            characters = self._extract_characters(characters_str)
        
        return characters
    
    def _extract_characters(self, text: str) -> Dict[str, Character]:
        """Extract character information from text"""
        characters: Dict[str, Character] = {}
        # Example: Use regex to extract information, adjust as needed
        character_blocks = re.findall(r"Character:\s*([^\n]+)\n([\s\S]*?)(?=\nCharacter:|\Z)", text)
        
        for block in character_blocks:
            char_name = block[0].strip()
            char_details = block[1]
            
            description_match = re.search(r"Description:\s*([^\n]+)", char_details)
            background_match = re.search(r"Background:\s*([^\n]+)", char_details)
            motivation_match = re.search(r"Motivation:\s*([^\n]+)", char_details)
            arc_match = re.search(r"Arc:\s*([^\n]+)", char_details)
            relationships_match = re.search(r"Relationships:\s*\{([\s\S]*?)\}", char_details)
            
            description = description_match.group(1).strip() if description_match else "Undefined"
            background = background_match.group(1).strip() if background_match else "Undefined"
            motivation = motivation_match.group(1).strip() if motivation_match else "Undefined"
            arc = arc_match.group(1).strip() if arc_match else "Undefined"
            
            relationships = {}
            if relationships_match:
                relationship_str = relationships_match.group(1).strip()
                for rel_pair in relationship_str.split(","):
                    try:
                        rel_char, rel_desc = rel_pair.split(":")
                        relationships[rel_char.strip()] = rel_desc.strip()
                    except ValueError:
                        pass
            
            characters[char_name] = Character(
                name=char_name,
                description=description,
                background=background,
                motivation=motivation,
                arc=arc,
                relationships=relationships
            )
        
        return characters
