from typing import List
import qbittorrentapi
from datetime import datetime, timedelta

MILLISECONDS_IN_SECOND = 1000


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

    def get_build_info(self) -> dict:
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

    def get_all_torrents(self) -> List[qbittorrentapi.TorrentDictionary]:
        """
        Retrieves a list of all torrents, including their hash, name, and current state.

        Returns:
            List[str]: A list of torrent summaries, where each entry includes the last 6 characters of the hash,
                       the torrent name, and its state.
        """
        return list(torrent for torrent in self.client.torrents_info())

    def get_rss_rules(self) -> dict:
        """
        Retrieves all configured RSS rules.

        Returns:
            dict: A dictionary of RSS rules.
        """
        return self.client.rss_rules()

    def stop_all_torrents(self):
        """
        Stops all currently running torrents.
        """
        self.client.torrents.stop.all()

    def search(self, pattern: str) -> qbittorrentapi.SearchResultsDictionary:
        """
        Searches for torrents based on a provided pattern using the YTS plugin and category filter.

        Args:
            pattern (str): The search pattern or keyword.

        Returns:
            qbittorrentapi.SearchResultsDictionary: Search results from qBittorrent's API.
        """
        search_id = self.client.search_start(
            pattern=f"{pattern}*1080p*x264*", plugins=["yts_mx"], category="all"
        )
        # Blocks until search has finished
        while search_id.status() == "Running":
            pass  # Optionally, handle timeouts or display progress here
        return search_id.results().results

    def torrents_add(self, urls: List[str]):
        """
        Adds torrents from a list of URLs and reannounces to trackers.

        Args:
            urls (List[str]): A list of URLs for the torrents to be added.
        """
        for url in urls:
            self.client.torrents_add(
                urls=url,
                save_path="/home/blitzcrank/downloads/qbittorrent/yify",
                content_layout="Original",
            )
        self.client.torrents_reannounce()

    def purge(self, days):
        cutoff_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())
        print(cutoff_timestamp)
        return [t for t in self.get_all_torrents() if t["completed"] < cutoff_timestamp]
