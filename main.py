from typing import List
import json
import qbittorrentapi.exceptions

from api_connection import ApiConnection


# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
# try:
#     self.client.auth_log_in()
# except qbittorrentapi.LoginFailed as e:
#     print(e)

# # if the Client will not be long-lived or many Clients may be created
# # in a relatively short amount of time, be sure to log out:
# self.client.auth_log_out()

# or use a context manager:
# z


if __name__ == "__main__":
    # instantiate a Client using the appropriate WebUI configuration
    conn_info = dict(
        host="169.150.223.229",
        port=28391,
        username="blitzcrank",
        password="t3nd3rTurd",
    )
    client = ApiConnection(conn_info)
    for x in client.purge(30):
        print(x.completion_on)
        exit()
    # for item in self.client.search_plugins():
    #     print(item)

    # result = self.client.rss_items(include_feed_data=True)
    # for k, v in result.items():
    #     print(json.dumps(v["articles"]))
    #     exit()

    # for item in client.search("Alien*Romulus"):
    #     print(item)
    # print(item["fileUrl"])
    #     try:
    #         torrents_add(urls=[item["fileUrl"]])
    #     except Exception as e:
    #         print(e)
    #         exit()
