import json
import os
from typing import Any

class JsonSave:
    """
    Easily save value-key pairs to json files

    Attributes
    ----------
    indent : int
        The json file format indent number of spaces (default: 4)
    sort_keys : bool
        If sort_keys is true (default: False), then the output of dictionaries will be sorted by key.
    """
    indent = 4
    sort_keys = False

    @classmethod
    def set_formatting(cls, indent=4, sort_keys=True) -> None:
        """
        Sets the json file formatting style

        Parameters
        ----------
        indent : int, optional
            The number of spaces to indent the file. If set to None, the dictionary is stored in the json file on one line without formatting
        sort_keys : bool
            If sort_keys is true (default: False), then the output of dictionaries will be sorted by key.

        Returns
        -------
        None
        """
        cls.indent, cls.sort_keys = indent, sort_keys

    @classmethod
    def clear_formatting(cls) -> None:
        """
        Sets the json file formatting style to the default (no formatting)

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        cls.indent, cls.sort_keys = None, False

    @classmethod
    def save(cls, file_path, key, value) -> None:
        """
        Saves a value to the specified key in the json file

        Parameters
        ----------
        file_path : str
            The path of the json file that the data is saved in
        key : str
            The key that corresponds to the data being stored
        value: Any
            The data being stored

        Returns
        -------
        None
        """
        data = JsonSave.get_contents(file_path)
        data[key] = value
        with open(file_path, 'w+') as f:
            json.dump(data, f, indent=cls.indent, sort_keys=cls.sort_keys)

    @staticmethod
    def load(file_path, key, default_value=dict()) -> Any:
        """
        Loads the value corresponding to the key in the json file

        Parameters
        ----------
        file_path : str
            The path of the json file that the data is saved in
        key : str
            The key that corresponds to the data being retrieved
        default_value: Any
            The default value to be stored and returned if there is no existing value

        Returns
        -------
        Any
            The value corresponding with the key. If there is no value, returns the default value
        """
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
    def set_contents(cls, file_path, contents=None) -> None:
        """
        Overrides the content of a json file. If the file does not exist, creates a new file and stores the contents in the file.

        Parameters
        ----------
        file_path : str
            The path of the json file that the data is saved in
        contents : Any, optional
            The contents to populate the file with

        Returns
        -------
        None
        """
        with open(file_path, 'w+') as f:
            if contents:
                json.dump(contents, f, indent=cls.indent, sort_keys=cls.sort_keys)

    @staticmethod
    def get_contents(file_path) -> Any:
        """
        Returns the contents of a json file. If the file does not exist, creates a new file and returns an empty dictionary.

        Parameters
        ----------
        file_path : str
            The path of the json file that the data is saved in

        Returns
        -------
        Any
            The contents to populate the file with
        """
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
    def clear_contents(file_path) -> None:
        """
        Clears the contents of a json file. If the file doesn't exist, creates a new file

        Parameters
        ----------
        file_path : str
            The path of the json file that the data is saved in

        Returns
        -------
        None
        """
        JsonSave.set_contents(file_path)

    @staticmethod
    def delete_key(file_path, key) -> None:
        """
        Deletes the specified key-value pair from the json file

        Parameters
        ----------
        file_path : str
            The path of the json file that the data is saved in
        key : str
            The key being deleted

        Returns
        -------
        None
        """
        data = JsonSave.get_contents(file_path)
        del data[key]
        JsonSave.set_contents(file_path, data)

    @staticmethod
    def delete_file(file_path) -> None:
        """
        Deletes the specified file

        Parameters
        ----------
        file_path : str
            The path of the file

        Returns
        -------
        None
        """
        if os.path.exists(file_path):
            os.remove(file_path)