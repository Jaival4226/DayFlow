from models.leave import Leave
from extensions import db

from models.leave import Leave
from extensions import db
from datetime import datetime

class LeaveService:
    @staticmethod
    def apply_leave(employee_id, data):
        # 1. Parse string dates into Date objects
        try:
            start = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

        # 2. VALIDATION LOGIC
        if start > end:
            return {"error": "End date cannot be before start date"}, 400
        
        if start < datetime.now().date():
             return {"error": "Cannot apply for leave in the past"}, 400

        # 3. Create Leave
        new_leave = Leave(
            employee_id=employee_id,
            leave_type=data['leave_type'],
            start_date=start,
            end_date=end,
            reason=data.get('reason')
        )
        db.session.add(new_leave)
        db.session.commit()
        return {"message": "Leave application submitted"}, 201
    
    # ... (approve_leave and reject_leave remain the same)
    @staticmethod
    def approve_leave(leave_id):
        leave_request = Leave.query.get(leave_id)
        
        if not leave_request:
            return {"error": "Leave request not found"}, 404
            
        if leave_request.status != 'Pending':
            return {"error": f"Leave is already {leave_request.status}"}, 400
            
        leave_request.status = 'Approved'
        db.session.commit()
        return {"message": "Leave approved successfully"}, 200

    @staticmethod
    def reject_leave(leave_id):
        # Good to have this too!
        leave_request = Leave.query.get(leave_id)
        if not leave_request: return {"error": "Not found"}, 404
        leave_request.status = 'Rejected'
        db.session.commit()
        return {"message": "Leave rejected successfully"}, 200
    
    # ... inside LeaveService class ...

    @staticmethod
    def get_all_pending():
        # Fetch ALL leaves where status is 'Pending'
        # We join with Employee model implicitly via the relationship
        return Leave.query.filter_by(status='Pending').order_by(Leave.applied_on.desc()).all()