from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from backend.models.models import Alert
from backend.schemas.alert_schemas import AlertCreate, AlertResponse
# from services.notification_service import send_alert_notifications

from datetime import datetime

async def send_alert_notifications(alert):
    """Simple notification placeholder"""
    print(f"ALERT: {alert.severity.upper()} - {alert.message} at {alert.location}")
    return {"status": "sent"}

router = APIRouter()

@router.post("/", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    db_alert = Alert(
        alert_type=alert.alert_type,
        location=alert.location,
        message=alert.message,
        severity=alert.severity,
        affected_population=alert.affected_population
    )
    
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    # Send notifications to relevant authorities
    await send_alert_notifications(db_alert)
    
    return db_alert

@router.get("/")
async def get_alerts(location: str = None, active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Alert)
    if location:
        query = query.filter(Alert.location.contains(location))
    if active_only:
        query = query.filter(Alert.is_resolved == False)
    return query.order_by(Alert.created_at.desc()).all()

@router.put("/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    db.commit()
    return {"message": "Alert resolved successfully"}

@router.get("/dashboard")
async def get_alert_dashboard(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
    
    dashboard = {
        "total_active_alerts": len(alerts),
        "by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
        "by_type": {},
        "recent_alerts": [a for a in alerts if (datetime.now() - a.created_at).total_seconds() <= 86400]
    }
    
    for alert in alerts:
        dashboard["by_severity"][alert.severity] += 1
        dashboard["by_type"][alert.alert_type] = dashboard["by_type"].get(alert.alert_type, 0) + 1
    
    return dashboard