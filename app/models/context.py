from datetime import date
class Context:
    def __init__(self, today=None):
        self.today = today or date.today()