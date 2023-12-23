#!/usr/bin/env python3
import typer

import across.release
from across.plot import Plotter

app = typer.Typer()
app.add_typer(across.release.app, name="release", help="Start and finish a release")


# Doesn't work: makes it: across.py plot plot
# app.add_typer(plot.app, name="plot", help="Plot dependencies")
@app.command()
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
