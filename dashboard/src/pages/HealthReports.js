import React, { useState, useEffect } from 'react';

const HealthReports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
    const interval = setInterval(fetchReports, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchReports = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/health/reports');
      if (response.ok) {
        const data = await response.json();
        setReports(data);
      }
    } catch (error) {
      console.error('Error fetching reports:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteReport = async (id) => {
    if (!window.confirm('Are you sure you want to delete this report?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/health/reports/${id}`, {
        method: 'DELETE'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        // Remove from UI immediately
        setReports(reports.filter(r => r.id !== id));
        alert('✅ Report deleted successfully');
        // Refresh data after a short delay
        setTimeout(() => fetchReports(), 500);
      } else {
        alert('❌ Failed to delete report: ' + (result.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert('❌ Error deleting report: ' + error.message);
    }
  };

  const markCured = async (id) => {
    if (!window.confirm('Mark this patient as cured?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/health/reports/${id}/cure`, {
        method: 'PUT'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        // Remove from UI immediately
        setReports(reports.filter(r => r.id !== id));
        alert('✅ Patient marked as cured successfully');
        // Refresh data after a short delay
        setTimeout(() => fetchReports(), 500);
      } else {
        alert('❌ Failed to mark patient as cured: ' + (result.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Cure error:', error);
      alert('❌ Error updating patient status: ' + error.message);
    }
  };

  if (loading) return <div style={{color: 'white', textAlign: 'center', padding: '50px'}}>Loading reports...</div>;

  return (
    <div style={{padding: '20px', color: 'white'}}>
      <h1 style={{textAlign: 'center', marginBottom: '30px'}}>🏥 Health Reports Management</h1>
      
      <div style={{
        background: 'rgba(255,255,255,0.1)', 
        borderRadius: '20px', 
        padding: '20px'
      }}>
        <h3 style={{marginBottom: '20px'}}>Active Health Cases ({reports.length})</h3>
        
        {reports.length === 0 ? (
          <div style={{textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.7)'}}>
            No active health reports
          </div>
        ) : (
          <div style={{display: 'grid', gap: '15px'}}>
            {reports.map(report => (
              <div key={report.id} style={{
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '12px',
                padding: '20px',
                borderLeft: `4px solid ${getSeverityColor(report.severity)}`
              }}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                  <div style={{flex: 1}}>
                    <div style={{display: 'flex', gap: '15px', marginBottom: '10px'}}>
                      <span style={{
                        background: getSeverityColor(report.severity),
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '12px',
                        fontWeight: 'bold'
                      }}>
                        {report.severity?.toUpperCase()}
                      </span>
                      <span style={{
                        background: 'rgba(255,255,255,0.2)',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '12px'
                      }}>
                        ID: {report.id}
                      </span>
                    </div>
                    
                    <h4 style={{margin: '10px 0', fontSize: '18px'}}>
                      {report.disease?.replace('_', ' ').toUpperCase()}
                    </h4>
                    
                    <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', marginTop: '15px'}}>
                      <div>
                        <strong>📍 Location:</strong><br/>
                        {report.location}
                      </div>
                      <div>
                        <strong>👤 Patient:</strong><br/>
                        Age: {report.patient_age || 'N/A'}, Gender: {report.patient_gender || 'N/A'}
                      </div>
                      <div>
                        <strong>📅 Reported:</strong><br/>
                        {new Date(report.reported_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  
                  <div style={{display: 'flex', flexDirection: 'column', gap: '10px', marginLeft: '20px'}}>
                    <button
                      onClick={() => markCured(report.id)}
                      style={{
                        background: 'linear-gradient(45deg, #2ecc71, #27ae60)',
                        color: 'white',
                        border: 'none',
                        padding: '8px 16px',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '12px',
                        fontWeight: 'bold'
                      }}
                    >
                      ✅ Mark Cured
                    </button>
                    
                    <button
                      onClick={() => deleteReport(report.id)}
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
                      🗑️ Delete
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
    case 'critical': return '#e74c3c';
    case 'severe': return '#e67e22';
    case 'high': return '#f39c12';
    case 'moderate': return '#f1c40f';
    case 'medium': return '#3498db';
    case 'mild': return '#2ecc71';
    case 'low': return '#95a5a6';
    default: return '#95a5a6';
  }
};

export default HealthReports;