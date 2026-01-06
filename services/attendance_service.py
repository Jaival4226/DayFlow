from models.attendance import Attendance
from models.leave import Leave
from extensions import db
from datetime import datetime, date
from utils.helpers import Helpers

class AttendanceService:
    @staticmethod
    def get_employee_current_status(employee_id):
        today = date.today()
        
        # 1. Check for Approved Leave
        leave = Leave.query.filter(
            Leave.employee_id == employee_id,
            Leave.status == 'Approved',
            Leave.start_date <= today,
            Leave.end_date >= today
        ).first()
        if leave: return "On Leave"

        # 2. Check Attendance Record
        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        
        if attendance:
            # If they have checked out, show they have left (or just 'Checked Out')
            if attendance.check_out:
                return "Checked Out"
            
            # If currently checked in, return the specific status (Late / On Time)
            return attendance.status
            
        return "Absent"

    @staticmethod
    def get_employee_history(employee_id):
        records = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc()).all()
        return [{
            "date": r.date.strftime("%Y-%m-%d"),
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
            
        now_time = datetime.now().replace(microsecond=0).time()
        
        # DYNAMIC STATUS: Check if Late or On Time
        # Default shift start is 09:00:00. You can make this configurable later.
        status = Helpers.get_attendance_status(now_time, shift_start="09:00:00")
        
        new_attendance = Attendance(
            employee_id=employee_id, 
            date=today, 
            check_in=now_time, 
            status=status  # Saves 'Late' or 'On Time'
        )
        db.session.add(new_attendance)
        db.session.commit()
        return {"message": f"Clocked in ({status})", "status": status}, 200

    @staticmethod
    def clock_out(employee_id):
        today = date.today()
        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if not attendance or not attendance.check_in: return {"error": "No clock-in found"}, 404
            
        now_time = datetime.now().replace(microsecond=0).time()
        
        attendance.check_out = now_time
        attendance.work_hours = Helpers.calculate_work_hours(attendance.check_in, attendance.check_out)
        
        # We don't change the status (Late/On Time) upon checkout, 
        # but the dashboard will now show "Checked Out" via get_employee_current_status
        
        db.session.commit()
        return {"message": "Clocked out successfully", "status": "Checked Out"}, 200