// Cell Collective Explorer - Kid-Friendly JavaScript

const API_BASE = 'http://localhost:8000/api';
let authToken = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Check if token exists in localStorage
    const savedToken = localStorage.getItem('cellCollectiveToken');

    if (savedToken) {
        authToken = savedToken;
        document.getElementById('tokenModal').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');
        initializeApp();
    } else {
        // Show token setup modal
        document.getElementById('tokenModal').style.display = 'flex';
    }
});

// Set authentication token
async function setToken() {
    const tokenInput = document.getElementById('tokenInput');
    const token = tokenInput.value.trim();
    const errorDiv = document.getElementById('tokenError');

    if (!token) {
        errorDiv.textContent = '❌ Please enter a token';
        errorDiv.classList.add('show');
        return;
    }

    try {
        // Send token to backend
        const response = await fetch(`${API_BASE}/set-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token })
        });

        const data = await response.json();

        if (data.success) {
            // Save token
            authToken = token;
            localStorage.setItem('cellCollectiveToken', token);

            // Hide modal, show app
            document.getElementById('tokenModal').classList.add('hidden');
            document.getElementById('app').classList.remove('hidden');

            // Initialize app
            initializeApp();
        } else {
            errorDiv.textContent = '❌ Invalid token. Please try again.';
            errorDiv.classList.add('show');
        }
    } catch (error) {
        errorDiv.textContent = '❌ Connection error. Is the backend running?';
        errorDiv.classList.add('show');
        console.error('Token error:', error);
    }
}

// Initialize the app
async function initializeApp() {
    try {
        // Get user profile
        const profile = await fetchAPI('/profile');
        if (profile && profile.data) {
            const userInfo = document.getElementById('userInfo');
            userInfo.textContent = `👋 Welcome, ${profile.data.firstName || 'Explorer'}!`;
        }

        // Load models
        await loadModels();

    } catch (error) {
        console.error('Init error:', error);
        showError('Failed to initialize. Please refresh the page.');
    }
}

// Load all models
async function loadModels() {
    const loadingDiv = document.getElementById('loading');
    const gridDiv = document.getElementById('modelGrid');
    const errorDiv = document.getElementById('error');

    // Show loading
    loadingDiv.style.display = 'block';
    gridDiv.innerHTML = '';
    errorDiv.style.display = 'none';

    try {
        const response = await fetchAPI('/models');

        if (response.success && response.models) {
            const models = response.models;

            // Hide loading
            loadingDiv.style.display = 'none';

            if (models.length === 0) {
                gridDiv.innerHTML = '<p style="color: white; text-align: center;">No models found. Try refreshing!</p>';
                return;
            }

            // Update stats
            document.getElementById('modelCount').textContent = models.length;

            let totalComponents = 0;
            models.forEach(model => {
                if (model.componentCount) {
                    totalComponents += model.componentCount;
                }
            });
            document.getElementById('componentCount').textContent = totalComponents;
            document.getElementById('exploreCount').textContent = models.length;

            // Render model cards
            models.forEach(model => {
                const card = createModelCard(model);
                gridDiv.appendChild(card);
            });

        } else {
            throw new Error('Failed to load models');
        }

    } catch (error) {
        loadingDiv.style.display = 'none';
        showError('Failed to load models. Please check your connection.');
        console.error('Load models error:', error);
    }
}

// Create model card element
function createModelCard(model) {
    const card = document.createElement('div');
    card.className = 'model-card';
    card.onclick = () => showModelDetail(model.id);

    const title = document.createElement('h3');
    title.textContent = model.name || 'Unnamed Model';

    const description = document.createElement('p');
    description.textContent = model.description
        ? (model.description.substring(0, 120) + (model.description.length > 120 ? '...' : ''))
        : 'No description available';

    const meta = document.createElement('div');
    meta.className = 'model-meta';

    const componentTag = document.createElement('span');
    componentTag.className = 'model-tag';
    componentTag.textContent = `🧬 ${model.componentCount || 0} Components`;

    const versionTag = document.createElement('span');
    versionTag.className = 'model-tag';
    versionTag.textContent = `v${model.version || 1}`;

    meta.appendChild(componentTag);
    meta.appendChild(versionTag);

    card.appendChild(title);
    card.appendChild(description);
    card.appendChild(meta);

    return card;
}

// Show model detail in modal
async function showModelDetail(modelId) {
    const modal = document.getElementById('detailModal');
    const detailDiv = document.getElementById('modelDetail');

    // Show modal with loading
    modal.classList.remove('hidden');
    detailDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading model details...</p></div>';

    try {
        const response = await fetchAPI(`/model/${modelId}`);

        if (response.success && response.model) {
            const model = response.model;

            let html = `
                <div class="model-detail-header">
                    <h2>${model.name || 'Unnamed Model'}</h2>
                    <p style="color: #666;">${model.description || 'No description available'}</p>
                </div>

                <div class="model-detail-section">
                    <h3>📊 Overview</h3>
                    <p><strong>Model ID:</strong> ${model.id}</p>
                    <p><strong>Version:</strong> ${model.version || 1}</p>
                    <p><strong>Components:</strong> ${model.components ? model.components.length : 0}</p>
                    <p><strong>Relationships:</strong> ${model.relationships ? model.relationships.length : 0}</p>
                </div>
            `;

            // Show components
            if (model.components && model.components.length > 0) {
                html += '<div class="model-detail-section"><h3>🧬 Components</h3><div class="component-list">';
                model.components.slice(0, 10).forEach(component => {
                    html += `<div class="component-item">${component.name || component}</div>`;
                });
                if (model.components.length > 10) {
                    html += `<p style="color: #999; margin-top: 10px;">...and ${model.components.length - 10} more</p>`;
                }
                html += '</div></div>';
            }

            // Show relationships
            if (model.relationships && model.relationships.length > 0) {
                html += '<div class="model-detail-section"><h3>🔗 Relationships</h3><div class="relationship-list">';
                model.relationships.slice(0, 5).forEach(rel => {
                    const relText = typeof rel === 'object'
                        ? `${rel.source || 'Unknown'} → ${rel.target || 'Unknown'}`
                        : rel;
                    html += `<div class="relationship-item">${relText}</div>`;
                });
                if (model.relationships.length > 5) {
                    html += `<p style="color: #999; margin-top: 10px;">...and ${model.relationships.length - 5} more</p>`;
                }
                html += '</div></div>';
            }

            detailDiv.innerHTML = html;

        } else {
            detailDiv.innerHTML = '<p class="error show">Failed to load model details.</p>';
        }

    } catch (error) {
        detailDiv.innerHTML = '<p class="error show">Connection error. Please try again.</p>';
        console.error('Detail error:', error);
    }
}

// Close detail modal
function closeDetail() {
    document.getElementById('detailModal').classList.add('hidden');
}

// Refresh models
function refreshModels() {
    loadModels();
}

// Fetch from API
async function fetchAPI(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: authToken ? { 'x-auth-token': authToken } : {}
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');

    setTimeout(() => {
        errorDiv.classList.remove('show');
    }, 5000);
}

// Close modal on outside click
document.addEventListener('click', (e) => {
    const detailModal = document.getElementById('detailModal');
    if (e.target === detailModal) {
        closeDetail();
    }
});

// ESC key to close modal
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDetail();
    }
});
