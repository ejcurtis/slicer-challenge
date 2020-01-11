from slicer.models import dicomTopng
from slicer.models import ImageSeries
from slicer.views import image_series_list, image_slider
import pytest
import os

# Create your tests here.

def test_dicomTopng():
    """DCM files are being converted to png"""
    source_folder = r'media/dicom_test'
    output_folder = r'media/png_test'
    dicomTopng(source_folder, output_folder)
    pngfiles = os.listdir(output_folder)
    #loop is not allowing me to use pngfiles
    assert 'png' in  pngfiles[0]

@pytest.mark.django_db
def test_image_series_list_view():
    request = "GET '/'"
    response = image_series_list(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_image_slider_view():
    # with more time I would ceat a new mock etry in the database
    # query for a list of ther pk's and test each get route for
    # each id in the database
    request = "GET '/123'"
    response = image_series_list(request)
    assert response.status_code == 200