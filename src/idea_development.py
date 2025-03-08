import logging
from typing import List, Dict

from src.ollama_client import OllamaClient
from src.novel import Novel
from prompts.idea_development import IDEA_DEVELOPMENT_SYSTEM, FOLLOW_UP_QUESTIONS

logger = logging.getLogger(__name__)

class IdeaDevelopmentStage:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def develop_idea(self, novel: Novel) -> Novel:
        """Develop the initial idea into a more structured concept"""
        logger.info("Starting idea development stage")
        
        # Generate follow-up questions based on the initial idea
        follow_up_prompt = FOLLOW_UP_QUESTIONS.format(idea=novel.idea)
        follow_up_questions = self.ollama_client.generate(follow_up_prompt)
        
        # In headless mode, we'll generate answers to these questions automatically
        # In interactive mode, we'd ask the user to answer these questions
        
        # For now, let's assume we're in headless mode and generate answers
        questions = self._parse_questions(follow_up_questions)
        answers = {}
        
        for q_id, question in questions.items():
            logger.info(f"Generating answer for question: {question}")
            # Generate an answer for each question
            answer = self.ollama_client.generate(f"Based on the novel idea: '{novel.idea}', please provide a detailed answer to this question: {question}")
            answers[q_id] = answer
        
        # Develop the idea based on the answers
        idea_development_prompt = IDEA_DEVELOPMENT_SYSTEM.format(
            idea=novel.idea,
            answers="\n".join([f"Q{q_id}: {q}\nA{q_id}: {answers[q_id]}" for q_id, q in questions.items()])
        )
        
        developed_idea = self.ollama_client.generate(idea_development_prompt)
        
        # Update the novel with the developed idea
        novel.idea = developed_idea
        logger.info("Idea development completed")
        
        return novel
    
    def _parse_questions(self, questions_text: str) -> Dict[str, str]:
        """Parse the follow-up questions from the generated text"""
        questions = {}
        lines = questions_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract question number and text
            if ':' in line:
                parts = line.split(':', 1)
                q_id = parts[0].strip().replace('Q', '').replace('.', '')
                try:
                    q_id = int(q_id)
                    questions[q_id] = parts[1].strip()
                except ValueError:
                    # If we can't parse the question ID, just add it with a sequential ID
                    questions[len(questions) + 1] = line
            else:
                # If there's no colon, just add the whole line
                questions[len(questions) + 1] = line
        
        return questions
