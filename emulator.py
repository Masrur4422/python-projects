import datetime
from zipfile import ZipFile, ZipInfo
import io

filepath = "test.zip"
user = "admin"
computer = "test_computer"
name_of_system = "Linux"
current_dir = "/"
# Список для отслеживания добавленных файлов (симуляция)
added_files = []


# Function to display current working directory
def get_current_dir():
    return current_dir


def change_directory(new_dir, zip_file):
    global current_dir

    if new_dir.startswith("/"):
        temp_dir = new_dir
    else:
        temp_dir = f"{current_dir}/{new_dir}".strip("/")

    possible_dirs = [
        file
        for file in zip_file.namelist()
        if file.startswith(temp_dir.strip("/") + "/")
    ]

    if possible_dirs:
        current_dir = "/" + temp_dir.strip("/")
    else:
        print(f"cd: no such directory: {new_dir}")



def reverse_string(input_string):
    return input_string[::-1]



def touch(filename, zip_file):
    full_path = f"{current_dir.strip('/')}/{filename}".strip("/")

    if full_path in zip_file.namelist() or full_path in added_files:
        print(f"touch: cannot touch '{filename}': File exists")
    else:
        added_files.append(full_path)
        print(f"Created empty file: {full_path}")


with ZipFile(filepath, "r") as zip_file:
    while True:
        command = input(f"{user}:{computer}$ ")

        if command == "exit":
            break

        elif command == "ls":
            print(zip_file.namelist() + added_files)

        elif command == "pwd":
            print(current_dir)

        elif command.startswith("cd "):
            _, new_dir = command.split(" ", 1)
            change_directory(new_dir, zip_file)

        elif command == "uname":
            print(f"{name_of_system}  {user} {computer}")

        elif command == "datetime":
            current_time = datetime.datetime.now().time()
            print(current_time)

        elif command == "tree":
            for tree in zip_file.namelist() + added_files:
                print(tree)

        elif command.startswith("rev "):
            _, argument = command.split(" ", 1)
            reversed_argument = reverse_string(argument)
            print(reversed_argument)

        elif command.startswith("touch "):
            _, filename = command.split(" ", 1)
            touch(filename, zip_file)

        elif command.startswith("cat "):
            _, filename = command.split(" ", 1)
            if filename in zip_file.namelist() or filename in added_files:
                if filename in zip_file.namelist():
                    with zip_file.open(filename) as file:
                        print(file.read().decode())
                else:
                    print(f"{filename} is empty")
            else:
                print(f"cat: {filename}: Нет такого файла в архиве")

        else:
            print("Введите допустимую команду (ls, pwd, exit, datetime, tree, rev, touch)")