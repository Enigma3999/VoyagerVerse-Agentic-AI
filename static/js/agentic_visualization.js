/**
 * VoyagerVerse Agentic AI Visualization
 * 
 * This script provides visual representations of the agentic AI's
 * perception, reasoning, action, and learning processes.
 */

class AgenticVisualizer {
    constructor() {
        this.perceptionElement = document.getElementById('perception-visual');
        this.reasoningElement = document.getElementById('reasoning-visual');
        this.actionElement = document.getElementById('action-visual');
        this.learningElement = document.getElementById('learning-visual');
        this.dataSourcesElement = document.getElementById('data-sources');
        this.confidenceElement = document.getElementById('ai-confidence');
        
        // Initialize visualization containers if they exist
        this.initializeVisualElements();
    }
    
    initializeVisualElements() {
        // Create elements if they don't exist
        if (!this.perceptionElement && document.getElementById('agentic-visualization')) {
            const container = document.getElementById('agentic-visualization');
            
            this.perceptionElement = this.createVisualElement('perception-visual', 'Perception', container);
            this.reasoningElement = this.createVisualElement('reasoning-visual', 'Reasoning', container);
            this.actionElement = this.createVisualElement('action-visual', 'Action', container);
            this.learningElement = this.createVisualElement('learning-visual', 'Learning', container);
            this.dataSourcesElement = this.createVisualElement('data-sources', 'Data Sources', container);
            this.confidenceElement = this.createVisualElement('ai-confidence', 'AI Confidence', container);
        }
    }
    
    createVisualElement(id, title, container) {
        const element = document.createElement('div');
        element.id = id;
        element.className = 'agentic-visual-component';
        
        const titleEl = document.createElement('h3');
        titleEl.textContent = title;
        element.appendChild(titleEl);
        
        const contentEl = document.createElement('div');
        contentEl.className = 'visual-content';
        element.appendChild(contentEl);
        
        container.appendChild(element);
        return element;
    }
    
    // Visualize the perception process (data gathering)
    visualizePerception(data) {
        if (!this.perceptionElement) return;
        
        const content = this.perceptionElement.querySelector('.visual-content');
        content.innerHTML = '';
        
        // Create weather perception visualization
        if (data.weather) {
            const weatherEl = document.createElement('div');
            weatherEl.className = 'perception-item weather-perception';
            
            // Add animation for data fetching
            weatherEl.innerHTML = `
                <div class="data-source">
                    <span class="source-icon">🌤️</span>
                    <span class="source-name">${data.weather.data_source}</span>
                </div>
                <div class="data-animation">
                    <div class="pulse-animation"></div>
                </div>
                <div class="data-values">
                    <div class="data-value"><span class="value-label">Temperature:</span> <span class="value-data">${data.weather.temperature}°C</span></div>
                    <div class="data-value"><span class="value-label">Conditions:</span> <span class="value-data">${data.weather.conditions}</span></div>
                    <div class="data-value"><span class="value-label">Last Updated:</span> <span class="value-data">${new Date(data.weather.last_updated).toLocaleTimeString()}</span></div>
                </div>
            `;
            
            content.appendChild(weatherEl);
        }
        
        // Create location perception visualization
        if (data.location) {
            const locationEl = document.createElement('div');
            locationEl.className = 'perception-item location-perception';
            
            locationEl.innerHTML = `
                <div class="data-source">
                    <span class="source-icon">📍</span>
                    <span class="source-name">Location Service</span>
                </div>
                <div class="data-animation">
                    <div class="pulse-animation"></div>
                </div>
                <div class="data-values">
                    <div class="data-value"><span class="value-label">City:</span> <span class="value-data">${data.location.city}</span></div>
                    <div class="data-value"><span class="value-label">District:</span> <span class="value-data">${data.location.district}</span></div>
                </div>
            `;
            
            content.appendChild(locationEl);
        }
        
        // Visualize time context
        if (data.time_context) {
            const timeEl = document.createElement('div');
            timeEl.className = 'perception-item time-perception';
            
            timeEl.innerHTML = `
                <div class="data-source">
                    <span class="source-icon">🕒</span>
                    <span class="source-name">Time Context</span>
                </div>
                <div class="data-values">
                    <div class="data-value"><span class="value-label">Local Time:</span> <span class="value-data">${new Date(data.time_context.local_time).toLocaleTimeString()}</span></div>
                    <div class="data-value"><span class="value-label">Day:</span> <span class="value-data">${data.time_context.day_of_week}</span></div>
                    <div class="data-value"><span class="value-label">Time of Day:</span> <span class="value-data">${data.time_context.time_of_day}</span></div>
                </div>
            `;
            
            content.appendChild(timeEl);
        }
    }
    
