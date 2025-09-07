import React, { useState, useEffect } from 'react';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/alerts');
      if (response.ok) {
        const data = await response.json();
        setAlerts(data);
      }
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteAlert = async (id) => {
    if (!window.confirm('Are you sure you want to resolve/delete this alert?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/alerts/${id}`, {
        method: 'DELETE'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        // Remove from UI immediately
        setAlerts(alerts.filter(a => a.id !== id));
        alert('✅ Alert resolved successfully');
        // Refresh data after a short delay
        setTimeout(() => fetchAlerts(), 500);
      } else {
        alert('❌ Failed to resolve alert: ' + (result.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert('❌ Error resolving alert: ' + error.message);
    }
  };

  if (loading) return <div style={{color: 'white', textAlign: 'center', padding: '50px'}}>Loading alerts...</div>;

  const criticalAlerts = alerts.filter(a => a.severity === 'critical');
  const highAlerts = alerts.filter(a => a.severity === 'high');
  const mediumAlerts = alerts.filter(a => a.severity === 'medium');
  const lowAlerts = alerts.filter(a => a.severity === 'low');

  return (
    <div style={{padding: '20px', color: 'white'}}>
      <h1 style={{textAlign: 'center', marginBottom: '30px'}}>🚨 Alert Management System</h1>
      
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px', marginBottom: '30px'}}>
        <div style={{background: 'rgba(192, 57, 43, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#c0392b'}}>{criticalAlerts.length}</div>
          <div>Critical</div>
        </div>
        <div style={{background: 'rgba(231, 76, 60, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#e74c3c'}}>{highAlerts.length}</div>
          <div>High</div>
        </div>
        <div style={{background: 'rgba(243, 156, 18, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#f39c12'}}>{mediumAlerts.length}</div>
          <div>Medium</div>
        </div>
        <div style={{background: 'rgba(46, 204, 113, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#2ecc71'}}>{lowAlerts.length}</div>
          <div>Low</div>
        </div>
      </div>

      <div style={{
        background: 'rgba(255,255,255,0.1)', 
        borderRadius: '20px', 
        padding: '20px'
      }}>
        <h3 style={{marginBottom: '20px'}}>Active Alerts ({alerts.length})</h3>
        
        {alerts.length === 0 ? (
          <div style={{textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.7)'}}>
            ✅ No active alerts - All systems normal
          </div>
        ) : (
          <div style={{display: 'grid', gap: '15px'}}>
            {alerts.map(alert => (
              <div key={alert.id} style={{
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '12px',
                padding: '20px',
                borderLeft: `4px solid ${getSeverityColor(alert.severity)}`,
                animation: alert.severity === 'critical' ? 'pulse 2s infinite' : 'none'
              }}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                  <div style={{flex: 1}}>
                    <div style={{display: 'flex', gap: '15px', marginBottom: '10px'}}>
                      <span style={{
                        background: getSeverityColor(alert.severity),
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '12px',
                        fontWeight: 'bold'
                      }}>
                        {getSeverityIcon(alert.severity)} {alert.severity?.toUpperCase()}
                      </span>
                      <span style={{
                        background: 'rgba(255,255,255,0.2)',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '12px'
                      }}>
                        ID: {alert.id}
                      </span>
                    </div>
                    
                    <h4 style={{margin: '10px 0', fontSize: '18px'}}>
                      📍 {alert.location || 'System Alert'}
                    </h4>
                    
                    <div style={{
                      background: 'rgba(255,255,255,0.1)',
                      padding: '15px',
                      borderRadius: '8px',
                      marginTop: '15px'
                    }}>
                      <strong>Alert Message:</strong><br/>
                      {alert.message || 'No message provided'}
                    </div>
                    
                    <div style={{marginTop: '15px', fontSize: '14px', opacity: 0.8}}>
                      <strong>📅 Created:</strong> {new Date(alert.created_at).toLocaleString()}
                    </div>
                  </div>
                  
                  <div style={{marginLeft: '20px'}}>
                    <button
                      onClick={() => deleteAlert(alert.id)}
                      style={{
                        background: 'linear-gradient(45deg, #e74c3c, #c0392b)',
                        color: 'white',
                        border: 'none',
                        padding: '8px 16px',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '12px',
                        fontWeight: 'bold'
                      }}
                    >
                      🗑️ Resolve
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const getSeverityColor = (severity) => {
  switch (severity?.toLowerCase()) {
    case 'critical': return '#c0392b';
    case 'high': return '#e74c3c';
    case 'medium': return '#f39c12';
    case 'low': return '#2ecc71';
    default: return '#95a5a6';
  }
};

const getSeverityIcon = (severity) => {
  switch (severity?.toLowerCase()) {
    case 'critical': return '🔴';
    case 'high': return '🟠';
    case 'medium': return '🟡';
    case 'low': return '🟢';
    default: return '⚪';
  }
};

export default Alerts;