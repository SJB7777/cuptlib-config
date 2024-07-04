# XFEL Data Analysis Package for Configuration

This package provides configuration tools for XFEL (X-ray Free Electron Laser) data analysis, including configuration management and I/O utilities.

## Features

- Configuration management using classes and enums
- Support for reading and writing configuration files in (.INI)
- Easily extendable for new configurations and settings

## Installation

You can install this package via pip:

```bash
pip install cuptlib-config
```

## Usage

### Basic Configuration

#### Saving Configuration Settings

Here's an example of how to use the package to save configuration settings:

```python
from cupdlib_config.config_reader import save_config_dict

config_dict = {
    'param': {
        'name': 'sample', 
        'load_dir': 'load', 
        'save_dir': 'save', 
        'image_dir': 'image_dir', 
        'param_dir': 'param_dir'
    }, 
    'path': {
        'beam_energy': 10, 
        'dps': 7.5e-05, 
        'sdd': 1.3, 
        'wavelength': 1239.8419843320025
    }
}

save_config_dict(config_dict, "sample.ini")
```

Configuration file (`sample.ini`):

```ini
[param]
name = sample
load_dir = load
save_dir = save
image_dir = image_dir
param_dir = param_dir

[path]
beam_energy = 10
dps = 7.5e-05
sdd = 1.3
wavelength = 1239.8419843320025
```

#### Loading Configuration Settings

Here's an example of how to use the package to load configuration settings:

```python
import os
from cupdlib_config.configclasses import configclass
from cupdlib_config.config_reader import load_config

@configclass
class ConfigurationPaths:
    load_dir: str = "load_dir"
    save_dir: str = "save_dir"
    param_dir: str = "param_dir"
    image_dir: str = "image_dir"

    def __post_init__(self) -> None:
        self.param_dir = os.path.join(self.save_dir, self.param_dir)
        self.image_dir = os.path.join(self.save_dir, self.image_dir)
        
@configclass
class ConfigurationParameters:
    name: str = "name"
    sdd: float = 1.3
    dps: float = 7.5e-5
    beam_energy: float = 10

    def __post_init__(self) -> None:
        self.wavelength = 12398.419843320025 / self.beam_energy
        
@configclass
class ExperimentConfiguration:
    param: ConfigurationParameters = ConfigurationParameters()
    path: ConfigurationPaths = ConfigurationPaths()

config_dict = load_config(ExperimentConfiguration, "sample.ini")
print(config_dict)
```

Expected Output:

```
ExperimentConfiguration(param=ConfigurationParameters(name='sample', sdd=1.3, dps=7.5e-05, beam_energy=10, wavelength=1239.8419843320025), path=ConfigurationPaths(load_dir='load_dir', save_dir='save_dir', param_dir='save_dir\\param_dir', image_dir='save_dir\\image_dir'))
```

### PAL-XFEL Configuration Classes

The package includes several classes to represent different configurations. For example:

- `ConfigurationParameters`: Represents parameters like hutch settings, detector settings, etc.
- `ConfigurationPaths`: Manages paths for loading and saving data.
- `ExperimentConfiguration`: Combines parameters and paths into a single configuration object.

### Enums

Enums are used to ensure consistency in setting values:

- `Detector`: Enumeration of different detectors.
- `Hutch`: Enumeration of different hutches.
- `Xray`: Enumeration of X-ray types.
- `Hertz`: Enumeration of frequency settings.

### Saving PAL-XFEL Configuration Settings

```python
from pal_xfel.config_io import save_palxfel_dict

config_dict = {
    'path': {
        'load_dir': 'your/path', 
        'save_dir': 'your/path',
        'image_dir': 'Image', 
        'mat_dir': 'mat_files', 
        'npz_dir': 'npz_files', 
        'param_dir': 'DataParameter', 
        'tif_dir': 'tif_files'
    },
    'param': {
        'xray': 'HX',
        'detector': 'jungfrau2',
        'pump_setting': '15HZ',
        'hutch': 'eh1',
        'sdd': 1.3,
        'dps': 7.5e-05,
        'beam_energy': 9.7,
        'x1': 0, 
        'x2': 1, 
        'y1': 2, 
        'y2': 3
    }
}

config_file = "palxfel_setting.ini"

save_palxfel_dict(config_dict, config_file)
```

### Sample PAL-XFEL Configuration File

You can find a sample configuration file (`sample.ini`) in the `cupdlib_config` directory. Here's an example of its content:

```ini
[path]
load_dir = your/path
save_dir = your/path
image_dir = Image
mat_dir = mat_files
npz_dir = npz_files_qbpm
param_dir = DataParameter
tif_dir = tif_files

[param]
xray = HX
detector = jungfrau2
pump_setting = 15HZ
hutch = eh1
sdd = 1.3
dps = 7.5e-05
beam_energy = 9.7
x1 = 0
x2 = 1
y1 = 2
y2 = 3
```

### Paths Configuration

When converting configuration paths into a configuration object, they are combined with the `save_dir` as shown below:

```python
@configclass
class ConfigurationPaths:
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
```

### Loading PAL-XFEL Configuration

```python
from pal_xfel.config_io import load_palxfel_config

palxfel_config = load_palxfel_config("palxfel_setting.ini")
print("palxfel_config: ", palxfel_config)
print("pump_setting: ", palxfel_config.param.pump_setting)
print("mat_dir: ", palxfel_config.path.mat_dir)
```

Expected Output:

```
palxfel_config:  ExperimentConfiguration(param=ConfigurationParameters(hutch='eh1', detector='jungfrau2', xray='HX', pump_setting='15HZ', x1=0, x2=1, y1=2, y2=3, sdd=1.3, dps=7.5e-05, beam_energy=9.7, sigma_factor=1, wavelength=1239.8419843320025), path=ConfigurationPaths(load_dir='your/path', save_dir='your/path', param_dir='DataParameter', image_dir='Image', mat_dir='mat_files', npz_dir='npz_files_qbpm', tif_dir='tif_files'))
pump_setting:  15HZ
mat_dir:  mat_files
```

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact:

- Name: Isaac Yong
- Email: esakyong1866@naver.com

---

### Acknowledgements

This package was developed as part of the research at the Center for Ultrafast Phase Transformation, Sogang University.
