import os
from dotenv import load_dotenv
import pandas as pd
import loguru
from qbittorrentapi import SearchResultsDictionary
import typer

from api_connection import ApiConnection

# Configure the logger
logger = loguru.logger
load_dotenv()
app = typer.Typer()


def get_client() -> ApiConnection:
    """
    Instantiates and returns an ApiConnection client with predefined
    connection details.

    Returns:
        ApiConnection: An initialized client instance for API interactions.
    """
    conn_info = {
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }
    return ApiConnection(conn_info)


# Instantiate the client on module load
client = get_client()


@app.command()
def search(term: str) -> SearchResultsDictionary:
    """
    Searches for the given term and prints the results in CSV format.

    Args:
        term (str): The term to search for.

    Returns:
        SearchResultsDictionary: The search results.
    """
    logger.debug(f"Searching for term: {term}")

    try:
        result = client.search(term)
        pretty(result)
        return result
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise typer.Exit(code=1)


@app.command()
def grab(term: str):
    results = search(term)
    if len(results):
        url = results[0]["fileUrl"]  # type: ignore
        assert isinstance(url, str)
        add_torrent(url)


@app.command()
def plugins_list():
    """
    Retrieves and displays the list of available plugins from the client.
    """
    try:
        plugins = client.plugins
        if plugins:
            pretty(plugins)
        else:
            logger.info("No plugins available.")
    except Exception as e:
        logger.error(f"Error retrieving plugins: {e}")
        raise typer.Exit(code=1)


@app.command()
def purge(days: int) -> None:
    """
    Purges items older than the specified number of days.

    Args:
        days (int): Number of days to use as threshold for purging.
    """
    try:
        purged_items = client.purge(days)
        for item in purged_items:
            logger.info(f"Purged '{item.name}'")
    except Exception as e:
        logger.error(f"Error during purge: {e}")
        raise typer.Exit(code=1)


@app.command()
def add_torrent(url: str):
    """
    Adds a torrent from the specified URL to the client.

    Args:
        url (str): The URL of the torrent to add.
    """
    try:
        client.torrents_add([url])
        logger.info(f"Torrent added successfully: {url}")
    except Exception as e:
        logger.error(f"Error adding torrent: {e}")
        raise typer.Exit(code=1)


def pretty(value):
    """
    Formats and logs data in a CSV format.

    Args:
        value (dict or list): Data to format and display as CSV.
    """
    try:
        df = pd.DataFrame(value)
        logger.info(f"Results:\n{df.to_csv(index=False)}\n")
    except Exception as e:
        logger.error(f"Error formatting data: {e}")


if __name__ == "__main__":
    app()
