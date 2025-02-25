from fastapi import FastAPI, HTTPException, Request
from src.qbit import Qbit
import loguru
import uvicorn
from fastapi import File, UploadFile

# Configure the logger
logger = loguru.logger

app = FastAPI(docs_url="/", redoc_url=None)
qbit = Qbit()


@app.get("/search/{term}")
def search(term: str, _: Request):
    try:
        return qbit.search(term)
    except Exception as e:
        logger.error(f"Error during search operation: {e}")
        raise HTTPException(status_code=500, detail="Search operation failed") from e


@app.post("/grab/{term}")
def grab(term: str, _: Request):
    try:
        qbit.grab(term)
        return {"message": "Torrent grabbed successfully"}
    except Exception as e:
        logger.error(f"Error during grab operation: {e}")
        raise HTTPException(status_code=500, detail="Grab operation failed") from e


@app.get("/plugins")
def plugins_list(_: Request):
    try:
        return qbit.plugins_list()
    except Exception as e:
        logger.error(f"Error retrieving plugins: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve plugins") from e


@app.delete("/purge/{days}")
def purge(days: int, _: Request):
    try:
        qbit.purge(days)
        return {"message": "Purge operation completed successfully"}
    except Exception as e:
        logger.error(f"Error during purge operation: {e}")
        raise HTTPException(status_code=500, detail="Purge operation failed") from e


@app.post("/add_torrent")
def add_torrent(url: str, _: Request):
    try:
        qbit.add_torrent(url)
        return {"message": "Torrent added successfully"}
    except Exception as e:
        logger.error(f"Error adding torrent: {e}")
        raise HTTPException(status_code=500, detail="Failed to add torrent") from e


@app.post("/add_torrent_url")
def add_torrent_url(url: str, _: Request):
    try:
        qbit.client.torrents_add_url([url])
        return {"message": "Torrent added successfully from URL"}
    except Exception as e:
        logger.error(f"Error adding torrent from URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to add torrent from URL") from e


@app.post("/add_torrent_file")
async def add_torrent_file(file: UploadFile = File(...), is_series: bool = False):
    try:
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        qbit.client.torrents_add_files([file_location], is_series)
        return {"message": "Torrent added successfully from file"}
    except Exception as e:
        logger.error(f"Error adding torrent from file: {e}")
        raise HTTPException(status_code=500, detail="Failed to add torrent from file") from e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10333)
