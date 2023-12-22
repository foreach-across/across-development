from dataclasses import dataclass
from typing import List

import dataconf


@dataclass
class Repository:
    name: str
    modules: List[str]


@dataclass
class AcrossConfig:
    repositories: List[Repository]


def parse():
    config = dataconf.load("data-across.yml", AcrossConfig)
    print(config)


if __name__ == '__main__':
    parse()
