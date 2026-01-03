from datetime import datetime, date

class Helpers:
    @staticmethod
    def calculate_work_hours(check_in, check_out):
        """Calculates total hours worked between two time objects."""
        if not check_in or not check_out:
            return 0
        
        # Combine with a dummy date to subtract time objects
        dummy_date = date.today()
        start = datetime.combine(dummy_date, check_in)
        end = datetime.combine(dummy_date, check_out)
        
        duration = end - start
        return round(duration.total_seconds() / 3600, 2) # Returns hours (e.g., 8.5)

    @staticmethod
    def format_currency(amount):
        """Formats numbers into currency string for salary slips."""
        return f"₹{amount:,.2f}"

    @staticmethod
    def get_attendance_status(check_in_time, shift_start="09:00:00"):
        """Checks if an employee is 'On Time' or 'Late'."""
        if not check_in_time:
            return "Absent"
            
        shift_time = datetime.strptime(shift_start, "%H:%M:%S").time()
        if check_in_time > shift_time:
            return "Late"
        return "On Time"