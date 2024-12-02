import os
from dotenv import load_dotenv
import pandas as pd
import loguru
from qbittorrentapi import SearchResultsDictionary
import typer

from api_connection import ApiConnection

# Configure the logger
logger = loguru.logger
load_dotenv()  # Load environment variables from a .env file
app = typer.Typer()


def get_client() -> ApiConnection:
    """
    Initializes and returns an ApiConnection client with details loaded from environment variables.

    Returns:
        ApiConnection: An initialized client instance for interacting with the API.
    """
    conn_info = {
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }
    return ApiConnection(conn_info)


# Create a single, reusable instance of ApiConnection
client = get_client()


@app.command()
def search(term: str) -> SearchResultsDictionary:
    """
    Searches for torrents using the given term and prints the results in CSV format.

    Args:
        term (str): The search keyword.

    Returns:
        SearchResultsDictionary: The dictionary containing search results.
    """
    logger.debug(f"Initiating search for term: {term}")
    try:
        result = client.search(term)
        pretty(result)  # Format and display results
        return result
    except Exception as e:
        logger.error(f"Error during search operation: {e}")
        raise typer.Exit(code=1)  # Exit with an error code


@app.command()
def grab(term: str):
    """
    Searches for a term and adds the first result as a torrent.

    Args:
        term (str): The search keyword.
    """
    results = search(term)  # Reuse the search command
    if results:
        try:
            url = results[0]["fileUrl"]  # type: ignore
            assert isinstance(url, str)
            add_torrent(url)
        except IndexError:
            logger.warning("No results found to grab.")
        except Exception as e:
            logger.error(f"Error adding torrent from search results: {e}")


@app.command()
def plugins_list():
    """
    Retrieves and displays the list of available plugins.
    """
    logger.debug("Fetching list of plugins.")
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
def purge(days: int):
    """
    Removes items older than a specified number of days.

    Args:
        days (int): The age threshold (in days) for purging.
    """
    logger.debug(f"Purging items older than {days} days.")
    try:
        purged_items = client.purge(days)
        for item in purged_items:
            logger.info(f"Purged item: '{item.name}'")
    except Exception as e:
        logger.error(f"Error during purge operation: {e}")
        raise typer.Exit(code=1)


@app.command()
def add_torrent(url: str):
    """
    Adds a torrent to the client using the specified URL.

    Args:
        url (str): The URL of the torrent to add.
    """
    logger.debug(f"Adding torrent from URL: {url}")
    try:
        client.torrents_add([url])
        logger.info(f"Torrent successfully added: {url}")
    except Exception as e:
        logger.error(f"Error adding torrent: {e}")
        raise typer.Exit(code=1)


def pretty(value):
    """
    Formats and displays data in CSV format using Pandas.

    Args:
        value (dict or list): The data to be displayed as CSV.
    """
    logger.debug("Formatting data for display.")
    try:
        df = pd.DataFrame(value)
        logger.info(f"Formatted Results:\n{df.to_csv(index=False)}\n")
    except Exception as e:
        logger.error(f"Error formatting data: {e}")


if __name__ == "__main__":
    app()
