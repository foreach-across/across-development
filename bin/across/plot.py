from typing import Dict

import graphviz as gv  # type: ignore
import typer

from .config import AcrossConfig
from .repository import Repository


class Plotter:
    # config: AcrossConfig
    # repos: list[Repository]
    # module_id_to_repository: dict[str, Repository]
    # projects: dict[str, Project]

    def __init__(self, all_modules: bool, versions: bool):
        self.all_modules = all_modules
        self.versions = versions
        directory, self.config = AcrossConfig.load()
        self.repositories = Repository.read_all(directory)
        self.module_id_to_repository = self._build_module_id_to_repository()
        self.projects = dict()
        for repo in self.repositories:
            for project in repo.projects.values():
                self.projects[project.artifact_id] = project

    def _build_module_id_to_repository(self) -> Dict[str, Repository]:
        """Builds a dictionary from artifactId to the corresponding Git repository"""
        result = dict()
        for repo in self.repositories:
            for project in repo.projects.values():
                result[project.artifact.artifact_id] = repo
        return result

    def build_repo_graph(self) -> gv.Digraph:
        g = gv.Digraph(
            comment="Across repo dependencies",
            graph_attr={
                "bgcolor": "transparent",
            },
        )
        for repo in self.repositories:
            node_label = repo.name
            if self.versions:
                node_label += "\n" + repo.version
            g.node(repo.name, label=node_label)
            for artifactId, version in repo.versioned_deps.items():
                dependency_repo = self.module_id_to_repository[artifactId]
                if repo != dependency_repo:
                    self._make_edge(
                        g,
                        repo.name,
                        dependency_repo.name,
                        version,
                        dependency_repo.version,
                    )
        return g

    def build_module_graph(self) -> gv.Digraph:
        show_versions: bool = self.versions
        g = gv.Digraph(
            comment="Across module dependencies",
            graph_attr={
                "bgcolor": "transparent",
            },
        )
        for repo in self.repositories:
            repo_config = self.config.find_repository_config(repo.name)
            for project in repo.projects.values():
                if project.artifact.packaging != "pom" and (
                    self.all_modules or project.artifact_id in self.config.modules
                ):
                    node_label = project.artifact_id
                    if show_versions:
                        node_label += "\n" + project.artifact.version
                    g.node(
                        project.artifact_id,
                        label=node_label,
                        color=repo_config.color if repo_config else None,
                        href="https://foreach-across.github.io/modules/%s/"
                        % project.artifact_id,
                    )
                    for dep in project.direct_dependencies:
                        if dep.is_foreach() and (
                            self.all_modules or dep.artifact_id in self.config.modules
                        ):
                            head_project = self.projects[dep.artifact_id]
                            self._make_edge(
                                g,
                                project.artifact_id,
                                dep.artifact_id,
                                dep.version,
                                head_project.version,
                            )
        return g

    def _make_edge(
        self,
        g: gv.Digraph,
        tail_name: str,
        head_name: str,
        dependency_version: str,
        head_version: str,
    ):
        edge_label = None
        edge_color = None
        if self.versions:
            edge_label = dependency_version
            # TODO: use git branch here as well:
            if dependency_version != head_version:
                if (
                    dependency_version.endswith("-SNAPSHOT")
                    and head_version == "local-SNAPSHOT"
                ):
                    edge_color = "orange"
                else:
                    edge_color = "red"
            else:
                edge_color = "black"
        g.edge(tail_name, head_name, label=edge_label, fontcolor=edge_color)


app = typer.Typer()

if __name__ == "__main__":
    app()
