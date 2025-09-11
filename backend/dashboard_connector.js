// Dashboard Connector - Bridge between mobile.html and React Dashboard Components
class DashboardConnector {
    constructor() {
        this.API_URL = 'http://localhost:8000/api';
        this.dashboardURL = 'http://localhost:3000'; // React dashboard URL
        this.init();
    }

    init() {
        // Listen for mobile app data updates
        window.addEventListener('healthDataUpdate', (event) => {
            this.syncWithDashboard(event.detail);
        });

        // Auto-sync every 10 seconds
        setInterval(() => {
            this.syncAllData();
        }, 10000);
    }

    // Sync data from mobile app to dashboard components
    async syncWithDashboard(mobileData) {
        try {
            // Send data to each dashboard component endpoint
            await Promise.all([
                this.updateHealthReports(mobileData),
                this.updateWaterQuality(mobileData),
                this.updateAlerts(mobileData),
                this.updateMaps(mobileData),
                this.updatePredictions(mobileData),
                this.updateDashboardStats(mobileData)
            ]);
        } catch (error) {
            console.error('Dashboard sync failed:', error);
        }
    }

    // Update Health Reports component
    async updateHealthReports(data) {
        const healthReports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
        
        // Format for dashboard
        const formattedReports = healthReports.map(report => ({
            id: report.id || Date.now(),
            disease: report.disease || report.data?.disease,
            severity: report.severity || report.data?.severity || 'mild',
            location: report.location || report.data?.location,
            patient_age: report.patient_age || report.data?.patient_age || 25,
            patient_gender: report.patient_gender || report.data?.patient_gender || 'unknown',
            reported_at: report.timestamp || new Date().toISOString()
        }));

        // Store for dashboard access
        localStorage.setItem('dashboardHealthReports', JSON.stringify(formattedReports));
        
        // Trigger dashboard update
        this.notifyDashboard('healthReports', formattedReports);
    }

    // Update Water Quality component
    async updateWaterQuality(data) {
        const waterReports = JSON.parse(localStorage.getItem('waterReports') || '[]');
        
        const formattedWater = waterReports.map(report => ({
            id: report.id || Date.now(),
            location: report.location,
            is_safe: report.is_safe,
            ph_level: report.ph_level,
            turbidity: report.turbidity,
            bacterial_count: report.bacterial_count,
            temperature: report.temperature,
            source_type: report.source_type,
            tested_at: report.timestamp || new Date().toISOString()
        }));

        localStorage.setItem('dashboardWaterReports', JSON.stringify(formattedWater));
        this.notifyDashboard('waterQuality', formattedWater);
    }

    // Update Alerts component
    async updateAlerts(data) {
        const alerts = JSON.parse(localStorage.getItem('systemAlerts') || '[]');
        
        const formattedAlerts = alerts.map(alert => ({
            id: alert.id || Date.now(),
            severity: alert.severity || 'medium',
            location: alert.location || 'System',
            message: alert.message || 'Health surveillance alert',
            created_at: alert.timestamp || new Date().toISOString()
        }));

        localStorage.setItem('dashboardAlerts', JSON.stringify(formattedAlerts));
        this.notifyDashboard('alerts', formattedAlerts);
    }

    // Update Maps component
    async updateMaps(data) {
        const healthReports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
        const waterReports = JSON.parse(localStorage.getItem('waterReports') || '[]');
        const alerts = JSON.parse(localStorage.getItem('systemAlerts') || '[]');

        const mapData = {
            health: healthReports,
            water: waterReports,
            alerts: alerts,
            lastUpdate: new Date().toISOString()
        };

        localStorage.setItem('dashboardMapData', JSON.stringify(mapData));
        this.notifyDashboard('maps', mapData);
    }

    // Update Predictions component
    async updatePredictions(data) {
        const healthReports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
        
        // Simple prediction logic
        const predictions = this.generatePredictions(healthReports);
        
        localStorage.setItem('dashboardPredictions', JSON.stringify(predictions));
        this.notifyDashboard('predictions', predictions);
    }

    // Update Dashboard Stats component
    async updateDashboardStats(data) {
        const healthReports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
        const waterReports = JSON.parse(localStorage.getItem('waterReports') || '[]');
        const alerts = JSON.parse(localStorage.getItem('systemAlerts') || '[]');

        const stats = {
            healthStats: {
                total_reports: healthReports.length,
                recent_reports: healthReports.filter(r => this.isRecent(r.timestamp)).length,
                by_disease: this.groupBy(healthReports, 'disease'),
                by_severity: this.groupBy(healthReports, 'severity')
            },
            alertStats: {
                total_active_alerts: alerts.length,
                by_severity: this.groupBy(alerts, 'severity')
            },
            waterStats: {
                total_sources: waterReports.length,
                contaminated_sources: waterReports.filter(w => !w.is_safe).length,
                safe_sources: waterReports.filter(w => w.is_safe).length
            }
        };

        localStorage.setItem('dashboardStats', JSON.stringify(stats));
        this.notifyDashboard('dashboard', stats);
    }

