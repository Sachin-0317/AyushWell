let currentQuestionIndex = 0;
let assessmentAnswers = [];
let hasAssessment = false;

const questions = [
    { question: "What is your body build (physique)?", options: [{ text: "Thin, bony, light frame", dosha: "vata" }, { text: "Medium, muscular, athletic", dosha: "pitta" }, { text: "Large, broad, heavy frame", dosha: "kapha" }] },
    { question: "How is your weight?", options: [{ text: "Low, hard to gain weight", dosha: "vata" }, { text: "Moderate, easy to gain/lose", dosha: "pitta" }, { text: "Heavy, gain easily, lose hard", dosha: "kapha" }] },
    { question: "What is your skin texture?", options: [{ text: "Dry, rough, cool, thin", dosha: "vata" }, { text: "Warm, oily, sensitive, reddish", dosha: "pitta" }, { text: "Thick, smooth, cool, moist", dosha: "kapha" }] },
    { question: "How is your hair?", options: [{ text: "Dry, brittle, frizzy, scarce", dosha: "vata" }, { text: "Fine, soft, early graying/balding", dosha: "pitta" }, { text: "Thick, lustrous, wavy, oily", dosha: "kapha" }] },
    { question: "What are your eyes like?", options: [{ text: "Small, active, dry, darting", dosha: "vata" }, { text: "Medium, penetrating, light sensitivity", dosha: "pitta" }, { text: "Large, lovely, calm, white sclera", dosha: "kapha" }] },
    { question: "How are your teeth?", options: [{ text: "Irregular, protruding, gums recede", dosha: "vata" }, { text: "Medium, yellowish, gums bleed", dosha: "pitta" }, { text: "Large, white, strong, healthy gums", dosha: "kapha" }] },
    { question: "How are your nails?", options: [{ text: "Dry, rough, brittle, break easily", dosha: "vata" }, { text: "Pink, soft, medium strength", dosha: "pitta" }, { text: "Thick, strong, smooth, white", dosha: "kapha" }] },
    { question: "What is your joint health?", options: [{ text: "Prominent, potential popping/cracking", dosha: "vata" }, { text: "Medium, flexible", dosha: "pitta" }, { text: "Large, sturdy, well-padded", dosha: "kapha" }] },
    { question: "How is your appetite?", options: [{ text: "Irregular, sometimes hungry sometimes not", dosha: "vata" }, { text: "Strong, unbearable if meal skipped", dosha: "pitta" }, { text: "Steady, low but constant", dosha: "kapha" }] },
    { question: "How is your digestion?", options: [{ text: "Gas, bloating, constipation", dosha: "vata" }, { text: "Quick, heartburn, acidity", dosha: "pitta" }, { text: "Slow, heavy after meals", dosha: "kapha" }] },
    { question: "What are your taste preferences?", options: [{ text: "Sweet, sour, salty", dosha: "vata" }, { text: "Sweet, bitter, astringent", dosha: "pitta" }, { text: "Pungent, bitter, astringent", dosha: "kapha" }] },
    { question: "How is your thirst?", options: [{ text: "Variable", dosha: "vata" }, { text: "Excessive, thirsty often", dosha: "pitta" }, { text: "Low, rarely thirsty", dosha: "kapha" }] },
    { question: "How are your bowel movements?", options: [{ text: "Dry, hard, constipated, irregular", dosha: "vata" }, { text: "Soft, loose, frequent", dosha: "pitta" }, { text: "Heavy, slow, reliable", dosha: "kapha" }] },
    { question: "How do you react to temperature?", options: [{ text: "Dislike cold, love warmth", dosha: "vata" }, { text: "Dislike heat, love cool", dosha: "pitta" }, { text: "Dislike damp/cool, love warm/dry", dosha: "kapha" }] },
    { question: "How is your body temperature?", options: [{ text: "Cold hands and feet", dosha: "vata" }, { text: "Warm throughout body", dosha: "pitta" }, { text: "Cool but comfortable", dosha: "kapha" }] },
    { question: "How much do you sweat?", options: [{ text: "Scanty, minimal odor", dosha: "vata" }, { text: "Profuse, strong odor", dosha: "pitta" }, { text: "Moderate, pleasant/neutral smell", dosha: "kapha" }] },
    { question: "What is your energy level?", options: [{ text: "Bursts of energy, then exhaustion", dosha: "vata" }, { text: "Moderate, intense, focused", dosha: "pitta" }, { text: "Steady, high endurance, slow to start", dosha: "kapha" }] },
    { question: "How is your sleep?", options: [{ text: "Light, interrupted, dreams often", dosha: "vata" }, { text: "Moderate, sound, can go back to sleep", dosha: "pitta" }, { text: "Deep, heavy, hard to wake up", dosha: "kapha" }] },
    { question: "What is your walking pace?", options: [{ text: "Fast, irregular", dosha: "vata" }, { text: "Medium, determined walk", dosha: "pitta" }, { text: "Slow, steady glide", dosha: "kapha" }] },
    { question: "How do you work?", options: [{ text: "Creative, multitasker, start many things", dosha: "vata" }, { text: "Organized, plotted, efficient", dosha: "pitta" }, { text: "Methodical, consistent, supportive", dosha: "kapha" }] },
    { question: "How is your mind?", options: [{ text: "Restless, active, imaginative", dosha: "vata" }, { text: "Sharp, intellectual, critical", dosha: "pitta" }, { text: "Calm, steady, slow", dosha: "kapha" }] },
    { question: "How is your memory?", options: [{ text: "Learn quickly, forget quickly", dosha: "vata" }, { text: "Sharp, clear, distinct", dosha: "pitta" }, { text: "Learn slowly, remember forever", dosha: "kapha" }] },
    { question: "How do you handle stress?", options: [{ text: "Anxiety, worry, fear", dosha: "vata" }, { text: "Irritability, anger, frustration", dosha: "pitta" }, { text: "Withdrawal, depression, eating", dosha: "kapha" }] },
    { question: "What is your speaking style?", options: [{ text: "Fast, talkative, changes topics", dosha: "vata" }, { text: "Sharp, clear, precise, convincing", dosha: "pitta" }, { text: "Slow, melodious, listens well", dosha: "kapha" }] },
    { question: "How are your finances?", options: [{ text: "Spend impulsively on small things", dosha: "vata" }, { text: "Spend on luxury/status items", dosha: "pitta" }, { text: "Save money, spend cautiously", dosha: "kapha" }] },
    { question: "How are your dreams?", options: [{ text: "Flying, running, fear, active", dosha: "vata" }, { text: "Fire, fighting, problem solving", dosha: "pitta" }, { text: "Water, romance, nature, slow", dosha: "kapha" }] },
    { question: "How are your friendships?", options: [{ text: "Many casual friends, short-term", dosha: "vata" }, { text: "Few close friends, work-related", dosha: "pitta" }, { text: "Long-lasting, deep, loyal", dosha: "kapha" }] },
    { question: "What is your decision-making style?", options: [{ text: "Indecisive, change mind often", dosha: "vata" }, { text: "Decisive, leader-like", dosha: "pitta" }, { text: "Slow, consults others", dosha: "kapha" }] },
    { question: "How do you react to conflict?", options: [{ text: "Run away, avoid it", dosha: "vata" }, { text: "Argue, try to win", dosha: "pitta" }, { text: "Peacemaker, or silent treatment", dosha: "kapha" }] },
    { question: "What is your pulse type?", options: [{ text: "Thready, fast, snake-like", dosha: "vata" }, { text: "Bounding, jumping, frog-like", dosha: "pitta" }, { text: "Slow, broad, swan-like", dosha: "kapha" }] },
    { question: "How is your sexual drive?", options: [{ text: "Variable, fantasy-based", dosha: "vata" }, { text: "Moderate, passionate", dosha: "pitta" }, { text: "Steady, devoted", dosha: "kapha" }] },
    { question: "Which weather do you prefer?", options: [{ text: "Warm and humid", dosha: "vata" }, { text: "Cool and dry", dosha: "pitta" }, { text: "Warm and dry", dosha: "kapha" }] },
    { question: "How do you walk?", options: [{ text: "Quickly, light steps", dosha: "vata" }, { text: "Purposefully, medium pace", dosha: "pitta" }, { text: "Slowly, heavy steps", dosha: "kapha" }] },
    { question: "What motivates you?", options: [{ text: "Novelty and freedom", dosha: "vata" }, { text: "Achievement and goals", dosha: "pitta" }, { text: "Stability and security", dosha: "kapha" }] },
    { question: "How is your stamina?", options: [{ text: "Low, tire easily", dosha: "vata" }, { text: "Moderate", dosha: "pitta" }, { text: "High, excellent stamina", dosha: "kapha" }] },
    { question: "How do you start your day?", options: [{ text: "Hard to get going, need coffee", dosha: "vata" }, { text: "Jump out of bed, plan day", dosha: "pitta" }, { text: "Slow to wake, need time", dosha: "kapha" }] },
    { question: "How sensitive are you?", options: [{ text: "Very sensitive to noise/environment", dosha: "vata" }, { text: "Sensitive to light/heat", dosha: "pitta" }, { text: "Not very sensitive, tolerant", dosha: "kapha" }] },
    { question: "How often do you change interests?", options: [{ text: "Very often", dosha: "vata" }, { text: "Sometimes, if better option arises", dosha: "pitta" }, { text: "Rarely, stick to what I know", dosha: "kapha" }] },
    { question: "How is your mood generally?", options: [{ text: "Changes hourly/daily", dosha: "vata" }, { text: "Generally intense", dosha: "pitta" }, { text: "Generally happy/content", dosha: "kapha" }] },
    { question: "What is your main challenge?", options: [{ text: "Fear and anxiety", dosha: "vata" }, { text: "Anger and control", dosha: "pitta" }, { text: "Inertia and attachment", dosha: "kapha" }] }
];

