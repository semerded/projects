import globals, json
def readJson() -> dict | list:
    with open(globals.JSON_FILE_LOCATION) as filePath:
        return json.load(filePath)
        
def saveJson(data: dict | list):
    with open(globals.JSON_FILE_LOCATION, 'w') as json_file:
        json.dump(data, json_file, indent = 4, separators=(',',': '))
        