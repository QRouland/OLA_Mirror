import os
import unittest

from pathlib import Path

from builtins import print

from app.tools.FusionPdf import fusion_fichiers, get_pdf_from_directory


class TestFusionTestCase(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__))
        self.list_pdf = [self.datadir + "/page1.pdf", self.datadir + "/page2.pdf"]

    def test_fusion(self):
        fusion_fichiers(self.datadir, "testFusion.pdf", self.list_pdf)
        print(self.datadir)
        self.assertTrue(Path(self.datadir + "/testFusion.pdf").is_file(), "Pdf fusionne inexistant")
        self.assertTrue(len(get_pdf_from_directory(self.datadir)) > 0, "pdf non trouve")
        os.remove(self.datadir + "/testFusion.pdf")
