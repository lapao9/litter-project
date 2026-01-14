from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve todas as imagens em output/frames
app.mount(
    "/images",
    StaticFiles(directory="output/frames"),
    name="images"
)
