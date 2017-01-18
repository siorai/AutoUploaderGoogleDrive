import json


def settingsLoader():
    with open("/var/lib/AutoUploaderGoogleDrive/AutoUploaderGoogleDrive/AutoUploaderGoogleDrive/settings.json", "rb") as settingsDict:
        settings = json.load(settingsDict)
    return settings

#def settingsValidator(filename=None):



