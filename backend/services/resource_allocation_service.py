from typing import Dict, List
import sqlite3
from datetime import datetime, timedelta
import json

class ResourceAllocationService:
    """Resource allocation and management service"""
    
    def __init__(self, db_path: str = "health_surveillance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize resource allocation tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Resource types table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resource_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    description TEXT
                )
            """)
            
            # Resource inventory table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resource_inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resource_type_id INTEGER NOT NULL,
                    location TEXT NOT NULL,
                    total_quantity INTEGER NOT NULL DEFAULT 0,
                    available_quantity INTEGER NOT NULL DEFAULT 0,
                    allocated_quantity INTEGER NOT NULL DEFAULT 0,
                    reserved_quantity INTEGER NOT NULL DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (resource_type_id) REFERENCES resource_types (id)
                )
            """)
            
            # Resource requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resource_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resource_type TEXT NOT NULL,
                    quantity_requested INTEGER NOT NULL,
                    priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high', 'critical')),
                    location TEXT NOT NULL,
                    requester_name TEXT,
                    requester_contact TEXT,
                    justification TEXT,
                    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected', 'fulfilled')),
                    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    approved_at TIMESTAMP,
                    fulfilled_at TIMESTAMP
                )
            """)
            
            # Resource allocations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resource_allocations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id INTEGER NOT NULL,
                    resource_type TEXT NOT NULL,
                    quantity_allocated INTEGER NOT NULL,
                    location TEXT NOT NULL,
                    allocated_by TEXT,
                    allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expected_delivery TIMESTAMP,
                    actual_delivery TIMESTAMP,
                    status TEXT DEFAULT 'allocated' CHECK(status IN ('allocated', 'in_transit', 'delivered', 'cancelled')),
                    FOREIGN KEY (request_id) REFERENCES resource_requests (id)
                )
            """)
            
            # Initialize default resource types
            default_resources = [
                ('Medical Team', 'personnel', 'team', 'Mobile medical team with doctor and nurse'),
                ('Water Testing Kit', 'equipment', 'kit', 'Portable water quality testing kit'),
                ('Emergency Supplies', 'supplies', 'package', 'Emergency medical and food supplies'),
                ('Vehicle', 'transport', 'unit', 'Emergency response vehicle'),
                ('Medicine', 'medical', 'package', 'Essential medicines package'),
                ('Water Purification Tablets', 'supplies', 'box', 'Water purification tablets (100 tablets per box)'),
                ('ORS Packets', 'medical', 'box', 'Oral Rehydration Solution packets'),
                ('Disinfectant', 'supplies', 'liter', 'Surface and water disinfectant')
            ]
            
            for resource in default_resources:
                cursor.execute("""
                    INSERT OR IGNORE INTO resource_types (name, category, unit, description)
                    VALUES (?, ?, ?, ?)
                """, resource)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Resource database initialization error: {e}")
    
    def submit_resource_request(self, request_data: Dict) -> Dict:
        """Submit a resource request"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO resource_requests 
                (resource_type, quantity_requested, priority, location, 
                 requester_name, requester_contact, justification)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                request_data.get('resource_type'),
                request_data.get('quantity', 1),
                request_data.get('priority', 'medium'),
                request_data.get('location'),
                request_data.get('requester_name', 'Mobile User'),
                request_data.get('requester_contact'),
                request_data.get('justification', 'Mobile app request')
            ))
            
            request_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Auto-approve critical requests
            if request_data.get('priority') == 'critical':
                self._auto_approve_critical_request(request_id)
            
            return {
                'status': 'success',
                'request_id': request_id,
                'message': 'Resource request submitted successfully'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _auto_approve_critical_request(self, request_id: int):
        """Auto-approve critical resource requests"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE resource_requests 
                SET status = 'approved', approved_at = ?
                WHERE id = ? AND priority = 'critical'
            """, (datetime.now(), request_id))
            
            conn.commit()
            conn.close()
            
            # Try to allocate resources immediately
            self._attempt_resource_allocation(request_id)
            
        except Exception as e:
            print(f"Error auto-approving critical request: {e}")
    
    def _attempt_resource_allocation(self, request_id: int):
        """Attempt to allocate resources for approved request"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get request details
            cursor.execute("""
                SELECT resource_type, quantity_requested, location, priority
                FROM resource_requests 
                WHERE id = ? AND status = 'approved'
            """, (request_id,))
            
            request = cursor.fetchone()
            if not request:
                return
            
            resource_type, quantity_requested, location, priority = request
            
            # Check available resources (mock allocation logic)
            available_quantity = self._get_available_quantity(resource_type, location)
            
            if available_quantity >= quantity_requested:
                # Full allocation
                allocated_quantity = quantity_requested
                cursor.execute("""
                    INSERT INTO resource_allocations 
                    (request_id, resource_type, quantity_allocated, location, allocated_by)
                    VALUES (?, ?, ?, ?, ?)
                """, (request_id, resource_type, allocated_quantity, location, 'System'))
                
                cursor.execute("""
                    UPDATE resource_requests 
                    SET status = 'fulfilled', fulfilled_at = ?
                    WHERE id = ?
                """, (datetime.now(), request_id))
            else:
                # Partial allocation
                if available_quantity > 0:
                    cursor.execute("""
                        INSERT INTO resource_allocations 
                        (request_id, resource_type, quantity_allocated, location, allocated_by)
                        VALUES (?, ?, ?, ?, ?)
                    """, (request_id, resource_type, available_quantity, location, 'System'))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error attempting resource allocation: {e}")
    
    def _get_available_quantity(self, resource_type: str, location: str) -> int:
        """Get available quantity for resource type (mock implementation)"""
        # Mock availability based on resource type
        base_availability = {
            'Medical Team': 5,
            'Water Testing Kit': 20,
            'Emergency Supplies': 50,
            'Vehicle': 3,
            'Medicine': 100,
            'Water Purification Tablets': 200,
            'ORS Packets': 150,
            'Disinfectant': 80
        }
        
        return base_availability.get(resource_type, 10)
    
    def get_resource_allocation_dashboard(self) -> List[Dict]:
        """Get resource allocation dashboard data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get resource types and their allocation status
            cursor.execute("SELECT name FROM resource_types")
            resource_types = [row[0] for row in cursor.fetchall()]
            
            dashboard_data = []
            for resource_type in resource_types:
                # Get requests for this resource type
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_requests,
                        SUM(quantity_requested) as total_requested,
                        SUM(CASE WHEN status = 'fulfilled' THEN quantity_requested ELSE 0 END) as total_fulfilled
                    FROM resource_requests 
                    WHERE resource_type = ?
                """, (resource_type,))
                
                stats = cursor.fetchone()
                total_requests, total_requested, total_fulfilled = stats or (0, 0, 0)
                
                # Get allocations for this resource type
                cursor.execute("""
                    SELECT SUM(quantity_allocated) 
                    FROM resource_allocations 
                    WHERE resource_type = ?
                """, (resource_type,))
                
                total_allocated = cursor.fetchone()[0] or 0
                
                # Mock available quantity
                available = self._get_available_quantity(resource_type, 'Central')
                needed = total_requested or (total_allocated + 10)  # Estimate need
                
                dashboard_data.append({
                    'type': resource_type,
                    'allocated': int(total_allocated),
                    'available': available,
                    'needed': int(needed),
                    'requests': int(total_requests),
                    'fulfillment_rate': round((total_fulfilled / total_requested * 100) if total_requested > 0 else 0, 1)
                })
            
            conn.close()
            return dashboard_data
            
        except Exception as e:
            print(f"Error getting resource dashboard: {e}")
            return []
    
    def get_resource_requests(self, status: str = None, priority: str = None, limit: int = 50) -> List[Dict]:
        """Get resource requests with optional filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT id, resource_type, quantity_requested, priority, location,
                       requester_name, status, requested_at, approved_at, fulfilled_at
                FROM resource_requests
            """
            params = []
            conditions = []
            
            if status:
                conditions.append("status = ?")
                params.append(status)
            
            if priority:
                conditions.append("priority = ?")
                params.append(priority)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY requested_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            
            requests = []
            for row in cursor.fetchall():
                requests.append({
                    'id': row[0],
                    'resource_type': row[1],
                    'quantity_requested': row[2],
                    'priority': row[3],
                    'location': row[4],
                    'requester_name': row[5],
                    'status': row[6],
                    'requested_at': row[7],
                    'approved_at': row[8],
                    'fulfilled_at': row[9]
                })
            
            conn.close()
            return requests
            
        except Exception as e:
            print(f"Error getting resource requests: {e}")
            return []
    
    def approve_resource_request(self, request_id: int, approver: str = 'Admin') -> Dict:
        """Approve a resource request"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE resource_requests 
                SET status = 'approved', approved_at = ?
                WHERE id = ? AND status = 'pending'
            """, (datetime.now(), request_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                
                # Attempt allocation
                self._attempt_resource_allocation(request_id)
                
                return {'status': 'success', 'message': 'Request approved successfully'}
            else:
                conn.close()
                return {'status': 'error', 'message': 'Request not found or already processed'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_resource_statistics(self) -> Dict:
        """Get resource allocation statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total requests
            cursor.execute("SELECT COUNT(*) FROM resource_requests")
            total_requests = cursor.fetchone()[0]
            
            # Requests by status
            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM resource_requests 
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Requests by priority
            cursor.execute("""
                SELECT priority, COUNT(*) 
                FROM resource_requests 
                GROUP BY priority
            """)
            priority_counts = dict(cursor.fetchall())
            
            # Recent requests (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM resource_requests 
                WHERE requested_at >= datetime('now', '-1 day')
            """)
            recent_requests = cursor.fetchone()[0]
            
            # Average response time (mock calculation)
            cursor.execute("""
                SELECT AVG(
                    CASE 
                        WHEN approved_at IS NOT NULL 
                        THEN (julianday(approved_at) - julianday(requested_at)) * 24 
                        ELSE NULL 
                    END
                ) FROM resource_requests
            """)
            avg_response_time = cursor.fetchone()[0] or 0
            
            # Resource utilization by type
            cursor.execute("""
                SELECT resource_type, 
                       SUM(quantity_requested) as requested,
                       SUM(CASE WHEN status = 'fulfilled' THEN quantity_requested ELSE 0 END) as fulfilled
                FROM resource_requests 
                GROUP BY resource_type
            """)
            
            utilization = {}
            for row in cursor.fetchall():
                resource_type, requested, fulfilled = row
                utilization[resource_type] = {
                    'requested': requested,
                    'fulfilled': fulfilled,
                    'fulfillment_rate': round((fulfilled / requested * 100) if requested > 0 else 0, 1)
                }
            
            conn.close()
            
            return {
                'total_requests': total_requests,
                'status_breakdown': status_counts,
                'priority_breakdown': priority_counts,
                'recent_requests': recent_requests,
                'avg_response_time_hours': round(avg_response_time, 2),
                'resource_utilization': utilization
            }
            
        except Exception as e:
            print(f"Error getting resource statistics: {e}")
            return {}
    
    def get_resource_forecast(self, days_ahead: int = 7) -> Dict:
        """Get resource demand forecast"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Analyze historical patterns
            cursor.execute("""
                SELECT resource_type, 
                       COUNT(*) as request_count,
                       AVG(quantity_requested) as avg_quantity
                FROM resource_requests 
                WHERE requested_at >= datetime('now', '-30 days')
                GROUP BY resource_type
            """)
            
            forecast = {}
            for row in cursor.fetchall():
                resource_type, request_count, avg_quantity = row
                
                # Simple forecast based on historical data
                daily_demand = request_count / 30  # requests per day
                forecasted_requests = daily_demand * days_ahead
                forecasted_quantity = forecasted_requests * avg_quantity
                
                forecast[resource_type] = {
                    'forecasted_requests': round(forecasted_requests, 1),
                    'forecasted_quantity': round(forecasted_quantity, 1),
                    'confidence': 'medium'  # Mock confidence level
                }
            
            conn.close()
            return forecast
            
        except Exception as e:
            print(f"Error getting resource forecast: {e}")
            return {}