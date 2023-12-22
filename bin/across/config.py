from dataclasses import dataclass
from typing import List, Dict, Optional

import dataconf


@dataclass
class Repository:
    name: str
    color: Optional[str]
    modules: List[str]


@dataclass
class AcrossConfig:
    repositories: List[Repository]
    # modules: Dict[str, Repository]

    def __post_init__(self):
        self.modules = dict()
        for repository in self.repositories:
            for module in repository.modules:
                self.modules[module] = repository
        # print(self.modules)


def parse():
    config = dataconf.load("data-across.yml", AcrossConfig)
    # print(config)
    return config


if __name__ == "__main__":
    parse()
