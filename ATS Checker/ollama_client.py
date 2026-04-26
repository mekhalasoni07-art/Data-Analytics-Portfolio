"""
Ollama Client

Wrapper for interacting with Ollama API.
"""

import ollama
import json
from typing import Optional


class OllamaClient:
    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Generate text using Ollama.

        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        if not self.is_available():
            return self._mock_response(prompt)

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
            )
            return response.get("response", "")
        except Exception as e:
            print(f"Ollama API error: {e}. Using mock response.")
            return self._mock_response(prompt)

    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """
        Chat with Ollama using conversation format.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature

        Returns:
            Assistant response
        """
        if not self.is_available():
            return self._mock_chat_response(messages)

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options={'temperature': temperature}
            )
            return response.get("message", {}).get("content", "")
        except Exception as e:
            print(f"Ollama API error: {e}. Using mock response.")
            return self._mock_chat_response(messages)

    def is_available(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            # Try to list models
            models = ollama.list()
            model_names = [model['name'] for model in models.get('models', [])]
            return self.model_name in model_names or any(self.model_name in name for name in model_names)
        except:
            return False

    def _extract_skills_from_text(self, text: str) -> list:
        """Extract skills from text using keyword matching."""
        skill_keywords = {
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust",
            "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "data science",
            "sql", "mongodb", "postgresql", "mysql", "redis", "nosql",
            "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform",
            "react", "angular", "vue", "node.js", "django", "flask", "spring", "fastapi",
            "git", "github", "gitlab", "ci/cd", "jenkins", "gitlab ci",
            "agile", "scrum", "kanban", "devops",
            "linux", "windows", "bash", "powershell", "shell",
            "html", "css", "xml", "json", "rest", "graphql", "api",
            "tensorflow", "pytorch", "scikit-learn", "keras",
            "ec2", "s3", "lambda", "rds", "dynamodb",
            "docker compose", "helm", "prometheus", "grafana"
        }
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates

    def _extract_skill_from_prompt(self, prompt: str) -> str:
        """Extract the main skill being discussed from the prompt."""
        skill_keywords = [
            "tensorflow", "pytorch", "scikit-learn", "keras",
            "machine learning", "deep learning", "nlp", "natural language processing", 
            "computer vision", "data science", "fastapi", "docker compose",
            "google cloud", "gitlab ci",
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust",
            "sql", "mongodb", "postgresql", "mysql", "redis", "nosql",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "react", "angular", "vue", "node.js", "django", "flask", "spring",
            "git", "github", "gitlab", "ci/cd", "jenkins",
            "agile", "scrum", "kanban", "devops",
            "linux", "windows", "bash", "powershell", "shell",
            "html", "css", "xml", "json", "rest", "graphql", "api",
            "ec2", "s3", "lambda", "rds", "dynamodb", "helm", "prometheus", "grafana"
        ]
        
        prompt_lower = prompt.lower()
        for skill in skill_keywords:
            if skill in prompt_lower:
                return skill
        return "general technology"

    def _extract_difficulty_from_prompt(self, prompt: str) -> str:
        """Extract difficulty level from prompt."""
        if "beginner" in prompt.lower():
            return "Beginner"
        elif "advanced" in prompt.lower():
            return "Advanced"
        else:
            return "Intermediate"

    def _generate_resources_for_skill(self, skill: str, difficulty: str) -> str:
        """Generate learning resources for a specific skill."""
        resources_map = {
            "python": [
                {"title": "Python for Everybody", "platform": "Coursera", "url": "https://coursera.org/learn/python", "duration": "8 weeks", "suitability": "Perfect for all levels"},
                {"title": "Real Python", "platform": "Website", "url": "https://realpython.com", "duration": "Self-paced", "suitability": "Comprehensive tutorials"},
                {"title": "Python Official Docs", "platform": "Official", "url": "https://python.org/docs", "duration": "Self-paced", "suitability": "Reference material"}
            ],
            "machine learning": [
                {"title": "Machine Learning by Andrew Ng", "platform": "Coursera", "url": "https://coursera.org/learn/machine-learning", "duration": "11 weeks", "suitability": "Industry-standard course"},
                {"title": "Fast.ai - Practical Deep Learning", "platform": "Fast.ai", "url": "https://fast.ai", "duration": "7 weeks", "suitability": "Top-down approach"},
                {"title": "Scikit-learn Documentation", "platform": "Official", "url": "https://scikit-learn.org", "duration": "Self-paced", "suitability": "Practical implementation guide"}
            ],
            "aws": [
                {"title": "AWS Certified Cloud Practitioner", "platform": "A Cloud Guru", "url": "https://acloudguru.com", "duration": "20 hours", "suitability": "Beginner-friendly certification prep"},
                {"title": "AWS Free Tier", "platform": "AWS", "url": "https://aws.amazon.com/free", "duration": "Self-paced hands-on", "suitability": "Free practice environment"},
                {"title": "AWS Solutions Architect Associate", "platform": "Udemy", "url": "https://udemy.com", "duration": "40 hours", "suitability": "Intermediate level"}
            ],
            "docker": [
                {"title": "Docker for Beginners", "platform": "Udemy", "url": "https://udemy.com", "duration": "12 hours", "suitability": "Practical introduction"},
                {"title": "Docker Official Documentation", "platform": "Official", "url": "https://docs.docker.com", "duration": "Self-paced", "suitability": "Complete reference"},
                {"title": "Docker Deep Dive", "platform": "Pluralsight", "url": "https://pluralsight.com", "duration": "20 hours", "suitability": "In-depth exploration"}
            ],
            "kubernetes": [
                {"title": "Kubernetes for Developers", "platform": "edX", "url": "https://edx.org", "duration": "6 weeks", "suitability": "Developer-focused"},
                {"title": "Kubernetes Official Tutorials", "platform": "Official", "url": "https://kubernetes.io/docs/tutorials", "duration": "Self-paced", "suitability": "Hands-on labs"},
                {"title": "CKA Certification Prep", "platform": "Linux Academy", "url": "https://linuxacademy.com", "duration": "40 hours", "suitability": "Advanced certification"}
            ],
            "react": [
                {"title": "React - The Complete Guide", "platform": "Udemy", "url": "https://udemy.com", "duration": "48 hours", "suitability": "Comprehensive course"},
                {"title": "React Official Documentation", "platform": "Official", "url": "https://react.dev", "duration": "Self-paced", "suitability": "Official guide"},
                {"title": "Scrimba React Course", "platform": "Scrimba", "url": "https://scrimba.com", "duration": "20 hours", "suitability": "Interactive learning"}
            ],
            "sql": [
                {"title": "SQL for Data Analysis", "platform": "Udacity", "url": "https://udacity.com", "duration": "8 weeks", "suitability": "Data-focused SQL"},
                {"title": "SQL Tutorial", "platform": "W3Schools", "url": "https://w3schools.com/sql", "duration": "Self-paced", "suitability": "Interactive basics"},
                {"title": "Advanced SQL", "platform": "DataCamp", "url": "https://datacamp.com", "duration": "10 hours", "suitability": "Advanced topics"}
            ],
            "javascript": [
                {"title": "The Complete JavaScript Course", "platform": "Udemy", "url": "https://udemy.com", "duration": "69 hours", "suitability": "Comprehensive beginner to advanced"},
                {"title": "JavaScript.info", "platform": "Website", "url": "https://javascript.info", "duration": "Self-paced", "suitability": "Interactive and modern"},
                {"title": "Eloquent JavaScript", "platform": "Online Book", "url": "https://eloquentjavascript.net", "duration": "Self-paced", "suitability": "Deep dive into concepts"}
            ]
        }
        
        skill_lower = skill.lower()
        resources = resources_map.get(skill_lower, [
            {"title": f"Introduction to {skill}", "platform": "Online Learning Platform", "url": f"https://search.com?q={skill}", "duration": "Variable", "suitability": f"Suitable for {difficulty} level"},
            {"title": f"{skill} Official Documentation", "platform": "Official", "url": f"https://{skill.lower().replace(' ', '')}.org/docs", "duration": "Self-paced", "suitability": "Reference and examples"},
            {"title": f"Practical {skill} Projects", "platform": "GitHub", "url": "https://github.com", "duration": "Self-paced", "suitability": "Hands-on learning"}
        ])
        
        return json.dumps(resources)

    def _generate_objectives_for_skill(self, skill: str, difficulty: str) -> str:
        """Generate learning objectives for a specific skill."""
        objectives_map = {
            "python": {
                "Beginner": ["Understand Python syntax and basic data types", "Write simple functions and scripts", "Work with lists and dictionaries", "Understand control flow (if/else/loops)", "Handle basic file operations"],
                "Intermediate": ["Use object-oriented programming concepts", "Work with libraries and modules", "Handle exceptions effectively", "Write and run unit tests", "Understand decorators and generators"],
                "Advanced": ["Optimize code for performance", "Master advanced OOP patterns", "Contribute to open-source projects", "Understand asyncio and threading", "Create professional-grade applications"]
            },
            "machine learning": {
                "Beginner": ["Understand ML fundamentals and problem types", "Prepare and explore data", "Train and evaluate basic models", "Use scikit-learn for classification/regression", "Understand overfitting and validation"],
                "Intermediate": ["Build end-to-end ML pipelines", "Implement deep learning models", "Perform feature engineering", "Deploy ML models", "Understand model evaluation metrics"],
                "Advanced": ["Design custom neural networks", "Implement advanced algorithms from papers", "Optimize model performance", "Handle big data scenarios", "Lead ML projects"]
            },
            "aws": {
                "Beginner": ["Understand AWS core services", "Create and manage EC2 instances", "Use S3 for storage", "Understand IAM and security basics", "Deploy simple applications"],
                "Intermediate": ["Design scalable architectures", "Use RDS and DynamoDB", "Implement load balancing", "Set up CI/CD pipelines", "Monitor and optimize costs"],
                "Advanced": ["Design enterprise solutions", "Implement auto-scaling", "Set up disaster recovery", "Optimize cloud infrastructure", "Achieve AWS certification"]
            },
            "docker": {
                "Beginner": ["Understand containerization concepts", "Build and run Docker images", "Use Docker Compose for multi-container apps", "Manage volumes and networks", "Push images to registries"],
                "Intermediate": ["Optimize Docker images", "Implement best practices", "Use Docker in CI/CD", "Handle security concerns", "Debug containerized applications"],
                "Advanced": ["Design microservices architecture", "Implement container orchestration", "Performance tuning", "Production deployment patterns", "Security hardening"]
            },
            "react": {
                "Beginner": ["Understand React components", "Work with JSX", "Manage component state", "Handle events and forms", "Build simple applications"],
                "Intermediate": ["Use React Hooks effectively", "Implement state management", "Work with APIs", "Optimize performance", "Handle routing"],
                "Advanced": ["Build large-scale applications", "Implement complex state patterns", "Custom hooks and libraries", "Performance profiling", "Testing strategies"]
            },
            "sql": {
                "Beginner": ["Understand database basics", "Write SELECT queries", "Use WHERE and ORDER BY", "Understand JOINs", "Create and manage tables"],
                "Intermediate": ["Write complex queries with subqueries", "Aggregate data effectively", "Optimize query performance", "Work with indexes", "Understand transactions"],
                "Advanced": ["Design efficient database schemas", "Master query optimization", "Implement stored procedures", "Handle replication and scaling", "Troubleshoot performance issues"]
            }
        }
        
        skill_lower = skill.lower()
        objectives = objectives_map.get(skill_lower, {}).get(difficulty, [
            f"Understand core concepts of {skill}",
            f"Implement practical {skill} solutions",
            f"Complete a project using {skill}",
            f"Master advanced {skill} techniques",
            f"Apply {skill} in real-world scenarios"
        ])
        
        return json.dumps(objectives)

    def _generate_adjacent_skills(self, target_skill: str, existing_skills: list) -> str:
        """Generate adjacent skills related to the target skill based on existing skills."""
        # Map of skills to their adjacent/related skills
        adjacent_map = {
            "python": [
                {"skill": "Django", "rationale": "Web framework built on Python for backend development", "difficulty": "Intermediate", "prerequisites": ["Python"]},
                {"skill": "Flask", "rationale": "Lightweight Python web framework for building APIs and web apps", "difficulty": "Beginner", "prerequisites": ["Python"]},
                {"skill": "FastAPI", "rationale": "Modern Python web framework for building fast APIs", "difficulty": "Intermediate", "prerequisites": ["Python"]},
                {"skill": "Pandas", "rationale": "Data manipulation library built on Python", "difficulty": "Intermediate", "prerequisites": ["Python"]},
                {"skill": "NumPy", "rationale": "Numerical computing library fundamental to data science", "difficulty": "Beginner", "prerequisites": ["Python"]},
            ],
            "machine learning": [
                {"skill": "TensorFlow", "rationale": "Deep learning framework for building neural networks", "difficulty": "Intermediate", "prerequisites": ["Python", "Machine Learning"]},
                {"skill": "PyTorch", "rationale": "Popular deep learning framework with dynamic computation", "difficulty": "Intermediate", "prerequisites": ["Python", "Machine Learning"]},
                {"skill": "Scikit-learn", "rationale": "Machine learning library for classification and regression", "difficulty": "Beginner", "prerequisites": ["Python"]},
                {"skill": "Data Visualization", "rationale": "Essential for communicating ML results", "difficulty": "Beginner", "prerequisites": ["Python"]},
                {"skill": "Feature Engineering", "rationale": "Critical skill for improving model performance", "difficulty": "Intermediate", "prerequisites": ["Machine Learning"]},
            ],
            "aws": [
                {"skill": "EC2", "rationale": "Virtual computing resource for running applications on AWS", "difficulty": "Beginner", "prerequisites": ["AWS"]},
                {"skill": "S3", "rationale": "Object storage service for scalable data storage", "difficulty": "Beginner", "prerequisites": ["AWS"]},
                {"skill": "Lambda", "rationale": "Serverless computing for event-driven applications", "difficulty": "Intermediate", "prerequisites": ["AWS"]},
                {"skill": "RDS", "rationale": "Managed database service on AWS", "difficulty": "Intermediate", "prerequisites": ["AWS", "SQL"]},
                {"skill": "CloudFormation", "rationale": "Infrastructure as code on AWS", "difficulty": "Advanced", "prerequisites": ["AWS"]},
            ],
            "docker": [
                {"skill": "Kubernetes", "rationale": "Container orchestration platform for managing Docker containers", "difficulty": "Advanced", "prerequisites": ["Docker"]},
                {"skill": "Docker Compose", "rationale": "Tool for defining multi-container Docker applications", "difficulty": "Intermediate", "prerequisites": ["Docker"]},
                {"skill": "Container Security", "rationale": "Security best practices for containerized applications", "difficulty": "Intermediate", "prerequisites": ["Docker"]},
                {"skill": "Docker Registry", "rationale": "Managing and storing Docker images", "difficulty": "Beginner", "prerequisites": ["Docker"]},
                {"skill": "CI/CD with Docker", "rationale": "Integrating Docker into continuous integration pipelines", "difficulty": "Intermediate", "prerequisites": ["Docker", "CI/CD"]},
            ],
            "kubernetes": [
                {"skill": "Helm", "rationale": "Package manager for Kubernetes applications", "difficulty": "Intermediate", "prerequisites": ["Kubernetes"]},
                {"skill": "Service Mesh", "rationale": "Manage microservice communication with tools like Istio", "difficulty": "Advanced", "prerequisites": ["Kubernetes"]},
                {"skill": "Kubernetes Operators", "rationale": "Extend Kubernetes functionality", "difficulty": "Advanced", "prerequisites": ["Kubernetes"]},
                {"skill": "Container Security", "rationale": "Security best practices for Kubernetes", "difficulty": "Intermediate", "prerequisites": ["Kubernetes"]},
            ],
            "react": [
                {"skill": "Redux", "rationale": "State management library for complex React applications", "difficulty": "Intermediate", "prerequisites": ["React", "JavaScript"]},
                {"skill": "React Router", "rationale": "Routing library for single-page applications", "difficulty": "Beginner", "prerequisites": ["React"]},
                {"skill": "Next.js", "rationale": "React framework for production-ready applications", "difficulty": "Intermediate", "prerequisites": ["React", "JavaScript"]},
                {"skill": "TypeScript", "rationale": "Add type safety to React applications", "difficulty": "Intermediate", "prerequisites": ["React", "JavaScript"]},
                {"skill": "Testing React", "rationale": "Unit and integration testing for React components", "difficulty": "Intermediate", "prerequisites": ["React"]},
            ],
            "sql": [
                {"skill": "Database Design", "rationale": "Designing efficient database schemas", "difficulty": "Intermediate", "prerequisites": ["SQL"]},
                {"skill": "Query Optimization", "rationale": "Writing efficient SQL queries", "difficulty": "Intermediate", "prerequisites": ["SQL"]},
                {"skill": "Stored Procedures", "rationale": "Database programming with stored procedures", "difficulty": "Intermediate", "prerequisites": ["SQL"]},
                {"skill": "NoSQL Databases", "rationale": "Alternative database paradigms like MongoDB", "difficulty": "Intermediate", "prerequisites": ["SQL"]},
            ],
            "javascript": [
                {"skill": "Node.js", "rationale": "JavaScript runtime for backend development", "difficulty": "Intermediate", "prerequisites": ["JavaScript"]},
                {"skill": "React", "rationale": "Popular frontend framework for building UIs", "difficulty": "Intermediate", "prerequisites": ["JavaScript"]},
                {"skill": "Vue.js", "rationale": "Progressive framework for building user interfaces", "difficulty": "Beginner", "prerequisites": ["JavaScript"]},
                {"skill": "TypeScript", "rationale": "Typed superset of JavaScript", "difficulty": "Intermediate", "prerequisites": ["JavaScript"]},
                {"skill": "Web APIs", "rationale": "Understanding browser and server APIs", "difficulty": "Intermediate", "prerequisites": ["JavaScript"]},
            ],
        }
        
        target_lower = target_skill.lower()
        suggestions = adjacent_map.get(target_lower, [
            {"skill": f"{target_skill} Advanced Concepts", "rationale": f"Deepen expertise in {target_skill}", "difficulty": "Intermediate", "prerequisites": [target_skill]},
            {"skill": f"{target_skill} in Production", "rationale": f"Learn production deployment of {target_skill}", "difficulty": "Advanced", "prerequisites": [target_skill]},
        ])
        
        # Filter to show 2-3 suggestions
        return json.dumps(suggestions[:3])

    def _mock_response(self, prompt: str) -> str:
        """Provide mock responses when Ollama is not available."""
        prompt_lower = prompt.lower()

        if "skill" in prompt_lower and "extract" in prompt_lower:
            # Extract skills from the actual text in the prompt
            extracted_skills = self._extract_skills_from_text(prompt)
            
            # If we found skills, return them
            if extracted_skills:
                return ", ".join(extracted_skills)
            
            # Fallback to default if no skills found
            if "resume" in prompt_lower:
                return "Python, SQL, Git"
            else:
                return "Python, SQL, Git"
                
        elif "assess" in prompt_lower and "proficiency" in prompt_lower:
            # Extract the skill name from the prompt
            for skill_word in ["python", "java", "javascript", "aws", "docker", "machine learning", 
                              "sql", "kubernetes", "react", "node.js", "tensorflow"]:
                if skill_word in prompt_lower:
                    # Vary confidence based on mention frequency in prompt
                    confidence = 0.5 if prompt.lower().count(skill_word) > 2 else 0.3
                    level = "Intermediate" if confidence > 0.4 else "Beginner"
                    return json.dumps({
                        "level": level,
                        "confidence": confidence,
                        "evidence": f"Based on resume mentions of {skill_word.title()}"
                    })
            
            return json.dumps({
                "level": "Intermediate",
                "confidence": 0.7,
                "evidence": "Based on resume experience"
            })
            
        elif "adjacent" in prompt_lower or "related" in prompt_lower:
            # Extract target skill and existing skills from prompt
            target_skill = self._extract_skill_from_prompt(prompt)
            
            # Extract existing skills (they're usually listed in the prompt)
            existing_skills = self._extract_skills_from_text(prompt)
            if not existing_skills:
                existing_skills = []
            
            # Generate dynamic adjacent skills
            return self._generate_adjacent_skills(target_skill, existing_skills)
            
        elif "resource" in prompt_lower or "learning" in prompt_lower:
            # Extract the skill from the prompt
            skill = self._extract_skill_from_prompt(prompt)
            difficulty = self._extract_difficulty_from_prompt(prompt)
            return self._generate_resources_for_skill(skill, difficulty)
        elif "objective" in prompt_lower:
            # Extract the skill from the prompt
            skill = self._extract_skill_from_prompt(prompt)
            difficulty = self._extract_difficulty_from_prompt(prompt)
            return self._generate_objectives_for_skill(skill, difficulty)
        else:
            return "This is a mock response. Please install and run Ollama for full functionality."

    def _mock_chat_response(self, messages: list) -> str:
        """Mock chat response."""
        last_message = messages[-1]["content"] if messages else ""
        return f"Mock response to: {last_message[:50]}..."