    // Visualize the reasoning process
    visualizeReasoning(decision) {
        if (!this.reasoningElement || !decision) return;
        
        const content = this.reasoningElement.querySelector('.visual-content');
        content.innerHTML = '';
        
        // Create reasoning visualization
        const reasoningEl = document.createElement('div');
        reasoningEl.className = 'reasoning-process';
        
        // Determine reasoning type based on decision
        let reasoningType = 'weather';
        if (decision.reason === 'energy') reasoningType = 'energy';
        
        // Create reasoning visualization based on type
        if (reasoningType === 'weather') {
            reasoningEl.innerHTML = `
                <div class="reasoning-header">
                    <div class="reasoning-icon">🧠</div>
                    <div class="reasoning-title">Weather-based Decision Analysis</div>
                </div>
                <div class="reasoning-animation">
                    <div class="thinking-animation"></div>
                </div>
                <div class="reasoning-factors">
                    <div class="factor">
                        <div class="factor-name">Temperature Impact</div>
                        <div class="factor-bar">
                            <div class="factor-value" style="width: 90%;"></div>
                        </div>
                    </div>
                    <div class="factor">
                        <div class="factor-name">User Comfort Threshold</div>
                        <div class="factor-bar">
                            <div class="factor-value" style="width: 85%;"></div>
                        </div>
                    </div>
                    <div class="factor">
                        <div class="factor-name">Activity Suitability</div>
                        <div class="factor-bar">
                            <div class="factor-value" style="width: 30%;"></div>
                        </div>
                    </div>
                </div>
                <div class="reasoning-conclusion">
                    <p>Outdoor activities are unsuitable due to extreme heat exceeding traveler comfort threshold.</p>
                </div>
            `;
        } else if (reasoningType === 'energy') {
            reasoningEl.innerHTML = `
                <div class="reasoning-header">
                    <div class="reasoning-icon">🧠</div>
                    <div class="reasoning-title">Energy-based Decision Analysis</div>
                </div>
                <div class="reasoning-animation">
                    <div class="thinking-animation"></div>
                </div>
                <div class="reasoning-factors">
                    <div class="factor">
                        <div class="factor-name">Current Energy Level</div>
                        <div class="factor-bar">
                            <div class="factor-value" style="width: 35%;"></div>
                        </div>
                    </div>
                    <div class="factor">
                        <div class="factor-name">Activity Energy Requirement</div>
                        <div class="factor-bar">
                            <div class="factor-value" style="width: 80%;"></div>
                        </div>
                    </div>
                    <div class="factor">
                        <div class="factor-name">Rest Opportunity</div>
                        <div class="factor-bar">
                            <div class="factor-value" style="width: 20%;"></div>
                        </div>
                    </div>
                </div>
                <div class="reasoning-conclusion">
                    <p>High-energy activities are unsuitable due to current low energy levels.</p>
                </div>
            `;
        }
        
        content.appendChild(reasoningEl);
        
        // Update confidence visualization
        if (this.confidenceElement && decision.confidence) {
            const confidenceContent = this.confidenceElement.querySelector('.visual-content');
            confidenceContent.innerHTML = '';
            
            const confidenceEl = document.createElement('div');
            confidenceEl.className = 'confidence-meter';
            
            const confidenceValue = decision.confidence * 100;
            const confidenceColor = confidenceValue > 80 ? '#4CAF50' : 
                                   confidenceValue > 60 ? '#FFC107' : '#F44336';
            
            confidenceEl.innerHTML = `
                <div class="confidence-label">AI Confidence in Decision</div>
                <div class="confidence-bar-container">
                    <div class="confidence-bar" style="width: ${confidenceValue}%; background-color: ${confidenceColor};"></div>
                </div>
                <div class="confidence-value">${confidenceValue.toFixed(0)}%</div>
                <div class="confidence-explanation">
                    ${confidenceValue >= 70 ? 
                        'High confidence: AI can autonomously implement this change.' : 
                        'Lower confidence: Human approval recommended before proceeding.'}
                </div>
            `;
            
            confidenceContent.appendChild(confidenceEl);
        }
    }
    
