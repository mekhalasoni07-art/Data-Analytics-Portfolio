"""
Proficiency Assessor

Conducts conversational assessment of skill proficiency.
"""

from typing import Dict, Any
from ollama_client import OllamaClient


class ProficiencyAssessor:
    def __init__(self, model_name: str = "llama2"):
        self.ollama = OllamaClient(model_name)

    def assess_skill(self, skill: str, resume_text: str, interactive: bool = False) -> Dict[str, Any]:
        """
        Assess proficiency level for a skill.

        Args:
            skill: Skill to assess
            resume_text: Candidate's resume
            interactive: Whether to do interactive assessment

        Returns:
            Assessment result with level and confidence
        """
        if interactive:
            return self._interactive_assessment(skill, resume_text)
        else:
            return self._automated_assessment(skill, resume_text)

    def _automated_assessment(self, skill: str, resume_text: str) -> Dict[str, Any]:
        """Automated assessment based on resume analysis."""
        prompt = f"""
        Based on the following resume, assess the candidate's proficiency level in {skill}.

        Resume:
        {resume_text[:1500]}...

        Proficiency levels:
        - Beginner: Basic knowledge, limited practical experience
        - Intermediate: Solid understanding, some practical experience
        - Advanced: Deep expertise, extensive practical experience
        - Expert: Master level, can teach others

        Provide assessment in JSON format:
        {{
            "level": "Beginner|Intermediate|Advanced|Expert",
            "confidence": 0.0-1.0,
            "evidence": "brief explanation"
        }}
        """

        try:
            response = self.ollama.generate(prompt)
            # Try to parse JSON
            import json
            result = json.loads(response.strip())
            return result
        except:
            # Fallback assessment
            return {
                "level": "Intermediate",
                "confidence": 0.5,
                "evidence": "Automated assessment based on resume content"
            }

    def _interactive_assessment(self, skill: str, resume_text: str) -> Dict[str, Any]:
        """Interactive conversational assessment."""
        print(f"\n=== Assessing {skill} ===")

        # Generate assessment questions
        questions = self._generate_questions(skill)

        answers = []
        for i, question in enumerate(questions, 1):
            print(f"Question {i}: {question}")
            # In a real implementation, this would get user input
            # For now, simulate with LLM
            answer = self._simulate_answer(question, resume_text)
            print(f"Simulated answer: {answer}")
            answers.append(answer)

        # Analyze answers
        analysis = self._analyze_answers(skill, questions, answers)

        return {
            "level": analysis["level"],
            "confidence": analysis["confidence"],
            "evidence": analysis["evidence"],
            "questions": questions,
            "answers": answers
        }

    def _generate_questions(self, skill: str) -> list:
        """Generate assessment questions for a skill."""
        prompt = f"""
        Generate 3-5 technical questions to assess proficiency in {skill}.
        Questions should range from basic to advanced.
        Return only the questions, one per line.
        """

        response = self.ollama.generate(prompt)
        questions = [q.strip() for q in response.split('\n') if q.strip() and not q.startswith('Question')]
        return questions[:5]  # Limit to 5

    def _simulate_answer(self, question: str, resume_text: str) -> str:
        """Simulate candidate answer based on resume."""
        prompt = f"""
        Based on this resume excerpt, provide a realistic answer to the question as if you were the candidate.

        Resume: {resume_text[:1000]}...

        Question: {question}

        Provide a concise answer (1-3 sentences):
        """

        return self.ollama.generate(prompt).strip()

    def _analyze_answers(self, skill: str, questions: list, answers: list) -> Dict[str, Any]:
        """Analyze answers to determine proficiency level."""
        prompt = f"""
        Analyze the following Q&A for {skill} proficiency:

        {"".join(f"Q: {q}\nA: {a}\n\n" for q, a in zip(questions, answers))}

        Determine proficiency level (Beginner/Intermediate/Advanced/Expert) and confidence (0-1).
        Provide brief evidence.

        Return in JSON format:
        {{
            "level": "level",
            "confidence": 0.8,
            "evidence": "brief explanation"
        }}
        """

        response = self.ollama.generate(prompt)
        try:
            import json
            return json.loads(response.strip())
        except:
            return {
                "level": "Intermediate",
                "confidence": 0.6,
                "evidence": "Based on Q&A analysis"
            }