// Tool Calling Visualization for VoyagerVerse
// This script visualizes the agentic AI's tool-calling process

const toolCallingVisualization = {
    init: function() {
        this.toolCallContainer = document.getElementById('tool-calls-container');
        if (!this.toolCallContainer) return;
        
        this.setupEventListeners();
    },
    
    setupEventListeners: function() {
        const demoButton = document.getElementById('run-tool-calling-demo');
        if (demoButton) {
            demoButton.addEventListener('click', () => this.runToolCallingDemo());
        }
    },
    
    runToolCallingDemo: function() {
        // Clear previous demo
        this.toolCallContainer.innerHTML = '';
        const demoButton = document.getElementById('run-tool-calling-demo');
        if (demoButton) demoButton.disabled = true;
        
        // Show loading state
        this.addToolCall('system', 'Starting Tom & Priya scenario with tool-calling agentic AI...', 'loading');
        
        // Simulate the tool-calling process
        setTimeout(() => this.perceptionPhase(), 1500);
    },
    
    perceptionPhase: function() {
        this.addToolCall('system', 'Entering Perception Phase', 'phase');
        
        // Tool Call 1: Get Weather
        setTimeout(() => {
            this.addToolCall('tool-call', 'get_current_weather("Dubai")', 'request');
            
            // Tool Response
            setTimeout(() => {
                const weatherData = {
                    temperature: 44,
                    condition: 'Sunny',
                    humidity: 28,
                    feels_like: 47,
                    uv_index: 'Extreme',
                    wind_speed: 12
                };
                this.addToolCall('tool-response', JSON.stringify(weatherData, null, 2), 'response');
                
                // Tool Call 2: Get Itinerary
                setTimeout(() => {
                    this.addToolCall('tool-call', 'get_traveler_itinerary("Tom_and_Priya")', 'request');
                    
                    // Tool Response
                    setTimeout(() => {
                        const itineraryData = {
                            traveler_id: "Tom_and_Priya",
                            today_activities: [
                                { time: "09:00-10:30", activity: "Breakfast at Hotel", location: "Burj Al Arab", is_outdoor: false },
                                { time: "11:00-15:00", activity: "Desert Safari", location: "Dubai Desert Conservation Reserve", is_outdoor: true },
                                { time: "16:00-18:00", activity: "Relaxation Time", location: "Hotel", is_outdoor: false },
                                { time: "19:00-21:00", activity: "Dinner Cruise", location: "Dubai Marina", is_outdoor: false }
                            ]
                        };
                        this.addToolCall('tool-response', JSON.stringify(itineraryData, null, 2), 'response');
                        
                        // Move to reasoning phase
                        setTimeout(() => this.reasoningPhase(), 1500);
                    }, 1000);
                }, 1000);
            }, 1000);
        }, 1000);
    },
    
    reasoningPhase: function() {
        this.addToolCall('system', 'Entering Reasoning Phase', 'phase');
        
        // Tool Call: Analyze Safety
        setTimeout(() => {
            this.addToolCall('tool-call', 'analyze_activity_safety({"activity": "Desert Safari", "temperature": 44, "is_outdoor": true})', 'request');
            
            // Tool Response
            setTimeout(() => {
                const safetyData = {
                    is_safe: false,
                    risk_level: "High",
                    reason: "Temperature exceeds safe threshold for outdoor activities (>40°C)",
                    recommendation: "Reschedule to early morning or find indoor alternative"
                };
                this.addToolCall('tool-response', JSON.stringify(safetyData, null, 2), 'response');
                
                // Tool Call: Find Alternatives
                setTimeout(() => {
                    this.addToolCall('tool-call', 'find_alternative_activities({"preferences": ["cultural", "indoor"], "time_slot": "11:00-15:00"})', 'request');
                    
                    // Tool Response
                    setTimeout(() => {
                        const alternativesData = {
                            alternatives: [
                                { activity: "Dubai Museum Visit", location: "Al Fahidi Fort", is_outdoor: false, category: "cultural" },
                                { activity: "Mall of the Emirates", location: "Sheikh Zayed Road", is_outdoor: false, category: "shopping" },
                                { activity: "Burj Khalifa Observation Deck", location: "Downtown Dubai", is_outdoor: false, category: "attraction" }
                            ]
                        };
                        this.addToolCall('tool-response', JSON.stringify(alternativesData, null, 2), 'response');
                        
                        // Move to action phase
                        setTimeout(() => this.actionPhase(), 1500);
                    }, 1000);
                }, 1000);
            }, 1000);
        }, 1000);
    },
    
    actionPhase: function() {
        this.addToolCall('system', 'Entering Action Phase', 'phase');
        
        // Tool Call: Cancel Booking
        setTimeout(() => {
            this.addToolCall('tool-call', 'cancel_booking({"activity": "Desert Safari", "booking_id": "DS12345", "reason": "Extreme heat safety concern"})', 'request');
            
            // Tool Response
            setTimeout(() => {
                const cancelData = {
                    success: true,
                    refund_status: "Full refund processed",
                    confirmation_code: "CXL78901"
                };
                this.addToolCall('tool-response', JSON.stringify(cancelData, null, 2), 'response');
                
                // Tool Call: Book Alternative
                setTimeout(() => {
                    this.addToolCall('tool-call', 'book_activity({"activity": "Dubai Museum Visit", "time": "11:00-13:00", "travelers": ["Tom", "Priya"]})', 'request');
                    
                    // Tool Response
                    setTimeout(() => {
                        const bookingData = {
                            success: true,
                            booking_id: "DM54321",
                            confirmation_code: "BKG12345",
                            tickets: ["Adult x2"],
                            total_price: "140 AED"
                        };
                        this.addToolCall('tool-response', JSON.stringify(bookingData, null, 2), 'response');
                        
                        // Tool Call: Send Notification
                        setTimeout(() => {
                            this.addToolCall('tool-call', 'send_notification({"to": "Tom_and_Priya", "type": "itinerary_change", "priority": "high"})', 'request');
                            
                            // Tool Response
                            setTimeout(() => {
                                const notificationData = {
                                    sent: true,
                                    notification_id: "NT98765",
                                    channels: ["app", "email", "sms"],
                                    time_sent: new Date().toISOString()
                                };
                                this.addToolCall('tool-response', JSON.stringify(notificationData, null, 2), 'response');
                                
                                // Move to learning phase
                                setTimeout(() => this.learningPhase(), 1500);
                            }, 1000);
                        }, 1000);
                    }, 1000);
                }, 1000);
            }, 1000);
        }, 1000);
    },
    
    learningPhase: function() {
        this.addToolCall('system', 'Entering Learning Phase', 'phase');
        
        // Tool Call: Update Preferences
        setTimeout(() => {
            this.addToolCall('tool-call', 'update_traveler_preferences({"traveler_id": "Tom_and_Priya", "preferences": {"avoid_outdoor_high_heat": true}})', 'request');
            
            // Tool Response
            setTimeout(() => {
                const preferencesData = {
                    success: true,
                    updated_preferences: [
                        "avoid_outdoor_high_heat",
                        "preferred_activities_extreme_heat"
                    ],
                    preference_strength: 0.85
                };
                this.addToolCall('tool-response', JSON.stringify(preferencesData, null, 2), 'response');
                
                // Tool Call: Log Decision
                setTimeout(() => {
                    this.addToolCall('tool-call', 'log_agentic_decision({"decision": "itinerary_change", "reason": "safety", "confidence": 0.92})', 'request');
                    
                    // Tool Response
                    setTimeout(() => {
                        const logData = {
                            logged: true,
                            decision_id: "DEC87654",
                            timestamp: new Date().toISOString()
                        };
                        this.addToolCall('tool-response', JSON.stringify(logData, null, 2), 'response');
                        
                        // Complete the demo
                        setTimeout(() => this.completeDemoPhase(), 1500);
                    }, 1000);
                }, 1000);
            }, 1000);
        }, 1000);
    },
    
    completeDemoPhase: function() {
        this.addToolCall('system', 'Tool-Calling Demo Complete', 'phase');
        this.addToolCall('system', 'The agentic AI has successfully adapted Tom & Priya\'s itinerary in response to extreme heat, demonstrating perception, reasoning, action, and learning through tool-calling.', 'summary');
        
        // Re-enable demo button
        const demoButton = document.getElementById('run-tool-calling-demo');
        if (demoButton) demoButton.disabled = false;
    },
    
    addToolCall: function(type, content, className) {
        const toolCallElement = document.createElement('div');
        toolCallElement.className = `tool-call ${className}`;
        
        let icon = '';
        let title = '';
        
        switch(type) {
            case 'tool-call':
                icon = '<span class="tool-icon">🔧</span>';
                title = '<span class="tool-title">Tool Call:</span>';
                break;
            case 'tool-response':
                icon = '<span class="tool-icon">📤</span>';
                title = '<span class="tool-title">Response:</span>';
                break;
            case 'system':
                icon = '<span class="tool-icon">🤖</span>';
                title = '<span class="tool-title">System:</span>';
                break;
        }
        
        toolCallElement.innerHTML = `
            ${icon}
            <div class="tool-content">
                ${title}
                <pre>${content}</pre>
            </div>
        `;
        
        this.toolCallContainer.appendChild(toolCallElement);
        this.toolCallContainer.scrollTop = this.toolCallContainer.scrollHeight;
    }
};

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    toolCallingVisualization.init();
});
