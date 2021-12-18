# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 17:37:44 2021

@author: Awuah
"""

import numpy as np
from osgeo import gdal, gdal_array


def tiff_to_array(input_file, dim_ordering = 'channels_last', dtype = 'float32'):
     ''' Converts image to array.
     input_file: (str) path to image file.
     '''
     input_file = gdal.Open(input_file)
     bands = [input_file.GetRasterBand(i) for i in range(1, input_file.RasterCount + 1)]
     arr = np.array([gdal_array.BandReadAsArray(band) for band in bands]).astype(dtype)
     if dim_ordering == 'channels_last':
          arr = np.transpose(arr, [1,2,0])
     return arr


def array_to_tiff(array, src_raster, dst_filename):
     '''Converts n-dimensional array to raster in tif format.
     For a single band 3-D array (i.e. len(array.shape)=3), reshape such that len(array.shape) = 2.
     array: (numpy array) n-dimensional array to be converted.
     src_raster: (str) path to source/reference raster from which metadata is taken.
     dst_filename: (str) ouput filename or path to output file.
     '''
     #open source raster
     src = gdal.Open(src_raster)

     #get metadata
     geo_trans = src.GetGeoTransform()
     proj = src.GetProjection()

     #get array data type
     dtype = str(array.dtype)
     datatype_mapping = {'byte': gdal.GDT_Byte, 'uint8': gdal.GDT_Byte, 'uint16': gdal.GDT_UInt16,
                          'int8': gdal.GDT_Byte, 'int16': gdal.GDT_Int16, 'int32': gdal.GDT_Int32,
                          'uint32': gdal.GDT_UInt32, 'float32': gdal.GDT_Float32, 'float64':gdal.GDT_Float64}

     #create empty raster and write array values into it
     driver = gdal.GetDriverByName('GTiff')
     if len(array.shape) == 2:
          out_ds = driver.Create(dst_filename, array.shape[0], array.shape[1], 1, datatype_mapping[dtype])
          out_ds.GetRasterBand(1).WriteArray(array)
          #apply transformation and projection
          out_ds.SetGeoTransform(geo_trans)
          out_ds.SetProjection(proj)
          # write to disk
          out_ds.FlushCache()
     elif len(array.shape) == 3:
          out_ds = driver.Create(dst_filename, array.shape[0], array.shape[1], array.shape[2], datatype_mapping[dtype])
          for i in range(0, array.shape[2]):
               out_ds.GetRasterBand(i+1).WriteArray(array[:,:,i])
          #apply transformation and projection
          out_ds.SetGeoTransform(geo_trans)
          out_ds.SetProjection(proj)
          # write to disk
          out_ds.FlushCache()
          #compute statistics
          for i in range(0, array.shape[2]):
               out_ds.GetRasterBand(i+1).ComputeStatistics(False)
          #build overviews/pyramid layers
          out_ds.BuildOverviews('average', [2,4,8,16,32])

     out_ds = None


def split_raster(input_file, x, y, output_folder):
     '''Splits raster into smaller chunks according to specified divisions in rows and columns
     input_file: (str) path to image file to be split.
     x: (int) number of row divisions.
     y: (int) number of column divisions.
     output_folder: (str) path to destination folder where image chunks are stored.
     '''
     #open input raster and get transformation
     inRaster = gdal.Open(input_file)
     geoTrans = inRaster.GetGeoTransform()

     #get upper left corner coordinates and raster resolution
     x_min = geoTrans[0]
     y_max = geoTrans[3]
     res = geoTrans[1]

     #get raster width and height
     width = res * inRaster.RasterXSize
     height = res * inRaster.RasterYSize

     #size of sigle division
     x_size = width/x
     y_size = height/y

     #list of xy coordinates
     x_steps = [x_min + x_size * i for i in range(x+1)]
     y_steps = [y_max - y_size * i for i in range(y+1)]

     #get raster divisions and save to file
     for i in range(x):
          for j in range(y):
               xmin = x_steps[i]
               xmax = x_steps[i+1]
               ymax = y_steps[j]
               ymin = y_steps[j+1]

               gdal.Translate(output_folder+'/tile'+str(i)+str(j)+'.tif', inRaster,
                         projWin = (xmin, ymax, xmax, ymin))
     inRaster = None

