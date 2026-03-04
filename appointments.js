// ==================== AYUSHWELL+ APPOINTMENT BOOKING SYSTEM ====================

const DOCTORS = [
    {
        id: 1,
        name: "Dr. Priya Sharma",
        specialization: "Ayurvedic Physician & Panchakarma",
        experience: 12,
        rating: 4.9,
        avatar: "👩‍⚕️",
        slots: ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"]
    },
    {
        id: 2,
        name: "Dr. Rajesh Iyer",
        specialization: "Vata & Nervous System Specialist",
        experience: 15,
        rating: 4.8,
        avatar: "👨‍⚕️",
        slots: ["10:00 AM", "11:30 AM", "02:30 PM", "04:00 PM", "05:00 PM"]
    },
    {
        id: 3,
        name: "Dr. Lakshmi Nair",
        specialization: "Pitta & Digestive Health Expert",
        experience: 10,
        rating: 4.7,
        avatar: "👩‍⚕️",
        slots: ["09:30 AM", "11:00 AM", "01:00 PM", "03:30 PM", "05:30 PM"]
    },
    {
        id: 4,
        name: "Dr. Arjun Menon",
        specialization: "Kapha & Respiratory Specialist",
        experience: 18,
        rating: 5.0,
        avatar: "👨‍⚕️",
        slots: ["08:00 AM", "09:00 AM", "10:30 AM", "02:00 PM", "04:30 PM"]
    },
    {
        id: 5,
        name: "Dr. Meera Krishnan",
        specialization: "Women's Health & Skin",
        experience: 9,
        rating: 4.9,
        avatar: "👩‍⚕️",
        slots: ["10:00 AM", "11:00 AM", "01:30 PM", "03:00 PM", "05:00 PM"]
    }
];

// In-memory appointment storage (persists during session)
let appointments = JSON.parse(localStorage.getItem('ayushAppointments') || '[]');

function saveAppointments() {
    localStorage.setItem('ayushAppointments', JSON.stringify(appointments));
}

function getMinDate() {
    const today = new Date();
    today.setDate(today.getDate() + 1);
    return today.toISOString().split('T')[0];
}

function getMaxDate() {
    const d = new Date();
    d.setDate(d.getDate() + 30);
    return d.toISOString().split('T')[0];
}

function isSlotBooked(doctorId, date, slot) {
    return appointments.some(a =>
        a.doctorId === doctorId && a.date === date && a.slot === slot && a.status !== 'cancelled'
    );
}

