// Device tracking and visualization
class BLEProximityMonitor {
    constructor() {
        this.devices = new Map();
        this.signalHistory = new Map();
        this.maxHistoryLength = 20;
        this.updateInterval = 1000; // 1 second

        this.radarCanvas = document.getElementById('radar-canvas');
        this.radarCtx = this.radarCanvas.getContext('2d');
        this.historyCanvas = document.getElementById('history-canvas');
        this.historyCtx = this.historyCanvas.getContext('2d');

        this.selectedDevice = null;

        this.initCanvas();
        this.startMonitoring();
        this.updateTimestamp();
    }

    initCanvas() {
        // Set canvas size
        this.radarCanvas.width = 500;
        this.radarCanvas.height = 500;
        this.historyCanvas.width = 300;
        this.historyCanvas.height = 200;
    }

    async fetchDevices() {
        try {
            const response = await fetch('/api/devices');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching devices:', error);
            return {};
        }
    }

    calculateProximity(rssi) {
        // Convert RSSI to approximate distance category
        // RSSI values typically range from -30 (very close) to -100 (far)
        if (rssi >= -50) return 'immediate';
        if (rssi >= -70) return 'near';
        return 'far';
    }

    calculateMovementConfidence(mac) {
        const history = this.signalHistory.get(mac) || [];
        if (history.length < 3) return 0;

        // Calculate variance in RSSI values
        const recent = history.slice(-10);
        const mean = recent.reduce((sum, val) => sum + val, 0) / recent.length;
        const variance = recent.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / recent.length;

        // Higher variance = more movement
        // Normalize to 0-100 scale
        return Math.min(100, Math.round(variance * 2));
    }

    updateDeviceHistory(mac, rssi) {
        if (!this.signalHistory.has(mac)) {
            this.signalHistory.set(mac, []);
        }
        const history = this.signalHistory.get(mac);
        history.push(rssi);

        // Keep only recent history
        if (history.length > this.maxHistoryLength) {
            history.shift();
        }
    }

    async updateDevices() {
        const deviceData = await this.fetchDevices();

        // Clear old devices
        const currentMacs = new Set(Object.keys(deviceData));
        for (let mac of this.devices.keys()) {
            if (!currentMacs.has(mac)) {
                this.devices.delete(mac);
                this.signalHistory.delete(mac);
            }
        }

        // Update devices
        for (let [mac, info] of Object.entries(deviceData)) {
            const rssi = info.rssi || -100;
            this.updateDeviceHistory(mac, rssi);

            this.devices.set(mac, {
                mac: mac,
                name: info.name || 'Unknown Device',
                rssi: rssi,
                proximity: this.calculateProximity(rssi),
                movement: this.calculateMovementConfidence(mac),
                manufacturer: info.manufacturer || 'Unknown',
                lastSeen: Date.now()
            });
        }

        this.render();
    }

    render() {
        this.renderDeviceList();
        this.renderRadar();
        this.renderAnalytics();
        this.renderMovementDetection();
        if (this.selectedDevice) {
            this.renderSignalHistory();
        }
    }

    renderDeviceList() {
        const deviceList = document.getElementById('device-list');
        const deviceCount = document.getElementById('device-count');

        deviceCount.textContent = this.devices.size;
        deviceList.innerHTML = '';

        const sortedDevices = Array.from(this.devices.values())
            .sort((a, b) => b.rssi - a.rssi);

        sortedDevices.forEach(device => {
            const item = document.createElement('div');
            item.className = 'device-item';
            if (this.selectedDevice === device.mac) {
                item.classList.add('selected');
            }

            // Calculate signal strength percentage (RSSI -30 to -100 range)
            const signalPercent = Math.max(0, Math.min(100, ((device.rssi + 100) / 70) * 100));

            let barColor;
            if (device.proximity === 'immediate') barColor = '#ff0040';
            else if (device.proximity === 'near') barColor = '#ffa500';
            else barColor = '#00ff41';

            item.innerHTML = `
                <div class="device-name">${device.name}</div>
                <div class="device-mac">${device.mac}</div>
                <div class="device-rssi">
                    <span>RSSI: ${device.rssi} dBm</span>
                    <span>${device.proximity.toUpperCase()}</span>
                </div>
                <div class="rssi-bar">
                    <div class="rssi-fill" style="width: ${signalPercent}%; background: ${barColor};"></div>
                </div>
            `;

            item.addEventListener('click', () => {
                this.selectedDevice = device.mac;
                this.render();
            });

            deviceList.appendChild(item);
        });
    }

