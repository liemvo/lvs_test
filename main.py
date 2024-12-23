# Example: Simulate motion detection and capture image
import logging
from lvs import EVENT_TYPE, capture_image, log_event


def main():
    try:
        print("Simulating motion detection...")
        image_file = capture_image()
        if image_file:
            log_event(EVENT_TYPE["motion"], "Motion detected", image_file)
        else:
            log_event(EVENT_TYPE["motion"], "Motion detection failed")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
