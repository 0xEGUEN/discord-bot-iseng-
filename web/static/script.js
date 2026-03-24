// Check bot status on page load
document.addEventListener('DOMContentLoaded', function() {
    checkBotStatus();
    loadBotStats();
    setupCommandFilters();
    
    // Auto-refresh stats every 5 seconds
    setInterval(loadBotStats, 5000);
});

// Check bot status
async function checkBotStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        const statusElement = document.getElementById('bot-status');
        if (data.status === 'online') {
            statusElement.textContent = 'Bot Status: Online ✓';
            statusElement.style.color = '#10b981';
        } else {
            statusElement.textContent = 'Bot Status: Offline ✗';
            statusElement.style.color = '#ef4444';
        }
    } catch (error) {
        console.error('Error checking bot status:', error);
        document.getElementById('bot-status').textContent = 'Bot Status: Unable to check';
    }
}

// Load real-time bot statistics
async function loadBotStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update status indicator
        const statusDot = document.querySelector('.status-dot');
        if (data.online) {
            statusDot.className = 'status-dot online';
        } else {
            statusDot.className = 'status-dot offline';
        }
        
        // Update stats cards
        const statsContainer = document.getElementById('bot-stats');
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-icon">⏱️</div>
                    <div class="stat-content">
                        <div class="stat-label">Uptime</div>
                        <div class="stat-value">${data.uptime}</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🖥️</div>
                    <div class="stat-content">
                        <div class="stat-label">Guilds</div>
                        <div class="stat-value">${data.guilds}</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-content">
                        <div class="stat-label">Users</div>
                        <div class="stat-value">${data.users}</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📡</div>
                    <div class="stat-content">
                        <div class="stat-label">Latency</div>
                        <div class="stat-value">${data.latency}</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">⚙️</div>
                    <div class="stat-content">
                        <div class="stat-label">Version</div>
                        <div class="stat-value">v${data.version}</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📊</div>
                    <div class="stat-content">
                        <div class="stat-label">Commands Used</div>
                        <div class="stat-value">${data.commands_used}</div>
                    </div>
                </div>
            `;
        }
        
        // Add pulse animation for online status
        if (data.online) {
            const statusDot = document.querySelector('.status-dot');
            if (statusDot) {
                statusDot.style.animation = 'pulse 2s infinite';
            }
        }
    } catch (error) {
        console.error('Error loading bot stats:', error);
    }
}

// Setup command filter buttons
function setupCommandFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const commandCards = document.querySelectorAll('.command-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get filter value
            const filter = this.getAttribute('data-filter');
            
            // Filter commands
            commandCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-type') === filter) {
                    card.classList.remove('hidden');
                    // Add animation
                    card.style.animation = 'none';
                    setTimeout(() => {
                        card.style.animation = 'fadeIn 0.3s ease-in';
                    }, 10);
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
}

// Add fadeIn and pulse animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        50% {
            box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
`;
document.head.appendChild(style);

// Refresh status every 30 seconds
setInterval(checkBotStatus, 30000);
