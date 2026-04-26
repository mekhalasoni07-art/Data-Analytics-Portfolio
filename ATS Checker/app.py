"""
Flask Web Interface for AI Skill Assessment Agent
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
from pathlib import Path
from agent import SkillAssessmentAgent
import tempfile

app = Flask(__name__)
app.secret_key = 'skill_assessment_secret_key_2024'

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    """Main page with upload forms."""
    return render_template('index.html')

@app.route('/assess', methods=['POST'])
def assess():
    """Handle assessment request."""
    try:
        # Get form data
        model_name = request.form.get('model', 'llama2')

        # Handle JD input
        jd_text = ""
        if 'jd_file' in request.files and request.files['jd_file'].filename:
            jd_file = request.files['jd_file']
            jd_path = os.path.join(app.config['UPLOAD_FOLDER'], 'jd_temp.txt')
            jd_file.save(jd_path)
            jd_text = Path(jd_path).read_text()
        elif request.form.get('jd_text'):
            jd_text = request.form.get('jd_text')
        else:
            flash('Please provide a job description', 'error')
            return redirect(url_for('index'))

        # Handle resume input
        resume_text = ""
        if 'resume_file' in request.files and request.files['resume_file'].filename:
            resume_file = request.files['resume_file']
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resume_temp.txt')
            resume_file.save(resume_path)
            resume_text = Path(resume_path).read_text()
        elif request.form.get('resume_text'):
            resume_text = request.form.get('resume_text')
        else:
            flash('Please provide a resume', 'error')
            return redirect(url_for('index'))

        # Initialize agent and run assessment
        agent = SkillAssessmentAgent(model_name)
        result = agent.assess_and_plan(jd_text, resume_text)

        # Clean up temp files
        for temp_file in ['jd_temp.txt', 'resume_temp.txt']:
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_file)
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return render_template('results.html', result=result, model_name=model_name)

    except Exception as e:
        flash(f'Error during assessment: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/assess', methods=['POST'])
def api_assess():
    """API endpoint for assessment (returns JSON)."""
    try:
        data = request.get_json()
        jd_text = data.get('jd_text', '')
        resume_text = data.get('resume_text', '')
        model_name = data.get('model', 'llama2')

        if not jd_text or not resume_text:
            return jsonify({'error': 'JD and resume text are required'}), 400

        agent = SkillAssessmentAgent(model_name)
        result = agent.assess_and_plan(jd_text, resume_text)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)