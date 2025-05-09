from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

try:
    from crunchyroll import Crunchyroll
except ImportError:
    Crunchyroll = None

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(data: LoginRequest):
    if not Crunchyroll:
        return JSONResponse(status_code=500, content={"success": False, "error": "crunchyroll.py non installato"})

    try:
        session = await Crunchyroll.login(data.email, data.password)
        return { "success": True, "username": session.user.name }
    except Exception as e:
        return { "success": False, "error": str(e) }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
