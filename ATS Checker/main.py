"""
AI Skill Assessment Agent

This agent takes a Job Description and candidate's resume,
conversationally assesses proficiency on required skills,
identifies gaps, and generates personalized learning plans.
"""

import argparse
import json
from pathlib import Path
from agent import SkillAssessmentAgent


def main():
    parser = argparse.ArgumentParser(description="AI Skill Assessment Agent")
    parser.add_argument("--jd", required=True, help="Path to job description file")
    parser.add_argument("--resume", required=True, help="Path to resume file")
    parser.add_argument("--output", default="learning_plan.json", help="Output file for learning plan")
    parser.add_argument("--model", default="llama2", help="Ollama model to use (default: llama2)")

    args = parser.parse_args()

    # Read inputs
    jd_text = Path(args.jd).read_text()
    resume_text = Path(args.resume).read_text()

    # Initialize agent
    agent = SkillAssessmentAgent(args.model)

    # Run assessment
    learning_plan = agent.assess_and_plan(jd_text, resume_text)

    # Save output
    with open(args.output, 'w') as f:
        json.dump(learning_plan, f, indent=2)

    print(f"Learning plan saved to {args.output}")


if __name__ == "__main__":
    main()