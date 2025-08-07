from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from api.runner import run_pipeline
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi import WebSocket, WebSocketDisconnect, status, HTTPException
from fastapi import APIRouter
from asyncio import run_coroutine_threadsafe
import asyncio

import os

app = FastAPI(websocket_allowed_origins=["*"], title="AI Story Maker API")

router = APIRouter()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vite dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
base_dir = os.path.dirname(os.path.abspath(__file__))  # This is AI_STORY_MAKER/api
assets_path = os.path.abspath(os.path.join(base_dir, "..", "assets"))
app.mount("/assets", StaticFiles(directory=os.path.abspath(assets_path)), name="videos")

class StoryRequest(BaseModel):
    prompt: str = "make a story about a journey to Mars"
    story_id: str = "story_000"
    is_custom_story: bool = False

@app.get("/")
def root():
    return {"message": "Welcome to the AI Story Maker API"}

@app.post("/generate/")
def generate_story(request: StoryRequest):
    try:
        result = run_pipeline(request.prompt, request.is_custom_story, request.story_id)
        return {
            "success": True,
            "message": "Story generated successfully!",
            "story_title": result["title"],
            "final_video_ui": result["final_video_ui"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", None]
@app.websocket("/ws/generate/")
async def websocket_generate(websocket: WebSocket):
    origin = websocket.headers.get("origin")
    print(f"WebSocket connection attempt with origin: {origin}")
    if origin not in allowed_origins:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    try:
        data = await websocket.receive_json()
        prompt = data["prompt"]
        story_id = data["story_id"]
        user_story_title = data['user_story_title']
        is_custom_story = data.get("is_custom_story", False)

        async def send_progress(message: str):
            print(f"[WS Progress] {message}")
            await websocket.send_text(message)

        loop = asyncio.get_event_loop()

        def progress_callback(message: str):
            run_coroutine_threadsafe(send_progress(message), loop)


        # Run the blocking pipeline in a thread so event loop stays free
        result = await asyncio.to_thread(run_pipeline, prompt, user_story_title, is_custom_story, story_id, progress_callback)

        await websocket.send_json({
            "type": "final",
            "data": {
                "title": result["title"],
                "final_video_ui": result["final_video_ui"]
            }
        })
        await websocket.close()

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        await websocket.close()
