import cv2
import os
import json
import logging
from datetime import datetime

from utilities import createPathIfNotExists

# Configure logging
logging.basicConfig(filename="system_log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# Constants for event types
EVENT_TYPE = {
    "motion": "motion"
}


# Path to store captured images and event logs
IMAGE_PATH = "images"
LOG_PATH = "logs"

EVENT_LOG_FILE = "event_log.json"

createPathIfNotExists(IMAGE_PATH)
createPathIfNotExists(LOG_PATH)


# Load or create event log JSON file
def load_event_log(event_log_file):
    event_log = []
    event_log_path = os.path.join(LOG_PATH, event_log_file)
    if os.path.exists(event_log_path):
        with open(event_log_path, "r") as f:
            event_log = json.load(f)
    return event_log


def save_event_log(event_log, event_log_file):
    event_log_path = os.path.join(LOG_PATH, event_log_file)
    with open(event_log_path, "w") as f:
        json.dump(event_log, f, indent=4)


# Function to capture an image using the webcam
def capture_image():
    try:
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()

        if not return_value:
            logging.error("Failed to capture image from webcam")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_file = f"{IMAGE_PATH}/image_{timestamp}.jpg"
        cv2.imwrite(image_file, image)

        camera.release()

        logging.info(f"Image captured and saved as: {image_file}")
        return image_file
    except Exception as e:
        logging.error(f"Error capturing image: {str(e)}")
        return None


# Function to log an event
def log_event(event_type, event_description='', image_file=None, event_log_file=EVENT_LOG_FILE):
    event_log = load_event_log(event_log_file)
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "description": event_description,
        "image": image_file
    }
    event_log.append(event)
    save_event_log(event_log, event_log_file)
    logging.info(f"Event logged: {event_type} - {event_description}")
    return event
