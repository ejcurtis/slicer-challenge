from django.test import TestCase
from slicer.models import dicom2png
import os
# Create your tests here.

class Dcm2PngCase(TestCase):
    def test_dicom2png(self):
        """DCM files are being converted to png"""
        source_folder = r'media/dicom/DICOM pics'
        output_folder = f'media/{self.series_uid}'
        dicom2png(source_folder, output_folder)
        pngfiles = os.listdir(output_folder)
        'png' in pngfiles[0]