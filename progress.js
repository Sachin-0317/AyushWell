let progressChart = null;

async function initProgressPage() {
    await loadProgressData();
    renderProgressForm();
}

function renderProgressForm() {
    const progressPage = document.getElementById('patientProgress');
    
    const formHTML = `
        <div class="card" style="margin-bottom: 24px;">
            <h3 class="card-title" style="margin-bottom: 20px;">📝 Log Today's Progress</h3>
            <div class="grid-2" style="gap: 16px;">
                <div class="form-group">
                    <label class="form-label">Calories Consumed</label>
                    <input type="number" id="caloriesInput" class="form-input" placeholder="e.g., 1800" min="0">
                </div>
                <div class="form-group">
                    <label class="form-label">Activity Minutes</label>
                    <input type="number" id="activityInput" class="form-input" placeholder="e.g., 45" min="0">
                </div>
                <div class="form-group">
                    <label class="form-label">Water (cups)</label>
                    <input type="number" id="waterInput" class="form-input" placeholder="e.g., 8" min="0" max="20">
                </div>
                <div class="form-group">
                    <label class="form-label">Sleep (hours)</label>
                    <input type="number" id="sleepInput" class="form-input" placeholder="e.g., 7.5" min="0" max="24" step="0.5">
                </div>
                <div class="form-group">
                    <label class="form-label">Weight (kg) - Optional</label>
                    <input type="number" id="weightInput" class="form-input" placeholder="e.g., 65.5" step="0.1">
                </div>
                <div class="form-group">
                    <label class="form-label">Stress Level (1-10)</label>
                    <input type="range" id="stressInput" class="form-input" min="1" max="10" value="5" style="padding: 8px;">
                    <span id="stressValue" style="font-size: 14px; color: var(--text-secondary); margin-top: 4px; display: block;">5 - Moderate</span>
                </div>
            </div>
            <div class="form-group" style="margin-top: 16px;">
                <label class="form-label">Notes (Optional)</label>
                <textarea id="notesInput" class="form-input" rows="2" placeholder="How are you feeling today? Any observations..."></textarea>
            </div>
            <button class="btn-primary" onclick="saveProgressData()" style="width: 100%; margin-top: 16px;">Save Today's Progress</button>
        </div>
    `;
    
    const existingContent = progressPage.innerHTML;
    progressPage.innerHTML = formHTML + existingContent;
    
    document.getElementById('stressInput').addEventListener('input', (e) => {
        const value = e.target.value;
        const labels = ['', 'Very Low', 'Low', 'Low-Moderate', 'Moderate', 'Moderate', 'Moderate-High', 'High', 'High', 'Very High', 'Extreme'];
        document.getElementById('stressValue').textContent = `${value} - ${labels[value]}`;
    });
    
    loadTodayProgress();
}

async function loadTodayProgress() {
    try {
        const data = await api.getProgress(1);
        if (data && data.length > 0) {
            const today = data[0];
            document.getElementById('caloriesInput').value = today.calories || '';
            document.getElementById('activityInput').value = today.activity_minutes || '';
            document.getElementById('waterInput').value = Math.round(today.water_ml / 250) || '';
            document.getElementById('sleepInput').value = today.sleep_hours || '';
            document.getElementById('weightInput').value = today.weight_kg || '';
            document.getElementById('stressInput').value = today.stress_level || 5;
            document.getElementById('notesInput').value = today.notes || '';
            
            const stressLabels = ['', 'Very Low', 'Low', 'Low-Moderate', 'Moderate', 'Moderate', 'Moderate-High', 'High', 'High', 'Very High', 'Extreme'];
            document.getElementById('stressValue').textContent = `${today.stress_level || 5} - ${stressLabels[today.stress_level || 5]}`;
        }
    } catch (error) {
        console.log('No data for today yet');
    }
}

