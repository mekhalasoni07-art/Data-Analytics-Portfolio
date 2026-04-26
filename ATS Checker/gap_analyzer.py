"""
Gap Analyzer

Identifies skill gaps and suggests adjacent skills for learning.
"""

from typing import List, Dict, Set, Any
from ollama_client import OllamaClient


class GapAnalyzer:
    def __init__(self, model_name: str = "llama2"):
        self.ollama = OllamaClient(model_name)

    def identify_gaps(self, required_skills: List[str], candidate_skills: List[str],
                     assessments: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify skill gaps based on required skills and candidate proficiency.

        Args:
            required_skills: Skills required for the job
            candidate_skills: Skills the candidate has
            assessments: Proficiency assessments

        Returns:
            List of gap dictionaries
        """
        gaps = []

        for skill in required_skills:
            candidate_has_skill = skill.lower() in [s.lower() for s in candidate_skills]
            assessment = assessments.get(skill, {})

            # Determine if there's a gap
            level = assessment.get("level", "Beginner")
            confidence = assessment.get("confidence", 0.5)

            # Consider it a gap if:
            # - Candidate doesn't have the skill, OR
            # - Has skill but proficiency is low (Beginner with low confidence)
            is_gap = not candidate_has_skill or (level == "Beginner" and confidence < 0.7)

            if is_gap:
                gap_info = {
                    "skill": skill,
                    "has_skill": candidate_has_skill,
                    "current_level": level,
                    "confidence": confidence,
                    "gap_severity": self._calculate_gap_severity(skill, level, confidence)
                }
                gaps.append(gap_info)

        return gaps

    def suggest_adjacent_skills(self, gaps: List[Dict[str, Any]], candidate_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Suggest adjacent skills that can help bridge gaps.

        Args:
            gaps: Identified skill gaps
            candidate_skills: Skills the candidate already has

        Returns:
            List of suggested adjacent skills
        """
        suggestions = []

        for gap in gaps:
            skill = gap["skill"]

            # Get adjacent skills
            adjacent = self._find_adjacent_skills(skill, candidate_skills)

            for adj_skill in adjacent:
                suggestion = {
                    "target_gap": skill,
                    "suggested_skill": adj_skill["skill"],
                    "rationale": adj_skill["rationale"],
                    "difficulty": adj_skill["difficulty"],
                    "prerequisites": adj_skill["prerequisites"]
                }
                suggestions.append(suggestion)

        return suggestions

    def _calculate_gap_severity(self, skill: str, level: str, confidence: float) -> str:
        """Calculate gap severity."""
        if level == "Beginner" and confidence < 0.5:
            return "Critical"
        elif level in ["Beginner", "Intermediate"] and confidence < 0.7:
            return "High"
        elif level == "Intermediate":
            return "Medium"
        else:
            return "Low"

    def _find_adjacent_skills(self, skill: str, candidate_skills: List[str]) -> List[Dict[str, Any]]:
        """Find skills adjacent to the target skill."""
        prompt = f"""
        For the skill "{skill}", suggest 2-3 adjacent skills that someone with these existing skills could realistically learn:

        Existing skills: {', '.join(candidate_skills)}

        Adjacent skills should be:
        - Related to {skill}
        - Build upon existing skills
        - Realistic to acquire (not requiring years of experience)
        - Have clear learning paths

        For each suggested skill, provide:
        - Skill name
        - Rationale (why it's adjacent)
        - Difficulty level (Beginner/Intermediate/Advanced)
        - Prerequisites (what existing skills help)

        Return in JSON format:
        [
            {{
                "skill": "skill name",
                "rationale": "why it's useful",
                "difficulty": "Beginner",
                "prerequisites": ["skill1", "skill2"]
            }}
        ]
        """

        try:
            response = self.ollama.generate(prompt)
            import json
            suggestions = json.loads(response.strip())
            return suggestions if isinstance(suggestions, list) else []
        except:
            # Fallback suggestions
            return [
                {
                    "skill": f"Advanced {skill}",
                    "rationale": f"Builds directly on basic {skill} knowledge",
                    "difficulty": "Intermediate",
                    "prerequisites": [skill]
                }
            ]