from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import os

app = FastAPI(title="PUB Realtime System", version="1.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data storage
latest_data = []


@app.post("/ingest")
async def ingest(data: dict):
    """Receive data from client and store in buffer"""
    latest_data.append(data)
    return JSONResponse({"message": "Data received", "total_records": len(latest_data)})


@app.get("/stream")
async def stream():
    """Server-Sent Events stream for dashboard"""

    async def event_generator():
        last_index = 0
        while True:
            if last_index < len(latest_data):
                payload = json.dumps(latest_data[last_index])
                yield {"data": payload}
                last_index += 1

            await asyncio.sleep(0.5)  # keepalive rate

    return EventSourceResponse(event_generator())


@app.get("/health")
async def health():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy", "total_records": len(latest_data)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)