from unittest.mock import MagicMock, patch
from PIL import Image
from meme_convention.meme_feature.autocomplete import AutoComplete  # Replace with your actual module path

def test_gui_display_meme():
    # Mock the context and get_image_func
    mock_context = "test_context"
    mock_get_image_func = MagicMock(return_value=[None, None, None, Image.new('RGB', (100, 100))])

    # Create an instance of AutoComplete
    autocomplete = AutoComplete(None, None, None)

    # Patch the GUI class to avoid actual GUI operations
    with patch('meme_convention.autocompleting.autocomplete.GUI') as MockGUI:
        autocomplete.display_meme_gui(mock_context)

        # Check if GUI was called with the correct parameters
        MockGUI.assert_called_once_with(
            autocomplete.root,
            autocomplete.label,
            autocomplete.meme_img,
            mock_context,
            mock_get_image_func
        )
