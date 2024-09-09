import requests
from InquirerPy import inquirer
import shutil
import pyfiglet
import os

api_url = "http://127.0.0.1:8000/tasks"
iterador_id = 0


def center_menu_options(text):
    total_width = shutil.get_terminal_size().columns - 10
    text_length = len(text)
    total_spaces = total_width - text_length - 2
    left_spaces = total_spaces // 2
    right_spaces = total_spaces - left_spaces

    return f"--<{' ' * left_spaces}{text}{' ' * right_spaces}>--"


def center_figlet_text(figlet_text):
    lines = figlet_text.split("\n")
    terminal_width = os.get_terminal_size().columns
    centered_lines = [
        line.center(terminal_width) for line in lines if line.strip() != ""
    ]
    return "\n".join(centered_lines)


def menu():
    global iterador_id
    header = pyfiglet.figlet_format("Requests")
    centered_header = center_figlet_text(header)
    print("\n" + centered_header + "\n")

    options = [
        "Create/Update a task",
        "List a task",
        "List all task",
        "Delete a task",
        "Exit",
    ]

    centered_options = [center_menu_options(option) for option in options]

    choice = inquirer.select(
        message="\n",
        instruction="Selecione uma opção ('Ctrl'+'C' para sair):",
        choices=centered_options,
        default=centered_options[0],
        wrap_lines=False,
        border=True,
        pointer="👉",
        qmark="$",
    ).execute()

    if choice == centered_options[0]:
        task_name = input("Task name: ")
        task_description = input("Task description: ")
        task_status = input("Task done (True/False): ").capitalize()
        task_data = {
            "id": iterador_id,
            "name": task_name,
            "description": task_description,
            "done": task_status,
        }
        response = requests.get(api_url, json=task_data)
        if response.status_code == 200:
            print("Task created successfully!")
            iterador_id += 1
        else:
            print("Error creating task")
            print(response.status_code, response.text)

    elif choice == centered_options[1]:
        task_id = input("Task ID: ")
        response = requests.get(api_url + task_id)
        if response.status_code == 200:
            task = response.json()
            print(f"Task ID: {task['id']}")
            print(f"Task Name: {task['name']}")
            print(f"Task Description: {task['description']}")
            print(f"Task Done: {task['done']}")
        else:
            print("Task not found")

    elif choice == centered_options[2]:
        for task_id in range(iterador_id):
            response = requests.get(api_url + str(task_id))
            if response.status_code == 200:
                task = response.json()
                print(f"Task ID: {task['id']}")
                print(f"Task Name: {task['name']}")
                print(f"Task Description: {task['description']}")
                print(f"Task Done: {task['done']}")
                print()

    elif choice == centered_options[3]:
        task_id = input("Task ID: ")
        response = requests.delete(api_url + task_id)
        if response.status_code == 200:
            print("Task deleted successfully!")
        else:
            print("Task not found")

    else:
        print("Exiting...")
        exit()


if __name__ == "__main__":
    while True:
        menu()
