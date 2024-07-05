from ..basic_config.config_reader import load_config, save_config_dict
from ..palxfel.setting import ExperimentConfiguration

def load_palxfel_config(file: str) -> ExperimentConfiguration:
    return load_config(ExperimentConfiguration, file)

def save_palxfel_dict(config_dict, file) -> None:
    save_config_dict(config_dict, file)


if __name__ == "__main__":
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
    
    config = load_palxfel_config(config_file)
    print("config object:\n", config)
    