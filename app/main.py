from app.background_task import UpdateLightsTask
from app.routers.status import router as status_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(status_router)

@app.on_event("startup")
async def startup_event():
    thread = UpdateLightsTask()
    thread.start()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
