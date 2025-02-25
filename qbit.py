import os
from dotenv import load_dotenv
import pandas as pd
import loguru
from qbittorrentapi import SearchResultsDictionary
import typer

from src.api_connection import ApiConnection
from src.crypt import decrypt

# Configure the logger
logger = loguru.logger
load_dotenv()  # Load environment variables from a .env file
app = typer.Typer()

USERNAME = "gAAAAABnvjdspyfpNGO7nfxqQiN8MOz7YCk8z9nIm2Mmjmj7mpNAp1OwJBPqK07PjzgFnD5Yq_Obbs7TDGWbJFkNYBwta3WrMA=="
PASSWORD = "gAAAAABnvjYNs2R0gvmU8614OR5FkkcaWaED_4A0jqZS-oOzQN8xfpmkfqnYQTWsXdGxU5tmMqU_VpqzBVcS79S_fbHOMQLREw=="


class Qbit:
    """
    A class to interact with the qBittorrent API using the ApiConnection client.
    """

    def __init__(self):
        self.client = self.get_client()

    def get_client(self) -> ApiConnection:
        """
        Initializes and returns an ApiConnection client with details loaded from environment variables.

        Returns:
            ApiConnection: An initialized client instance for interacting with the API.
        """
        key = os.getenv("API_KEY")
        assert key is not None
        conn_info = {
            "host": os.getenv("HOST"),
            "port": os.getenv("PORT"),
            "username": decrypt(key, USERNAME),
            "password": decrypt(key, PASSWORD),
        }
        return ApiConnection(conn_info)

    def search(self, term: str) -> SearchResultsDictionary:
        """
        Searches for torrents using the given term and prints the results in CSV format.

        Args:
            term (str): The search keyword.

        Returns:
            SearchResultsDictionary: The dictionary containing search results.
        """
        logger.debug(f"Initiating search for term: {term}")
        try:
            result = self.client.search(term)
            pretty(result)  # Format and display results
            return result
        except Exception as e:
            logger.error(f"Error during search operation: {e}")
            raise typer.Exit(code=1)  # Exit with an error code

    def grab(self, term: str):
        """
        Searches for a term and adds the first result as a torrent.

        Args:
            term (str): The search keyword.
        """
        results = self.search(term)  # Reuse the search command
        if results:
            try:
                url = results[0]["fileUrl"]  # type: ignore
                assert isinstance(url, str)
                self.add_torrent(url)
            except IndexError:
                logger.warning("No results found to grab.")
            except Exception as e:
                logger.error(f"Error adding torrent from search results: {e}")

    def plugins_list(self):
        """
        Retrieves and displays the list of available plugins.
        """
        logger.debug("Fetching list of plugins.")
        try:
            plugins = self.client.plugins
            if plugins:
                pretty(plugins)
            else:
                logger.info("No plugins available.")
        except Exception as e:
            logger.error(f"Error retrieving plugins: {e}")
            raise typer.Exit(code=1)

    def purge(self, days: int):
        """
        Removes items older than a specified number of days.

        Args:
            days (int): The age threshold (in days) for purging.
        """
        logger.debug(f"Purging items older than {days} days.")
        try:
            purged_items = self.client.purge(days)
            for item in purged_items:
                logger.info(f"Purged item: '{item.name}'")
        except Exception as e:
            logger.error(f"Error during purge operation: {e}")
            raise typer.Exit(code=1)

    def add_torrent(self, url: str):
        """
        Adds a torrent to the client using the specified URL.

        Args:
            url (str): The URL of the torrent to add.
        """
        logger.debug(f"Adding torrent from URL: {url}")
        try:
            self.client.torrents_add([url])
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
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        logger.error(f"Error formatting data: {e}")
