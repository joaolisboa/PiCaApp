import json
import os

class Config:

    def __init__(self, file):
        workingDir = os.getcwd()
        self.file = workingDir + file
        self.data = self.readConfigFile()

    def readConfigFile(self):
        with open(self.file, "r") as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
            return data

    def writeConfigFile(self):
        with open(self.file, "w") as jsonFile:
            json.dump(self.data, jsonFile, indent=4)
            jsonFile.close()

    def get(self, key, **value):
        if key in self.data:
            return self.data[key]
        # return default value if no value in config is set
        if 'default' in value:
            return value['default']
        return False

    def set(self, key, value):
        self.data[key] = value
        self.writeConfigFile()
        return True