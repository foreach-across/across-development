#!/usr/bin/env python3

import argparse
from typing import Dict, Any

import graphviz as gv  # type: ignore
import networkx as ns  # type: ignore

from across.config import parse
from across.model import Project, Repository
from across.config import AcrossConfig


# ax-plot-deps.py | tred | dot -Tsvg > repo-deps.svg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--versions",
        help="Include versions in modules/repos and dependencies",
        action="store_true",
    )
    # TODO subcommands repo and module instead of an option
    parser.add_argument(
        "--modules",
        help="Plot modules instead of repository",
        action="store_true",
    )
    parser.add_argument(
        "--all",
        help="Include all modules",
        action="store_true",
    )
    args = parser.parse_args()
    app = Application(args)
    app.run()


class Application:
    config: AcrossConfig
    repos: list[Repository]
    module_id_to_repository: dict[str, Repository]
    projects: dict[str, Project]

    def __init__(self, args: Any):
        self.args = args
        self.config = parse()
        self.repos = Repository.read_all()
        self.module_id_to_repository = self._build_module_id_to_repository()
        self.projects = dict()
        for repo in self.repos:
            for project in repo.projects.values():
                self.projects[project.artifact_id] = project

    def run(self):
        if self.args.modules:
            g = self.build_module_graph()
        else:
            g = self.build_repo_graph()
        print(g.source)

    def _build_module_id_to_repository(self) -> Dict[str, Repository]:
        """Builds a dictionary from artifactId to the corresponding Git repository"""
        result = dict()
        for repo in self.repos:
            for project in repo.projects.values():
                result[project.artifact.artifact_id] = repo
        return result

    def build_repo_graph(self) -> gv.Digraph:
        show_versions: bool = self.args.versions
        g = gv.Digraph(
            comment="Across repo dependencies"
        )  # , graph_attr={"rankdir": "LR"})
        for repo in self.repos:
            node_label = repo.name
            if show_versions:
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
        show_versions: bool = self.args.versions
        g = gv.Digraph(
            comment="Across module dependencies"
        )  # , graph_attr={"rankdir": "LR"})
        for repo in self.repos:
            for project in repo.projects.values():
                if project.artifact.packaging != "pom" and (
                    self.args.all or project.artifact_id in self.config.modules
                ):
                    node_label = project.artifact_id
                    if show_versions:
                        node_label += "\n" + project.artifact.version
                    g.node(
                        project.artifact_id,
                        label=node_label,
                        color=self.config.modules.get(project.artifact_id).color,
                    )
                    for dep in project.direct_dependencies:
                        if dep.is_foreach() and (
                            self.args.all or dep.artifact_id in self.config.modules
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
        if self.args.versions:
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


# TODO plot declared dependencies vs all dependencies (recursive or via brute-force, heuristic dependency:tree)
if __name__ == "__main__":
    main()
