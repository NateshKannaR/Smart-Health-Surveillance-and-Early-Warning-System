from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from backend.models.models import WaterQualityReport
from backend.schemas.water_schemas import WaterQualityCreate, WaterQualityResponse
# from services.water_analysis import analyze_water_quality

def analyze_water_quality(ph, turbidity, bacterial_count, chlorine):
    """Simple water quality analysis"""
    contamination_factors = 0
    
    if ph < 6.5 or ph > 8.5:
        contamination_factors += 1
    if turbidity > 5:
        contamination_factors += 1
    if bacterial_count > 0:
        contamination_factors += 1
    if chlorine < 0.2:
        contamination_factors += 1
        
    return contamination_factors > 0

router = APIRouter()

@router.post("/quality", response_model=WaterQualityResponse)
async def create_water_quality_report(report: WaterQualityCreate, db: Session = Depends(get_db)):
    # Analyze water quality parameters
    is_contaminated = analyze_water_quality(
        ph=report.ph_level,
        turbidity=report.turbidity,
        bacterial_count=report.bacterial_count,
        chlorine=report.chlorine_level
    )
    
    db_report = WaterQualityReport(
        location=report.location,
        ph_level=report.ph_level,
        turbidity=report.turbidity,
        bacterial_count=report.bacterial_count,
        chlorine_level=report.chlorine_level,
        temperature=report.temperature,
        tested_by=report.tested_by,
        source_type=report.source_type,
        is_contaminated=is_contaminated
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/quality")
async def get_water_quality_reports(location: str = None, contaminated_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(WaterQualityReport)
    if location:
        query = query.filter(WaterQualityReport.location.contains(location))
    if contaminated_only:
        query = query.filter(WaterQualityReport.is_contaminated == True)
    return query.all()

@router.get("/quality/hotspots")
async def get_contamination_hotspots(db: Session = Depends(get_db)):
    contaminated_reports = db.query(WaterQualityReport).filter(
        WaterQualityReport.is_contaminated == True
    ).all()
    
    hotspots = {}
    for report in contaminated_reports:
        location = report.location
        if location not in hotspots:
            hotspots[location] = {"count": 0, "latest_test": None, "risk_level": "low"}
        hotspots[location]["count"] += 1
        if not hotspots[location]["latest_test"] or report.tested_at > hotspots[location]["latest_test"]:
            hotspots[location]["latest_test"] = report.tested_at
        
        # Determine risk level based on contamination frequency
        if hotspots[location]["count"] >= 5:
            hotspots[location]["risk_level"] = "high"
        elif hotspots[location]["count"] >= 3:
            hotspots[location]["risk_level"] = "medium"
    
    return hotspots