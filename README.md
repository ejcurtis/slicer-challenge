# Slicer Coding Challenge

## Setup

You must have python 3 installed.

All of the python requirements are listed in `requirements.txt`.  You can install them using:

    pip install -r requirements.txt

Once you have installed everything, be sure to run the Django migrations, and
to create a super user (so you can login to the admin).  You can do this by running:

    python manage.py migrate
    python manage.py createsuperuser
    
You can start the Django development server, using:

    python manage.py runserver

Once the development server is running you can login to the Django admin by navigating 
to http://127.0.0.1:8000/admin and logging in as the superuser you just created.

## Upload Test Dataset via the Django Admin

You can download a zip archive with a set of test DICOM files
[here](https://github.com/innolitics/example-files/raw/master/example-lung-ct.zip).

You can find many more example DICOM sets online---for example at the [Cancer
Imaging Archive](http://www.cancerimagingarchive.net)---but this one data set
should be sufficient.

To upload test datasets, login to the django admin (see above) and then navigate 
to the image series page and click the "add" button in the top-right corner, and 
upload the sample zip-archives containing DICOM files.

After uploading the sample dataset in the Django admin, you should see it in
the "home" page of the site (e.g. http://127.0.0.1:8000/).  There should be one
row for each archive you uploaded.  The "View" link in the table won't do
anything yet, but you it will soon!

## Overview

In this challenge your job is to create a simple image-slice viewer, and
link it to these dead links in the image series table.

## Part I - Create Slices

Update `ImageSeries`'s custom save method so that it dumps a set of PNGs---one
for each axial slice (one veiw of the brain) of the data.  You can assume that the third dimension of
the voxel array is the axial dimension.

## Part II - Create a Slice Viewer Page

Now create a new Django view and template that displays the set of PNGs you generated.

Ensure that only one PNG is displayed at a time, and include a mechanism that
allows the user to quickly step through the stack of images (e.g. a slider),
*without requiring a full page reload* to view each new image.

## Other Details

Please do not fork this repository, and instead work on a local copy of the repository.

As you code, create logical commits with good commit messages.

To submit your solution, please zip up your entire repository, and email it to
`info@innolitics.com`.

If you have any questions about the requirements, ask!  Part of being a good
engineer is knowing when to clarify requirements.

## Notes

Really, it would be better to generate the images in a separate task, outside
of the request-response cycle.  For example, using a tool like celery.  This
added too much complexity for this project.

## Additional comments.

Part 1- 
In order to creat png files from the DICOM file uploaded to ImageSeries, I created a helper function called DicomToPng. See notes about its functionality above the ImageSeries class in models.py. 

I called the DicomToPng function at the end of the ImageSeries class. Something I would optimize about this function would be to store the output file in a more organized place. Origionally I tried storing the png files in 'media/png/{series_uid}', but my function would not properly read the output folder and would not save the png file, nor make a new voxel file. I ran into several errors after this, all related to the voxel method in ImageSeries because the class was looking for a non-existent voxel file and was askng me to set pickling to true. I ended up resolving to saving the png files in 'media/{series_uid}', but for scalability I would consider changing this.

Part 2- 
My image slider is made with a bootstrap carasoul. I felt this method was the most practical way to put together an app in a short amount of time. The carasoul allows a user to quickly see all png images from an image series. I also added my own CSS for styling the page layout for the purpose of showing my knowledge of CSS and flexbox. If I where to make this a scalable production app, I would consider changing my styling to all Bootstrap or all CSS depending on the needs of the UI, and how much control I need to have over the styling. 

I added my CSS stylesheets to the base HTML and extended my other two views (image_series_list, image_slider) from this sheet. I passed in information to my views in the views.py file and you can see my comments about this process there. I additionally creted a dynamic URL using the image series PK as the parameter for the URL. You can see my notes about this in the slicer/urls.py file. If I were to expand this app, I would ensure this app required a login, and pass session data into the HTTP request due to the sensitivity of medcal information. Lastly, I changed the URLs from regex expressions in the slicer/urls.py file because newer versions of django no longer require regex for url paths.


Tests- I used pytest-django to complete three tests for this app. The first test I made was to ensure the DicomToPng function works properly. I tested that the function converts dicom files from the dicom_test folder to png_files in the png_file folder. To minimize runtime, the test only checks the first file in the png folder. I also tested the view functions were correctly rendering my views. I passed the two existing http reqests into the image_series_list and 
Conclusion- I would be happy to go over any of the code I wrote in a future code reveiw. I had