from dotenv import load_dotenv
import loguru
import typer
from src.qbit import Qbit

# Configure the logger
logger = loguru.logger
load_dotenv()  # Load environment variables from a .env file
app = typer.Typer()


qbit = Qbit()


@app.command()
def search(term: str):
    qbit.search(term)


@app.command()
def grab(term: str):
    qbit.grab(term)


@app.command()
def plugins_list():
    qbit.plugins_list()


@app.command()
def purge(days: int):
    qbit.purge(days)


@app.command()
def add_torrent_url(url: str):
    qbit.client.torrents_add_url([url])


@app.command()
def add_torrent_file(file_path: str, is_series: bool = False):
    qbit.client.torrents_add_files([file_path], is_series)


if __name__ == "__main__":
    app()
