from typing import List
import qbittorrentapi
from datetime import datetime, timedelta
import time
import loguru

MILLISECONDS_IN_SECOND = 1000
DEFAULT_SEARCH_PLUGINS = ["enabled"]
DEFAULT_SEARCH_TOKENS = "*1080p*"

logger = loguru.logger


class ApiConnection:
    """
    A class to handle API connection and operations with qBittorrent.

    Attributes:
        client (qbittorrentapi.Client): The client to interface with qBittorrent's API.
    """

    def __init__(self, conn_info: dict):
        """
        Initializes the connection to the qBittorrent API using the provided connection information.

        Args:
            conn_info (dict): Dictionary containing connection parameters (host, username, password, etc.).
        """
        self.client = qbittorrentapi.Client(**conn_info)

    @property
    def build_info(self) -> dict:
        """
        Retrieves version and build information for qBittorrent and its web API.

        Returns:
            dict: A dictionary with qBittorrent version, Web API version, and build information.
        """
        result = {
            "qBittorrent Version": self.client.app.version,
            "Web API Version": self.client.app.web_api_version,
        }
        result.update({k: str(v) for k, v in self.client.app.build_info.items()})
        return result

    @property
    def torrents(self) -> List[qbittorrentapi.TorrentDictionary]:
        """
        Retrieves a list of all torrents, including their hash, name, and current state.

        Returns:
            List[str]: A list of torrent summaries, where each entry includes the last 6 characters of the hash,
                       the torrent name, and its state.
        """
        return list(torrent for torrent in self.client.torrents_info())

    @property
    def rss_rules(self) -> dict:
        """
        Retrieves all configured RSS rules.

        Returns:
            dict: A dictionary of RSS rules.
        """
        return self.client.rss_rules()

    @property
    def plugins(self) -> qbittorrentapi.SearchPluginsList:
        return self.client.search_plugins()

    def stop_all_torrents(self):
        """
        Stops all currently running torrents.
        """
        self.client.torrents.stop.all()

    def search(
        self,
        pattern: str,
        plugins: List[str] = DEFAULT_SEARCH_PLUGINS,
        category: str = "all",
    ) -> qbittorrentapi.SearchResultsDictionary:
        """
        Searches for torrents based on a provided pattern using the YTS plugin and category filter.

        Args:
            pattern (str): The search pattern or keyword.

        Returns:
            qbittorrentapi.SearchResultsDictionary: Search results from qBittorrent's API.
        """
        search_id = self.client.search_start(
            pattern=f"{pattern}{DEFAULT_SEARCH_TOKENS}",
            plugins=plugins,
            category=category,
        )
        # Blocks until search has finished
        while search_id.status() == "Running":
            logger.debug(f"{search_id.status()}")
            time.sleep(1)

        logger.debug(f"{search_id.status()}")
        return search_id.results().results

    def torrents_add(self, urls: List[str]):
        """
        Adds torrents from a list of URLs and reannounces to trackers.

        Args:
            urls (List[str]): A list of URLs for the torrents to be added.
        """
        for url in urls:
            logger.info(f"URL is {url}")
            self.client.torrents_add(
                urls=url,
                save_path="/home/blitzcrank/downloads/qbittorrent/yify",
                content_layout="Original",
            )
        self.client.torrents_reannounce("all")

    def purge(self, days):
        logger.debug(f"days: {days}")
        cutoff_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())

        to_delete = list(
            [
                torrent
                for torrent in self.torrents
                if torrent["completion_on"] < cutoff_timestamp  # type: ignore
            ]
        )

        # self.client.torrents_delete(delete_files=True, torrent_hashes=list(to_delete))
        self.client.torrents_delete(
            delete_files=True, torrent_hashes=[torrent.hash for torrent in to_delete]
        )
        return to_delete
