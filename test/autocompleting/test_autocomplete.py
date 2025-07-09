import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
import io

from meme_convention.db.user import User
from your_module import AutoComplete  # Replace with your actual module path

@pytest.fixture
def dummy_analysis_model():
    return MagicMock()

@pytest.fixture
def dummy_text():
    return "sample text"

@pytest.fixture
def dummy_image():
    # Create a simple 1x1 pixel image for testing
    img = Image.new('RGB', (1, 1), color='white')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

@pytest.fixture
def context_categories():
    return ["funny", "serious", "test"]

@pytest.fixture
def autocomplete_instance(dummy_analysis_model, dummy_text, dummy_image):
    with patch('meme_convention.db.user.User') as MockUser:
        instance = AutoComplete(dummy_analysis_model, dummy_text, dummy_image)
        instance.user_db = MockUser()
        return instance

def test_classify_context_category_valid(autocomplete_instance, context_categories):
    result = autocomplete_instance.classify_context_category("funny", context_categories)
    assert result == "funny"

def test_classify_context_category_invalid(autocomplete_instance, context_categories):
    with pytest.raises(ValueError):
        autocomplete_instance.classify_context_category("not_a_category", context_categories)

@patch.object(AutoComplete, "gui_display_meme")
def test_autocomplete_calls_classify_and_gui_display(mock_gui_display, autocomplete_instance, context_categories):
    # Mock gui_display_meme to return fake meme bytes
    fake_meme_bytes = [None, None, b'\x89PNG\r\n\x1a\n']
    mock_gui_display.return_value = fake_meme_bytes

    # Patch Image.open to avoid actual image loading
    with patch("PIL.Image.open", return_value=MagicMock(spec=Image.Image)):
        result = autocomplete_instance.autocomplete("funny", context_categories)
        assert mock_gui_display.called
        assert result is not None