async function saveProgressData() {
    const progressData = {
        calories: parseInt(document.getElementById('caloriesInput').value) || 0,
        activity_minutes: parseInt(document.getElementById('activityInput').value) || 0,
        water_ml: (parseInt(document.getElementById('waterInput').value) || 0) * 250,
        sleep_hours: parseFloat(document.getElementById('sleepInput').value) || 0,
        weight_kg: parseFloat(document.getElementById('weightInput').value) || null,
        stress_level: parseInt(document.getElementById('stressInput').value) || 5,
        notes: document.getElementById('notesInput').value || null
    };
    
    try {
        await api.addProgress(progressData);
        alert('✅ Progress saved successfully!');
        await loadProgressData();
    } catch (error) {
        console.error('Progress save error:', error);
        alert('❌ Failed to save progress: ' + error.message);
    }
}

async function loadProgressData(days = 30) {
    try {
        const data = await api.getProgress(days);
        updateStatCards(data);
        renderProgressCharts(data);
        renderProgressTable(data);
    } catch (error) {
        console.error('Progress load error:', error);
        alert('Failed to load progress data');
    }
}

function updateStatCards(data) {
    if (!data || data.length === 0) return;
    
    const latest = data[data.length - 1];
    const previous = data.length > 1 ? data[data.length - 2] : null;
    
    const calorieChange = previous ? ((latest.calories - previous.calories) / previous.calories * 100).toFixed(0) : 0;
    const activityChange = previous ? ((latest.activity_minutes - previous.activity_minutes) / previous.activity_minutes * 100).toFixed(0) : 0;
    
    const statsHTML = `
        <div class="grid-4">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: var(--text-secondary);">Calories</span>
                    <span style="font-size: 20px;">🍽️</span>
                </div>
                <h2 style="font-size: 32px; font-weight: 700; margin: 0;">${latest.calories.toLocaleString()}</h2>
                <p style="margin: 8px 0 0; font-size: 13px; color: ${calorieChange >= 0 ? 'var(--accent-tertiary)' : '#ef4444'}; font-weight: 600;">
                    ${calorieChange >= 0 ? '↑' : '↓'} ${Math.abs(calorieChange)}% from yesterday
                </p>
            </div>
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: var(--text-secondary);">Activity</span>
                    <span style="font-size: 20px;">🏃</span>
                </div>
                <h2 style="font-size: 32px; font-weight: 700; margin: 0;">${latest.activity_minutes} min</h2>
                <p style="margin: 8px 0 0; font-size: 13px; color: ${activityChange >= 0 ? 'var(--accent-tertiary)' : '#ef4444'}; font-weight: 600;">
                    ${activityChange >= 0 ? '↑' : '↓'} ${Math.abs(activityChange)}% from yesterday
                </p>
            </div>
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: var(--text-secondary);">Water</span>
                    <span style="font-size: 20px;">💧</span>
                </div>
                <h2 style="font-size: 32px; font-weight: 700; margin: 0;">${Math.round(latest.water_ml / 250)} cups</h2>
                <p style="margin: 8px 0 0; font-size: 13px; color: var(--text-secondary);">Goal: 8 cups daily</p>
            </div>
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 14px; font-weight: 600; color: var(--text-secondary);">Sleep</span>
                    <span style="font-size: 20px;">😴</span>
                </div>
                <h2 style="font-size: 32px; font-weight: 700; margin: 0;">${latest.sleep_hours} hrs</h2>
                <p style="margin: 8px 0 0; font-size: 13px; color: ${latest.sleep_hours >= 7 ? 'var(--accent-tertiary)' : '#ef4444'}; font-weight: 600;">
                    ${latest.sleep_hours >= 7 ? 'Excellent!' : 'Aim for 7-8 hours'}
                </p>
            </div>
        </div>
    `;
    
    const existingStats = document.querySelector('#patientProgress .grid-4');
    if (existingStats) {
        existingStats.outerHTML = statsHTML;
    }
}

