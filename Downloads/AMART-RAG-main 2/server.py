from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import json
import asyncio
import glob
import uvicorn

app = FastAPI(title="Red Team Command Center API")

# CORS for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
LOG_FILE = "logs/successful_attacks.json"
ATTACK_IMAGE_PATH = "attack_image.png"
POISON_PDF_PATH = "poisoned_doc.pdf"

class AttackRequest(BaseModel):
    mode: str = "full" # 'full' or 'safe'

@app.get("/")
async def root():
    return {"status": "Red Team API Online", "docs": "/docs"}

@app.get("/stats")
async def get_stats():
    """
    Returns total attacks vs successful breaks.
    """
    successful_count = 0
    total_attacks_mock = 0 # In a real DB we'd track this. using Mock+Log for now.
    
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
                successful_count = len(logs)
                # Assuming some ratio or tracking total runs separately (mocking total heavily dependent on runs)
                # For demo, we estimate or read a counter file if we had one.
                # Let's say total is success * 4 (mock) or just start at 0 if no file.
                total_attacks_mock = max(successful_count * 3, 10) 
        except:
            pass
            
    return {
        "total_attacks": total_attacks_mock,
        "successful_breaks": successful_count,
        "success_rate": round((successful_count / max(total_attacks_mock, 1)) * 100, 1)
    }

@app.get("/logs")
async def get_logs():
    """
    Streams the latest lines from a log file (if we diverted stdout to one).
    For now, we'll read a 'latest.log' if we modify main_pipeline to write to one,
    OR we can just return the successful attack logs as 'activity'.
    Simulating 'Live Terminal' via successful logs for this MVP iteration 
    unless we hook stdout.
    
    Better approach for MVP: Return last 5 'events' from the success log 
    formatted compatibility for terminal.
    """
    events = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
                # Sort by timestamp desc
                sorted_data = sorted(data, key=lambda x: x.get('timestamp', 0), reverse=True)
                for entry in sorted_data[:10]:
                    events.append(f"[SUCCESS] Flag leaked via prompt: {entry['prompt'][:50]}...")
        except:
            pass
            
    if not events:
        events = ["[SYSTEM] Ready via API...", "[SYSTEM] Waiting for attack initiation..."]
        
    return {"logs": events}

@app.post("/start")
async def start_attack(request: AttackRequest):
    """
    Triggers the main_pipeline.py script.
    """
    try:
        # We run it as a subprocess. 
        # Note: This blocks until finished if we use subprocess.run, 
        # which might be too long for an HTTP request.
        # But for 'main_pipeline.py', it loops. We might want to run just ONE round 
        # or start the background process.
        
        # For the dashboard "Initiate" button, let's assume it runs ONE batch/loop 
        # or starts the script detached. 
        # Making it non-blocking is best.
        
        proc = subprocess.Popen(["python", "main_pipeline.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"status": "Attack Sequence Initiated", "pid": proc.pid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gallery")
async def get_gallery():
    """
    Returns list of available artifact files.
    """
    # Just check if files exist
    artifacts = []
    if os.path.exists(ATTACK_IMAGE_PATH):
        artifacts.append({"type": "image", "name": "Latest Poison Image", "url": "/artifacts/image"})
    if os.path.exists(POISON_PDF_PATH):
        artifacts.append({"type": "pdf", "name": "Latest Poison PDF", "url": "/artifacts/pdf"})
        
    return {"artifacts": artifacts}

@app.get("/artifacts/image")
async def get_image_artifact():
    if os.path.exists(ATTACK_IMAGE_PATH):
        return FileResponse(ATTACK_IMAGE_PATH)
    return {"error": "No image generated yet"}

@app.get("/artifacts/pdf")
async def get_pdf_artifact():
    if os.path.exists(POISON_PDF_PATH):
        return FileResponse(POISON_PDF_PATH)
    return {"error": "No PDF generated yet"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
