#!/usr/bin/env python3
import typer

from across.plot import Plotter

app = typer.Typer()


@app.command(
    help="""
    Output dependencies between repositories and/or modules, which can be plotted using GraphViz:
    ax-dependencies.py [OPTIONS] | tred | dot -Tsvg > deps.svg
    """
)
def plot(
    modules: bool = True,
    repositories: bool = False,
    all_modules: bool = False,
    versions: bool = False,
):
    if not modules and not repositories:
        raise (Exception("Must plot at least one of repositories or modules"))
    if modules and repositories:
        # Requires using GraphViz clusters
        raise (Exception("Plotting repositories and modules is not yet supported."))
    plotter = Plotter(all_modules, versions)
    if modules:
        g = plotter.build_module_graph()
    else:
        g = plotter.build_repo_graph()
    print(g.source)


if __name__ == "__main__":
    app()
