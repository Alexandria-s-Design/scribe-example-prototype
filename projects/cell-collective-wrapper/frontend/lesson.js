/**
 * Cell Collective Lesson Interface
 * Loads and displays lesson data with 3-panel layout
 */

console.log('=== LESSON.JS STARTING ===');

const API_BASE = 'http://localhost:8000';
let currentLesson = null;
let hasToken = false;

console.log('Variables initialized:', { API_BASE, currentLesson, hasToken });

// Update debug status
function updateDebugStatus(message) {
    console.log('DEBUG:', message);
    const debugDiv = document.getElementById('debugStatus');
    if (debugDiv) {
        debugDiv.textContent = 'Debug: ' + message;
        debugDiv.style.display = 'block';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('=== DOMContentLoaded fired ===');
    updateDebugStatus('DOM loaded, checking token...');

    try {
        // Check if token exists
        checkToken();
    } catch (error) {
        console.error('Error in DOMContentLoaded:', error);
        updateDebugStatus('Error: ' + error.message);
    }
});

/**
 * Check if token is set, show modal if not
 */
async function checkToken() {
    console.log('checkToken() called');
    updateDebugStatus('Checking for token...');

    const token = localStorage.getItem('cellCollectiveToken');
    console.log('Token from localStorage:', token ? 'Found' : 'Not found');

    if (token) {
        updateDebugStatus('Token found, sending to backend...');

        // Send token to backend first
        try {
            console.log('POSTing token to backend...');
            const response = await fetch(`${API_BASE}/api/set-token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token })
            });

            console.log('Token response status:', response.status);
            const data = await response.json();
            console.log('Token response data:', data);

            if (data.success) {
                hasToken = true;
                updateDebugStatus('Token accepted, loading lesson...');
                document.getElementById('tokenModal').classList.add('hidden');

                // Get model ID from URL parameter
                const urlParams = new URLSearchParams(window.location.search);
                const modelId = urlParams.get('model') || 298697; // Default to Water Cycle
                console.log('Model ID:', modelId);

                loadLesson(modelId);
            } else {
                // Token invalid, show modal
                console.error('Token rejected by server');
                updateDebugStatus('Token invalid, please re-enter');
                localStorage.removeItem('cellCollectiveToken');
                document.getElementById('tokenModal').classList.remove('hidden');
            }
        } catch (error) {
            // Error setting token, show modal
            console.error('Error setting token:', error);
            updateDebugStatus('Error: ' + error.message);
            document.getElementById('tokenModal').classList.remove('hidden');
        }
    } else {
        // Show token modal
        console.log('No token found, showing modal');
        updateDebugStatus('No token found, showing modal...');
        document.getElementById('tokenModal').classList.remove('hidden');
    }
}

/**
 * Set authentication token
 */
async function setToken() {
    const tokenInput = document.getElementById('tokenInput');
    const errorDiv = document.getElementById('tokenError');
    const token = tokenInput.value.trim();

    if (!token) {
        errorDiv.textContent = 'Please enter a token';
        errorDiv.classList.add('show');
        return;
    }

    try {
        // Send token to backend
        const response = await fetch(`${API_BASE}/api/set-token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });

        const data = await response.json();

        if (data.success) {
            // Save to localStorage
            localStorage.setItem('cellCollectiveToken', token);
            hasToken = true;

            // Hide modal
            document.getElementById('tokenModal').classList.add('hidden');

            // Load lesson
            const urlParams = new URLSearchParams(window.location.search);
            const modelId = urlParams.get('model') || 298697;
            loadLesson(modelId);
        } else {
            errorDiv.textContent = 'Failed to set token: ' + data.message;
            errorDiv.classList.add('show');
        }
    } catch (error) {
        errorDiv.textContent = 'Network error: ' + error.message;
        errorDiv.classList.add('show');
    }
}

/**
 * Load lesson data from backend
 */
async function loadLesson(modelId) {
    console.log('Loading lesson for model:', modelId);

    try {
        console.log('Fetching from:', `${API_BASE}/api/lesson/${modelId}`);
        const response = await fetch(`${API_BASE}/api/lesson/${modelId}`);
        console.log('Response status:', response.status);

        const data = await response.json();
        console.log('Response data:', data);

        if (data.success) {
            currentLesson = data.lesson;
            console.log('Lesson loaded:', currentLesson);
            renderLesson();
        } else {
            console.error('Lesson load failed:', data.error);
            showError('Failed to load lesson: ' + data.error);
        }
    } catch (error) {
        console.error('Network error loading lesson:', error);
        showError('Network error: ' + error.message);
    }
}

/**
 * Render the complete lesson interface
 */
function renderLesson() {
    if (!currentLesson) return;

    // Update title
    document.getElementById('modelTitle').textContent = currentLesson.model.name;

    // Render each panel
    renderInstructionsPanel();
    renderGraphPanel();
    renderControlsPanel();

    // Enable simulation buttons
    document.getElementById('startButton').disabled = false;
    document.getElementById('resetButton').disabled = false;

    // Attach button handlers
    document.getElementById('startButton').onclick = startSimulation;
    document.getElementById('resetButton').onclick = resetSimulation;
}

/**
 * Render instructions in left panel
 */
