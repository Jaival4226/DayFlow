from models.attendance import Attendance
from models.leave import Leave
from extensions import db
from datetime import datetime, date
from utils.helpers import Helpers

class AttendanceService:
    @staticmethod
    def get_employee_current_status(employee_id):
        today = date.today()
        # Check approved leave first
        leave = Leave.query.filter(
            Leave.employee_id == employee_id,
            Leave.status == 'Approved',
            Leave.start_date <= today,
            Leave.end_date >= today
        ).first()
        
        if leave: return "on_leave"

        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if attendance:
            # If checked out, they are done for the day (shown as absent or present depending on logic, usually present if worked)
            # But for status dot, 'absent' means "Not currently working"
            return "absent" if attendance.check_out else "present"
        return "absent"

    @staticmethod
    def get_employee_history(employee_id):
        records = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc()).all()
        return [{
            "date": r.date.strftime("%Y-%m-%d"),
            # FIXED: Use strftime to remove microseconds
            "check_in": r.check_in.strftime("%H:%M:%S") if r.check_in else "-",
            "check_out": r.check_out.strftime("%H:%M:%S") if r.check_out else "-",
            "work_hours": r.work_hours,
            "status": r.status
        } for r in records]

    @staticmethod
    def clock_in(employee_id):
        today = date.today()
        existing = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if existing: return {"error": "Already checked in"}, 400
            
        # FIXED: .replace(microsecond=0) removes the .583837 part before saving
        now = datetime.now().replace(microsecond=0).time()
        
        new_attendance = Attendance(employee_id=employee_id, date=today, check_in=now, status='present')
        db.session.add(new_attendance)
        db.session.commit()
        return {"message": "Clocked in successfully", "status": "present"}, 200

    @staticmethod
    def clock_out(employee_id):
        today = date.today()
        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if not attendance or not attendance.check_in: return {"error": "No clock-in found"}, 404
            
        # FIXED: .replace(microsecond=0)
        now = datetime.now().replace(microsecond=0).time()
        
        attendance.check_out = now
        attendance.work_hours = Helpers.calculate_work_hours(attendance.check_in, attendance.check_out)
        db.session.commit()
        return {"message": "Clocked out successfully", "status": "absent"}, 200