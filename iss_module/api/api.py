from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

@app.get("/sign-cali", response_class=HTMLResponse)
async def sign_cali():
    html_path = Path(__file__).parent.parent.parent / "sign_cali.html"
    return html_path.read_text()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)