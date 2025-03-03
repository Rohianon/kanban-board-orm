from fastapi import APIRouter, HTTPException
from models.board import Board
from models.task import Task

router = APIRouter()

@router.post("/boards/")
def create_board(name: str, description: str = ""):
    board = Board(name=name, description=description)
    board.save()
    return {"id": board.id, "name": board.name, "description": board.description}

@router.get("/boards/{board_id}")
def get_board(board_id: int):
    board = Board.select(where=Board.id == board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board[0]

@router.post("/tasks/")
def create_task(board_id: int, title: str, status: str = "TODO"):
    task = Task(board_id=board_id, title=title, status=status)
    task.save()
    return {"id": task.id, "board_id": task.board_id, "title": task.title, "status": task.status}

@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = Task.select(where=Task.id == task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task[0]
