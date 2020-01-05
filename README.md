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
