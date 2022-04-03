import json
import os

class JsonSave:
    indent = 4
    sort_keys = True

    @classmethod
    def set_formatting(cls, indent=4, sort_keys=True):
        cls.indent, cls.sort_keys = indent, sort_keys

    @classmethod
    def clear_formatting(cls):
        cls.indent, cls.sort_keys = None, False

    @classmethod
    def save(cls, file_path, key, value):
        data = JsonSave.get_contents(file_path)
        data[key] = value
        with open(file_path, 'w+') as f:
            json.dump(data, f, indent=cls.indent, sort_keys=cls.sort_keys)
    
    @staticmethod
    def load(file_path, key, default_value=dict()):
        value = default_value
        if not os.path.exists(file_path):
            JsonSave.save(file_path, key, default_value)

        with open(file_path, 'r+') as f:
            value = json.load(f).get(key)
        
        if not value:
            value = default_value
            JsonSave.save(file_path, key, default_value)
        return value

    @classmethod
    def set_contents(cls, file_path, contents=None):
        with open(file_path, 'w+') as f:
            if contents:
                json.dump(contents, f, indent=cls.indent, sort_keys=cls.sort_keys)

    @staticmethod
    def get_contents(file_path):
        if not os.path.exists(file_path):
            JsonSave.set_contents(file_path, dict())
            return dict()
        
        with open(file_path, 'r+') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = dict()
        return data

    @staticmethod
    def clear_contents(file_path):
        JsonSave.set_contents(file_path)

    @staticmethod
    def delete_key(file_path, key):
        data = JsonSave.get_contents(file_path)
        del data[key]
        JsonSave.set_contents(file_path, data)

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)