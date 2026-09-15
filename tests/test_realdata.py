import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from astrolab import realdata


class TestFetchSkyImage(unittest.TestCase):

    @patch("astroquery.skyview.SkyView.get_images")
    def test_fetches_and_returns_image(self, mock_get_images):
        expected_image = np.ones((200, 200), dtype=np.float32)

        class FakeHDU:
            data = expected_image

        mock_get_images.return_value = [[FakeHDU()]]

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(realdata, "CACHE_DIR", Path(temp_dir)):
                image = realdata.fetch_sky_image(
                    position="M42",
                    survey="DSS",
                    pixels=200,
                )

        np.testing.assert_array_equal(image, expected_image)
        self.assertEqual(image.shape, (200, 200))
        mock_get_images.assert_called_once_with(
            position="M42",
            survey=["DSS"],
            pixels=200,
        )

    @patch("astroquery.skyview.SkyView.get_images")
    def test_uses_cache_on_second_call(self, mock_get_images):
        expected_image = np.ones((200, 200), dtype=np.float32)

        class FakeHDU:
            data = expected_image

        mock_get_images.return_value = [[FakeHDU()]]

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(realdata, "CACHE_DIR", Path(temp_dir)):
                first_image = realdata.fetch_sky_image(
                    position="M42",
                    survey="DSS",
                    pixels=200,
                )

                second_image = realdata.fetch_sky_image(
                    position="M42",
                    survey="DSS",
                    pixels=200,
                )

        np.testing.assert_array_equal(first_image, expected_image)
        np.testing.assert_array_equal(second_image, expected_image)

        # SkyView should only have been called for the first request.
        mock_get_images.assert_called_once()


if __name__ == "__main__":
    unittest.main()