function renderProgressCharts(data) {
    if (!data || data.length === 0) {
        document.querySelector('.chart-container .chart-placeholder').innerHTML = 
            '<p style="text-align: center; color: var(--text-secondary);">No data yet. Start logging your progress!</p>';
        return;
    }
    
    const dates = data.map(d => new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    const activity = data.map(d => d.activity_minutes);
    
    const chartContainer = document.querySelector('.chart-container .chart-placeholder');
    chartContainer.innerHTML = '<canvas id="progressChart" style="max-height: 280px;"></canvas>';
    
    const ctx = document.getElementById('progressChart').getContext('2d');
    const canvas = document.getElementById('progressChart');
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = 280;
    
    ctx.clearRect(0, 0, width, height);
    
    const barWidth = width / dates.length;
    const maxActivity = Math.max(...activity, 60);
    
    activity.forEach((val, i) => {
        const barHeight = (val / maxActivity) * (height - 40);
        ctx.fillStyle = 'rgba(20, 184, 166, 0.6)';
        ctx.fillRect(i * barWidth + barWidth * 0.2, height - barHeight - 20, barWidth * 0.6, barHeight);
    });
    
    ctx.fillStyle = 'var(--text-secondary)';
    ctx.font = '11px Inter';
    ctx.textAlign = 'center';
    dates.forEach((date, i) => {
        if (i % Math.ceil(dates.length / 8) === 0) {
            ctx.fillText(date, i * barWidth + barWidth / 2, height - 5);
        }
    });
    
    ctx.fillStyle = 'var(--text-primary)';
    ctx.font = 'bold 14px Inter';
    ctx.textAlign = 'left';
    ctx.fillText('Activity Minutes', 10, 20);
}

function renderProgressTable(data) {
    if (!data || data.length === 0) return;
    
    const tableHTML = `
        <div class="card" style="margin-top: 24px;">
            <h3 class="card-title" style="margin-bottom: 20px;">📋 Progress History</h3>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--border-color);">
                            <th style="padding: 12px; text-align: left; font-size: 14px; color: var(--text-secondary);">Date</th>
                            <th style="padding: 12px; text-align: center; font-size: 14px; color: var(--text-secondary);">Calories</th>
                            <th style="padding: 12px; text-align: center; font-size: 14px; color: var(--text-secondary);">Activity</th>
                            <th style="padding: 12px; text-align: center; font-size: 14px; color: var(--text-secondary);">Water</th>
                            <th style="padding: 12px; text-align: center; font-size: 14px; color: var(--text-secondary);">Sleep</th>
                            <th style="padding: 12px; text-align: center; font-size: 14px; color: var(--text-secondary);">Stress</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.slice().reverse().slice(0, 14).map(d => `
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 12px; font-size: 14px;">${new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</td>
                                <td style="padding: 12px; text-align: center; font-size: 14px;">${d.calories}</td>
                                <td style="padding: 12px; text-align: center; font-size: 14px;">${d.activity_minutes} min</td>
                                <td style="padding: 12px; text-align: center; font-size: 14px;">${Math.round(d.water_ml / 250)} cups</td>
                                <td style="padding: 12px; text-align: center; font-size: 14px;">${d.sleep_hours} hrs</td>
                                <td style="padding: 12px; text-align: center; font-size: 14px;">${d.stress_level}/10</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            ${data.length > 14 ? `<p style="margin: 16px 0 0; font-size: 14px; color: var(--text-secondary); text-align: center;">Showing last 14 days</p>` : ''}
        </div>
    `;
    
    const chartContainer = document.querySelector('.chart-container');
    const existingTable = document.querySelector('#patientProgress .card:last-child table');
    
    if (existingTable) {
        existingTable.closest('.card').outerHTML = tableHTML;
    } else {
        chartContainer.insertAdjacentHTML('afterend', tableHTML);
    }
}

const originalShowPatientView = window.showPatientView;
window.showPatientView = function(view) {
    originalShowPatientView(view);
    if (view === 'progress') {
        setTimeout(() => {
            if (!document.getElementById('caloriesInput')) {
                initProgressPage();
            }
        }, 100);
    }
};