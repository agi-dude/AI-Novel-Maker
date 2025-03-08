import logging

from src.ollama_client import OllamaClient
from src.novel import Novel
from prompts.review import FINAL_REVIEW_SYSTEM

logger = logging.getLogger(__name__)

class FinalReviewStage:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def conduct_final_review(self, novel: Novel) -> str:
        """Conduct final review of the novel"""
        logger.info("Starting final review...")
        
        prompt = FINAL_REVIEW_SYSTEM.format(
            novel_title=novel.title,
            novel_idea=novel.idea,
            style_guide=novel.style_guide,
            world_lore=novel.world_lore,
            plot=novel.plot,
            characters=novel.characters,
            chapters="\n\n".join([f"Chapter {chap.number}:\n{chap.content}" for chap in novel.chapters])
        )
        
        final_review_result = self.ollama_client.generate(prompt)
        
        logger.info("Final review completed")
        return final_review_result
