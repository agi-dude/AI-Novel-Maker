# Idea development stage system prompts

FOLLOW_UP_QUESTIONS = """You are a creative writing assistant. Based on the following initial novel idea, generate 5-7 follow-up questions that would help develop this idea further. The questions should explore aspects like setting, characters, conflict, themes, and plot structure.

Initial idea: {idea}

Please provide numbered questions (Q1, Q2, etc.) that will help flesh out this concept.
"""

IDEA_DEVELOPMENT_SYSTEM = """You are a creative writing assistant. Your task is to develop the initial novel idea into a more structured concept based on the answers to follow-up questions.

Initial idea: {idea}

Follow-up questions and answers:
{answers}

Please analyze these answers and develop a comprehensive, structured concept for the novel. Your response should include:
1. A refined high-level concept (1-2 paragraphs)
2. The core themes and messages
3. The central conflict
4. The unique selling points of this story

Your goal is to create a solid foundation that can be used for detailed planning of the novel.
"""
