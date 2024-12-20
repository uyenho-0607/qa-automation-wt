import os
import base64
import allure
import subprocess

from selenium.webdriver.remote.webdriver import WebDriver

seleniumGridS3BucketUrl = "https://selenium-grid-file-dev.s3.ap-southeast-1.amazonaws.com"

"""
------------------------------------------------------------------------------------------------------------------------------------
                                                        SCREENSHOT / ATTACH TEXT
------------------------------------------------------------------------------------------------------------------------------------
"""

def take_screenshot(driver: WebDriver, screenshot_name: str) -> None:
    allure.attach(driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)


def attach_text(get_text: str, name: str) -> None:
    allure.attach(get_text, name=name, attachment_type=allure.attachment_type.TEXT)

"""
------------------------------------------------------------------------------------------------------------------------------------
                                                        DESKTOP - SCREEN RECORDING
------------------------------------------------------------------------------------------------------------------------------------
"""

def start_screen_recording():
    
    print('start screen recording')
    # # Define the screen recording file path using the class name
    # screen_recording_dir = "./allure-results"
    # screen_recording_file = os.path.join(screen_recording_dir, f"{class_name}.mp4")
    
    # # Ensure the directory exists
    # os.makedirs(screen_recording_dir, exist_ok=True)
    
    # ffmpeg_command = [
    #     "ffmpeg",                        # Command to invoke ffmpeg
    #     "-y",                            # Overwrite output files without asking
    #     "-f", "avfoundation",            # Use AVFoundation framework for input
    #     "-framerate", "30",              # Set input frame rate to 30 FPS
    #     "-i", "1",                       # Capture from screen index 1 (primary display)
    #     "-vcodec", "h264_videotoolbox",  # Use hardware-accelerated H.264 encoding (Mac)
    #     "-r", "30",                      # Set output frame rate to 30 FPS
    #     "-preset", "ultrafast",          # Encoding preset: ultrafast for quick processing
    #     "-b:v", "5000k",                 # Bitrate: 5000 kbps
    #     "-crf", "18",                    # Quality setting: 18 (lower is better quality)
    #     screen_recording_file             # Output file path for the screen recording
    # ]

    # ffmpeg_process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE)

    # return ffmpeg_process, screen_recording_file
    return 0, 0


# Function to stop ffmpeg recording
def stop_screen_recording():
    print('stop screen recording')
    # process.terminate()
    # process.wait()


def attach_video_to_allure():
    print('attach video')
    # with open(file_path, "rb") as video_file:
    #     video_bytes = video_file.read()
    #     allure.attach(video_bytes, name=f"{class_name} - Passed Screen Recording", attachment_type=allure.attachment_type.MP4)
    # os.remove(file_path)

def attach_session_video_to_allure(sessionId):
    print('attach video')
    s3SessionVideoUrl = f'<a href="{seleniumGridS3BucketUrl}/videos/{sessionId}.mp4">Session Video</a>'.format(seleniumGridS3BucketUrl, sessionId)

    allure.attach(s3SessionVideoUrl, name="Screen Recording Link", attachment_type=allure.attachment_type.HTML)

"""
------------------------------------------------------------------------------------------------------------------------------------
                                                        MOBILE - SCREEN RECORDING
------------------------------------------------------------------------------------------------------------------------------------
"""

def start_recording_mobile(driver):
    driver.start_recording_screen()
    

def stop_recording_mobile(driver):
    # Stop screen recording and get the Base64 encoded video
    video_base64 = driver.stop_recording_screen()
    
    # Decode the Base64 video
    video_data = base64.b64decode(video_base64)
    return video_data


def attach_video_to_allure_mobile(video_data, class_name):
    allure.attach(video_data, name=f"{class_name} - Passed Screen Recording", attachment_type=allure.attachment_type.MP4)