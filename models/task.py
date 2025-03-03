from db.manager import Model

class Task(Model):
    board_id: int
    title: str
    status: str