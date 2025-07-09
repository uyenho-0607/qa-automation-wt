import base64
import os.path
import time

from src.data.consts import VIDEO_DIR


def save_recorded_video(video_raw):
    raw_path = os.path.join(VIDEO_DIR, f"test_video_{round(time.time())}.mp4")

    with open(raw_path, "wb") as f:
        f.write(base64.b64decode(video_raw))

    return raw_path