from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

@dataclass
class Resource:
    type: str
    name: str
    action: str
    def __init__(self):
        name = None
        type = None
        action = None

def _get_modifications():
   with open("plan.txt") as f:
        return [line.strip().removeprefix("# ") for line in f if line.startswith("  #")]
def _fix_action(action: str):
     return action if action in (["created", "destroyed"]) else "modified" 

def _get_parts(line: str):
    resource = Resource()
    parts = line.split(" ")
    resource.type = parts[0].split(".")[0]
    resource.name = parts[0].split(".")[1]
    resource.action = _fix_action(parts[-1])
    return resource

def _colorize(action: str):
    if action == "created":
        return f"[green]{action}[/green]"
    if action == "destroyed":
        return f"[red]{action}[/red]"
    return f"[yellow]{action}[/yellow]"

resources = [_get_parts(line) for line in _get_modifications()]

def _symbolize(action: str):
    if action == "created":
        return ":ok:"
    if action == "destroyed":
        return ":thumbs_up"
    return ":ok:"

def render_table():
    console = Console()
    table = Table(title="Plan Summary", show_header=True)
    table.add_column("Type")
    table.add_column("Name")
    table.add_column("Action")
    for resource in resources:
        table.add_row(resource.type, resource.name, _colorize(resource.action))

    console.print(table)

def render_markdown():
    text = "# Plan Summary\n"
    header = "| Type | Name | Action |\n| --- | --- | --- |\n"
    text += header
    for resource in resources:
        text += f"|{resource.type} | {resource.name} | {_symbolize(resource.action)}|\n"
    console = Console(file=open("plan.md", "w"))
    console.print(text)


render_markdown()