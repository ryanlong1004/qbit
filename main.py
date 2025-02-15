from dotenv import load_dotenv
import loguru
import typer
from qbit import Qbit

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
def add_torrent(url: str):
    qbit.add_torrent(url)


if __name__ == "__main__":
    app()