    renderRadar() {
        const ctx = this.radarCtx;
        const width = this.radarCanvas.width;
        const height = this.radarCanvas.height;
        const centerX = width / 2;
        const centerY = height / 2;

        // Clear canvas
        ctx.fillStyle = '#0a0e27';
        ctx.fillRect(0, 0, width, height);

        // Draw radar circles (proximity zones)
        const zones = [
            { radius: 80, color: '#ff0040', label: 'immediate' },
            { radius: 160, color: '#ffa500', label: 'near' },
            { radius: 240, color: '#00ff41', label: 'far' }
        ];

        zones.forEach(zone => {
            ctx.beginPath();
            ctx.arc(centerX, centerY, zone.radius, 0, Math.PI * 2);
            ctx.strokeStyle = zone.color;
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.3;
            ctx.stroke();
            ctx.globalAlpha = 1;
        });

        // Draw center point
        ctx.beginPath();
        ctx.arc(centerX, centerY, 8, 0, Math.PI * 2);
        ctx.fillStyle = '#00ff41';
        ctx.fill();

        // Draw devices
        let angle = 0;
        const angleStep = (Math.PI * 2) / Math.max(1, this.devices.size);

        Array.from(this.devices.values()).forEach((device, index) => {
            let radius;
            let color;

            if (device.proximity === 'immediate') {
                radius = 60;
                color = '#ff0040';
            } else if (device.proximity === 'near') {
                radius = 140;
                color = '#ffa500';
            } else {
                radius = 220;
                color = '#00ff41';
            }

            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;

            // Draw connecting line
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(x, y);
            ctx.strokeStyle = color;
            ctx.lineWidth = 1;
            ctx.globalAlpha = 0.3;
            ctx.stroke();
            ctx.globalAlpha = 1;

            // Draw device point
            ctx.beginPath();
            ctx.arc(x, y, 6, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();

            // Pulsing effect for moving devices
            if (device.movement > 50) {
                ctx.beginPath();
                ctx.arc(x, y, 10, 0, Math.PI * 2);
                ctx.strokeStyle = color;
                ctx.lineWidth = 2;
                ctx.globalAlpha = 0.5;
                ctx.stroke();
                ctx.globalAlpha = 1;
            }

            angle += angleStep;
        });
    }

    renderAnalytics() {
        const totalDevices = document.getElementById('total-devices');
        const immediateCount = document.getElementById('immediate-count');
        const nearCount = document.getElementById('near-count');
        const farCount = document.getElementById('far-count');

        let immediate = 0, near = 0, far = 0;

        this.devices.forEach(device => {
            if (device.proximity === 'immediate') immediate++;
            else if (device.proximity === 'near') near++;
            else far++;
        });

        totalDevices.textContent = this.devices.size;
        immediateCount.textContent = immediate;
        nearCount.textContent = near;
        farCount.textContent = far;
    }

    renderMovementDetection() {
        const movementGrid = document.getElementById('movement-grid');
        movementGrid.innerHTML = '';

        const sortedByMovement = Array.from(this.devices.values())
            .sort((a, b) => b.movement - a.movement)
            .slice(0, 6); // Show top 6 devices

        sortedByMovement.forEach(device => {
            const item = document.createElement('div');
            const isMoving = device.movement > 30;

            item.className = `movement-item ${isMoving ? 'moving' : 'stationary'}`;
            item.innerHTML = `
                <div class="movement-info">
                    <h4>${device.name}</h4>
                    <p>${device.mac}</p>
                    <p style="color: ${isMoving ? '#ff0040' : '#00ff41'};">
                        ${isMoving ? 'MOVING' : 'STATIONARY'}
                    </p>
                </div>
                <div class="confidence-meter">
                    <div class="confidence-value" style="color: ${isMoving ? '#ff0040' : '#00ff41'};">
                        ${device.movement}%
                    </div>
                    <div class="confidence-label">CONFIDENCE</div>
                </div>
            `;
            movementGrid.appendChild(item);
        });
    }

    renderSignalHistory() {
        const ctx = this.historyCtx;
        const width = this.historyCanvas.width;
        const height = this.historyCanvas.height;
        const history = this.signalHistory.get(this.selectedDevice) || [];

        // Clear canvas
        ctx.fillStyle = '#0f1729';
        ctx.fillRect(0, 0, width, height);

        if (history.length < 2) return;

        // Draw grid
        ctx.strokeStyle = '#1a2332';
        ctx.lineWidth = 1;
        for (let i = 0; i < 5; i++) {
            const y = (height / 4) * i;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }

        // Draw signal line
        ctx.beginPath();
        ctx.strokeStyle = '#00ff41';
        ctx.lineWidth = 2;

        const stepX = width / (this.maxHistoryLength - 1);

        history.forEach((rssi, index) => {
            const x = index * stepX;
            // Map RSSI (-100 to -30) to canvas height
            const normalizedRSSI = (rssi + 100) / 70; // 0 to 1
            const y = height - (normalizedRSSI * height);

            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });

        ctx.stroke();

        // Draw points
        history.forEach((rssi, index) => {
            const x = index * stepX;
            const normalizedRSSI = (rssi + 100) / 70;
            const y = height - (normalizedRSSI * height);

            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = '#00ff41';
            ctx.fill();
        });
    }

    updateTimestamp() {
        const timestamp = document.getElementById('timestamp');
        const now = new Date();
        const formatted = now.toLocaleString('en-US', {
            hour12: false,
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        timestamp.textContent = formatted;
    }

    startMonitoring() {
        // Initial update
        this.updateDevices();

        // Update devices periodically
        setInterval(() => {
            this.updateDevices();
        }, this.updateInterval);

        // Update timestamp every second
        setInterval(() => {
            this.updateTimestamp();
        }, 1000);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new BLEProximityMonitor();
});
