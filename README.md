# UnleashTheGeek2022

## Description

Competiton on platform **Coding Game** with around 150 teams of 3 from all Amadeus sites. 

The python file **mergeFiles.py** reads all python files inside UnleashTheGeek folder and merges them into one single file **UnleashTheGeek2022.py**, with distinct import at the beginning.

The python script can be automatically executed on save by adding this on the seetings.json file (File -> Preferences -> Settings -> Code Actions On Save):
```
  "emeraldwalk.runonsave": {
    "commands": [
      {
        "match": "\\.py$",
        "cmd": "python mergeFiles.py"
      }
    ]
  }
```

The file **UnleashTheGeek2022.py** can be used on Coding Game to synchronise the Coding Game IDE with this file and to automatically execute code on change. 