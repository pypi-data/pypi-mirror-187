# ConfigJ

A json base config lib.

## Usage

```python
from configj import ConfigJ, AbstractConfig

class ConfigData(AbstractConfig):
    config1: str = 'Default Value'
    config2: int = 166

cj = ConfigJ('config.json', ConfigData)
# Type hint
config: ConfigData

# when file not exists, create default config file and return it.
config = cj.load()
print(config.config1)  # Default Value

config.config2 = 1  # set value
cj.save(config)  # save config to file
```