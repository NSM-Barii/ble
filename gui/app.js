// Device tracking and visualization
class BLEProximityMonitor {
    constructor() {
        this.devices = new Map();
        this.signalHistory = new Map();
        this.wardrivingData = {};
        this.maxHistoryLength = 20;
        this.updateInterval = 1000; // 1 second
        this.currentTab = 'dashboard';

        this.radarCanvas = document.getElementById('radar-canvas');
        this.radarCtx = this.radarCanvas.getContext('2d');
        this.historyCanvas = document.getElementById('history-canvas');
        this.historyCtx = this.historyCanvas.getContext('2d');

        this.selectedDevice = null;
        this.searchFilter = '';
        this.manufacturerFilter = 'all';

        this.initCanvas();
        this.initTabs();
        this.startMonitoring();
        this.updateTimestamp();
    }

    initTabs() {
        const tabs = document.querySelectorAll('.nav-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.dataset.tab;
                this.switchTab(tabName);
            });
        });

        // Export button
        document.getElementById('export-btn').addEventListener('click', () => {
            this.exportData();
        });

        // Filters
        document.getElementById('search-filter').addEventListener('input', (e) => {
            this.searchFilter = e.target.value.toLowerCase();
            this.renderWardrivingTable();
        });

        document.getElementById('manufacturer-filter').addEventListener('change', (e) => {
            this.manufacturerFilter = e.target.value;
            this.renderWardrivingTable();
        });
    }

    switchTab(tabName) {
        this.currentTab = tabName;

        // Update tab buttons
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.tab === tabName) {
                tab.classList.add('active');
            }
        });

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Fetch wardriving data if switching to that tab
        if (tabName === 'wardriving') {
            this.fetchWardrivingData();
        }
    }

    initCanvas() {
        // Set canvas size
        this.radarCanvas.width = 600;
        this.radarCanvas.height = 600;
        this.historyCanvas.width = 300;
        this.historyCanvas.height = 200;
    }

    getManufacturerIcon(manufacturer) {
        // Return emoji/icon for popular manufacturers
        if (!manufacturer) return '';

        const manuf = manufacturer.toLowerCase();

        if (manuf.includes('apple')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23ffffff"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>';
        if (manuf.includes('samsung')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%231428A0"><rect width="24" height="24" rx="2"/><text x="12" y="17" font-size="14" fill="white" text-anchor="middle" font-family="Arial">S</text></svg>';
        if (manuf.includes('google')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%234285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="%2334A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="%23FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="%23EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>';
        if (manuf.includes('microsoft')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%23f25022" d="M0 0h11.377v11.372H0z"/><path fill="%2300a4ef" d="M12.623 0H24v11.372H12.623z"/><path fill="%237fba00" d="M0 12.623h11.377V24H0z"/><path fill="%23ffb900" d="M12.623 12.623H24V24H12.623z"/></svg>';
        if (manuf.includes('sony')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23000000"><rect width="24" height="24" fill="white"/><text x="12" y="17" font-size="12" fill="black" text-anchor="middle" font-family="Arial" font-weight="bold">SONY</text></svg>';
        if (manuf.includes('intel')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%230071C5"><rect width="24" height="24" rx="2"/><text x="12" y="17" font-size="10" fill="white" text-anchor="middle" font-family="Arial" font-weight="bold">INTEL</text></svg>';
        if (manuf.includes('lg')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23A50034"><circle cx="12" cy="12" r="11"/><text x="12" y="16" font-size="12" fill="white" text-anchor="middle" font-family="Arial" font-weight="bold">LG</text></svg>';
        if (manuf.includes('dell')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23007DB8"><rect width="24" height="24" rx="2"/><text x="12" y="17" font-size="10" fill="white" text-anchor="middle" font-family="Arial" font-weight="bold">DELL</text></svg>';
        if (manuf.includes('hp') || manuf.includes('hewlett')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%230096D6"><rect width="24" height="24" rx="2"/><text x="12" y="17" font-size="14" fill="white" text-anchor="middle" font-family="Arial" font-weight="bold">hp</text></svg>';
        if (manuf.includes('texas instruments')) return 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23CC0000"><rect width="24" height="24" rx="2"/><text x="12" y="17" font-size="12" fill="white" text-anchor="middle" font-family="Arial" font-weight="bold">TI</text></svg>';

        return '';
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

            const iconUrl = this.getManufacturerIcon(device.manufacturer);

            item.innerHTML = `
                <div class="device-header">
                    ${iconUrl ? `<img src="${iconUrl}" class="manuf-icon" alt="${device.manufacturer}">` : ''}
                    <div class="device-name">${device.name}</div>
                </div>
                <div class="device-mac">${device.mac}</div>
                ${device.manufacturer && device.manufacturer !== 'Unknown' ? `<div class="device-vendor">${device.manufacturer}</div>` : ''}
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
            { radius: 100, color: '#ff0040', label: 'immediate' },
            { radius: 200, color: '#ffa500', label: 'near' },
            { radius: 290, color: '#00ff41', label: 'far' }
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

        Array.from(this.devices.values()).forEach((device) => {
            let radius;
            let color;

            if (device.proximity === 'immediate') {
                radius = 80;
                color = '#ff0040';
            } else if (device.proximity === 'near') {
                radius = 180;
                color = '#ffa500';
            } else {
                radius = 270;
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

    async fetchWardrivingData() {
        try {
            const response = await fetch('/api/wardriving');
            const data = await response.json();
            this.wardrivingData = data;
            this.renderWardrivingTable();
            this.updateManufacturerFilter();
        } catch (error) {
            console.error('Error fetching wardriving data:', error);
        }
    }

    updateManufacturerFilter() {
        const manufacturers = new Set();
        Object.values(this.wardrivingData).forEach(device => {
            if (device.manuf && device.manuf !== 'Unknown') {
                manufacturers.add(device.manuf);
            }
        });

        const select = document.getElementById('manufacturer-filter');
        const currentValue = select.value;

        select.innerHTML = '<option value="all">ALL MANUFACTURERS</option>';
        Array.from(manufacturers).sort().forEach(manuf => {
            const option = document.createElement('option');
            option.value = manuf;
            option.textContent = manuf.toUpperCase();
            select.appendChild(option);
        });

        select.value = currentValue;
    }

    renderWardrivingTable() {
        const tbody = document.getElementById('wardriving-tbody');
        const totalBadge = document.getElementById('total-captured');

        // Filter data
        let filteredData = Object.entries(this.wardrivingData).filter(([index, device]) => {
            const searchMatch = !this.searchFilter ||
                device.addr.toLowerCase().includes(this.searchFilter) ||
                (device.name && device.name.toLowerCase().includes(this.searchFilter)) ||
                (device.vendor && device.vendor.toLowerCase().includes(this.searchFilter)) ||
                (device.manuf && device.manuf.toLowerCase().includes(this.searchFilter));

            const manufMatch = this.manufacturerFilter === 'all' ||
                device.manuf === this.manufacturerFilter;

            return searchMatch && manufMatch;
        });

        totalBadge.textContent = `${filteredData.length} DEVICES`;
        tbody.innerHTML = '';

        filteredData.forEach(([index, device]) => {
            const row = document.createElement('tr');

            const rssi = device.rssi || -100;
            let rssiClass = 'rssi-weak';
            if (rssi >= -50) rssiClass = 'rssi-good';
            else if (rssi >= -70) rssiClass = 'rssi-medium';

            const iconUrl = this.getManufacturerIcon(device.manuf || device.vendor);
            const uuidStr = Array.isArray(device.uuid) ? device.uuid.join(', ') : (device.uuid || 'N/A');

            row.innerHTML = `
                <td class="index-col">${index}</td>
                <td>${iconUrl ? `<img src="${iconUrl}" class="table-icon" alt="">` : '-'}</td>
                <td>${device.name || 'Unknown'}</td>
                <td class="mac-col">${device.addr}</td>
                <td>${device.manuf || 'Unknown'}</td>
                <td>${device.vendor || 'Unknown'}</td>
                <td class="rssi-col ${rssiClass}">${rssi} dBm</td>
                <td class="uuid-list" title="${uuidStr}">${uuidStr}</td>
                <td>${new Date().toLocaleDateString()}</td>
            `;

            tbody.appendChild(row);
        });
    }

    exportData() {
        const dataStr = JSON.stringify(this.wardrivingData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `bluemap_wardriving_${Date.now()}.json`;
        link.click();

        URL.revokeObjectURL(url);
    }

    startMonitoring() {
        // Initial update
        this.updateDevices();

        // Update devices periodically
        setInterval(() => {
            this.updateDevices();

            // Auto-update wardriving tab if active
            if (this.currentTab === 'wardriving') {
                this.fetchWardrivingData();
            }
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