// Get active questions (translated or default)
function getActiveQuestions() {
    if (typeof getQuestions === 'function') {
        const translated = getQuestions();
        if (translated) return translated;
    }
    return questions;
}

function renderQuestion() {
    const activeQuestions = getActiveQuestions();
    const q = activeQuestions[currentQuestionIndex];
    const total = activeQuestions.length;

    const qNumEl = document.getElementById('questionNumber');
    const qTextEl = document.getElementById('questionText');
    const progressEl = document.getElementById('assessmentProgress');
    const container = document.getElementById('optionsContainer');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (!q || !container) return;

    const qLabel = (typeof t === 'function') ? t('questionOf') : 'Question';
    const ofLabel = (typeof t === 'function') ? t('of') : 'of';
    const nextLabel = (typeof t === 'function') ? t('nextQuestion') : 'Next Question';
    const prevLabel = (typeof t === 'function') ? t('previous') : 'Previous';

    if (qNumEl) qNumEl.textContent = `${qLabel} ${currentQuestionIndex + 1} ${ofLabel} ${total}`;
    if (qTextEl) qTextEl.textContent = q.question;
    if (progressEl) progressEl.style.width = `${((currentQuestionIndex + 1) / total) * 100}%`;

    container.innerHTML = q.options.map((opt, i) => `
        <div class="option" onclick="selectOption(${i})">
            <div class="radio-dot"></div>
            <span>${opt.text}</span>
        </div>
    `).join('');

    if (prevBtn) prevBtn.style.display = currentQuestionIndex > 0 ? 'block' : 'none';
    if (prevBtn) prevBtn.textContent = prevLabel;
    if (nextBtn) {
        nextBtn.disabled = true;
        nextBtn.textContent = currentQuestionIndex === total - 1
            ? ((typeof t === 'function') ? t('submitAssessment') : 'Submit')
            : nextLabel;
    }

    if (assessmentAnswers[currentQuestionIndex] !== undefined) {
        const selectedIndex = q.options.findIndex(o => o.dosha === assessmentAnswers[currentQuestionIndex]);
        if (selectedIndex >= 0) {
            const opts = document.querySelectorAll('.option');
            if (opts[selectedIndex]) opts[selectedIndex].classList.add('selected');
            if (nextBtn) nextBtn.disabled = false;
        }
    }
}

