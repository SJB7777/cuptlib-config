"""
configclass module

This module provides a custom decorator to create configuration classes,
along with utility functions for configuration management.
The decorator automatically creates an __init__ method, sets class attributes,
and supports type annotations, default values, and __post_init__.
"""

class ConfigDictConvert:
    """
    Utility class to convert objects to configuration dictionaries.
    """
    def to_config_dict(self):
        """
        Converts the object's attributes to a dictionary.

        Returns:
            dict: A dictionary containing the object's attribute values.
        """
        def convert(value):
            if hasattr(value, 'to_config_dict') and callable(getattr(value, 'to_config_dict')):
                return value.to_config_dict()
            return value

        cls_dict = {}
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                if not callable(value) and not isinstance(value, (property, type)):
                    cls_dict[name] = convert(value)
        
        return cls_dict


def config_root(cls):
    setattr(cls, "to_config_dict", ConfigDictConvert.to_config_dict)
    return cls


def configclass(cls):
    """
    A custom decorator to create configuration classes.
    This decorator automatically creates __init__ method, sets class attributes,
    and supports type annotations, default values, and __post_init__.
    Work like dataclass but simpler.
    """
    annotations = getattr(cls, '__annotations__', {})
    
    # Get class attributes, including those without type hints
    class_attributes = {
        name: value for name, value in cls.__dict__.items()
        if not name.startswith('__') and not callable(value)
    }
    
    # Combine all parameters
    all_params = list(annotations.keys()) + [name for name in class_attributes if name not in annotations]
    
    # Prepare default values
    param_defaults = {
        name: getattr(cls, name)
        for name in all_params
        if hasattr(cls, name)
    }
    
    # Validate that default arguments do not precede non-default arguments
    non_defaults_met = False
    for param in all_params:
        if param in param_defaults:
            non_defaults_met = True
        elif non_defaults_met:
            raise TypeError(f'non-default argument {param!r} follows default argument')

    def __init__(self, *args, **kwargs):
        
        merged_args = param_defaults.copy()
        merged_args.update(dict(**dict(zip(all_params, args)), **kwargs))
        
        for name in all_params:
            if name in merged_args:
                setattr(self, name, merged_args[name])
            elif name not in param_defaults:
                raise TypeError(f'Missing required argument: {name}')
        
        # Call __post_init__ if it exists
        if hasattr(self, '__post_init__'):
            self.__post_init__()
            
    def __repr__(self) -> str:
        """
        Returns a string representation of the ConfigurationPaths object.

        Returns:
            str: A human-readable string representation of the object.
        """
        class_name = type(self).__name__
        attribute_values = {
            key.replace(f"_{class_name}__", ""): value
            for key, value in vars(self).items()
        }
        attributes = ", ".join(
            f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
            for key, value in attribute_values.items()
        )
        return f"{class_name}({attributes})"
    
    @classmethod
    def dict_to_object(cls, config_dict: dict):
        """
        Creates an object of the given class using configuration data from a dictionary.

        Args:
            cls (type): The class type to create an object of.
            config_dict (dict): A dictionary containing configuration data.

        Returns:
            object: An instance of the class with attributes set based on the config_dict.
        """
        instance = cls()

        for name, value in config_dict.items():
            if hasattr(instance, name):
                attr = getattr(instance, name)

                if hasattr(attr, 'to_config_dict') and callable(getattr(attr, 'to_config_dict')):
                    # Check if this is the deepest class with to_config_dict
                    if isinstance(value, dict) and not any(hasattr(v, 'to_config_dict') for v in value.values() if isinstance(v, object)):
                        # This is the deepest class, create it using class(name=value)
                        setattr(instance, name, attr.__class__(**value))
                    else:
                        # Recursively convert nested objects
                        setattr(instance, name, attr.__class__.dict_to_object(value))
                elif callable(attr) and hasattr(attr, "setter"):
                    # If it's a setter method, call it with the corresponding value
                    attr(value)
                elif isinstance(attr, property) and hasattr(attr, "fset"):
                    # If it's a property with a setter, call the setter with the value
                    attr.fset(instance, value)
                else:
                    setattr(instance, name, value)

        return instance
    
    cls.__init__ = __init__
    cls.__repr__ = __repr__
    cls.dict_to_object = dict_to_object
    
    return config_root(cls)