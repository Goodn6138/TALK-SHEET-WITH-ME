from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow all domains for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EchoRequest(BaseModel):
    message: str

@app.post("/echo-reverse")
def echo_reverse(data: EchoRequest):
    reversed_message = data.message[::-1]
    return {"reversed": reversed_message}
