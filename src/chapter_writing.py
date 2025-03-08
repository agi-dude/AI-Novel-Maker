import logging
from typing import List

from src.ollama_client import OllamaClient
from src.novel import Novel, Chapter
from prompts.chapter_writing import CHAPTER_WRITING_SYSTEM, CHAPTER_REVIEW_SYSTEM
from src.utils import remove_think_tags

logger = logging.getLogger(__name__)

class ChapterWritingStage:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def write_chapters(self, novel: Novel) -> Novel:
        """Write chapters for the novel"""
        for chapter in novel.chapters:
            if chapter.status == "completed":
                continue  # Skip already completed chapters
            
            logger.info(f"Writing Chapter {chapter.number}: {chapter.title}")
            
            prompt = CHAPTER_WRITING_SYSTEM.format(
                chapter_number=chapter.number,
                novel_title=novel.title,
                chapter_plan=chapter.plan,
                style_guide=novel.style_guide,
                world_lore=novel.world_lore,
                plot=novel.plot,
                characters=novel.characters
            )
            
            chapter_content = self.ollama_client.generate(prompt)
            chapter_content = remove_think_tags(chapter_content)
            chapter.content = chapter_content
            chapter.status = "writing"  # Set chapter status to writing
            
            # Review chapter
            self.review_chapter(novel, chapter)
            
            logger.info(f"Chapter {chapter.number}: {chapter.title} completed")
        
        return novel
    
    def review_chapter(self, novel: Novel, chapter: Chapter):
        """Review chapter content"""
        logger.info(f"Reviewing Chapter {chapter.number}: {chapter.title}")
        
        review_prompt = CHAPTER_REVIEW_SYSTEM.format(
            chapter_content=chapter.content,
            chapter_plan=chapter.plan,
            style_guide=novel.style_guide,
            world_lore=novel.world_lore,
            plot=novel.plot,
            characters=novel.characters
        )
        
        review_result = self.ollama_client.generate(review_prompt)
        review_result = remove_think_tags(review_result)
        
        # Assuming the review result contains the revised chapter content
        if "Revised Content:" in review_result:
            try:
                # Extract the revised content
                chapter.content = review_result.split("Revised Content:")[1].strip()
            except IndexError:
                logger.warning("Could not find revised content in review result, keeping original")
        
        chapter.status = "completed"  # Set chapter status to completed
        logger.info(f"Chapter {chapter.number}: {chapter.title} review completed")