function selectOption(index) {
    document.querySelectorAll('.option').forEach(el => el.classList.remove('selected'));
    document.querySelectorAll('.option')[index].classList.add('selected');
    assessmentAnswers[currentQuestionIndex] = getActiveQuestions()[currentQuestionIndex].options[index].dosha;
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) nextBtn.disabled = false;
}

function nextQuestion() {
    const total = getActiveQuestions().length;
    if (currentQuestionIndex < total - 1) {
        currentQuestionIndex++;
        renderQuestion();
    } else {
        submitAssessment();
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderQuestion();
    }
}

async function submitAssessment() {
    if (!currentUser) { alert('Please login first'); return; }
    try {
        const response = await api.submitAssessment(assessmentAnswers);
        const completeMsg = (typeof t === 'function') ? t('assessmentComplete') : 'Assessment Complete!';
        const prakMsg = (typeof t === 'function') ? t('yourPrakriti') : 'Your Prakriti';
        alert(`✨ ${completeMsg}\n\n${prakMsg}: ${response.dominant_dosha.toUpperCase()}\n\nVata: ${response.vata_score} | Pitta: ${response.pitta_score} | Kapha: ${response.kapha_score}`);
        hasAssessment = true;
        await loadRecommendations(response);
        showAssessmentResults(response);
        showPatientView('ai-plan');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function showAssessmentResults(data) {
    const assessmentView = document.getElementById('patientAssessment');
    const retakeLabel = (typeof t === 'function') ? t('retakeAssessment') : 'Retake Assessment';
    const dominantLabel = (typeof t === 'function') ? t('dominantDosha') : 'Your Dominant Dosha';
    assessmentView.innerHTML = `
        <div class="card">
            <div class="card-header"><div>
                <h2 class="card-title">${(typeof t === 'function') ? t('yourPrakriti') : 'Your Prakriti'} Results</h2>
                <p class="card-subtitle">Completed on ${new Date().toLocaleDateString()}</p>
            </div></div>
            <div class="ai-container" style="margin-top: 24px;">
                <div style="text-align: center; margin-bottom: 32px;">
                    <div style="font-size: 64px; margin-bottom: 16px;">✨</div>
                    <h2 style="font-size: 36px; font-weight: 800; color: var(--accent-primary); margin: 0;">${data.dominant_dosha.toUpperCase()}</h2>
                    <p style="margin: 16px 0 0; font-size: 18px; color: var(--text-secondary);">${dominantLabel}</p>
                </div>
                <div class="grid-3" style="margin-bottom: 32px;">
                    <div class="card" style="text-align: center;"><h3 style="color: var(--accent-primary); margin: 0 0 8px;">Vata</h3><p style="font-size: 32px; font-weight: 700; margin: 0;">${data.vata_score}</p></div>
                    <div class="card" style="text-align: center;"><h3 style="color: var(--accent-primary); margin: 0 0 8px;">Pitta</h3><p style="font-size: 32px; font-weight: 700; margin: 0;">${data.pitta_score}</p></div>
                    <div class="card" style="text-align: center;"><h3 style="color: var(--accent-primary); margin: 0 0 8px;">Kapha</h3><p style="font-size: 32px; font-weight: 700; margin: 0;">${data.kapha_score}</p></div>
                </div>
                <div style="text-align: center;">
                    <button class="btn-primary" onclick="retakeAssessment()" style="width: auto; padding: 14px 32px;">${retakeLabel}</button>
                </div>
            </div>
        </div>`;
}

function retakeAssessment() {
    hasAssessment = false;
    currentQuestionIndex = 0;
    assessmentAnswers = [];
    const assessmentView = document.getElementById('patientAssessment');
    const nextLabel = (typeof t === 'function') ? t('nextQuestion') : 'Next Question';
    const prevLabel = (typeof t === 'function') ? t('previous') : 'Previous';
    assessmentView.innerHTML = `
        <div class="progress-bar"><div id="assessmentProgress" class="progress-fill" style="width: 10%"></div></div>
        <div class="question-card">
            <div id="questionNumber" class="question-number">Question 1 of ${getActiveQuestions().length}</div>
            <h2 id="questionText" class="question-text"></h2>
            <div id="optionsContainer"></div>
        </div>
        <div style="display: flex; gap: 12px;">
            <button id="prevBtn" class="btn-secondary" style="flex: 1; display: none;" onclick="previousQuestion()">${prevLabel}</button>
            <button id="nextBtn" class="btn-primary" style="flex: 2;" onclick="nextQuestion()" disabled>${nextLabel}</button>
        </div>`;
    renderQuestion();
}

async function loadRecommendations(assessmentData) {
    const rec = assessmentData.recommendations;
    const aiPlanContainer = document.querySelector('#patientAIPlan .ai-container');
    if (aiPlanContainer) {
        aiPlanContainer.innerHTML = `
            <div class="ai-header">
                <div class="ai-badge"><span>✨</span><span>AI-Powered</span></div>
                <h2 class="ai-title">Your ${assessmentData.dominant_dosha.toUpperCase()} Wellness Plan</h2>
            </div>
            <p style="color: var(--text-secondary); margin: 0 0 24px;">Personalized recommendations based on your Prakriti assessment</p>
            <div class="recommendation-card">
                <div class="rec-header">
                    <div class="rec-icon">🥗</div>
                    <div class="rec-content">
                        <h3 class="rec-title">Your Diet Plan</h3>
                        <p class="rec-desc">${rec.diet.meal_timing}</p>
                        <div class="tag-container" style="margin-top: 12px;">
                            ${rec.diet.foods_to_favor.slice(0, 3).map(f => `<span class="tag">✅ ${f}</span>`).join('')}
                        </div>
                    </div>
                </div>
                <button class="btn-primary" onclick="showPatientView('diet')" style="margin-top: 16px; width: auto; padding: 12px 24px;">View Full Diet Plan</button>
            </div>
            <div class="recommendation-card">
                <div class="rec-header">
                    <div class="rec-icon">🧘</div>
                    <div class="rec-content">
                        <h3 class="rec-title">Your Yoga Plan</h3>
                        <p class="rec-desc">${rec.yoga.focus} • ${rec.yoga.duration} • ${rec.yoga.frequency}</p>
                        <div class="tag-container" style="margin-top: 12px;">
                            ${rec.yoga.poses.slice(0, 3).map(p => `<span class="tag">🧘 ${p}</span>`).join('')}
                        </div>
                    </div>
                </div>
                <button class="btn-primary" onclick="showPatientView('yoga')" style="margin-top: 16px; width: auto; padding: 12px 24px;">View Full Yoga Plan</button>
            </div>
            <div class="recommendation-card">
                <div class="rec-header">
                    <div class="rec-icon">✨</div>
                    <div class="rec-content">
                        <h3 class="rec-title">Lifestyle Tips</h3>
                        ${rec.lifestyle.slice(0, 3).map(tip => `<p style="margin: 8px 0; font-size: 14px; color: var(--text-secondary);">• ${tip}</p>`).join('')}
                    </div>
                </div>
            </div>`;
    }
    updateDietPage(rec.diet);
    updateYogaPage(rec.yoga);
}

function updateDietPage(diet) {
    const dietContent = document.getElementById('patientDiet');
    if (dietContent) {
        dietContent.innerHTML = `
            <div class="card">
                <div class="card-header"><div>
                    <h2 class="card-title">Your Personalized Diet Plan</h2>
                    <p class="card-subtitle">${diet.meal_timing}</p>
                </div></div>
                <div class="grid-2" style="margin-top: 24px;">
                    <div class="recommendation-card">
                        <h3 style="color: var(--accent-tertiary); margin: 0 0 16px; font-size: 20px;">✅ Foods to Favor</h3>
                        ${diet.foods_to_favor.map(f => `<p style="margin: 12px 0; font-size: 15px; padding: 8px; background: var(--bg-secondary); border-radius: 8px;">• ${f}</p>`).join('')}
                    </div>
                    <div class="recommendation-card">
                        <h3 style="color: #ef4444; margin: 0 0 16px; font-size: 20px;">❌ Foods to Avoid</h3>
                        ${diet.foods_to_avoid.map(f => `<p style="margin: 12px 0; font-size: 15px; padding: 8px; background: var(--bg-secondary); border-radius: 8px;">• ${f}</p>`).join('')}
                    </div>
                </div>
                <div class="card" style="margin-top: 24px; background: rgba(20, 184, 166, 0.05);">
                    <h3 style="margin: 0 0 16px; font-size: 18px;">💡 Meal Timing Tips</h3>
                    <p style="margin: 0; font-size: 15px; line-height: 1.6;">${diet.meal_timing}</p>
                </div>
            </div>`;
    }
}

function updateYogaPage(yoga) {
    const yogaContent = document.getElementById('patientYoga');
    if (yogaContent) {
        yogaContent.innerHTML = `
            <div class="card">
                <div class="card-header"><div>
                    <h2 class="card-title">Your Personalized Yoga Plan</h2>
                    <p class="card-subtitle">${yoga.focus} • ${yoga.duration} • ${yoga.frequency}</p>
                </div></div>
                <div style="margin-top: 24px;">
                    <h3 style="margin: 0 0 20px; font-size: 20px;">🧘 Recommended Poses</h3>
                    <div class="grid-3">
                        ${yoga.poses.map(pose => `
                            <div class="recommendation-card" style="text-align: center;">
                                <div class="rec-icon" style="margin: 0 auto 12px;">🧘</div>
                                <h4 style="margin: 0; font-size: 16px; font-weight: 700;">${pose}</h4>
                            </div>`).join('')}
                    </div>
                </div>
                <div class="card" style="margin-top: 32px; background: rgba(20, 184, 166, 0.05);">
                    <h3 style="margin: 0 0 12px; font-size: 18px;">⏰ Practice Schedule</h3>
                    <p style="margin: 0 0 8px; font-size: 15px;"><strong>Duration:</strong> ${yoga.duration}</p>
                    <p style="margin: 0 0 8px; font-size: 15px;"><strong>Frequency:</strong> ${yoga.frequency}</p>
                    <p style="margin: 0; font-size: 15px;"><strong>Focus:</strong> ${yoga.focus}</p>
                </div>
            </div>`;
    }
}

async function loadExistingAssessment() {
    if (!currentUser) return;
    try {
        const data = await api.getAssessment();
        if (data.recommendations && data.recommendations.diet) {
            hasAssessment = true;
            await loadRecommendations({ dominant_dosha: data.dominant_dosha, vata_score: data.vata_score, pitta_score: data.pitta_score, kapha_score: data.kapha_score, recommendations: data.recommendations });
            showAssessmentResults(data);
        }
    } catch (error) { console.log('No existing assessment'); }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('patientAssessment') && !hasAssessment) {
        renderQuestion();
    }
});
