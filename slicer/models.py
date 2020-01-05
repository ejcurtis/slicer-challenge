import zipfile

import numpy as np
from django.db import models
from django.core.files.base import ContentFile
import png, os, pydicom

from slicer.dicom_import import dicom_datasets_from_zip, combine_slices

"""
Django acts as the ORM from python so there is no need
to write SQL. Each of the methods creates a new row in 
the database.
"""

# source folder has to have .dcm files
# use the zipfile.ZipFile.extractall() to 


def dicom2png(source_folder, output_folder):
    list_of_files = os.listdir(source_folder)
    for file in list_of_files:
        try:
            ds = pydicom.dcmread(os.path.join(source_folder,file))
            shape = ds.pixel_array.shape

            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)

            # Rescaling grey scale between 0-255
            image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)

            # Write the PNG file
            with open(os.path.join(output_folder,file)+'.png' , 'wb') as png_file:
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(png_file, image_2d_scaled)
        except:
            print('Could not convert: ', file)

class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    @property
    def voxels(self):
        with self.voxel_file as f:
            voxel_array = np.load(f)
        return voxel_array

    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            f.extractall('media/dicom')
            source_folder = r'media/dicom/DICOM pics'
            output_folder = r'media/png'
            print(dicom2png(source_folder, output_folder))
            # read the zip file self.dicom archive
            # zipfile.ZipFile reads the zip file, "with" as "f" 
            # automatically closes file after reading, 
            # 'r' specifies read only
            dicom_datasets = dicom_datasets_from_zip(f)
            # dicom_datasets variable is now equal to the read files 
            # imported from the dicom import in the slicer project in Django
            #(see imports)
        voxels, _ = combine_slices(dicom_datasets)
            # combine_slices is a utility function that makes a three dimensional 
            # numpy array and a 4 x 4 affine matrix (calculates space between objects)
            # from the dicom_datasets that were just read.
            # voxels is now the three dimensional array and 
            # it is saved in content_file
        content_file = ContentFile(b'')  # empty zero byte file
        np.save(content_file, voxels)
        # numpy.save()function is used to store the input array in a disk file with npy extension(.npy).
        self.voxel_file.save(name='voxels', content=content_file, save=False)
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID
            # the first index of the dicom_dataset contains the PatientID,
            # StudyInstance, and Series insance that isa shown on the UI
            # where is the PNG file stored? how do I print the dicom_datasets
            # on the console?
        # Image.open(self).save(self + '.png') -- doesnt work
        # need to find a file to save the png to
        # where do I 'dump' my files to?
        super(ImageSeries, self).save(*args, **kwargs)
        # source_folder = r'media/dicom'
        # output_folder = r'media/png'
        # dicom2png(source_folder, output_folder)
    class Meta:
        verbose_name_plural = 'Image Series'
