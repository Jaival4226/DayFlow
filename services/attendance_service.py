from models.attendance import Attendance
from extensions import db
from datetime import datetime, date

class AttendanceService:
    @staticmethod
    def clock_in(employee_id):
        today = date.today()
        # Check if already exists
        existing = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if existing:
            return {"error": "Already checked in today"}, 400
        
        new_record = Attendance(
            employee_id=employee_id,
            date=today,
            check_in_time=datetime.now().time(),
            status='Present'
        )
        db.session.add(new_record)
        db.session.commit()
        return {"message": "Clocked in successfully"}, 201

    @staticmethod
    def clock_out(employee_id):
        record = Attendance.query.filter_by(employee_id=employee_id, date=date.today()).first()
        if not record or record.check_out_time:
            return {"error": "Invalid clock-out request"}, 400
        
        record.check_out_time = datetime.now().time()
        db.session.commit()
        return {"message": "Clocked out successfully"}, 200