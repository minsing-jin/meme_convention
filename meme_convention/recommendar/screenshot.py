from io import BytesIO
import pyautogui
import base64


def take_screenshot():
    """
    Take a screenshot of the current screen and save it to a file.

    Returns:
        str: Path to the saved screenshot file.
    """
    try:
        screenshot = pyautogui.screenshot()
        # TODO: This is for testing purposes, remove later
        screenshot.show()

        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode()
        return base64_image
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None
