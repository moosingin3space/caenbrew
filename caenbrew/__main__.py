# -*- coding: utf-8 -*-
import click

import caenbrew.packages

from . import get_config
from .packages import load_packages


@click.group()
@click.option("--verbose/-v",
              default=None,
              help="Show all output")
@click.pass_context
def cli(ctx, verbose):
    """caenbrew -- install packages on CAEN."""
    config = get_config()

    # Check against `None` because the user can specify a default verbosity in
    # their config file.
    if verbose is not None:
        config["verbose"] = verbose

    packages = load_packages(caenbrew.packages)
    packages = {i: j(config) for i, j in packages.iteritems()}

    ctx.obj = {
        "config": config,
        "packages": packages,
    }


@cli.command()
@click.argument("name")
@click.pass_context
def install(ctx, name):
    """Install a package."""
    try:
        package = ctx.obj["packages"][name]
    except KeyError:
        click.echo("Package {} not found.".format(name))
        return

    if package.is_installed:
        click.echo("Package {} already installed."
                   .format(click.style(name, bold=True)))
        return

    with package.prepare():
        package.download()
        package.install()

    click.echo("{} Package {} installed."
               .format(click.style("✓", fg="green"),
                       click.style(package.name, bold=True)))