    // Visualize the action process
    visualizeAction(originalPlan, newPlan) {
        if (!this.actionElement) return;
        
        const content = this.actionElement.querySelector('.visual-content');
        content.innerHTML = '';
        
        // Create action visualization
        const actionEl = document.createElement('div');
        actionEl.className = 'action-process';
        
        // Create comparison of original vs new plan
        actionEl.innerHTML = `
            <div class="action-header">
                <div class="action-icon">🔄</div>
                <div class="action-title">Itinerary Adaptation</div>
            </div>
            <div class="action-animation">
                <div class="action-progress-animation"></div>
            </div>
            <div class="plan-comparison">
                <div class="original-plan">
                    <h4>Original Plan</h4>
                    <div class="plan-activities">
                        ${this.renderActivities(originalPlan?.activities || [])}
                    </div>
                </div>
                <div class="plan-arrow">→</div>
                <div class="new-plan">
                    <h4>Adapted Plan</h4>
                    <div class="plan-activities">
                        ${this.renderActivities(newPlan?.activities || [])}
                    </div>
                </div>
            </div>
            <div class="action-status">
                <div class="status-icon">✓</div>
                <div class="status-message">Itinerary successfully adapted</div>
            </div>
        `;
        
        content.appendChild(actionEl);
    }
    
    // Helper to render activities
    renderActivities(activities) {
        if (!activities || activities.length === 0) return '<p>No activities</p>';
        
        return activities.map(activity => `
            <div class="activity ${activity.is_outdoor ? 'outdoor' : 'indoor'}">
                <div class="activity-time">${activity.time}</div>
                <div class="activity-name">${activity.name}</div>
                <div class="activity-location">${activity.location}</div>
                <div class="activity-tags">
                    ${activity.is_outdoor ? '<span class="tag outdoor">Outdoor</span>' : '<span class="tag indoor">Indoor</span>'}
                    <span class="tag energy-${Math.round(activity.energy_required * 10)}">Energy: ${Math.round(activity.energy_required * 10)}/10</span>
                </div>
            </div>
        `).join('');
    }
    
    // Visualize the learning process
    visualizeLearning(preferences, feedback) {
        if (!this.learningElement) return;
        
        const content = this.learningElement.querySelector('.visual-content');
        content.innerHTML = '';
        
        // Create learning visualization
        const learningEl = document.createElement('div');
        learningEl.className = 'learning-process';
        
        // Create preference learning visualization
        learningEl.innerHTML = `
            <div class="learning-header">
                <div class="learning-icon">📊</div>
                <div class="learning-title">Preference Learning</div>
            </div>
            <div class="learning-animation">
                <div class="learning-progress-animation"></div>
            </div>
            <div class="preference-model">
                <h4>Current Preference Model</h4>
                <div class="preference-items">
                    ${this.renderPreferences(preferences)}
                </div>
            </div>
            <div class="learning-status">
                <div class="status-icon">📝</div>
                <div class="status-message">Preferences updated based on recent decisions</div>
            </div>
        `;
        
        content.appendChild(learningEl);
    }
    
