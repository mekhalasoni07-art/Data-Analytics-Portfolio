# AI Skill Assessment Agent

An intelligent agent that analyzes job descriptions and candidate resumes to provide personalized skill gap analysis and learning plans.

## Features

- **Skill Extraction**: Automatically extracts technical skills from job descriptions and resumes
- **Conversational Assessment**: Assesses real proficiency levels through interactive questioning
- **Gap Analysis**: Identifies skill gaps and areas for improvement
- **Adjacent Skills**: Suggests related skills that are realistic to acquire
- **Personalized Learning Plans**: Creates customized learning paths with:
  - Curated resources (courses, tutorials, books)
  - Time estimates
  - Weekly breakdowns
  - Success metrics

## Prerequisites

1. **Python 3.8+**
2. **Ollama** installed and running locally
   - Download from: https://ollama.ai/
   - Pull a model: `ollama pull llama2`

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install and run Ollama:
   ```bash
   # Install Ollama from https://ollama.ai/
   
   # Pull the desired model (e.g., Llama3)
   ollama pull llama3
   
   # Start Ollama server
   ollama serve
   ```

## Usage

### Web Interface (Recommended)

The easiest way to use the agent is through the web interface:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
python run_web.py
```

Then open your browser to `http://localhost:5000`

**Features:**
- 📤 Upload JD and resume files (TXT, PDF, DOC, DOCX) or paste text directly
- 🤖 Select AI model (Llama2, Llama3, etc.)
- 📊 Beautiful results dashboard with skill assessments and charts
- 📚 Detailed learning plans with resources and timelines
- 💾 Download assessment reports as JSON
- 🎯 Gap analysis with severity indicators
- 💡 Adjacent skill suggestions

**Web Interface Screenshots:**
- **Home Page**: Upload forms with drag-and-drop file support
- **Results Page**: Comprehensive dashboard showing:
  - Skill proficiency levels with confidence scores
  - Identified gaps with severity ratings
  - Suggested adjacent skills to learn
  - Personalized learning plans with weekly breakdowns
  - Success metrics and resource recommendations

### API Integration

For developers who want to integrate the agent into other applications:

```python
import requests

# POST to the API endpoint
response = requests.post('http://localhost:5000/api/assess', json={
    'jd_text': 'Your job description here...',
    'resume_text': 'Your resume here...',
    'model': 'llama3'  # optional
})

result = response.json()
print(result)
```

**API Response Format:**
```json
{
  "job_description_skills": ["Python", "Machine Learning"],
  "resume_skills": ["Python", "SQL"],
  "skill_assessments": {...},
  "identified_gaps": [...],
  "suggested_adjacent_skills": [...],
  "learning_plan": {...}
}
```

### Command Line

```bash
python main.py --jd job_description.txt --resume candidate_resume.txt --output learning_plan.json
```

### Using Different Models

The agent supports any Ollama model. To use Llama3:

```bash
python main.py --jd job_description.txt --resume candidate_resume.txt --model llama3 --output learning_plan.json
```

Available models depend on what you've installed in Ollama. Common options:
- `llama2` (default)
- `llama3`
- `llama3:8b`
- `llama3:70b`
- `codellama`
- `mistral`

### Interactive Assessment

Modify the agent to enable interactive assessment in `agent.py`:

```python
# In assess_and_plan method
proficiency = self.assessor.assess_skill(skill, resume_text, interactive=True)
```

## Input Formats

### Job Description File
Plain text file containing the job requirements, preferred skills, etc.

### Resume File
Plain text file containing the candidate's resume content.

## Output

The agent generates a JSON file with:

- Extracted skills from JD and resume
- Proficiency assessments
- Identified gaps
- Suggested adjacent skills
- Detailed learning plan with timeline and resources

## Example Output Structure

```json
{
  "job_description_skills": ["Python", "Machine Learning", "SQL"],
  "resume_skills": ["Python", "Java", "Git"],
  "skill_assessments": {
    "Python": {"level": "Intermediate", "confidence": 0.8},
    "Machine Learning": {"level": "Beginner", "confidence": 0.6}
  },
  "identified_gaps": [...],
  "suggested_adjacent_skills": [...],
  "learning_plan": {
    "total_duration_weeks": 8,
    "modules": [...],
    "weekly_schedule": {...},
    "success_metrics": [...]
  }
}
```

## Customization

- **Models**: Change the Ollama model in the agent initialization
- **Skill Keywords**: Extend the skill database in `skill_extractor.py`
- **Assessment Questions**: Modify question generation in `assessor.py`
- **Resources**: Update resource finding logic in `learning_planner.py`

## Architecture

- `main.py`: Entry point and CLI
- `agent.py`: Main orchestration logic
- `skill_extractor.py`: NLP-based skill extraction
- `assessor.py`: Proficiency assessment (automated/interactive)
- `gap_analyzer.py`: Gap identification and adjacent skill suggestions
- `learning_planner.py`: Learning plan generation
- `ollama_client.py`: Ollama API wrapper

## Troubleshooting

1. **Ollama not responding**: Ensure Ollama is running with `ollama serve`
2. **Model not found**: Pull the model with `ollama pull <model_name>`
3. **Empty extractions**: Check input file formats and content
4. **Assessment errors**: Verify resume content is detailed enough

## Future Enhancements

- Web interface for easier interaction
- Integration with LinkedIn/Indeed for job data
- Resume parsing from PDF/docx formats
- Integration with learning platforms (Coursera, Udemy)
- Progress tracking and reminders