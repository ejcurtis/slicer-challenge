from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import ImageSeries
import os 
import numpy as np

def image_series_list(request):
    return render(request, 'slicer/image_series_list.html', {
        # third oprional context argument to pass information into template
        'all_image_series': ImageSeries.objects.all(),
    })
def image_slider(request, id):
    image_series = ImageSeries.objects.get(id=id)
    series_uid = image_series.series_uid
    # get the series uid that matches the chosen image series
    return render(request, 'slicer/image_slider.html', 
    {
        #used to iterate through the remaining images
        'all_png_files': np.asarray(os.listdir(f'media/{series_uid}')),
        #used for first active slider image
        'first_png': np.asarray(os.listdir(f'media/{series_uid}'))[0],
        #used to display the name of the current set of images
        'png_folder': series_uid
    })