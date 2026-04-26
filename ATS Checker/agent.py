"""
Skill Assessment Agent

Main agent class that orchestrates the skill assessment process.
"""

import json
from typing import Dict, List, Any
from skill_extractor import SkillExtractor
from assessor import ProficiencyAssessor
from gap_analyzer import GapAnalyzer
from learning_planner import LearningPlanner


class SkillAssessmentAgent:
    def __init__(self, model_name: str = "llama2"):
        self.skill_extractor = SkillExtractor(model_name)
        self.assessor = ProficiencyAssessor(model_name)
        self.gap_analyzer = GapAnalyzer(model_name)
        self.learning_planner = LearningPlanner(model_name)

    def assess_and_plan(self, jd_text: str, resume_text: str) -> Dict[str, Any]:
        """
        Main method to assess skills and generate learning plan.

        Args:
            jd_text: Job description text
            resume_text: Resume text

        Returns:
            Dictionary containing assessment results and learning plan
        """
        # Extract skills from JD and resume
        jd_skills = self.skill_extractor.extract_skills(jd_text, "job_description")
        resume_skills = self.skill_extractor.extract_skills(resume_text, "resume")

        print(f"Extracted {len(jd_skills)} skills from JD")
        print(f"Extracted {len(resume_skills)} skills from resume")

        # Assess proficiency for each required skill
        assessments = {}
        for skill in jd_skills:
            print(f"Assessing proficiency for: {skill}")
            proficiency = self.assessor.assess_skill(skill, resume_text)
            assessments[skill] = proficiency

        # Identify gaps and suggest adjacent skills
        gaps = self.gap_analyzer.identify_gaps(jd_skills, resume_skills, assessments)
        adjacent_skills = self.gap_analyzer.suggest_adjacent_skills(gaps, resume_skills)

        # Generate learning plan
        learning_plan = self.learning_planner.generate_plan(gaps, adjacent_skills, assessments)

        return {
            "job_description_skills": jd_skills,
            "resume_skills": resume_skills,
            "skill_assessments": assessments,
            "identified_gaps": gaps,
            "suggested_adjacent_skills": adjacent_skills,
            "learning_plan": learning_plan
        }