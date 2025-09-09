// Data Bridge for connecting Mobile App, Admin Dashboard, and Map Integration
class HealthSurveillanceDataBridge {
    constructor() {
        this.data = {
            healthReports: [],
            waterReports: [],
            alerts: [],
            predictions: {},
            hotspots: [],
            resources: {}
        };
        
        this.subscribers = [];
        this.init();
    }
    
    init() {
        // Load existing data from localStorage
        this.loadStoredData();
        
        // Set up event listeners for real-time updates
        window.addEventListener('healthDataUpdate', (event) => {
            this.handleDataUpdate(event.detail);
        });
        
        window.addEventListener('triggerPrediction', (event) => {
            this.updatePredictions(event.detail);
        });
        
        // Auto-sync every 30 seconds
        setInterval(() => {
            this.syncData();
        }, 30000);
    }
    
    loadStoredData() {
        try {
            // Load from localStorage
            const storedData = localStorage.getItem('healthSurveillanceData');
            if (storedData) {
                const parsed = JSON.parse(storedData);
                this.data = { ...this.data, ...parsed };
            }
            
            // Load offline reports
            const offlineReports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
            this.data.healthReports = [...this.data.healthReports, ...offlineReports];
            
            // Load mobile app data
            const mobileData = localStorage.getItem('mobileAppData');
            if (mobileData) {
                const parsed = JSON.parse(mobileData);
                this.processMobileData(parsed);
            }
        } catch (error) {
            console.error('Error loading stored data:', error);
        }
    }
    
    processMobileData(mobileData) {
        if (mobileData.reports) {
            const reports = JSON.parse(mobileData.reports);
            this.data.healthReports = [...this.data.healthReports, ...reports];
        }
        
        // Update user location
        if (mobileData.location) {
            this.data.userLocation = mobileData.location;
        }
        
        // Update language preference
        if (mobileData.language) {
            this.data.language = mobileData.language;
        }
    }
    
    handleDataUpdate(updateData) {
        // Process new health reports
        if (updateData.newReport) {
            this.data.healthReports.push(updateData.newReport);
            this.generateHotspots();
            this.notifySubscribers('healthReportAdded', updateData.newReport);
        }
        
        // Update statistics
        this.updateStatistics();
        
        // Save to localStorage
        this.saveData();
    }
    
    updatePredictions(predictionInput) {
        // Simple AI prediction logic
        const { newReport, existingReports, location } = predictionInput;
        
        // Count recent reports by disease type
        const recentReports = existingReports.filter(report => {
            const reportDate = new Date(report.timestamp);
            const daysDiff = (new Date() - reportDate) / (1000 * 60 * 60 * 24);
            return daysDiff <= 7; // Last 7 days
        });
        
        const diseaseCount = {};
        recentReports.forEach(report => {
            diseaseCount[report.disease] = (diseaseCount[report.disease] || 0) + 1;
        });
        
        // Determine risk level
        const totalCases = Object.values(diseaseCount).reduce((sum, count) => sum + count, 0);
        let riskLevel = 'LOW';
        let predictedDisease = 'None';
        
        if (totalCases > 10) {
            riskLevel = 'HIGH';
        } else if (totalCases > 5) {
            riskLevel = 'MEDIUM';
        }
        
        // Find most common disease
        if (totalCases > 0) {
            predictedDisease = Object.keys(diseaseCount).reduce((a, b) => 
                diseaseCount[a] > diseaseCount[b] ? a : b
            );
        }
        
        this.data.predictions = {
            riskLevel,
            predictedDisease,
            confidence: Math.min(95, Math.max(50, totalCases * 8)),
            timeline: riskLevel === 'HIGH' ? '7-14 days' : '2-4 weeks',
            location,
            lastUpdated: new Date().toISOString(),
            recommendations: this.getRecommendations(riskLevel, predictedDisease)
        };
        
        this.notifySubscribers('predictionUpdated', this.data.predictions);
        this.saveData();
    }
    
    getRecommendations(riskLevel, disease) {
        const baseRecommendations = [
            'Increase water quality monitoring',
            'Distribute ORS packets to affected areas',
            'Launch hygiene awareness campaigns'
        ];
        
        if (riskLevel === 'HIGH') {
            baseRecommendations.push(
                'Deploy additional medical teams',
                'Set up temporary treatment centers',
                'Issue public health alerts'
            );
        }
        
        if (disease === 'cholera') {
            baseRecommendations.push('Implement strict water source isolation');
        } else if (disease === 'typhoid') {
            baseRecommendations.push('Focus on food safety inspections');
        }
        
        return baseRecommendations;
    }
    
