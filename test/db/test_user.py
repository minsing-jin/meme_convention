import pytest
from meme_convention.db.user import User
import os
import pathlib
import random
from PIL import Image
import io

root_dir = pathlib.PurePath(os.path.dirname(os.path.realpath(__file__))).parent.parent
resource_dir = os.path.join(root_dir, "resources", "db_test")


class TestUser:
    test_sample_contexts_categories = ["test_pr_situation", "test_issues"]

    @pytest.fixture
    def collect_meme_path(self):
        # List all files in the folder
        files = os.listdir(resource_dir)
        # Filter to include only image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        image_files = {f: os.path.join(resource_dir, f) for f in files if
                       os.path.splitext(f)[1].lower() in image_extensions}
        if not image_files:
            return None  # No image files found

        return image_files

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, collect_meme_path):
        """Setup test user and ensure test meme data is cleaned up afterward."""

        # --- Setup ---
        self.user = User(username='testuser', password='testpass')
        yield  # --- Run the test ---

        # --- Teardown ---
        # Delete test memes from the database
        for context in self.test_sample_contexts_categories:
            for picture_name in collect_meme_path.keys():
                self.user.cursor.execute(
                    """
                    DELETE FROM memes 
                    WHERE context_category = %s AND picture_name = %s
                    """,
                    (context, picture_name)
                )
        self.user.conn.commit()

        # Verify that all test memes have been removed
        for context in self.test_sample_contexts_categories:
            for picture_name in collect_meme_path.keys():
                self.user.cursor.execute(
                    """
                    SELECT COUNT(*) 
                    FROM memes 
                    WHERE context_category = %s AND picture_name = %s
                    """,
                    (context, picture_name)
                )
                count = self.user.cursor.fetchone()[0]
                assert count == 0, f"Cleanup failed: {count} rows still exist for {context}, {picture_name}"

    def test_upload_meme(self, collect_meme_path):
        for picture_name, picture_path in collect_meme_path.items():
            context_category = random.choice(self.test_sample_contexts_categories)
            self.user.upload_meme(context_category, picture_name, picture_path)
            self.user.cursor.execute(
                "SELECT context_category, picture_name FROM memes WHERE context_category=%s AND picture_name=%s",
                (context_category, picture_name)
            )
            result = self.user.cursor.fetchone()
            assert result is not None
            assert result[0] == context_category
            assert result[1] == picture_name

    # TODO: Is it right test code?? haha
    def test_get_random_meme(self, collect_meme_path):
        for context_category in self.test_sample_contexts_categories:
            for picture_name, picture_path in collect_meme_path.items():
                self.user.upload_meme(context_category, picture_name, picture_path)
                meme = self.user.get_random_meme(context_category)
                img = Image.open(io.BytesIO(bytes(meme[-1])))
                img.show()
                assert meme is not None