    // Helper to render preferences
    renderPreferences(preferences) {
        if (!preferences) return '<p>No preference data available</p>';
        
        let preferenceHtml = '';
        
        if (preferences.max_comfortable_temperature) {
            preferenceHtml += `
                <div class="preference-item">
                    <div class="preference-name">Max Comfortable Temperature</div>
                    <div class="preference-value">${preferences.max_comfortable_temperature}°C</div>
                    <div class="confidence-indicator" style="width: 90%;"></div>
                </div>
            `;
        }
        
        if (preferences.cuisine_preferences) {
            preferenceHtml += `
                <div class="preference-item">
                    <div class="preference-name">Cuisine Preferences</div>
                    <div class="preference-value">${preferences.cuisine_preferences.join(', ')}</div>
                    <div class="confidence-indicator" style="width: 85%;"></div>
                </div>
            `;
        }
        
        if (preferences.activity_preferences) {
            preferenceHtml += `
                <div class="preference-item">
                    <div class="preference-name">Activity Preferences</div>
                    <div class="preference-value">${preferences.activity_preferences.join(', ')}</div>
                    <div class="confidence-indicator" style="width: 80%;"></div>
                </div>
            `;
        }
        
        if (preferences.budget_level) {
            preferenceHtml += `
                <div class="preference-item">
                    <div class="preference-name">Budget Level</div>
                    <div class="preference-value">${preferences.budget_level}</div>
                    <div class="confidence-indicator" style="width: 95%;"></div>
                </div>
            `;
        }
        
        return preferenceHtml || '<p>No specific preferences found</p>';
    }
    
    // Visualize data sources
    visualizeDataSources(sources) {
        if (!this.dataSourcesElement) return;
        
        const content = this.dataSourcesElement.querySelector('.visual-content');
        content.innerHTML = '';
        
        // Create data sources visualization
        const sourcesEl = document.createElement('div');
        sourcesEl.className = 'data-sources-list';
        
        // Add default sources if none provided
        if (!sources) {
            sources = [
                { name: 'OpenWeatherMap', type: 'Weather', status: 'active' },
                { name: 'WeatherAPI', type: 'Weather', status: 'standby' },
                { name: 'TripAdvisor', type: 'Attractions', status: 'active' },
                { name: 'Dubai Tourism API', type: 'Local Info', status: 'active' },
                { name: 'Zomato', type: 'Dining', status: 'active' },
                { name: 'Uber', type: 'Transportation', status: 'active' }
            ];
        }
        
        // Create source list
        sourcesEl.innerHTML = `
            <div class="sources-header">
                <div class="source-icon">🔌</div>
                <div class="source-title">Real-Time Data Sources</div>
            </div>
            <div class="sources-list">
                ${sources.map(source => `
                    <div class="source-item ${source.status}">
                        <div class="source-status-indicator"></div>
                        <div class="source-name">${source.name}</div>
                        <div class="source-type">${source.type}</div>
                        <div class="source-status">${source.status}</div>
                    </div>
                `).join('')}
            </div>
        `;
        
        content.appendChild(sourcesEl);
    }
    
    // Update all visualizations with new data
    updateVisualizations(data) {
        // Extract data components
        const context = data.context || {};
        const decision = data.decision || {};
        const originalPlan = data.notification?.original_plan || {};
        const newPlan = data.notification?.new_plan || {};
        const preferences = data.preferences || {};
        
        // Update each visualization component
        this.visualizePerception(context);
        this.visualizeReasoning(decision);
        this.visualizeAction(originalPlan, newPlan);
        this.visualizeLearning(preferences);
        this.visualizeDataSources();
    }
}

// Initialize the visualizer when the page loads
let agenticVisualizer;
document.addEventListener('DOMContentLoaded', () => {
    agenticVisualizer = new AgenticVisualizer();
    
    // Listen for updates from the server
    const eventSource = new EventSource('/api/events');
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        agenticVisualizer.updateVisualizations(data);
    };
});

// Function to manually update visualizations (for demo purposes)
function updateAgenticVisualizations(data) {
    if (agenticVisualizer) {
        agenticVisualizer.updateVisualizations(data);
    }
}
