document.addEventListener('DOMContentLoaded', function () {
    const jdFileInput = document.getElementById('jd_file');
    const resumeFileInput = document.getElementById('resume_file');

    if (jdFileInput) {
        jdFileInput.addEventListener('change', function (e) {
            if (e.target.files.length > 0) {
                const jdText = document.getElementById('jd_text');
                if (jdText) {
                    jdText.value = '';
                }
            }
        });
    }

    if (resumeFileInput) {
        resumeFileInput.addEventListener('change', function (e) {
            if (e.target.files.length > 0) {
                const resumeText = document.getElementById('resume_text');
                if (resumeText) {
                    resumeText.value = '';
                }
            }
        });
    }
});

function loadSampleData() {
    alert('Sample data loading feature coming soon! Use the file upload or text input above.');
}

function toggleJson() {
    const container = document.getElementById('jsonContainer');
    if (!container) {
        return;
    }
    container.classList.toggle('visible');
}