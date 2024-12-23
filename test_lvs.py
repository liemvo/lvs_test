import unittest
import os
from unittest.mock import patch, MagicMock, mock_open
from lvs import log_event, capture_image, load_event_log, save_event_log

TEST_EVENT_LOG_FILE = "test_event_log.json"


class TestLvs(unittest.TestCase):

    @patch("lvs.datetime")
    @patch("lvs.json")
    @patch("lvs.os.path.join", return_value=TEST_EVENT_LOG_FILE)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"event": "log"}]')
    def test_log_event(self, mock_open, mock_path_join, mock_json, mock_datetime):
        mock_datetime.now().strftime.return_value = "2021-01-01 01:01:01"
        expected_event = {
            "timestamp": "2021-01-01 01:01:01",
            "type": "test_event",
            "description": "test_description",
            "image": "test_image"
        }
        mock_event_log = [expected_event]

        mock_json.load.return_value = mock_event_log

        log_event("test_event", "test_description",
                  "test_image", TEST_EVENT_LOG_FILE)

        mock_path_join.assert_called_with(
            "logs", TEST_EVENT_LOG_FILE)
        handle = mock_open()
        mock_json.dump.assert_called_with(mock_event_log, handle, indent=4)

    @patch("lvs.datetime")
    @patch("lvs.cv2")
    @patch("lvs.logging")
    def test_capture_image_success(self, mock_logging, mock_cv2, mock_datetime):
        mock_datetime.now().strftime.return_value = "20210101_010101"
        mock_camera = MagicMock()
        mock_cv2.VideoCapture.return_value = mock_camera
        mock_camera.read.return_value = (True, "image")
        mock_cv2.imwrite.return_value = True

        image_file = capture_image()

        self.assertEqual(image_file, "images/image_20210101_010101.jpg")
        mock_logging.info.assert_called_with(
            "Image captured and saved as: images/image_20210101_010101.jpg")

    @patch("lvs.datetime")
    @patch("lvs.cv2")
    @patch("lvs.logging")
    def test_capture_image_error_when_camera_false(self, mock_logging, mock_cv2, mock_datetime):
        mock_datetime.now().strftime.return_value = "20210101_010101"
        mock_camera = MagicMock()
        mock_cv2.VideoCapture.return_value = mock_camera
        # Mock camera.read() to return False
        mock_camera.read.return_value = (False, None)

        image_file = capture_image()

        self.assertIsNone(image_file)
        mock_logging.error.assert_called_with(
            "Failed to capture image from webcam")

    @patch("lvs.datetime")
    @patch("lvs.cv2")
    @patch("lvs.logging")
    def test_capture_image_error_when_exception(self, mock_logging, mock_cv2, mock_datetime):
        mock_datetime.now().strftime.return_value = "20210101_010101"
        mock_camera = MagicMock()
        mock_cv2.VideoCapture.return_value = mock_camera
        # Mock camera.read() to raise an exception
        mock_camera.read.side_effect = Exception("Camera read error")

        image_file = capture_image()

        self.assertIsNone(image_file)
        mock_logging.error.assert_called_with(
            "Error capturing image: Camera read error")

    @patch("lvs.json")
    @patch("lvs.os")
    def test_load_event_log(self, mock_os, mock_json):
        mock_os.path.exists.return_value = True
        mock_event_log = [{"event": "log"}]
        mock_json.load.return_value = mock_event_log

        event_log = load_event_log(TEST_EVENT_LOG_FILE)

        self.assertEqual(event_log, mock_event_log)

    @patch("lvs.json")
    @patch("lvs.os")
    def test_load_event_log_file_not_exists(self, mock_os, mock_json):
        mock_os.path.exists.return_value = False

        event_log = load_event_log(TEST_EVENT_LOG_FILE)

        self.assertEqual(event_log, [])

    @patch("lvs.json")
    @patch("lvs.os.path.join", return_value=TEST_EVENT_LOG_FILE)
    @patch("builtins.open", new_callable=mock_open)
    def test_save_event_log(self, mock_open, mock_os, mock_json):

        mock_event_log = [{"event": "log"}]

        save_event_log(mock_event_log, TEST_EVENT_LOG_FILE)

        mock_open.assert_called_once_with(TEST_EVENT_LOG_FILE, "w")

        handle = mock_open()
        mock_json.dump.assert_called_with(mock_event_log, handle, indent=4)


if __name__ == "__main__":
    unittest.main()
