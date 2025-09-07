import React, { useState, useEffect } from 'react';

const WaterQuality = () => {
  const [waterSources, setWaterSources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWaterSources();
    const interval = setInterval(fetchWaterSources, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchWaterSources = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/water/sources');
      if (response.ok) {
        const data = await response.json();
        setWaterSources(data);
      }
    } catch (error) {
      console.error('Error fetching water sources:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteWaterSource = async (id) => {
    if (!window.confirm('Are you sure you want to delete this water source report?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/water/sources/${id}`, {
        method: 'DELETE'
      });
      
      const result = await response.json();
      
      if (response.ok && result.status === 'success') {
        // Remove from UI immediately
        setWaterSources(waterSources.filter(w => w.id !== id));
        alert('✅ Water source report deleted successfully');
        // Refresh data after a short delay
        setTimeout(() => fetchWaterSources(), 500);
      } else {
        alert('❌ Failed to delete water source report: ' + (result.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert('❌ Error deleting water source report: ' + error.message);
    }
  };

  if (loading) return <div style={{color: 'white', textAlign: 'center', padding: '50px'}}>Loading water sources...</div>;

  const safeWater = waterSources.filter(w => w.is_safe);
  const contaminatedWater = waterSources.filter(w => !w.is_safe);

  return (
    <div style={{padding: '20px', color: 'white'}}>
      <h1 style={{textAlign: 'center', marginBottom: '30px'}}>💧 Water Quality Management</h1>
      
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px', marginBottom: '30px'}}>
        <div style={{background: 'rgba(46, 204, 113, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#27ae60'}}>{safeWater.length}</div>
          <div>Safe Sources</div>
        </div>
        <div style={{background: 'rgba(231, 76, 60, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#e74c3c'}}>{contaminatedWater.length}</div>
          <div>Contaminated Sources</div>
        </div>
        <div style={{background: 'rgba(52, 152, 219, 0.2)', borderRadius: '15px', padding: '20px', textAlign: 'center'}}>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#3498db'}}>{waterSources.length}</div>
          <div>Total Sources</div>
        </div>
      </div>

      <div style={{
        background: 'rgba(255,255,255,0.1)', 
        borderRadius: '20px', 
        padding: '20px'
      }}>
        <h3 style={{marginBottom: '20px'}}>Water Source Reports ({waterSources.length})</h3>
        
        {waterSources.length === 0 ? (
          <div style={{textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.7)'}}>
            No water source reports available
          </div>
        ) : (
          <div style={{display: 'grid', gap: '15px'}}>
            {waterSources.map(source => (
              <div key={source.id} style={{
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '12px',
                padding: '20px',
                borderLeft: `4px solid ${source.is_safe ? '#2ecc71' : '#e74c3c'}`
              }}>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                  <div style={{flex: 1}}>
                    <div style={{display: 'flex', gap: '15px', marginBottom: '10px'}}>
                      <span style={{
                        background: source.is_safe ? '#2ecc71' : '#e74c3c',
                        color: 'white',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '12px',
                        fontWeight: 'bold'
                      }}>
                        {source.is_safe ? '✅ SAFE' : '❌ CONTAMINATED'}
                      </span>
                      <span style={{
                        background: 'rgba(255,255,255,0.2)',
                        padding: '4px 12px',
                        borderRadius: '15px',
                        fontSize: '12px'
                      }}>
                        ID: {source.id}
                      </span>
                    </div>
                    
                    <h4 style={{margin: '10px 0', fontSize: '18px'}}>
                      📍 {source.location}
                    </h4>
                    
                    <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px', marginTop: '15px'}}>
                      <div>
                        <strong>🧪 pH Level:</strong><br/>
                        <span style={{color: getPHColor(source.ph_level)}}>{source.ph_level}</span>
                        <small style={{display: 'block', opacity: 0.7}}>(Safe: 6.5-8.5)</small>
                      </div>
                      <div>
                        <strong>🌊 Turbidity:</strong><br/>
                        <span style={{color: getTurbidityColor(source.turbidity)}}>{source.turbidity} NTU</span>
                        <small style={{display: 'block', opacity: 0.7}}>(Safe: ≤5)</small>
                      </div>
                      <div>
                        <strong>🦠 Bacteria:</strong><br/>
                        <span style={{color: getBacteriaColor(source.bacterial_count)}}>{source.bacterial_count} CFU/ml</span>
                        <small style={{display: 'block', opacity: 0.7}}>(Safe: ≤10)</small>
                      </div>
                      <div>
                        <strong>🌡️ Temperature:</strong><br/>
                        {source.temperature}°C
                      </div>
                      <div>
                        <strong>💧 Source Type:</strong><br/>
                        {source.source_type?.toUpperCase()}
                      </div>
                      <div>
                        <strong>📅 Tested:</strong><br/>
                        {new Date(source.tested_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  
                  <div style={{marginLeft: '20px'}}>
                    <button
                      onClick={() => deleteWaterSource(source.id)}
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

const getPHColor = (ph) => {
  if (ph >= 6.5 && ph <= 8.5) return '#2ecc71';
  return '#e74c3c';
};

const getTurbidityColor = (turbidity) => {
  if (turbidity <= 5) return '#2ecc71';
  return '#e74c3c';
};

const getBacteriaColor = (count) => {
  if (count <= 10) return '#2ecc71';
  return '#e74c3c';
};

export default WaterQuality;