# merge files
import os

folder_name = "/UnleashTheGeek/"

list_files = ["Imports.py", "Coordinate.py", "Tile.py", "Inputs.py", "Game.py",  "main.py"]

merged_file = []
all_imports = []
for file_name in list_files:
    with open(os.getcwd() + folder_name + file_name, "r") as file:
        file_content = file.read()
        imports = list(filter(lambda x: x[0:6] == "import" or x[0:4] == "from", file_content.split("\n")))
        code = list(filter(lambda x: x[0:6] != "import" and x[0:4] != "from", file_content.split("\n")))
        all_imports += imports
        merged_file += code
        merged_file += ["\n"]

all_imports = "\n".join((list(set(all_imports))))
merged_file = all_imports + "\n" + "\n".join(merged_file)

with open(os.getcwd() + "/UnleashTheGeek2022.py", "w") as output_file:
    output_file.write(merged_file)
