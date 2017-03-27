import click
import json
import sys

from bevos import ghapi
from typing import Optional

@click.group()
def cli() -> None:
    pass

@cli.command()
@click.argument("owner")
@click.argument("repo")
@click.option("--tag", required=True)   # type: ignore # Option descends from Argument, where required is defined
@click.option("--target", default="master")
@click.option("--verbose", "-V", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--description", default="")
@click.option("--token-path", envvar="GH_TOKEN_PATH", type=click.Path(exists=True))
def release(owner: str, repo: str, tag: str, target: str, verbose: bool, dry_run: bool, description: str, token_path: Optional[str]) -> None:

    if token_path is None:
        raise click.UsageError("No path to a github api token defined. Specify GH_TOKEN_PATH or use --token-path.")

    click.echo("I'm doing a release! to {repo}".format(repo=repo))
    endpoint = ghapi.make_release_endpoint(owner, repo)
    url = ghapi.endpoint_url("https://github.com", endpoint)
    if verbose:
        click.echo("POST {url}".format(url=url))
        click.echo(json.dumps(ghapi.make_release_data(tag, target, description, True), indent=4))

    result = ghapi.perform_release(owner, repo, tag, target, description, dry_run)
    click.echo(result.message())
    if not result.success:
        sys.exit(1)