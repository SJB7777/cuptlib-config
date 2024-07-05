"""
experiment_config.py

This module provides specific classes for managing configuration parameters of an experiment. It builds upon the generic configuration management provided by the base_config module.

Classes:
    - `ConfigurationParameters`: A class representing configuration parameters for an experiment.
    - `ConfigurationPaths`: A class to manage configuration paths for an experiment.
    - `ExperimentConfiguration`: A dataclass representing the complete configuration for an experiment, combining configuration parameters and paths.
"""

import os

from ..basic_config.configclasses import configclass
from ..palxfel.enums import *

@configclass
class ConfigurationParameters:
    """
    A dataclass to represent configuration parameters for an experiment.

    Attributes:
        hutch (Hutch): The hutch setting.
        detector (Detector): The detector setting.
        xray (Xray): The x-ray setting.
        pump_setting (Hertz): The pump setting.
        x1 (int): The x1 setting.
        x2 (int): The x2 setting.
        y1 (int): The y1 setting.
        y2 (int): The y2 setting.
    """
    hutch: Hutch = Hutch.EH1
    detector: Detector = Detector.JUNGFRAU2
    xray: Xray = Xray.HARD
    pump_setting: Hertz = Hertz.FIFTEEN,
    x1: int = 0
    x2: int = 1
    y1: int = 2
    y2: int = 3
    sdd: float = 1.3
    dps: float = 7.5e-5
    beam_energy: float = 10
    sigma_factor: float = 1
    
    def __post_init__(self) -> None:
        # h * c / e / self.beam_energy / 1e-10 
        # Wavelength of Xray in Angstrom.
        self.wavelength =  12398.419843320025 / self.beam_energy 


@configclass
class ConfigurationPaths:
    """
    A class to manage configuration paths for an experiment.

    Attributes:
        load_dir (str): The load directory path.
        save_dir (str): The save directory path.
    """
    load_dir: str = ""
    save_dir: str = ""
    param_dir: str = "DataParameter"
    image_dir: str = "Image"
    mat_dir: str = "mat_files"
    npz_dir: str = "npz_files"
    tif_dir: str = "tif_files"

    def __post_init__(self) -> None:
        self.param_dir = os.path.join(self.save_dir, self.param_dir)
        self.image_dir = os.path.join(self.save_dir, self.image_dir)
        self.mat_dir = os.path.join(self.save_dir, self.mat_dir)
        self.npz_dir = os.path.join(self.save_dir, self.npz_dir)
        self.tif_dir = os.path.join(self.save_dir, self.tif_dir)


@configclass
class ExperimentConfiguration():
    """
    A dataclass to represent the complete configuration for an experiment.

    Attributes:
        param (ConfigurationParameters): The configuration parameters.
        path (ConfigurationPaths): The configuration paths.
    """
    param: ConfigurationParameters = ConfigurationParameters()
    path: ConfigurationPaths = ConfigurationPaths()