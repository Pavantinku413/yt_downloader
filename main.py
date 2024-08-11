from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update this path to your desired download directory
download_dir = r"C:\Users\pavan\Downloads"

# Ensure the download directory exists
os.makedirs(download_dir, exist_ok=True)

@app.post("/download")
async def download_video(link: str = Form(...)):
    video_id = link.split('=')[-1]  # Extract video ID or use another unique identifier
    file_path = os.path.join(download_dir, f"{video_id}.mp4")
    
    youtube_dl_options = {
        "format": "best",
        "outtmpl": file_path  # Save file to the specified path
    }

    try:
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

    return StreamingResponse(
        open(file_path, "rb"),
        media_type="video/mp4",
        headers={"Content-Disposition": f"attachment; filename={video_id}.mp4"}
    )
