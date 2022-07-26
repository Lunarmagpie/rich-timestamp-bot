import dataclasses

import dotenv


@dataclasses.dataclass
class Config:
    token: str
    invite_link: str


CONFIG = Config(
    **{k.lower(): v for k, v in dotenv.dotenv_values(".env").items()}  # type: ignore
)
