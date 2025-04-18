from uuid import uuid4
from typing import List

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

todos = {}

class Todo(BaseModel):
    id: str
    title: str
    completed: bool = False

class CreateTodoInput(BaseModel):
    title: str

class UpdateTodoInput(BaseModel):
    id: str
    title: str = None
    completed: bool = None

class GetTodoInput(BaseModel):
    id: str

class DeleteTodoInput(BaseModel):
    id: str


server = FastMCP(name="todo-server", version="1.0.0")


@server.tool(name="create_todo", description="Create a new todo")
def create_todo(data: CreateTodoInput) -> Todo:
    todo_id = str(uuid4())
    todo = Todo(id=todo_id, title=data.title)
    todos[todo_id] = todo
    return todo


@server.tool(name="list_todos", description="List all todos")
def list_todos() -> List[Todo]:
    return list(todos.values())


@server.tool(name="get_todo", description="Retrieve a todo by ID")
def get_todo(data: GetTodoInput) -> Todo:
    todo = todos.get(data.id)
    if not todo:
        raise ValueError(f"Todo with id {data.id} not found")
    return todo


@server.tool(name="update_todo", description="Update a todo")
def update_todo(data: UpdateTodoInput) -> Todo:
    todo = todos.get(data.id)
    if not todo:
        raise ValueError(f"Todo with id {data.id} not found")
    if data.title is not None:
        todo.title = data.title
    if data.completed is not None:
        todo.completed = data.completed
    todos[data.id] = todo
    return todo


@server.tool(name="delete_todo", description="Delete a todo")
def delete_todo(data: DeleteTodoInput) -> dict:
    if data.id not in todos:
        raise ValueError(f"Todo with id {data.id} not found")
    del todos[data.id]
    return {"status": "deleted"}


if __name__ == '__main__':
    server.run(transport='stdio')
