"""A small command-line task manager for the operations team."""

import csv


TODO_FILE = "todos.csv"
todos = []


def add_one_task(title):
    """Add a task title to the in-memory list."""
    todos.append(title)


def print_list():
    """Print all tasks using one-based positions for easy reference."""
    if not todos:
        print("No hay tareas pendientes.")
        return

    for position, title in enumerate(todos, start=1):
        print(f"{position}. {title}")


def delete_task(number_to_delete):
    """Delete a task by its one-based position.

    Returns True if a task was deleted, otherwise False.
    """
    if not isinstance(number_to_delete, int) or not 1 <= number_to_delete <= len(todos):
        return False

    del todos[number_to_delete - 1]
    return True


def save_todos():
    """Save the current tasks to ``todos.csv`` in CSV format."""
    with open(TODO_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for title in todos:
            writer.writerow([title])


def load_todos():
    """Replace the in-memory tasks with the contents of ``todos.csv``.

    If the file does not exist, leave the current list unchanged and return
    False. A successful load returns True.
    """
    try:
        with open(TODO_FILE, "r", newline="", encoding="utf-8") as csv_file:
            loaded_todos = [row[0] for row in csv.reader(csv_file) if row]
    except FileNotFoundError:
        return False

    todos.clear()
    todos.extend(loaded_todos)
    return True


def main():
    """Run the interactive command-line interface."""
    actions = "add, list, delete, save, load, exit"
    print("Gestor de tareas. Comandos: " + actions)

    while True:
        try:
            command = input("\n¿Qué quieres hacer? ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            break

        if command in {"add", "agregar", "añadir", "a"}:
            title = input("Título de la tarea: ").strip()
            if title:
                add_one_task(title)
                print("Tarea agregada.")
            else:
                print("El título no puede estar vacío.")
        elif command in {"list", "listar", "show", "l"}:
            print_list()
        elif command in {"delete", "eliminar", "remove", "d"}:
            print_list()
            if todos:
                try:
                    position = int(input("Posición de la tarea a eliminar: ").strip())
                except ValueError:
                    print("Introduce una posición numérica válida.")
                    continue
                if delete_task(position):
                    print("Tarea eliminada.")
                else:
                    print("No existe una tarea en esa posición.")
        elif command in {"save", "guardar", "s"}:
            try:
                save_todos()
                print(f"Tareas guardadas en {TODO_FILE}.")
            except OSError as error:
                print(f"No se pudieron guardar las tareas: {error}")
        elif command in {"load", "cargar", "c"}:
            try:
                if load_todos():
                    print(f"Tareas cargadas desde {TODO_FILE}.")
                else:
                    print(f"Todavía no existe {TODO_FILE}.")
            except (OSError, csv.Error) as error:
                print(f"No se pudieron cargar las tareas: {error}")
        elif command in {"exit", "quit", "salir", "q"}:
            print("Hasta luego.")
            break
        else:
            print("Comando no reconocido. Usa: " + actions)


if __name__ == "__main__":
    main()