    generateHotspots() {
        const locationCounts = {};
        
        // Count reports by location
        this.data.healthReports.forEach(report => {
            if (report.location) {
                locationCounts[report.location] = (locationCounts[report.location] || 0) + 1;
            }
        });
        
        // Generate hotspots
        this.data.hotspots = Object.entries(locationCounts)
            .map(([location, count]) => ({
                location,
                caseCount: count,
                riskLevel: count > 10 ? 'HIGH' : count > 5 ? 'MEDIUM' : 'LOW',
                coordinates: this.getLocationCoordinates(location)
            }))
            .sort((a, b) => b.caseCount - a.caseCount)
            .slice(0, 10); // Top 10 hotspots
    }
    
    getLocationCoordinates(location) {
        // Mock coordinates for common NE India locations
        const coordinates = {
            'Guwahati': { lat: 26.1445, lng: 91.7362 },
            'Dibrugarh': { lat: 27.4728, lng: 94.9120 },
            'Silchar': { lat: 24.8333, lng: 92.7789 },
            'Shillong': { lat: 25.5788, lng: 91.8933 },
            'Imphal': { lat: 24.8170, lng: 93.9368 },
            'Aizawl': { lat: 23.1645, lng: 92.9376 },
            'Agartala': { lat: 23.8315, lng: 91.2868 }
        };
        
        return coordinates[location] || { lat: 26.2006, lng: 92.9376 }; // Default to NE India center
    }
    
    updateStatistics() {
        const stats = {
            totalReports: this.data.healthReports.length,
            activeAlerts: this.data.alerts.filter(alert => alert.active).length,
            waterSources: this.data.waterReports.length,
            lastUpdate: new Date().toISOString()
        };
        
        this.data.statistics = stats;
        
        // Update UI elements if they exist
        this.updateUIElements(stats);
    }
    
    updateUIElements(stats) {
        const elements = {
            'total-reports': stats.totalReports,
            'active-alerts': stats.activeAlerts,
            'water-sources': stats.waterSources
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }
    
    subscribe(callback) {
        this.subscribers.push(callback);
    }
    
    notifySubscribers(eventType, data) {
        this.subscribers.forEach(callback => {
            try {
                callback(eventType, data);
            } catch (error) {
                console.error('Error notifying subscriber:', error);
            }
        });
    }
    
    saveData() {
        try {
            localStorage.setItem('healthSurveillanceData', JSON.stringify(this.data));
        } catch (error) {
            console.error('Error saving data:', error);
        }
    }
    
    syncData() {
        // Sync with server if online
        if (navigator.onLine) {
            this.syncWithServer();
        }
        
        // Update all connected components
        this.notifySubscribers('dataSync', this.data);
    }
    
    async syncWithServer() {
        try {
            // Sync health reports
            const unsyncedReports = this.data.healthReports.filter(report => !report.synced);
            if (unsyncedReports.length > 0) {
                // Send to server (mock for now)
                console.log('Syncing', unsyncedReports.length, 'reports with server');
                
                // Mark as synced
                unsyncedReports.forEach(report => report.synced = true);
                this.saveData();
            }
        } catch (error) {
            console.error('Server sync failed:', error);
        }
    }
    
    // Public API methods
    getHealthReports() {
        return this.data.healthReports;
    }
    
    getHotspots() {
        return this.data.hotspots;
    }
    
    getPredictions() {
        return this.data.predictions;
    }
    
    getStatistics() {
        return this.data.statistics;
    }
    
    addHealthReport(report) {
        this.handleDataUpdate({ newReport: report });
    }
    
    addWaterReport(report) {
        this.data.waterReports.push(report);
        this.updateStatistics();
        this.saveData();
        this.notifySubscribers('waterReportAdded', report);
    }
    
    createAlert(alert) {
        const newAlert = {
            ...alert,
            id: Date.now(),
            created_at: new Date().toISOString(),
            active: true
        };
        
        this.data.alerts.push(newAlert);
        this.updateStatistics();
        this.saveData();
        this.notifySubscribers('alertCreated', newAlert);
        
        return newAlert;
    }
}

// Initialize global data bridge
window.healthDataBridge = new HealthSurveillanceDataBridge();

// Export for use in other components
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HealthSurveillanceDataBridge;
}