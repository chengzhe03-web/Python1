from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    title: str
    done: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def mark_done(self) -> None:
        self.done = True

    def mark_undone(self) -> None:
        self.done = False


class TodoApp:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add_task(self, title: str) -> None:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        self.tasks.append(Task(title=title))

    def list_tasks(self) -> None:
        if not self.tasks:
            print("No tasks yet.")
            return

        for idx, t in enumerate(self.tasks, start=1):
            status = "✅" if t.done else "⬜"
            print(f"{idx:>2}. {status} {t.title}  (created {t.created_at})")

    def set_done(self, index: int, done: bool) -> None:
        if index < 1 or index > len(self.tasks):
            raise IndexError("Task index out of range.")
        if done:
            self.tasks[index - 1].mark_done()
        else:
            self.tasks[index - 1].mark_undone()

    def remove_task(self, index: int) -> None:
        if index < 1 or index > len(self.tasks):
            raise IndexError("Task index out of range.")
        self.tasks.pop(index - 1)

    def clear_done(self) -> int:
        """Remove all completed tasks. Returns how many removed."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        return before - len(self.tasks)
    
    def search(self, keyword: str) -> None:
        keyword = keyword.strip().lower()
        if not keyword:
            print("Search keyword cannot be empty.")
            return

        matches = [t for t in self.tasks if keyword in t.title.lower()]
        if not matches:
            print("No matching tasks.")
            return

        for idx, t in enumerate(matches, start=1):
            status = "✅" if t.done else "⬜"
            print(f"{idx:>2}. {status} {t.title}")



def print_help() -> None:
    print(
        "\nCommands:\n"
        "  add <title>       Add a task\n"
        "  list              List tasks\n"
        "  done <index>      Mark task done\n"
        "  undone <index>    Mark task not done\n"
        "  rm <index>        Remove a task\n"
        "  clear-done        Remove all completed tasks\n"
        "  help              Show help\n"
        "  quit              Exit the app\n"
        "  search <keyword>  Search tasks by keyword\n"

    )


def main() -> None:
    app = TodoApp()
    print("Simple Todo App (type 'help' for commands)")
    print_help()

    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = raw.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) == 2 else ""

            if cmd == "add":
                app.add_task(arg)
                print("Added.")
            elif cmd == "list":
                app.list_tasks()
            elif cmd == "done":
                app.set_done(int(arg), True)
                print("Marked done.")
            elif cmd == "undone":
                app.set_done(int(arg), False)
                print("Marked undone.")
            elif cmd == "rm":
                app.remove_task(int(arg))
                print("Removed.")
            elif cmd == "clear-done":
                removed = app.clear_done()
                print(f"Removed {removed} completed task(s).")
            elif cmd == "help":
                print_help()
            elif cmd in ("quit", "exit"):
                print("Bye!")
                break
            elif cmd == "search":
                app.search(arg)

            else:
                print("Unknown command. Type 'help'.")

        except ValueError as e:
            print(f"Error explained: {e}")
        except (IndexError, TypeError):
            print("Invalid index.")
        except KeyboardInterrupt:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
