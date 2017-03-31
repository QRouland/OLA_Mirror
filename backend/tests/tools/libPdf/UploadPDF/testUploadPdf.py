import filecmp
import os
import unittest
from pathlib import Path

from werkzeug.datastructures import FileStorage

from app.tools.LibPdf import upload_file, allowed_file


class TestFusionTestCase(unittest.TestCase):
    def setUp(self):
        self.datadir = "upload/page1.pdf"
        self.file_name = "page1.pdf"

    def test_fusion(self):
        with open(self.file_name, 'rb') as fp:
            file = FileStorage(fp)
            upload_file(file, "upload")

            self.assertTrue(Path(self.datadir).is_file(), "Pdf upload inexistant")
            self.assertTrue(filecmp.cmp(self.datadir, self.file_name), "fichiers non identique")
            self.assertTrue(allowed_file(self.file_name), "format non conforme")

            os.remove(self.datadir)
