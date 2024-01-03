from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple

import dataconf

ACROSS_CONFIG_FILE_NAME = "data-across.yml"


@dataclass
class RepositoryConfig:
    name: str
    color: Optional[str]
    modules: List[str]


@dataclass
class AcrossConfig:
    repositories: List[RepositoryConfig]

    # modules: Dict[str, Repository]

    def __post_init__(self):
        self._modules = dict()
        for repository in self.repositories:
            for module in repository.modules:
                self._modules[module] = repository
        # print(self._modules)

    @property
    def modules(self) -> Dict[str, RepositoryConfig]:
        return self._modules

    @property
    def repository_names(self) -> List[str]:
        return [r.name for r in self.repositories]

    def find_module_repository(self, module_name: str) -> Optional[RepositoryConfig]:
        return self._modules.get(module_name)

    @staticmethod
    def load(directory: Path = Path().absolute()) -> Tuple[Path, "AcrossConfig"]:
        """
        Returns The directory of the root repository (containing data-across.yml)
        and the contents of the data-across.yml file.
        """
        file = _find_config_file(directory)
        if file:
            config = dataconf.load(str(file), AcrossConfig)
            return file.parent, config
        raise (
            Exception(
                f"Could not find {ACROSS_CONFIG_FILE_NAME} in {directory} or above."
            )
        )

    def find_repository_config(self, repo_name) -> Optional[RepositoryConfig]:
        for repository in self.repositories:
            if repository.name == repo_name:
                return repository
        return None


def _find_config_file(dir_path: Path) -> Optional[Path]:
    if dir_path == "/":
        return None
    file = Path(dir_path, ACROSS_CONFIG_FILE_NAME)
    # file = dir_path.ACROSS_CONFIG_FILE_NAME
    if file.is_file():
        return file
    if dir_path.parent:
        return _find_config_file(dir_path.parent)
    return None


if __name__ == "__main__":
    print(AcrossConfig.load())
