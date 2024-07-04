from typing import Any, Dict
from configparser import ConfigParser

def save_config_dict(data: Dict[str, Dict[str, Any]], file_path: str = "config.ini"):
    """
    Save configuration data to a ConfigParser object and write it to a config file.

    Parameters:
        data (Dict[str, Dict[str, Any]]): A dictionary containing configuration data to be saved.
            Each key represents a section, and its value is another dictionary of key-value pairs.
        file_path (str): Path to the config file. Defaults to "config.ini" in the current directory.

    Raises:
        IOError: If there is an error while writing the configuration data to the config file.
    """
    config = ConfigParser()

    for section, section_data in data.items():
        config[section] = {k: str(v) for k, v in section_data.items()}

    try:
        with open(file_path, "w") as f:
            config.write(f)
    except IOError as e:
        raise IOError(f"Error writing config file: {str(e)}")

def load_config(config_class, file_path: str = "config.ini"):
    """
    Load and parse configuration settings from a config file.

    Parameters:
        config_class: configclass
        file_path (str): Path to the config file. Defaults to "config.ini" in the current directory.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary containing the parsed configuration settings.
    """
    config = ConfigParser()
    config.read(file_path)

    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for key, value in config[section].items():
            # Try to convert the value to int or float if possible
            try:
                config_dict[section][key] = int(value)
            except ValueError:
                try:
                    config_dict[section][key] = float(value)
                except ValueError:
                    config_dict[section][key] = value
                    
    return config_class.dict_to_object(config_dict)

