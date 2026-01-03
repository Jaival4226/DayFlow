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