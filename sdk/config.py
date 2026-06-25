import os
from pathlib import Path
import yaml
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class WatchConfig(BaseModel):
    project: str
    api_url: str
    token_env: str
    reporter: str

    @classmethod
    def from_yaml(cls, path: str | Path = 'attest.yaml'):
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def resolve_token(self):
        token = os.getenv(self.token_env)
        if token is None:
            raise RuntimeError(f'environment variable {self.token_env} is not set')
        return token
    