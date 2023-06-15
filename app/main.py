from fastapi import FastAPI, APIRouter
from starlette.responses import RedirectResponse
from app.routes import volopay_task
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter()
app.include_router(api_router)
app.include_router(volopay_task.api_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000, log_level="debug")
