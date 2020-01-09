
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
def dicomTopng(source_folder, output_folder):
    list_of_files = os.listdir(source_folder)
    # get all files from the source folder
    for file in list_of_files:
        #for each file in the source folder...
        try:
            #read and parse DICOM file properties of each file in the source folder
            #and make a new '.dcm' file in that folder ex: 000001.dcm <-- contains all patient and image info
            ds = pydicom.dcmread(os.path.join(source_folder,file))
            # returns two numbers that represent the size of the image that will
            #be used to rewrite it as a png
            shape = ds.pixel_array.shape
            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)
            # Rescaling grey scale between 0-255
            image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)   
            with open(os.path.join(output_folder, file)+'.png' , 'wb') as png_file:
            # Write the PNG file
            # wb writes the image in binary mode
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(png_file, image_2d_scaled)
        except:
            #if the file fails to be re writen print this error message
            print('Could not convert: ', file)

class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)
    #table properties that can be queried
    @property
    def voxels(self):
        with self.voxel_file as f:
            voxel_array = np.load(f)
        return voxel_array
    #create the voxel files
    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            print(f.extractall('media/dicom'))
            #Extract all files from the dicom archive zip file that 
            # is uploaded on the admin page in a "read only" format
            # and save each of the extracted dcm files in media/dicom --> DICOM pics
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
        # sets the value of each property on the instance
        source_folder = r'media/dicom/DICOM pics'
        #folder of files to be converted into a png
        output_folder = f'media/{self.series_uid}'
        #folder where the png files will be saved. They will each have the series id as their
        #name so each series is saves together and can be queried for the same slider
        os.mkdir(output_folder)
        #Make the output folder for the files to be saved to
        super(ImageSeries, self).save(*args, **kwargs)
        #dump the png files in the output folder
        dicomTopng(source_folder, output_folder)
    class Meta:
        verbose_name_plural = 'Image Series'