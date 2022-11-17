# merge files
import os

folderName = "/UnleashTheGeek/"

print(os.getcwd())
print(os.listdir(os.getcwd() + folderName))
# os.listdir(os.getcwd()+ folderName)
listFiles = ["Imports.py", "Tile.py", "Robot.py",
             "Inputs.py", "Game.py",  "main.py"]

wholeFile = ""
for fileName in listFiles:
    with open(os.getcwd() + folderName + fileName, "r") as file:
        wholeFile += file.read()
        wholeFile += "\n\n\n"

with open(os.getcwd() + "/UnleashTheGeek2022.py", "w") as outputFile:
    outputFile.write(wholeFile)
