from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/")
def running_bot():
    return {"status":"running bot media", "msg": "Hello World"}

@app.head("/", description="head check ok")
async def head_root():
    return {"status":"running bot media", "msg": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, port=608, log_level="info")