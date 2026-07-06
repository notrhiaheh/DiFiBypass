from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="DiFiBypass Link Resolver", version="1.0.0")

class LinkRequest(BaseModel):
    url: str

@app.get("/resolve")
async def resolve_url(url: str):
    """Resolve shortened links to show final destination (educational use only)"""
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": "DiFiBypass/1.0 (Educational Project; +https://github.com/notrhiaheh/DiFiBypass)"}
        ) as client:
            resp = await client.get(url)
            return {
                "success": True,
                "original_url": url,
                "resolved_url": str(resp.url),
                "status_code": resp.status_code,
                "note": "⚠️ This only shows the final link address — always complete any required steps on the original page to support creators."
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to resolve: {str(e)}")

@app.post("/resolve")
async def resolve_url_post(req: LinkRequest):
    """POST endpoint for Discord bot integration"""
    return await resolve_url(req.url)

@app.get("/")
async def root():
    return {"message": "DiFiBypass API is running! Use /resolve?url=YOUR_LINK"}
