import os
import unittest
from io import BytesIO
from pathlib import Path

from pdfjinja import PdfJinja

from app.tools.InsertTemplate import remplir_template


class InsertTemplateTestCase(unittest.TestCase):
    datadir = os.path.join(os.path.dirname(__file__))

    def setUp(self):
        pdffile = os.path.join(self.datadir, "sample.pdf")
        self.data = {
            'firstName': 'Renan',
            'lastName': 'Husson',
            'address': {
                'street': '24 rue de la pommes',
                'apt': 'C317',
                'city': 'TOULOUSE',
                'zipcode': 31000
            },
            'universite': 'Jean Jaures',
            'spirit': 'Panda',
            'evil': True,
            'language': {
                'french': True,
                'esperento': True
            }
        }
        self.pdfjinja = PdfJinja(pdffile)

    def tearDown(self):
        del self.data
        del self.pdfjinja

    def test_render(self):
        remplir_template(self.datadir, "sample.pdf", self.datadir, "output.pdf", self.data)
        output = self.pdfjinja(self.data)
        outfile = BytesIO()
        output.write(outfile)
        outfile.seek(0)
        self.assertTrue(len(outfile.read()) > 0, "Output PDF is not empty.")
        self.assertTrue(Path(self.datadir + "/output.pdf").is_file(), "Pdf généré inexistant")
        os.remove(self.datadir + "/output.pdf")


if __name__ == '__main__':
    unittest.main()