    // Generate AI predictions
    generatePredictions(healthReports) {
        const recentReports = healthReports.filter(r => this.isRecent(r.timestamp));
        const diseaseCount = this.groupBy(recentReports, 'disease');
        
        const predictions = [];
        
        Object.entries(diseaseCount).forEach(([disease, count]) => {
            if (count > 2) { // Only predict if there are multiple cases
                const riskScore = Math.min(95, count * 15 + Math.random() * 20);
                
                predictions.push({
                    id: predictions.length + 1,
                    disease: disease,
                    location: this.getMostAffectedLocation(recentReports, disease),
                    riskScore: Math.round(riskScore),
                    predictedCases: Math.round(count * 1.5 + Math.random() * 5),
                    confidence: Math.round(Math.min(95, riskScore + 10)),
                    factors: this.getPredictionFactors(disease),
                    timeframe: riskScore > 70 ? '3-7 days' : '7-14 days'
                });
            }
        });

        return predictions;
    }

    // Helper functions
    isRecent(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffDays = (now - date) / (1000 * 60 * 60 * 24);
        return diffDays <= 7;
    }

    groupBy(array, key) {
        return array.reduce((groups, item) => {
            const value = item[key] || item.data?.[key] || 'unknown';
            groups[value] = (groups[value] || 0) + 1;
            return groups;
        }, {});
    }

    getMostAffectedLocation(reports, disease) {
        const locations = reports
            .filter(r => (r.disease || r.data?.disease) === disease)
            .map(r => r.location || r.data?.location)
            .filter(Boolean);
        
        const locationCount = this.groupBy(locations.map(l => ({ location: l })), 'location');
        return Object.keys(locationCount).reduce((a, b) => 
            locationCount[a] > locationCount[b] ? a : b
        ) || 'Unknown';
    }

    getPredictionFactors(disease) {
        const factors = {
            'diarrhea': ['Water contamination', 'Poor sanitation', 'Monsoon season'],
            'cholera': ['Contaminated water', 'Poor hygiene', 'Overcrowding'],
            'typhoid': ['Food contamination', 'Poor water quality', 'Inadequate sanitation'],
            'hepatitis_a': ['Contaminated food/water', 'Poor hygiene', 'Close contact']
        };
        
        return factors[disease] || ['Environmental factors', 'Seasonal patterns'];
    }

    // Notify dashboard components
    notifyDashboard(component, data) {
        // Create custom event for dashboard components
        const event = new CustomEvent('dashboardUpdate', {
            detail: {
                component: component,
                data: data,
                timestamp: new Date().toISOString()
            }
        });
        
        window.dispatchEvent(event);
        
        // Also store in localStorage for dashboard components to access
        localStorage.setItem(`dashboard_${component}_data`, JSON.stringify(data));
        localStorage.setItem(`dashboard_${component}_lastUpdate`, new Date().toISOString());
    }

    // Sync all data
    async syncAllData() {
        const mobileData = {
            reports: localStorage.getItem('offlineReports') || '[]',
            waterReports: localStorage.getItem('waterReports') || '[]',
            alerts: localStorage.getItem('systemAlerts') || '[]'
        };
        
        await this.syncWithDashboard(mobileData);
    }

    // API methods for dashboard components to use
    async getHealthReports() {
        return JSON.parse(localStorage.getItem('dashboardHealthReports') || '[]');
    }

    async getWaterSources() {
        return JSON.parse(localStorage.getItem('dashboardWaterReports') || '[]');
    }

    async getAlerts() {
        return JSON.parse(localStorage.getItem('dashboardAlerts') || '[]');
    }

    async getPredictions() {
        return JSON.parse(localStorage.getItem('dashboardPredictions') || '[]');
    }

    async getStats() {
        return JSON.parse(localStorage.getItem('dashboardStats') || '{}');
    }

    async getMapData() {
        return JSON.parse(localStorage.getItem('dashboardMapData') || '{}');
    }

    // Delete methods
    async deleteHealthReport(id) {
        const reports = await this.getHealthReports();
        const filtered = reports.filter(r => r.id !== id);
        localStorage.setItem('dashboardHealthReports', JSON.stringify(filtered));
        
        // Also remove from offline reports
        const offlineReports = JSON.parse(localStorage.getItem('offlineReports') || '[]');
        const filteredOffline = offlineReports.filter(r => r.id !== id);
        localStorage.setItem('offlineReports', JSON.stringify(filteredOffline));
        
        this.notifyDashboard('healthReports', filtered);
        return { status: 'success' };
    }

    async deleteWaterSource(id) {
        const sources = await this.getWaterSources();
        const filtered = sources.filter(s => s.id !== id);
        localStorage.setItem('dashboardWaterReports', JSON.stringify(filtered));
        
        const waterReports = JSON.parse(localStorage.getItem('waterReports') || '[]');
        const filteredWater = waterReports.filter(w => w.id !== id);
        localStorage.setItem('waterReports', JSON.stringify(filteredWater));
        
        this.notifyDashboard('waterQuality', filtered);
        return { status: 'success' };
    }

    async deleteAlert(id) {
        const alerts = await this.getAlerts();
        const filtered = alerts.filter(a => a.id !== id);
        localStorage.setItem('dashboardAlerts', JSON.stringify(filtered));
        
        const systemAlerts = JSON.parse(localStorage.getItem('systemAlerts') || '[]');
        const filteredSystem = systemAlerts.filter(a => a.id !== id);
        localStorage.setItem('systemAlerts', JSON.stringify(filteredSystem));
        
        this.notifyDashboard('alerts', filtered);
        return { status: 'success' };
    }
}

// Initialize dashboard connector
window.dashboardConnector = new DashboardConnector();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardConnector;
}