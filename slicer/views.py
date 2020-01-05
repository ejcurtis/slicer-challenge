from django.shortcuts import render

from .models import ImageSeries


def image_series_list(request):
    return render(request, 'image_series_list.html', {
        'all_image_series': ImageSeries.objects.all(),
    })
# create a new view for each image in the image series
# def single_image(request):
#     return render(request, 'single_image.html', {
#         'single_image' : ImageSeries.voxel_file
#     })