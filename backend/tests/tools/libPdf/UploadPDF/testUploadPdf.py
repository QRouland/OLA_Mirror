import os
import unittest

from werkzeug.datastructures import FileStorage

from app.tools.LibPdf import upload_file


class TestFusionTestCase(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__))

    def test_fusion(self):
        with open("page1.pdf", 'rb') as fp:
            file = FileStorage(fp)
            upload_file(file, "upload")

            # self.assertTrue(Path(self.datadir + "/testFusion.pdf").is_file(), "Pdf fusionne inexistant")
            # self.assertTrue(len(get_pdf_from_directory(self.datadir)) > 0, "pdf non trouve")
            # os.remove(self.datadir + "/testFusion.pdf")
