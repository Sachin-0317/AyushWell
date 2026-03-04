async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await api.login({ email, password, role: currentRole });
        currentUser = response.user;
        document.getElementById('patientWelcome').textContent = `Welcome, ${response.user.name} 👋`;
        proceedToApp();
    } catch (error) {
        showError('loginEmailError', error.message || 'Invalid credentials');
    }
}

async function handleRegister(event) {
    event.preventDefault();

    const name = document.getElementById('registerName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const phone = document.getElementById('registerPhone').value.trim();
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;

    if (!validateEmail(email)) {
        showError('registerEmailError', 'Please enter a valid email address');
        return;
    }

    if (password !== confirmPassword) {
        showError('passwordMatchError', 'Passwords do not match');
        return;
    }

    try {
        await api.register({ name, email, phone, password, role: currentRole });
        alert('Registration successful! Please login.');
        switchAuthMode('login');
        document.getElementById('loginEmail').value = email;
    } catch (error) {
        showError('registerEmailError', error.message || 'Registration failed');
    }
}

async function logout() {
    try {
        await api.logout();
    } catch (error) {
        console.error('Logout error:', error);
    }

    currentUser = null;
    document.getElementById('patientApp').classList.add('hidden');
    document.getElementById('doctorApp').classList.add('hidden');
    document.getElementById('authPage').classList.remove('hidden');
}