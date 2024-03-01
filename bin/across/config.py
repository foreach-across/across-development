from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Set

import dataconf

ACROSS_CONFIG_FILE_NAME = "across.yml"


@dataclass
class ModuleConfig:
    id: str
    name: Optional[str]
    key: Optional[str]
    java_package: Optional[str]
    java_class: Optional[
        str
    ]  # class is a keyword, and dataconf cannot use an alternative field name
    refdoc: Optional[str]
    javadoc: Optional[str]
    bitbucket: Optional[str]
    description: Optional[str]

    @property
    def artifact_id(self) -> str:
        return self.id


@dataclass
class RepositoryConfig:
    id: str
    color: Optional[str]
    modules: List[ModuleConfig]
    key: Optional[str]
    bitbucket: Optional[str]
    refdoc: Optional[str]
    group: str

    @property
    def group_id(self) -> str:
        return self.group


@dataclass
class AcrossConfig:
    git_root_url: str
    repositories: List[RepositoryConfig]

    # modules: Dict[str, Repository]

    def __post_init__(self):
        self._modules = dict()
        for repository in self.repositories:
            for module in repository.modules:
                self._modules[module.id] = repository
        # print(self._modules)

    @property
    def modules(self) -> Dict[str, RepositoryConfig]:
        return self._modules

    @property
    def repository_ids(self) -> List[str]:
        return [r.id for r in self.repositories]

    @property
    def group_ids(self) -> Set[str]:
        return {repo.group_id for repo in self.repositories}

    def __getitem__(self, item: str) -> RepositoryConfig:
        for repository in self.repositories:
            if repository.id == item:
                return repository
        raise KeyError(f"Could not find repository {item} in {ACROSS_CONFIG_FILE_NAME}")

    def find_module_repository(self, module_name: str) -> Optional[RepositoryConfig]:
        return self._modules.get(module_name)

    @staticmethod
    def load(directory: Path = Path().absolute()) -> Tuple[Path, "AcrossConfig"]:
        """
        Returns The directory of the root repository (containing across.yml)
        and the contents of the across.yml file.
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
            if repository.id == repo_name:
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
