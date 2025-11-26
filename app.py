import sys
from todo import Todo

def main():
    t = Todo()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python app.py add <task>")
        print("  python app.py list")
        print("  python app.py done <task_number>")
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        t.add(task)
        print("Added:", task)

    elif command == "list":
        tasks = t.list()
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task}")

    elif command == "done" and len(sys.argv) == 3:
        index = int(sys.argv[2]) - 1
        t.complete(index)
        print("Completed task:", index + 1)

    else:
        print("Invalid command")

if __name__ == "__main__":
    main()
