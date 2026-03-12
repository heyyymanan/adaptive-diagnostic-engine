const API_BASE_URL = 'http://127.0.0.1:8000';

// DOM Elements
const views = {
    welcome: document.getElementById('welcome-view'),
    question: document.getElementById('question-view'),
    results: document.getElementById('results-view')
};

const dom = {
    startBtn: document.getElementById('start-btn'),
    qCounter: document.getElementById('q-counter'),
    qDifficulty: document.getElementById('q-difficulty'),
    qText: document.getElementById('question-text'),
    optionsContainer: document.getElementById('options-container'),
    feedbackContainer: document.getElementById('feedback-container'),
    feedbackText: document.getElementById('feedback-text'),
    finalScore: document.getElementById('final-score'),
    studyPlanContent: document.getElementById('study-plan-content'),
    loadingPulse: document.querySelector('.loading-pulse'),
    restartBtn: document.getElementById('restart-btn'),
    scoreCircle: document.querySelector('.score-circle')
};

// State
let sessionData = {
    id: null,
    ability: 0.5,
    questionCount: 0,
    currentQuestionId: null
};

// SVG Icons
const icons = {
    check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
    x: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`
};

// Event Listeners
dom.startBtn.addEventListener('click', startAssessment);
dom.restartBtn.addEventListener('click', resetApp);

// Functions
function switchView(viewName) {
    Object.values(views).forEach(v => {
        v.classList.remove('active');
        setTimeout(() => v.classList.add('hidden'), 300); // Wait for fade out delay
    });
    
    setTimeout(() => {
        views[viewName].classList.remove('hidden');
        views[viewName].classList.add('active');
    }, 300);
}

async function startAssessment() {
    dom.startBtn.disabled = true;
    dom.startBtn.innerHTML = 'Initializing...';
    
    try {
        const res = await fetch(`${API_BASE_URL}/start-session`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!res.ok) throw new Error("Failed to connect to API");

        const data = await res.json();
        
        sessionData.id = data.session_id;
        sessionData.ability = data.ability;
        sessionData.questionCount = 0;
        
        await loadNextQuestion();
        switchView('question');
    } catch (err) {
        console.error('Failed to start session:', err);
        alert('Could not connect to the backend API. Make sure it is running on port 8000.');
    } finally {
        dom.startBtn.disabled = false;
        dom.startBtn.innerHTML = 'Start Assessment';
    }
}

async function loadNextQuestion() {
    dom.feedbackContainer.classList.add('hidden');
    dom.qText.innerHTML = 'Loading AI customized question...';
    dom.optionsContainer.innerHTML = '';
    
    try {
        const res = await fetch(`${API_BASE_URL}/next-question/${sessionData.id}`);
        const data = await res.json();
        
        if (data.message === "No more questions" || sessionData.questionCount >= 10) {
            await showResults();
            return;
        }
        
        sessionData.questionCount++;
        sessionData.currentQuestionId = data.question_id;
        
        // Update UI
        dom.qCounter.textContent = sessionData.questionCount;
        dom.qDifficulty.textContent = (data.difficulty ?? 0.5).toFixed(2);
        dom.qText.textContent = data.question;
        
        // Render Options
        data.options.forEach(option => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.textContent = option;
            btn.onclick = () => submitAnswer(option, btn);
            dom.optionsContainer.appendChild(btn);
        });
        
    } catch (err) {
        console.error('Failed to load question:', err);
        dom.qText.innerHTML = 'Failed to load question. <button onclick="loadNextQuestion()" style="padding:6px 12px; font-size:14px; margin-top:10px;" class="secondary-btn">Retry</button>';
    }
}

async function submitAnswer(selectedAnswer, selectedBtn) {
    // Disable all options
    const allOptions = dom.optionsContainer.querySelectorAll('button');
    allOptions.forEach(btn => btn.disabled = true);
    
    selectedBtn.innerHTML += ' <span style="margin-left:auto;font-size:0.85em;opacity:0.8">Submitting...</span>';
    
    try {
        const res = await fetch(`${API_BASE_URL}/submit-answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionData.id,
                question_id: sessionData.currentQuestionId,
                answer: selectedAnswer
            })
        });
        const data = await res.json();
        
        // Update ability
        sessionData.ability = data.new_ability;
        
        showFeedback(data.correct, selectedBtn, allOptions);
        
        // Wait then log next
        setTimeout(loadNextQuestion, 2000);
        
    } catch (err) {
        console.error('Failed to submit answer:', err);
        selectedBtn.disabled = false;
        selectedBtn.innerHTML = selectedAnswer; // Revert
        alert('Failed to submit answer. Please try again.');
        allOptions.forEach(btn => btn.disabled = false);
    }
}

function showFeedback(isCorrect, selectedBtn, allOptions) {
    dom.feedbackContainer.className = `feedback-toast ${isCorrect ? 'success' : 'error'}`;
    dom.feedbackText.textContent = isCorrect ? 'Correct! Well done.' : 'Incorrect.';
    document.getElementById('feedback-icon').innerHTML = isCorrect ? icons.check : icons.x;
    
    selectedBtn.classList.add(isCorrect ? 'correct' : 'incorrect');
    selectedBtn.innerHTML = selectedBtn.textContent.replace('Submitting...', ''); // wipe out submitting text
    
    if (!isCorrect) {
        allOptions.forEach(btn => {
            if (btn !== selectedBtn) btn.classList.add('incorrect-dim');
        });
    }
}

async function showResults() {
    switchView('results');
    
    const finalScoreDisplay = sessionData.ability.toFixed(2);
    dom.finalScore.textContent = finalScoreDisplay;
    dom.scoreCircle.style.setProperty('--score-pct', Math.max(5, sessionData.ability * 100));
    
    dom.loadingPulse.classList.remove('hidden');
    dom.studyPlanContent.classList.add('hidden');
    
    try {
        const res = await fetch(`${API_BASE_URL}/study-plan/${sessionData.id}`);
        const data = await res.json();
        
        dom.loadingPulse.classList.add('hidden');
        renderStudyPlan(data.study_plan);
        dom.studyPlanContent.classList.remove('hidden');
        
    } catch (err) {
        console.error('Failed to get study plan:', err);
        dom.loadingPulse.classList.add('hidden');
        dom.studyPlanContent.innerHTML = '<p style="color:var(--error)">Failed to generate study plan. You might have run out of API quota, or the backend encountered an error.</p>';
        dom.studyPlanContent.classList.remove('hidden');
    }
}

// Simple markdown formatter
function renderStudyPlan(markdownText) {
    if (!markdownText) {
        dom.studyPlanContent.innerHTML = 'No study plan generated.';
        return;
    }
    
    let html = markdownText
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
        // Replace bold numbered items mimicking list items
        .replace(/^\d+\.\s+(.*$)/gim, '<p><strong>$1</strong></p>')
        .replace(/^- (.*$)/gim, '<ul><li>$1</li></ul>')
        .replace(/<\/ul>\n<ul>/gim, '')
        .replace(/\n\n/gim, '<br>');
        
    dom.studyPlanContent.innerHTML = html;
}

function resetApp() {
    switchView('welcome');
    dom.studyPlanContent.innerHTML = '';
}
