import sqlite3

from fasthtml.common import serve, Div, Span, P, Ul, Li, Script, to_xml
from monsterui.all import Theme, Container, Card, ButtonT, ContainerT, H1, H3, CheckboxX, Button, Form, Input, fast_app

con = sqlite3.connect('todo.db', check_same_thread=False)
con.row_factory = sqlite3.Row

con.executescript("""CREATE TABLE IF NOT EXISTS todos( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done INTEGER DEFAULT 0);""")

def one(i):  return con.execute("SELECT * FROM todos WHERE id=?", (i,)).fetchone()
def all():   return con.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()


def TaskCounterText():
    todos = all()
    remaining = len([t for t in todos if not t['done']])
    total = len(todos)

    return f"You have {remaining} of {total} tasks remaining"


def TaskCounter():
    return P(TaskCounterText(), id="task-counter")


def Item(t):
    li = Li(id=f"t{t['id']}", cls="group flex items-center gap-3 p-4 bg-card border rounded-lg hover:shadow-md transition-all duration-200")
    done = bool(t["done"])
    return li(
        CheckboxX(checked=done, hx_post=f"/toggle/{t['id']}",
                  hx_target="closest li", hx_swap="outerHTML",
                  cls="scale-110"),
        Span(t["title"], cls=f'flex-1 break-words text-sm {"line-through text-muted-foreground opacity-60" if done else "text-foreground"}'),
        Div(cls="opacity-0 group-hover:opacity-100 transition-opacity flex gap-1")(
            Button("✏️", cls=f"{ButtonT.ghost} px-2 py-1 text-xs",
                   hx_get=f"/edit/{t['id']}", hx_target="closest li", hx_swap="outerHTML"),
            Button("🗑️", cls=f"{ButtonT.ghost} px-2 py-1 text-xs text-destructive hover:text-destructive",
                   hx_delete=f"/del/{t['id']}", hx_target="closest li", hx_swap="outerHTML")))

def Edit(t):
    return Li(id=f"t{t['id']}", cls="p-4 bg-card border rounded-lg")(
        Form(hx_post=f"/upd/{t['id']}", hx_target="closest li", hx_swap="outerHTML", cls="flex gap-2")(
            Input(name="title", value=t["title"], required=True, 
                  cls="flex-1 focus:ring-2 focus:ring-primary"),
            Button("💾", "Save", cls=f"{ButtonT.primary} px-3 py-1 text-sm"),
            Button("✕", type="button", cls=f"{ButtonT.ghost} px-2 py-1 text-sm",
                   hx_get=f"/row/{t['id']}", hx_target="closest li", hx_swap="outerHTML")))


def EmptyState():
    return Div(cls="flex flex-col items-center justify-center py-12 text-center")(
        Div(cls="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4 text-2xl")(
            "📋"),
        H3("No tasks yet", cls="text-lg font-medium text-muted-foreground mb-2"),
        P("Add your first task to get started", cls="text-sm text-muted-foreground"))


app, rt = fast_app(hdrs=Theme.blue.headers(daisy=True))


@rt
def index():
    todos = all()
    return Container(
        Div(cls="text-center mb-8")(
            H1("📋 Task Manager", cls="text-3xl font-bold text-foreground mb-2"),
            P("Stay organized and get things done", cls="text-muted-foreground")),
        
        Card(cls="p-6 mb-6")(
            Form(hx_post="/add", hx_target="#list", hx_swap="afterbegin",
                 hx_reset=True, cls="flex gap-3")(
                Input(name="title", placeholder="What needs to be done?", required=True, 
                      cls="flex-1 text-sm focus:ring-2 focus:ring-primary"),
                Button("➕", "Add Task", cls=ButtonT.primary))),
        
        Card(cls="p-6")(
            Ul(id="list", cls="space-y-3")(
                *map(Item, todos) if todos else [EmptyState()])),
        
        Div(cls="mt-12 text-center text-xs text-muted-foreground")(
            TaskCounter()),
        
        cls=f"{ContainerT.sm} py-8")


@rt("/row/{i:int}") 
def row(i:int):   return Item(one(i))


@rt("/add", methods=["POST"])
def add(title:str):
    con.execute("INSERT INTO todos(title) VALUES(?)", (title,)); con.commit()
    i = con.execute("select last_insert_rowid()").fetchone()[0]
    return (Item(one(i)), 
            Script(f"if(document.querySelector('.text-center.py-12')) location.reload(); document.getElementById('task-counter').textContent = '{TaskCounterText()}'"))


@rt("/toggle/{i:int}", methods=["POST"])
def toggle(i:int):
    con.execute("UPDATE todos SET done=NOT done WHERE id=?", (i,)); con.commit()
    return (Item(one(i)), 
            Script(f"document.getElementById('task-counter').textContent = '{TaskCounterText()}'"))


@rt("/del/{i:int}", methods=["DELETE"])
def delete(i:int):
    con.execute("DELETE FROM todos WHERE id=?", (i,)); con.commit()
    remaining = len(all())
    if remaining == 0:
        return "", Script("document.getElementById('list').innerHTML = `" + to_xml(EmptyState()).replace('`', '\\`') + "`; document.getElementById('task-counter').textContent = 'You have 0 of 0 tasks remaining';")
    return "", Script(f"document.getElementById('task-counter').textContent = '{TaskCounterText()}';")


@rt("/edit/{i:int}")
def edit(i:int):   return Edit(one(i))


@rt("/upd/{i:int}", methods=["POST"])
def upd(i:int, title:str):
    con.execute("UPDATE todos SET title=? WHERE id=?", (title, i)); con.commit()
    return Item(one(i))


if __name__ == "__main__":
    serve()
