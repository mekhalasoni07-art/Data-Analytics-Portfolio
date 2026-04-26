"""
Learning Planner

Generates personalized learning plans with resources and time estimates.
"""

from typing import List, Dict, Any
from ollama_client import OllamaClient


class LearningPlanner:
    def __init__(self, model_name: str = "llama2"):
        self.ollama = OllamaClient(model_name)

    def generate_plan(self, gaps: List[Dict[str, Any]], adjacent_skills: List[Dict[str, Any]],
                     assessments: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive learning plan.

        Args:
            gaps: Identified skill gaps
            adjacent_skills: Suggested adjacent skills
            assessments: Current skill assessments

        Returns:
            Learning plan with milestones, resources, and timeline
        """
        # Group skills by priority
        prioritized_skills = self._prioritize_skills(gaps, adjacent_skills)

        # Generate learning modules
        modules = []
        for skill_info in prioritized_skills:
            module = self._create_learning_module(skill_info)
            modules.append(module)

        # Calculate total timeline
        total_weeks = sum(module["estimated_weeks"] for module in modules)

        return {
            "total_duration_weeks": total_weeks,
            "modules": modules,
            "weekly_schedule": self._create_schedule(modules),
            "success_metrics": self._define_success_metrics(prioritized_skills)
        }

    def _prioritize_skills(self, gaps: List[Dict[str, Any]], adjacent_skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize skills for learning based on gaps and feasibility."""
        all_skills = []

        # Add adjacent skills
        for adj in adjacent_skills:
            skill_info = {
                "skill": adj["suggested_skill"],
                "type": "adjacent",
                "target_gap": adj["target_gap"],
                "difficulty": adj["difficulty"],
                "rationale": adj["rationale"],
                "prerequisites": adj["prerequisites"]
            }
            all_skills.append(skill_info)

        # Sort by priority (adjacent skills that address critical gaps first)
        gap_severity_map = {gap["skill"]: gap["gap_severity"] for gap in gaps}

        def priority_key(skill):
            severity = gap_severity_map.get(skill["target_gap"], "Low")
            severity_score = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}.get(severity, 1)
            difficulty_score = {"Beginner": 3, "Intermediate": 2, "Advanced": 1}.get(skill["difficulty"], 2)
            return severity_score * 10 + difficulty_score

        all_skills.sort(key=priority_key, reverse=True)
        return all_skills[:5]  # Limit to top 5

    def _create_learning_module(self, skill_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a learning module for a skill."""
        skill = skill_info["skill"]
        difficulty = skill_info["difficulty"]

        # Generate learning resources
        resources = self._find_resources(skill, difficulty)

        # Estimate time based on difficulty
        time_estimates = {
            "Beginner": 2,
            "Intermediate": 4,
            "Advanced": 6
        }
        estimated_weeks = time_estimates.get(difficulty, 4)

        # Create learning objectives
        objectives = self._create_objectives(skill, difficulty)

        return {
            "skill": skill,
            "difficulty": difficulty,
            "estimated_weeks": estimated_weeks,
            "objectives": objectives,
            "resources": resources,
            "weekly_breakdown": self._create_weekly_breakdown(skill, estimated_weeks, objectives)
        }

    def _find_resources(self, skill: str, difficulty: str) -> List[Dict[str, str]]:
        """Find learning resources for a skill."""
        prompt = f"""
        Find high-quality learning resources for {skill} at {difficulty} level.

        Include:
        - 1-2 online courses (Coursera, Udemy, etc.)
        - 2-3 tutorials/articles
        - 1-2 books (if appropriate)
        - 1-2 practice platforms/projects

        For each resource, provide:
        - Title
        - Platform/Source
        - URL (if known, otherwise describe)
        - Duration/Time commitment
        - Why it's good for {difficulty} level

        Return in JSON format:
        [
            {{
                "title": "Course Name",
                "platform": "Coursera",
                "url": "https://...",
                "duration": "4 weeks",
                "suitability": "Perfect for beginners"
            }}
        ]
        """

        try:
            response = self.ollama.generate(prompt)
            import json
            resources = json.loads(response.strip())
            return resources if isinstance(resources, list) else []
        except:
            # Fallback resources
            return [
                {
                    "title": f"Introduction to {skill}",
                    "platform": "Online Course",
                    "url": "Search for it",
                    "duration": "2-4 weeks",
                    "suitability": f"Suitable for {difficulty} level"
                }
            ]

    def _create_objectives(self, skill: str, difficulty: str) -> List[str]:
        """Create learning objectives for a skill."""
        prompt = f"""
        Create 4-6 specific, measurable learning objectives for mastering {skill} at {difficulty} level.

        Objectives should be:
        - Specific and actionable
        - Progressive (building from basic to advanced)
        - Measurable (you can test if achieved)

        Return as a JSON array of strings.
        """

        try:
            response = self.ollama.generate(prompt)
            import json
            objectives = json.loads(response.strip())
            return objectives if isinstance(objectives, list) else []
        except:
            return [
                f"Understand basic concepts of {skill}",
                f"Complete a simple project using {skill}",
                f"Apply {skill} in a real-world scenario"
            ]

    def _create_weekly_breakdown(self, skill: str, weeks: int, objectives: List[str]) -> List[Dict[str, Any]]:
        """Create weekly learning breakdown."""
        breakdown = []
        objectives_per_week = len(objectives) // weeks + 1

        for week in range(1, weeks + 1):
            start_idx = (week - 1) * objectives_per_week
            end_idx = min(week * objectives_per_week, len(objectives))
            week_objectives = objectives[start_idx:end_idx]

            breakdown.append({
                "week": week,
                "objectives": week_objectives,
                "activities": [
                    "Study materials",
                    "Complete exercises",
                    "Work on mini-project"
                ],
                "assessment": f"Quiz or project review for {skill}"
            })

        return breakdown

    def _create_schedule(self, modules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create overall weekly schedule."""
        total_weeks = max((module["estimated_weeks"] for module in modules), default=4)

        schedule = {}
        for week in range(1, total_weeks + 1):
            week_modules = []
            for module in modules:
                if week <= module["estimated_weeks"]:
                    week_modules.append({
                        "skill": module["skill"],
                        "activities": module["weekly_breakdown"][week-1]["activities"] if week-1 < len(module["weekly_breakdown"]) else ["Review and practice"]
                    })

            schedule[f"week_{week}"] = {
                "focus_modules": week_modules,
                "total_hours": len(week_modules) * 10,  # Assume 10 hours per module per week
                "milestones": [f"Complete week {week} objectives for active modules"]
            }

        return schedule

    def _define_success_metrics(self, skills: List[Dict[str, Any]]) -> List[str]:
        """Define success metrics for the learning plan."""
        return [
            "Complete all learning modules within estimated timeframes",
            "Build and deploy a portfolio project incorporating learned skills",
            "Pass technical interviews for target skills",
            "Receive positive feedback on skill application in projects",
            "Achieve proficiency reassessment showing improvement"
        ]