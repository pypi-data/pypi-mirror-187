"""
make it easy to get common datetime
"""
import datetime


class DateGenerator:
    """
    just ask and get dates
    """
    def __init__(self, today=None):
        self.today = datetime.date.today() if not today else today

    def get_current_month(self):
        """
        get current month
        """
        return self.today.strftime('%Y-%m')

    def get_previous_month(self):
        """
        get previous month
        """
        return (self.today.replace(day=1) - datetime.timedelta(days=1)).strftime('%Y-%m')

    def get_next_month(self):
        """
        get next month
        """
        return (self.today.replace(day=1) + datetime.timedelta(days=31)).strftime('%Y-%m')

    def get_previous_n_months(self, periods):
        """
        get previous n months
        """
        month = self.today.month
        year = self.today.year
        months = [(month-i) % 12 + 1 for i in range(2, periods + 2)]
        years = [year + ((month-i) // 12) for i in range(2, periods + 2)]
        return [datetime.datetime(year, month, 1).strftime('%Y-%m') for year, month in zip(years, months)]

    def get_next_n_months(self, periods):
        """
        get next n months
        """
        month = self.today.month
        year = self.today.year
        months = [(month + i) % 12 + 1 for i in range(0, periods)]
        years = [year + ((month + i) // 12) for i in range(0, periods)]
        return [datetime.datetime(year, month, 1).strftime('%Y-%m') for year, month in zip(years, months)]

    def get_previous_n_days(self, periods):
        """
        get previous n days
        """
        return [(self.today - datetime.timedelta(days=i)).isoformat() for i in range(1, periods+1)]

    def get_next_n_days(self, periods):
        """
        get next n days
        """
        return [(self.today + datetime.timedelta(days=i)).isoformat() for i in range(1, periods+1)]

    def get_first_day_of_current_month(self):
        """
        get first day of current month
        """
        return self.today.replace(day=1).isoformat()

    def get_first_day_of_previous_month(self):
        """
        get first day of previous month
        """
        return (self.today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1).isoformat()

    def get_first_day_of_next_month(self):
        """
        get first day of next month
        """
        return (self.today.replace(day=1) + datetime.timedelta(days=31)).replace(day=1).isoformat()

    def get_last_day_of_current_month(self):
        """
        get last day of current month
        """
        first_day_of_next_month = (self.today.replace(day=1) + datetime.timedelta(days=31)).replace(day=1)
        return (first_day_of_next_month - datetime.timedelta(days=1)).isoformat()

    def get_last_day_of_previous_month(self):
        """
        get last day of previous month
        """
        return (self.today.replace(day=1) - datetime.timedelta(days=1)).isoformat()

    def get_last_day_of_next_month(self):
        """
        get last day of next month
        """
        return (self.today.replace(day=1) + datetime.timedelta(days=62)).replace(day=1).isoformat()

    def get_current_quarter(self):
        """
        get current quarter
        """
        year = self.today.year
        quarter = (self.today.month-1)//3 + 1
        return f'{year}-Q{quarter}'

    def get_previous_quarter(self):
        """
        get previous quarter
        """
        three_months_ago = self.get_previous_n_months(3)[-1]
        year = datetime.datetime.strptime(three_months_ago, '%Y-%m').year
        month = datetime.datetime.strptime(three_months_ago, '%Y-%m').month
        quarter = (month - 1) // 3 + 1
        return f'{year}-Q{quarter}'

    def get_previous_n_quarters(self, periods):
        """
        get previous n quarters
        """
        year = self.today.year
        quarter = (self.today.month - 1) // 3 + 1

        quarters = [(quarter - i) % 4 + 1 for i in range(2, periods + 2)]
        years = [year + ((quarter - i) // 4) for i in range(2, periods + 2)]
        return [f'{year}-Q{quarter}' for year, quarter in zip(years, quarters)]

    def get_next_quarter(self):
        """
        get previous quarter
        """
        three_months_ago = self.get_next_n_months(3)[-1]
        year = datetime.datetime.strptime(three_months_ago, '%Y-%m').year
        month = datetime.datetime.strptime(three_months_ago, '%Y-%m').month
        quarter = (month - 1) // 3 + 1
        return f'{year}-Q{quarter}'

    def get_next_n_quarters(self, periods):
        """
        get next n quarters
        """
        year = self.today.year
        quarter = (self.today.month - 1) // 3 + 1

        quarters = [(quarter + i) % 4 + 1 for i in range(0, periods)]
        years = [year + ((quarter + i) // 4) for i in range(0, periods)]
        return [f'{year}-Q{quarter}' for year, quarter in zip(years, quarters)]