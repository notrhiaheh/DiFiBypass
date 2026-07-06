from fastapi import FastApi, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="DiFiBypasa Link Resolver", version="1.0.0")

class LinkRequest(BaseModel):
  url: str

@app.get("/resolve")
async def resolve_url(url: str):
  """Resolve shortened links to show final destination"""
  try:
    async with httpx.AsyncClient(
      follow_redirects=True,
