import sqlite3
from datetime import datetime

conn = sqlite3.connect("../health_surveillance.db")
cursor = conn.cursor()

print("=== Health Surveillance Database Editor ===")

def add_health_report():
    print("\n--- Add Health Report ---")
    reporter_id = int(input("Reporter ID (1-5): ") or "3")
    age = int(input("Patient age: ") or "25")
    gender = input("Gender (male/female): ") or "female"
    symptoms = input("Symptoms (comma separated): ") or "fever,headache"
    location = input("Location: ") or "Village A"
    severity = input("Severity (mild/moderate/severe): ") or "mild"
    disease = input("Disease suspected: ") or "diarrhea"
    
    cursor.execute("""INSERT INTO health_reports 
                     (reporter_id, patient_age, patient_gender, symptoms, location, 
                      reported_at, severity, disease_suspected) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                   (reporter_id, age, gender, f'["{symptoms.replace(",", '", "')}"]', 
                    location, datetime.now(), severity, disease))
    print("Health report added!")

def add_water_report():
    print("\n--- Add Water Quality Report ---")
    location = input("Location: ") or "Village B"
    ph = float(input("pH level: ") or "7.0")
    turbidity = float(input("Turbidity: ") or "5.0")
    bacteria = int(input("Bacterial count: ") or "10")
    chlorine = float(input("Chlorine level: ") or "0.2")
    temp = float(input("Temperature: ") or "25.0")
    tester_id = int(input("Tester ID (1-5): ") or "5")
    source_type = input("Source type (well/river/pond): ") or "well"
    contaminated = input("Is contaminated? (y/n): ").lower() == 'y'
    
    cursor.execute("""INSERT INTO water_quality_reports 
                     (location, ph_level, turbidity, bacterial_count, chlorine_level,
                      temperature, tested_at, tested_by, source_type, is_contaminated)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (location, ph, turbidity, bacteria, chlorine, temp, 
                    datetime.now(), tester_id, source_type, contaminated))
    print("Water quality report added!")

def add_alert():
    print("\n--- Add Alert ---")
    alert_type = input("Alert type (outbreak_warning/water_contamination): ") or "outbreak_warning"
    location = input("Location: ") or "Village C"
    message = input("Message: ") or "Health alert issued"
    severity = input("Severity (low/medium/high/critical): ") or "medium"
    population = int(input("Affected population: ") or "100")
    
    cursor.execute("""INSERT INTO alerts 
                     (alert_type, location, message, severity, created_at, 
                      is_resolved, affected_population)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (alert_type, location, message, severity, datetime.now(), 0, population))
    print("Alert added!")

def view_data():
    print("\n--- Current Data ---")
    
    print("\nHealth Reports:")
    cursor.execute("SELECT * FROM health_reports ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(f"  ID:{row[0]} Age:{row[2]} Gender:{row[3]} Disease:{row[8]} Location:{row[5]}")
    
    print("\nWater Reports:")
    cursor.execute("SELECT * FROM water_quality_reports ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(f"  ID:{row[0]} Location:{row[1]} pH:{row[2]} Contaminated:{row[10]}")
    
    print("\nAlerts:")
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(f"  ID:{row[0]} Type:{row[1]} Severity:{row[4]} Location:{row[2]}")

# Menu
while True:
    print("\n1. Add Health Report")
    print("2. Add Water Quality Report") 
    print("3. Add Alert")
    print("4. View Data")
    print("5. Exit")
    
    choice = input("\nChoice (1-5): ")
    
    if choice == '1':
        add_health_report()
    elif choice == '2':
        add_water_report()
    elif choice == '3':
        add_alert()
    elif choice == '4':
        view_data()
    elif choice == '5':
        break
    else:
        print("Invalid choice")
    
    conn.commit()

conn.close()
print("Database editor closed!")