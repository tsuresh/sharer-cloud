import json
from types import SimpleNamespace

data = open('test_config.json').read();

configs = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))