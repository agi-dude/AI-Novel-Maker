import logging
from typing import List

from src.ollama_client import OllamaClient
from src.novel import Novel, ChapterPlan, Chapter
from prompts.chapter_planning import CHAPTER_PLAN_SYSTEM

logger = logging.getLogger(__name__)

class ChapterPlanningStage:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def generate_chapter_plans(self, novel: Novel) -> List[Chapter]:
        """Generate chapter plans for the novel"""
        chapters: List[Chapter] = []
        
        for i in range(1, 11):  # Assuming max 10 chapters, adjust as needed
            prompt = CHAPTER_PLAN_SYSTEM.format(
                chapter_number=i,
                novel_title=novel.title,
                idea=novel.idea,
                style_guide=novel.style_guide,
                world_lore=novel.world_lore,
                plot=novel.plot,
                characters=novel.characters
            )
            
            chapter_plan_str = self.ollama_client.generate(prompt)
            
            try:
                chapter_plan_data = eval(chapter_plan_str)
                chapter_plan = ChapterPlan(**chapter_plan_data)
                chapter = Chapter(number=i, title=chapter_plan.title, plan=chapter_plan)
                chapters.append(chapter)
            except (SyntaxError, TypeError):
                logger.error(f"Chapter {i}: JSON parsing failed, skipping")
                # Could choose to skip or handle error manually
                continue
        
        return chapters