function renderInstructionsPanel() {
    const panel = document.getElementById('instructionsPanel');
    const instructions = currentLesson.instructions;

    panel.innerHTML = `
        <div>
            <h3 style="margin-bottom: 15px; color: #667eea;">${instructions.title}</h3>
            <ul class="instructions-list">
                ${instructions.steps.map(step => `
                    <li>${step}</li>
                `).join('')}
            </ul>

            <div style="margin-top: 25px; padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                <strong style="color: #856404;">About this model:</strong>
                <p style="margin: 10px 0 0 0; font-size: 0.9rem; line-height: 1.6; color: #856404;">
                    ${currentLesson.model.description || 'Explore how different components interact in this biological system.'}
                </p>
            </div>

            <div style="margin-top: 20px; padding: 15px; background: #d1ecf1; border-left: 4px solid #0c5460; border-radius: 4px;">
                <strong style="color: #0c5460;">Model Info:</strong>
                <p style="margin: 8px 0 0 0; font-size: 0.85rem; color: #0c5460;">
                    Components: ${currentLesson.components.length}<br>
                    Relationships: ${currentLesson.relationships.length}<br>
                    Version: ${currentLesson.model.version}
                </p>
            </div>
        </div>
    `;
}

/**
 * Render graph visualization in center panel
 */
function renderGraphPanel() {
    const container = document.getElementById('graphContainer');
    const components = currentLesson.components;

    if (components.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 60px 20px; color: #666;">
                <h3>No components to display</h3>
                <p>This model doesn't have any visible components yet.</p>
            </div>
        `;
        return;
    }

    // Create simple node visualization
    // Position nodes in a circle for now (can be enhanced later)
    const centerX = 400;
    const centerY = 300;
    const radius = 200;
    const angleStep = (2 * Math.PI) / components.length;

    let nodesHTML = components.map((component, index) => {
        const angle = index * angleStep;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);

        const nodeName = component.name || component.externalName || `Component ${index + 1}`;

        return `
            <div class="graph-node"
                 style="left: ${x}px; top: ${y}px;"
                 data-component-id="${component.id}"
                 title="${nodeName}">
                ${nodeName}
            </div>
        `;
    }).join('');

    container.innerHTML = `
        <div style="position: relative; width: 100%; height: 100%; min-height: 600px;">
            ${nodesHTML}
        </div>
    `;
}

/**
 * Render control panel in right panel
 */
function renderControlsPanel() {
    const panel = document.getElementById('controlsPanel');
    const components = currentLesson.components;

    if (components.length === 0) {
        panel.innerHTML = `
            <p style="color: #666; text-align: center;">No components to control</p>
        `;
        return;
    }

    panel.innerHTML = `
        <div class="component-list">
            ${components.slice(0, 10).map((component, index) => {
                const nodeName = component.name || component.externalName || `Component ${index + 1}`;

                return `
                    <div class="component-item" data-component-id="${component.id}">
                        <div class="component-name">${nodeName}</div>
                        <div class="component-state">
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                                <input type="checkbox"
                                       class="component-toggle"
                                       data-component-id="${component.id}"
                                       style="cursor: pointer;">
                                <span>Active</span>
                            </label>
                        </div>
                    </div>
                `;
            }).join('')}
            ${components.length > 10 ? `
                <div style="text-align: center; padding: 10px; color: #666; font-size: 0.85rem;">
                    + ${components.length - 10} more components
                </div>
            ` : ''}
        </div>
    `;

    // Add event listeners to toggles
    panel.querySelectorAll('.component-toggle').forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            const componentId = e.target.dataset.componentId;
            const isActive = e.target.checked;
            updateComponentState(componentId, isActive);
        });
    });
}

/**
 * Update component state (placeholder for now)
 */
function updateComponentState(componentId, isActive) {
    console.log(`Component ${componentId} set to ${isActive ? 'active' : 'inactive'}`);
    // TODO: Send state update to backend when simulation API is ready
}

/**
 * Start simulation
 */
function startSimulation() {
    console.log('Starting simulation...');

    // Show feedback
    const button = document.getElementById('startButton');
    const originalText = button.textContent;
    button.textContent = '⏳ Running...';
    button.disabled = true;

    // TODO: Call simulation API when ready
    setTimeout(() => {
        button.textContent = '✓ Simulation Complete!';
        setTimeout(() => {
            button.textContent = originalText;
            button.disabled = false;
        }, 2000);
    }, 3000);
}

/**
 * Reset simulation
 */
function resetSimulation() {
    console.log('Resetting simulation...');

    // Reset all toggles
    document.querySelectorAll('.component-toggle').forEach(toggle => {
        toggle.checked = false;
    });

    // Show feedback
    const button = document.getElementById('resetButton');
    const originalText = button.textContent;
    button.textContent = '✓ Reset!';
    setTimeout(() => {
        button.textContent = originalText;
    }, 1000);
}

/**
 * Show error message
 */
function showError(message) {
    const container = document.querySelector('.lesson-container');
    container.innerHTML = `
        <div class="error" style="width: 100%; max-width: 600px; margin: 40px auto;">
            <h3>Oops! Something went wrong</h3>
            <p style="margin-top: 10px;">${message}</p>
            <button onclick="location.reload()" class="btn-primary" style="margin-top: 15px;">
                Try Again
            </button>
        </div>
    `;
}

/**
 * Load user profile info
 */
async function loadUserInfo() {
    try {
        const response = await fetch(`${API_BASE}/api/profile`);
        const data = await response.json();

        if (data.success && data.profile) {
            const profile = data.profile;
            document.getElementById('userInfo').textContent =
                `Welcome, ${profile.firstName || 'User'}!`;
        } else {
            document.getElementById('userInfo').textContent = 'Not logged in';
        }
    } catch (error) {
        document.getElementById('userInfo').textContent = 'Not logged in';
    }
}

// Load user info
loadUserInfo();
