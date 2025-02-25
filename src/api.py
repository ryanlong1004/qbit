from fastapi import FastAPI, HTTPException, Request
from src.qbit import Qbit
import loguru
import uvicorn

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
