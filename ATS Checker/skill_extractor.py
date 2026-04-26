"""
Skill Extractor

Extracts skills from job descriptions and resumes using NLP and LLM assistance.
"""

import re
from typing import List, Set
from ollama_client import OllamaClient


class SkillExtractor:
    def __init__(self, model_name: str = "llama2"):
        self.ollama = OllamaClient(model_name)
        # Common skill keywords (can be expanded)
        self.skill_keywords = {
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "go", "rust",
            "machine learning", "deep learning", "nlp", "computer vision", "data science",
            "sql", "mongodb", "postgresql", "mysql", "redis",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "react", "angular", "vue", "node.js", "django", "flask", "spring",
            "git", "ci/cd", "agile", "scrum", "kanban",
            "linux", "windows", "bash", "powershell"
        }

    def extract_skills(self, text: str, context: str = "general") -> List[str]:
        """
        Extract skills from text using keyword matching and LLM refinement.

        Args:
            text: Input text
            context: Context ("job_description" or "resume")

        Returns:
            List of extracted skills
        """
        # Initial keyword extraction
        found_skills = self._extract_keywords(text)

        # Use LLM to refine and find additional skills
        refined_skills = self._refine_with_llm(text, found_skills, context)

        return list(set(refined_skills))  # Remove duplicates

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract skills using keyword matching."""
        text_lower = text.lower()
        found = set()

        for skill in self.skill_keywords:
            if skill in text_lower:
                found.add(skill)

        # Also look for multi-word skills
        multi_word_skills = [
            "machine learning", "deep learning", "natural language processing",
            "computer vision", "data science", "data analysis", "web development",
            "software engineering", "cloud computing", "devops"
        ]

        for skill in multi_word_skills:
            if skill in text_lower:
                found.add(skill)

        return found

    def _refine_with_llm(self, text: str, initial_skills: Set[str], context: str) -> List[str]:
        """Use LLM to refine skill extraction."""
        prompt = f"""
        Extract technical skills from the following {context.replace('_', ' ')}:

        {text[:2000]}...  # Truncate for token limits

        Initial skills found: {', '.join(initial_skills)}

        Please provide a comprehensive list of technical skills mentioned or implied.
        Focus on programming languages, frameworks, tools, methodologies, and domain knowledge.
        Return only a comma-separated list of skills, no explanations.
        """

        try:
            response = self.ollama.generate(prompt)
            # Parse response
            skills = [skill.strip() for skill in response.split(',') if skill.strip()]
            return skills
        except Exception as e:
            print(f"LLM refinement failed: {e}")
            return list(initial_skills)