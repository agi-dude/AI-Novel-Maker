import logging
import os
import sys
from typing import Optional

from src.novel import Novel
from src.idea_development import IdeaDevelopmentStage
from src.planning import PlanningStage
from src.chapter_planning import ChapterPlanningStage
from src.chapter_writing import ChapterWritingStage
from src.review import FinalReviewStage
from src.ollama_client import OllamaClient
from config import HEADLESS_MODE, SAVE_DIR

logger = logging.getLogger(__name__)

class UserInterface:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
        self.idea_stage = IdeaDevelopmentStage(self.ollama_client)
        self.planning_stage = PlanningStage(self.ollama_client)
        self.chapter_planning_stage = ChapterPlanningStage(self.ollama_client)
        self.chapter_writing_stage = ChapterWritingStage(self.ollama_client)
        self.final_review_stage = FinalReviewStage(self.ollama_client)
        self.novel: Optional[Novel] = None
    
    def run(self):
        """Run the main program"""
        if HEADLESS_MODE:
            self.run_headless()
        else:
            self.run_interactive()
    
    def run_headless(self):
        """Run in headless mode without user interaction"""
        logger.info("Running in headless mode")
        self.novel = self.load_or_create_novel()
        
        if self.novel.status == "idea":
            self.develop_idea_headless()
        if self.novel.status == "planning":
            self.plan_novel_headless()
        if self.novel.status == "writing":
            self.write_novel_headless()
        if self.novel.status == "reviewing":
            self.review_novel_headless()
        if self.novel.status == "completed":
            self.output_novel()
    
    def run_interactive(self):
        """Run in interactive mode with user interaction"""
        logger.info("Running in interactive mode")
        self.novel = self.load_or_create_novel()
        
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.develop_idea()
            elif choice == '2':
                self.plan_novel()
            elif choice == '3':
                self.plan_chapters()
            elif choice == '4':
                self.write_chapters()
            elif choice == '5':
                self.review_novel()
            elif choice == '6':
                self.output_novel()
            elif choice == '7':
                self.save_novel()
            elif choice == '8':
                self.load_novel()
            elif choice == '9':
                break
            else:
                print("Invalid choice, please try again.")
    
    def load_or_create_novel(self) -> Novel:
        """Load or create a novel"""
        if os.path.exists(SAVE_DIR):
            saves = Novel.list_saves()
            if saves:
                print("Found saved novels:")
                for i, save in enumerate(saves):
                    print(f"{i+1}. {save.stem}")
                
                while True:
                    try:
                        choice = input("Select a novel to load (or enter 'n' to create new): ")
                        if choice.lower() == 'n':
                            return self.create_new_novel()
                        
                        index = int(choice) - 1
                        if 0 <= index < len(saves):
                            return Novel.load(str(saves[index]))
                        else:
                            print("Invalid choice, please try again.")
                    except ValueError:
                        print("Invalid input, please enter a number.")
            else:
                print("No saved novels found, creating a new one.")
                return self.create_new_novel()
        else:
            os.makedirs(SAVE_DIR)
            return self.create_new_novel()
    
    def create_new_novel(self) -> Novel:
        """Create a new novel"""
        title = input("Enter novel title: ")
        idea = input("Enter initial novel idea: ")
        novel = Novel(title=title, idea=idea)
        return novel
    
    def display_menu(self):
        """Display the main menu"""
        print("\nAI Novel Writer Menu:")
        print("1. Develop Novel Idea")
        print("2. Plan Novel")
        print("3. Plan Chapters")
        print("4. Write Chapters")
        print("5. Review Novel")
        print("6. Output Novel")
        print("7. Save Novel")
        print("8. Load Novel")
        print("9. Exit")
    
    # Idea Development
    def develop_idea(self):
        """Develop the novel idea"""
        if not self.novel:
            print("Please create or load a novel first.")
            return
        
        self.novel = self.idea_stage.develop_idea(self.novel)
        self.novel.status = "planning"
    
    def develop_idea_headless(self):
        """Develop the novel idea in headless mode"""
        if not self.novel:
            print("Please create or load a novel first.")
            sys.exit(1)
        
        if self.novel.status == "idea":
            self.novel = self.idea_stage.develop_idea(self.novel)
            self.novel.status = "planning"
            self.save_novel()
    
    # Planning
    def plan_novel(self):
        """Plan the novel"""
        if not self.novel or self.novel.status != "planning":
            print("Please develop the novel idea first.")
            return
        
        # Develop style guide
        self.novel.style_guide = self.planning_stage.develop_style_guide(self.novel)
        print("Style guide generated.")
        
        # Develop world lore
        self.novel.world_lore = self.planning_stage.develop_world_lore(self.novel)
        print("World lore generated.")
        
        # Develop plot
        self.novel.plot = self.planning_stage.develop_plot(self.novel)
        print("Plot generated.")
        
        # Develop characters
        self.novel.characters = self.planning_stage.develop_characters(self.novel)
        print("Characters generated.")
        
        self.novel.status = "writing"
    
    def plan_novel_headless(self):
        """Plan the novel in headless mode"""
        if not self.novel or self.novel.status != "planning":
            print("Please develop the novel idea first.")
            sys.exit(1)
        
        # Develop style guide
        self.novel.style_guide = self.planning_stage.develop_style_guide(self.novel)
        logger.info("Style guide generated.")
        
        # Develop world lore
        self.novel.world_lore = self.planning_stage.develop_world_lore(self.novel)
        logger.info("World lore generated.")
        
        # Develop plot
        self.novel.plot = self.planning_stage.develop_plot(self.novel)
        logger.info("Plot generated.")
        
        # Develop characters
        self.novel.characters = self.planning_stage.develop_characters(self.novel)
        logger.info("Characters generated.")
        
        self.novel.status = "writing"
        self.save_novel()
    
    # Chapter Planning
    def plan_chapters(self):
        """Plan the chapters"""
        if not self.novel or self.novel.status != "writing":
            print("Please plan the novel first.")
            return
        
        self.novel.chapters = self.chapter_planning_stage.generate_chapter_plans(self.novel)
        print("Chapter plans generated.")
        self.novel.status = "writing"
    
    # Writing Chapters
    def write_chapters(self):
        """Write the chapters"""
        if not self.novel or self.novel.status != "writing":
            print("Please plan the novel first.")
            return
        
        self.novel = self.chapter_writing_stage.write_chapters(self.novel)
        self.save_novel()
        print("Chapters written.")
        self.novel.status = "reviewing"
    
    def write_novel_headless(self):
        """Write the novel in headless mode"""
        if not self.novel or self.novel.status != "writing":
            print("Please plan the novel first.")
            sys.exit(1)
        
        self.novel = self.chapter_writing_stage.write_chapters(self.novel)
        self.save_novel()
        logger.info("Chapters written.")
        self.novel.status = "reviewing"
    
    # Review Novel
    def review_novel(self):
        """Review the novel"""
        if not self.novel or self.novel.status != "reviewing":
            print("Please write the chapters first.")
            return
        
        final_review = self.final_review_stage.conduct_final_review(self.novel)
        print("Final Review Result:")
        print(final_review)
        self.novel.status = "completed"
    
    def review_novel_headless(self):
        """Review the novel in headless mode"""
        if not self.novel or self.novel.status != "reviewing":
            print("Please write the chapters first.")
            sys.exit(1)
        
        final_review = self.final_review_stage.conduct_final_review(self.novel)
        logger.info("Final Review Result:\n" + final_review)
        self.novel.status = "completed"
        self.save_novel()
    
    # Output Novel
    def output_novel(self):
        """Output the novel"""
        if not self.novel or self.novel.status != "completed":
            print("Please complete the novel first.")
            return
        
        # Here you can implement exporting to different formats
        output_path = self.novel.export_to_markdown()
        print(f"Novel exported to: {output_path}")
    
    # Save and Load
    def save_novel(self):
        """Save the novel"""
        if not self.novel:
            print("No novel to save.")
            return
        
        save_path = self.novel.save()
        print(f"Novel saved to: {save_path}")
    
    def load_novel(self):
        """Load a novel"""
        saves = Novel.list_saves()
        if not saves:
            print("No saved novels found.")
            return
        
        print("Saved novels:")
        for i, save in enumerate(saves):
            print(f"{i+1}. {save.stem}")
        
        while True:
            try:
                choice = int(input("Select a novel to load: "))
                if 1 <= choice <= len(saves):
                    self.novel = Novel.load(str(saves[choice - 1]))
                    print(f"Loaded novel: {self.novel.title}")
                    return
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input, please enter a number.")
