import os
import yaml
from pathlib import Path
from dotmap import DotMap

def load_only_current_env(config):
    configs = yaml.load(config)
    return configs[os.environ['ENV']]

config_files = [os.path.join(r, file) for r, d, f in os.walk(os.environ['CONFIG']) for file in f if '.yaml' in file]
config = DotMap({Path(cfg).stem: load_only_current_env(open(cfg, 'r')) for cfg in config_files})
