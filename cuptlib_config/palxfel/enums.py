"""
experiment_enums.py

This module defines enumerations for various experiment configurations. It includes enums for detectors, hutch settings, X-ray types, and Hertz settings, 
providing a structured approach to handle these configuration options.

Classes:
    - `Detector`: Enum representing different types of detectors.
    - `Hutch`: Enum representing different hutch settings.
    - `Xray`: Enum representing different X-ray types.
    - `Hertz`: Enum representing different Hertz settings.

Each enum class provides a method to get a string representation of the enum value.
"""

from enum import Enum, auto

class Detector(Enum):
    """
    Enum representing different types of detectors.

    To add a new detector, follow these steps:

    1. Add the detector name in all uppercase:
        <DETECTOR_NAME> = auto()
    
    2. Add the string representation in the __str__ method:
        elif self == Detector.<DETECTOR_NAME>:
            return '<detector_name>'
    """
    JUNGFRAU1 = auto()
    JUNGFRAU2 = auto()

    def __str__(self):
        if self == Detector.JUNGFRAU1:
            return 'jungfrau1'
        elif self == Detector.JUNGFRAU2:
            return 'jungfrau2'
        else:
            return None

class Hutch(Enum):
    """
    Enum representing different hutch settings.

    To add a new hutch, follow these steps:

    1. Add the hutch name in all uppercase:
        <HUTCH_NAME> = auto()
    
    2. Add the string representation in the __str__ method:
        elif self == Hutch.<HUTCH_NAME>:
            return '<hutch_name>'
    """
    EH1 = auto()
    EH2 = auto()

    def __str__(self):
        if self == Hutch.EH1:
            return 'eh1'
        elif self == Hutch.EH2:
            return 'eh2'
        else:
            return None

class Xray(Enum):
    """
    Enum representing different X-ray types.

    DO NOT MODIFY THIS CLASS.
    """
    SOFT = auto()
    HARD = auto()

    def __str__(self):
        if self == Xray.SOFT:
            return 'SX'
        elif self == Xray.HARD:
            return 'HX'
        else:
            return None

class Hertz(Enum):
    """
    Enum representing different Hertz settings.

    DO NOT MODIFY THIS CLASS.
    """
    ZERO = auto()
    TEN = auto()
    FIFTEEN = auto()
    TWENTY = auto()
    THIRTY = auto()
    SIXTY = auto()

    def __str__(self):
        if self == Hertz.ZERO:
            return '0HZ'
        elif self == Hertz.TEN:
            return '10HZ'
        elif self == Hertz.FIFTEEN:
            return '15HZ'
        elif self == Hertz.TWENTY:
            return '20HZ'
        elif self == Hertz.THIRTY:
            return '30HZ'
        elif self == Hertz.SIXTY:
            return '60HZ'
        else:
            return None