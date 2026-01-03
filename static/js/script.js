// Modern JavaScript for CarValue AI

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupFormHandling();
    setupValidation();
    loadSavedData();
    setupAnimations();
    loadTheme();
}

// Theme Management
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Add transition effect
    document.body.style.transition = 'all 0.3s ease';
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

// Form Handling
function setupFormHandling() {
    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        await predictPrice();
    });
}

async function predictPrice() {
    showLoading();
    
    const formData = {
        year: document.getElementById('year').value,
        engine: document.getElementById('engine').value,
        transmission: document.getElementById('transmission').value,
        kms: document.getElementById('kms').value,
        owner: document.getElementById('owner').value,
        fuel: document.getElementById('fuel').value,
        power: document.getElementById('power').value,
        seats: document.getElementById('seats').value,
        mileage: document.getElementById('mileage').value,
        body: document.getElementById('body').value
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResult(result);
            saveToHistory(formData, result);
            showNotification('Price calculated successfully!', 'success');
        } else {
            showNotification(result.error, 'error');
        }
    } catch (error) {
        showNotification('Something went wrong. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

function displayResult(result) {
    // Update price
    const priceDisplay = document.getElementById('priceDisplay');
    priceDisplay.textContent = result.price;
    priceDisplay.classList.add('fade-in');
    
    // Update price range
    const priceRange = document.getElementById('priceRange');
    priceRange.textContent = getPriceCategory(result.price_value);
    
    // Show insights
    if (result.insights && result.insights.length > 0) {
        const insightsList = document.getElementById('insightsList');
        insightsList.innerHTML = '';
        
        result.insights.forEach(insight => {
            const alert = document.createElement('div');
            alert.className = `alert alert-${insight.type}`;
            alert.innerHTML = `<i class="fas fa-info-circle me-2"></i>${insight.text}`;
            insightsList.appendChild(alert);
        });
        
        document.getElementById('carAge').textContent = result.car_age + ' years';
        document.getElementById('depreciation').textContent = result.depreciation + '%';
        document.getElementById('insightsSection').style.display = 'block';
    }
    
    // Scroll to result
    document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function getPriceCategory(price) {
    if (price < 300000) return '💰 Budget Friendly';
    if (price < 700000) return '🚗 Mid Range';
    if (price < 1500000) return '⭐ Premium';
    return '💎 Luxury';
}

// Validation
function setupValidation() {
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            this.classList.remove('is-valid', 'is-invalid');
        });
    });
}

function validateInput(input) {
    if (input.value && input.checkValidity()) {
        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
    } else if (input.value) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    }
}

// Local Storage
function loadSavedData() {
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        const saved = localStorage.getItem('car_' + input.id);
        if (saved) input.value = saved;
        
        input.addEventListener('change', function() {
            localStorage.setItem('car_' + this.id, this.value);
        });
    });
}

function saveToHistory(formData, result) {
    let history = JSON.parse(localStorage.getItem('prediction_history') || '[]');
    history.unshift({
        date: new Date().toISOString(),
        data: formData,
        result: result
    });
    history = history.slice(0, 10); // Keep last 10
    localStorage.setItem('prediction_history', JSON.stringify(history));
}

// UI Functions
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
    `;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : 'times'}-circle me-2"></i>
        ${message}
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Animations
function setupAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    document.querySelectorAll('.feature-card, .insight-card').forEach(el => {
        observer.observe(el);
    });
}

// Utility Functions
function scrollToPredict() {
    document.getElementById('predict').scrollIntoView({ behavior: 'smooth' });
}

function downloadReport() {
    const priceDisplay = document.getElementById('priceDisplay').textContent;
    const carAge = document.getElementById('carAge').textContent;
    const depreciation = document.getElementById('depreciation').textContent;
    
    const report = `
CAR VALUATION REPORT
====================
Generated: ${new Date().toLocaleString()}

Estimated Value: ${priceDisplay}
Car Age: ${carAge}
Depreciation: ${depreciation}

This report is generated by CarValue AI
For more information, visit: carvalue.ai
    `;
    
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'car-valuation-report.txt';
    a.click();
    
    showNotification('Report downloaded successfully!', 'success');
}

// Smart Features
function suggestMaintenance(kms, year) {
    const age = 2024 - parseInt(year);
    const suggestions = [];
    
    if (kms > 50000) suggestions.push('Consider major service');
    if (age > 5) suggestions.push('Check for rust and wear');
    if (kms > 100000) suggestions.push('Timing belt replacement recommended');
    
    return suggestions;
}

function calculateROI(buyPrice, sellPrice, years) {
    const depreciation = ((buyPrice - sellPrice) / buyPrice) * 100;
    const annualDepreciation = depreciation / years;
    return {
        totalDepreciation: depreciation.toFixed(2),
        annualDepreciation: annualDepreciation.toFixed(2)
    };
}

// Export for global use
window.scrollToPredict = scrollToPredict;
window.downloadReport = downloadReport;
window.toggleTheme = toggleTheme;