function renderConsultPage() {
    const container = document.getElementById('patientConsult');
    if (!container) return;

    container.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
            <!-- Booking Card -->
            <div style="grid-column: 1 / -1;">
                <div class="card">
                    <div class="card-header">
                        <div>
                            <h2 class="card-title">📅 ${t('bookAppointment')}</h2>
                            <p class="card-subtitle">${t('chooseDoctor')}</p>
                        </div>
                    </div>

                    <!-- Step 1: Choose Doctor -->
                    <div style="margin-bottom: 24px;">
                        <label class="form-label">${t('selectDoctor')}</label>
                        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; margin-top: 12px;">
                            ${DOCTORS.map(doc => `
                                <div class="doctor-card" id="doc-${doc.id}" onclick="selectDoctor(${doc.id})"
                                    style="background: var(--bg-secondary); border: 2px solid var(--border-color); border-radius: 12px; padding: 16px; cursor: pointer; transition: all 0.2s;">
                                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                                        <span style="font-size: 28px;">${doc.avatar}</span>
                                        <div>
                                            <p style="margin: 0; font-weight: 700; font-size: 14px; color: var(--text-primary);">${doc.name}</p>
                                            <p style="margin: 0; font-size: 12px; color: var(--accent-primary);">⭐ ${doc.rating}</p>
                                        </div>
                                    </div>
                                    <p style="margin: 0; font-size: 12px; color: var(--text-secondary);">${doc.specialization}</p>
                                    <p style="margin: 4px 0 0; font-size: 12px; color: var(--text-secondary);">${doc.experience} ${t('years')} ${t('experience')}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Step 2: Date + Time -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                        <div>
                            <label class="form-label">📅 ${t('selectDate')}</label>
                            <input type="date" id="appointmentDate" class="form-input"
                                min="${getMinDate()}" max="${getMaxDate()}"
                                onchange="renderTimeSlots()"
                                style="margin-top: 8px;">
                        </div>
                        <div>
                            <label class="form-label">⏰ ${t('selectTime')}</label>
                            <div id="timeSlotsContainer" style="margin-top: 8px; display: flex; flex-wrap: wrap; gap: 8px; min-height: 48px; align-items: center;">
                                <p style="color: var(--text-secondary); font-size: 14px; margin: 0;">${t('selectDoctorFirst')}</p>
                            </div>
                        </div>
                    </div>

                    <button class="btn-primary" onclick="bookAppointment()" style="width: auto; padding: 14px 32px;">
                        ✅ ${t('bookNow')}
                    </button>
                </div>
            </div>

            <!-- Upcoming -->
            <div class="card">
                <h3 class="card-title">🗓️ ${t('upcomingConsultations')}</h3>
                <div id="upcomingList" style="margin-top: 16px;">
                    ${renderUpcomingAppointments()}
                </div>
            </div>

            <!-- Past -->
            <div class="card">
                <h3 class="card-title">📋 ${t('pastConsultations')}</h3>
                <div id="pastList" style="margin-top: 16px;">
                    ${renderPastAppointments()}
                </div>
            </div>
        </div>
    `;
}

let selectedDoctorId = null;
let selectedSlot = null;

function selectDoctor(id) {
    selectedDoctorId = id;
    selectedSlot = null;

    // Update card styles
    document.querySelectorAll('.doctor-card').forEach(card => {
        card.style.borderColor = 'var(--border-color)';
        card.style.background = 'var(--bg-secondary)';
    });
    const selected = document.getElementById(`doc-${id}`);
    if (selected) {
        selected.style.borderColor = 'var(--accent-primary)';
        selected.style.background = 'rgba(20, 184, 166, 0.08)';
    }

    renderTimeSlots();
}

function renderTimeSlots() {
    const container = document.getElementById('timeSlotsContainer');
    if (!container) return;

    if (!selectedDoctorId) {
        container.innerHTML = `<p style="color: var(--text-secondary); font-size: 14px; margin: 0;">${t('selectDoctorFirst')}</p>`;
        return;
    }

    const dateInput = document.getElementById('appointmentDate');
    if (!dateInput || !dateInput.value) {
        container.innerHTML = `<p style="color: var(--text-secondary); font-size: 14px; margin: 0;">${t('selectDateFirst')}</p>`;
        return;
    }

    const doctor = DOCTORS.find(d => d.id === selectedDoctorId);
    const availableSlots = doctor.slots.filter(slot => !isSlotBooked(selectedDoctorId, dateInput.value, slot));

    if (availableSlots.length === 0) {
        container.innerHTML = `<p style="color: #ef4444; font-size: 14px; margin: 0;">⚠️ ${t('noSlotsAvailable')}</p>`;
        return;
    }

    selectedSlot = null;
    container.innerHTML = availableSlots.map(slot => `
        <button onclick="selectSlot(this, '${slot}')"
            style="padding: 8px 14px; background: var(--bg-secondary); border: 2px solid var(--border-color); border-radius: 8px; color: var(--text-primary); font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s;"
            class="time-slot-btn">
            ${slot}
        </button>
    `).join('');
}

function selectSlot(btn, slot) {
    selectedSlot = slot;
    document.querySelectorAll('.time-slot-btn').forEach(b => {
        b.style.borderColor = 'var(--border-color)';
        b.style.background = 'var(--bg-secondary)';
        b.style.color = 'var(--text-primary)';
    });
    btn.style.borderColor = 'var(--accent-primary)';
    btn.style.background = 'var(--accent-primary)';
    btn.style.color = '#ffffff';
}

function bookAppointment() {
    if (!selectedDoctorId) { alert(t('selectDoctorFirst')); return; }
    const dateInput = document.getElementById('appointmentDate');
    if (!dateInput || !dateInput.value) { alert(t('selectDateFirst')); return; }
    if (!selectedSlot) { alert(t('selectTime')); return; }

    const doctor = DOCTORS.find(d => d.id === selectedDoctorId);
    const appt = {
        id: Date.now(),
        doctorId: selectedDoctorId,
        doctorName: doctor.name,
        doctorAvatar: doctor.avatar,
        specialization: doctor.specialization,
        date: dateInput.value,
        slot: selectedSlot,
        status: 'confirmed',
        bookedAt: new Date().toISOString()
    };

    appointments.push(appt);
    saveAppointments();

    alert(`✅ ${t('bookingConfirmed')}\n${t('appointmentWith')} ${doctor.name}\n${t('on')} ${formatDate(dateInput.value)} ${t('at')} ${selectedSlot}`);

    // Reset
    selectedDoctorId = null;
    selectedSlot = null;
    dateInput.value = '';
    renderConsultPage();
}

function cancelAppointment(id) {
    if (!confirm(t('confirmCancel'))) return;

    const idx = appointments.findIndex(a => a.id === id);
    if (idx !== -1) {
        appointments[idx].status = 'cancelled';
        saveAppointments();
        alert(t('bookingCancelled'));
        renderConsultPage();
    }
}

function formatDate(dateStr) {
    const d = new Date(dateStr + 'T00:00:00');
    return d.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
}

function renderUpcomingAppointments() {
    const today = new Date().toISOString().split('T')[0];
    const upcoming = appointments.filter(a => a.date >= today && a.status === 'confirmed')
        .sort((a, b) => a.date.localeCompare(b.date));

    if (upcoming.length === 0) {
        return `<p style="color: var(--text-secondary); font-size: 14px; text-align: center; padding: 20px 0;">${t('noUpcoming')}</p>`;
    }

    return upcoming.map(a => `
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="display: flex; gap: 12px; align-items: center;">
                    <span style="font-size: 28px;">${a.doctorAvatar}</span>
                    <div>
                        <p style="margin: 0; font-weight: 700; font-size: 15px; color: var(--text-primary);">${a.doctorName}</p>
                        <p style="margin: 2px 0; font-size: 13px; color: var(--text-secondary);">${a.specialization}</p>
                        <p style="margin: 4px 0 0; font-size: 13px; color: var(--accent-primary); font-weight: 600;">
                            📅 ${formatDate(a.date)} • ⏰ ${a.slot}
                        </p>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; align-items: flex-end;">
                    <span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">✅ ${t('confirmed')}</span>
                    <button onclick="cancelAppointment(${a.id})"
                        style="background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; padding: 4px 10px; font-size: 12px; font-weight: 600; cursor: pointer;">
                        ❌ ${t('cancelBooking')}
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function renderPastAppointments() {
    const today = new Date().toISOString().split('T')[0];
    const past = appointments.filter(a => a.date < today || a.status === 'cancelled')
        .sort((a, b) => b.date.localeCompare(a.date))
        .slice(0, 5);

    if (past.length === 0) {
        return `<p style="color: var(--text-secondary); font-size: 14px; text-align: center; padding: 20px 0;">${t('noPast')}</p>`;
    }

    return past.map(a => `
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; margin-bottom: 12px; opacity: ${a.status === 'cancelled' ? '0.7' : '1'};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 12px; align-items: center;">
                    <span style="font-size: 28px;">${a.doctorAvatar}</span>
                    <div>
                        <p style="margin: 0; font-weight: 700; font-size: 15px; color: var(--text-primary);">${a.doctorName}</p>
                        <p style="margin: 2px 0 0; font-size: 13px; color: var(--text-secondary);">📅 ${formatDate(a.date)} • ⏰ ${a.slot}</p>
                    </div>
                </div>
                <span style="background: ${a.status === 'cancelled' ? 'rgba(239,68,68,0.1)' : 'rgba(107,114,128,0.1)'}; 
                    color: ${a.status === 'cancelled' ? '#ef4444' : 'var(--text-secondary)'}; 
                    padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">
                    ${a.status === 'cancelled' ? '❌ ' + t('cancelled') : '✓ Completed'}
                </span>
            </div>
        </div>
    `).join('');
}
