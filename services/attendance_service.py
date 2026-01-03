from models.attendance import Attendance
from models.leave import Leave
from extensions import db
from datetime import datetime, date
from utils.helpers import Helpers

class AttendanceService:
    @staticmethod
    def get_employee_current_status(employee_id):
        """
        Determines the status dot color/icon for the landing page cards:
        🟢 Green: Present (Checked in)
        ✈️ Airplane: On Approved Leave
        🟡 Yellow: Absent (Not checked in, no leave applied)
        """
        today = date.today()

        # 1. Check if the employee is on an approved leave today
        leave = Leave.query.filter(
            Leave.employee_id == employee_id,
            Leave.status == 'Approved',
            Leave.start_date <= today,
            Leave.end_date >= today
        ).first()
        
        if leave:
            return "on_leave" # Frontend displays Airplane icon

        # 2. Check if the employee has checked in today
        attendance = Attendance.query.filter_by(
            employee_id=employee_id, 
            date=today
        ).first()

        if attendance:
            if attendance.check_out:
                return "absent" # They finished their shift and left
            return "present" # 🟢 Green dot

        # 3. If neither, they are simply absent today
        return "absent" # 🟡 Yellow dot

    @staticmethod
    def clock_in(employee_id):
        """Standard clock-in logic."""
        today = date.today()
        existing = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        
        if existing:
            return {"error": "Already checked in today"}, 400
            
        new_attendance = Attendance(
            employee_id=employee_id,
            date=today,
            check_in=datetime.now().time()
        )
        db.session.add(new_attendance)
        db.session.commit()
        return {"message": "Clocked in successfully", "status": "present"}, 200

    @staticmethod
    def clock_out(employee_id):
        """Standard clock-out logic."""
        today = date.today()
        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        
        if not attendance or not attendance.check_in:
            return {"error": "No clock-in record found for today"}, 404
            
        attendance.check_out = datetime.now().time()
        
        # Use helper to calculate total hours worked
        attendance.work_hours = Helpers.calculate_work_hours(attendance.check_in, attendance.check_out)
        
        db.session.commit()
        return {"message": "Clocked out successfully", "status": "absent"}, 200