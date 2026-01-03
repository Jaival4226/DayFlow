from models.attendance import Attendance
from models.leave import Leave
from extensions import db
from datetime import datetime, date
from utils.helpers import Helpers

class AttendanceService:
    @staticmethod
    def get_employee_current_status(employee_id):
        today = date.today()
        leave = Leave.query.filter(
            Leave.employee_id == employee_id,
            Leave.status == 'Approved',
            Leave.start_date <= today,
            Leave.end_date >= today
        ).first()
        
        if leave: return "on_leave"

        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if attendance:
            return "absent" if attendance.check_out else "present"
        return "absent"

    @staticmethod
    def get_employee_history(employee_id):
        """NEW: Required for attendance history page"""
        records = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc()).all()
        return [{
            "date": str(r.date),
            "check_in": str(r.check_in) if r.check_in else "-",
            "check_out": str(r.check_out) if r.check_out else "-",
            "work_hours": r.work_hours,
            "status": r.status
        } for r in records]

    @staticmethod
    def clock_in(employee_id):
        today = date.today()
        existing = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if existing: return {"error": "Already checked in"}, 400
            
        new_attendance = Attendance(employee_id=employee_id, date=today, check_in=datetime.now().time())
        db.session.add(new_attendance)
        db.session.commit()
        return {"message": "Clocked in successfully", "status": "present"}, 200

    @staticmethod
    def clock_out(employee_id):
        today = date.today()
        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if not attendance or not attendance.check_in: return {"error": "No clock-in found"}, 404
            
        attendance.check_out = datetime.now().time()
        attendance.work_hours = Helpers.calculate_work_hours(attendance.check_in, attendance.check_out)
        db.session.commit()
        return {"message": "Clocked out successfully", "status": "absent"}, 200