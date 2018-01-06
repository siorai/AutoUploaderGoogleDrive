import json


def settingsLoader():
    with open("/var/lib/AutoUploaderGoogleDrive/" +
              "AutoUploaderGoogleDrive/AutoUploaderGoogleDrive/" +
              "settingsNew.json", "rb") as settingsDict:
        settings = json.load(settingsDict)
    return settings
