from models.leave import Leave
from extensions import db

class LeaveService:
    @staticmethod
    def apply_leave(employee_id, data):
        new_leave = Leave(
            employee_id=employee_id,
            leave_type=data['leave_type'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            reason=data.get('reason')
        )
        db.session.add(new_leave)
        db.session.commit()
        return {"message": "Leave application submitted"}, 201
    
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