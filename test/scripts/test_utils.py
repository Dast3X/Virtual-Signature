import sys
import unittest
from unittest.mock import patch

from src.utils.utils import get_assets_path


class TestUtils(unittest.TestCase):

    def test_get_assets_path_in_bundle(self):
        setattr(sys, '_MEIPASS', '/mock/meipass/path')

        with patch('os.path.join') as mock_join:
            mock_join.side_effect = lambda *args: '/'.join(args)

            result = get_assets_path("test_icon.png")

            self.assertEqual(result, '/mock/meipass/path/resources/icons/test_icon.png')

        delattr(sys, '_MEIPASS')

    @patch('os.path.dirname')
    @patch('os.path.abspath')
    @patch('os.path.join')
    def test_get_assets_path_in_development(self, mock_join, mock_abspath, mock_dirname):
        mock_dirname.return_value = '/mock/src/utils'
        mock_abspath.side_effect = lambda path: path
        mock_join.side_effect = lambda *args: '/'.join(args)

        if hasattr(sys, '_MEIPASS'):
            delattr(sys, '_MEIPASS')

        result = get_assets_path("test_icon.png")

        self.assertIn('resources/icons/test_icon.png', result)


if __name__ == '__main__':
    unittest.main()
