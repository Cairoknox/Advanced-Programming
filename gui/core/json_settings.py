#Copyright (c) 2021 Wanderson M. Pimenta
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.
import json
import os

class Settings(object):
    json_file = "settings.json"
    app_path = os.path.abspath(os.getcwd()) #Path of the app
    settings_path = os.path.normpath(os.path.join(app_path, json_file))
    if not os.path.isfile(settings_path):
        print(f"WARNING: \"settings.json\" not found! check in the folder {settings_path}")
    def __init__(self): #Initialize settings
        super(Settings, self).__init__()
        self.items = {}
        self.deserialize()
    def serialize(self): #Write settings
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)
    def deserialize(self): #Read settings
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings
