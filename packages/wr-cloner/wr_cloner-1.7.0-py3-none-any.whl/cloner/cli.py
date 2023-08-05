import logging
import queue
import threading

import click
from requests import HTTPError

from cloner.__version__ import __version__
from cloner.clone_repos import clone_repos
from cloner.obtain_repos import obtain_repos
from cloner.split_queue import split_queue

repository_list_queue_lock = threading.Lock()
repository_list_queue = queue.Queue()

LOGGING_LEVELS = {
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def setup_logging(level: str) -> None:
    """Logging setup and configuration."""
    logging.basicConfig(
        level=LOGGING_LEVELS[level], format="%(levelname)s - %(message)s"
    )


@click.command()
@click.version_option(prog_name="cloner", version=__version__)
@click.argument("github_organization")
@click.option(
    "--token",
    "token",
    type=str,
    default=None,
    help="GitHub token to read private repos. This parameter is needed when cloning from an GitHub Enterprise server.",
    show_default=True,
)
@click.option(
    "--ghe",
    "github_enterprise",
    type=str,
    default=None,
    help="GitHub Enterprise URL. "
    "It needs the GITHUB_ORGANIZATION parameter to clone repos from there and the TOKEN option as well.",
    show_default=True,
)
@click.option(
    "--threads",
    "threads",
    type=int,
    default=4,
    help="Number of threads and processes to use.",
    show_default=True,
)
@click.option(
    "--logging",
    "logging_level",
    type=click.Choice(LOGGING_LEVELS.keys(), case_sensitive=True),
    default="INFO",
    help="Logging level",
    show_default=True,
)
@click.option(
    "--path",
    "clone_path",
    type=str,
    default=None,
    help="Sets a path where to clone the repositories (eg: ./another/path/)",
    show_default=True,
)
def cli(
    github_organization: str,
    token: str,
    github_enterprise: str,
    threads: int,
    logging_level: str,
    clone_path: str,
) -> None:
    """Clones all visible repositories for a given organization."""
    setup_logging(level=logging_level)

    logging.info(f"Cloning repos for: {github_organization}")

    try:
        obtain_repos(
            github_organization=github_organization,
            github_token=token,
            queue_lock=repository_list_queue_lock,
            repo_queue=repository_list_queue,
            ghe=github_enterprise,
        )
    except HTTPError as e:
        logging.error("An error has occurred while obtaining repos", exc_info=e)

    total_repos_to_clone = repository_list_queue.qsize()
    logging.info(f"Total repos to clone: {total_repos_to_clone}")

    if total_repos_to_clone > 0:
        repos_to_clone = split_queue(
            number_of_threads=threads,
            repository_queue=repository_list_queue,
            repository_queue_lock=repository_list_queue_lock,
        )

        logging.info("Cloning repos...")

        clone_repos(
            number_of_threads=threads,
            repos_to_clone=repos_to_clone,
            clone_path=clone_path,
        )

        logging.info("Repos cloned!")
