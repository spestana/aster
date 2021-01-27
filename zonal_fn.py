#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Steven Pestana (spestana@uw.edu)

def zonal_stats(aster_filepath, aster_band, shapefile_filepath, return_masked_array=False):
	'''Calculate zonal statistics for an ASTER TIR geotiff image within a single polygon from a shapefile.'''

	with rio.open(aster_filepath) as src:
		
		# Open the shapefile
		zone_shape = gpd.read_file(shapefile_filepath)

		# Make sure our shapefile is the same CRS as the ASTER TIR image
		zone_shape = zone_shape.to_crs(src.crs)

		# Mask the ASTER TIR image to the area of the shapefile
		try:
			masked_aster_band_DN, mask_transform = mask(dataset=src, 
											shapes=zone_shape.geometry,
											crop=True,
											all_touched=True,
											filled=True)
		# Note that we still have a "bands" axis (of size 1) even though there's only one band, we can remove it below
		except ValueError as e: 
			# ValueError when shape doesn't overlap raster
			return
		
		# change data type to float64 so we can fill in DN=0 with NaN values
		masked_aster_band_DN = masked_aster_band_DN.astype('float64')
		masked_aster_band_DN[masked_aster_band_DN==0] = np.nan
				
		# Convert DN to Radiance
		masked_aster_band_rad = tir_dn2rad(masked_aster_band_DN, aster_band)
		
		# Convert Radiance to Brightness Temperature
		masked_aster_band_tb = tir_rad2tb(masked_aster_band_rad, aster_band)
		
		# Remove the extra dimension (bands, we only have one band here)
		masked_aster_band_tb = masked_aster_band_tb.squeeze()
		
		# Get all pixel values in our masked area
		values = masked_aster_band_tb.flatten() # flatten to 1-D
		values = values[~np.isnan(values)] # remove NaN pixel values
		
		
		# Calculate zonal statistics for this area (mean, max, min, std:)
		try:
			masked_aster_band_tb_mean = values.mean()
			masked_aster_band_tb_max = values.max()
			masked_aster_band_tb_min = values.min()
			masked_aster_band_tb_std = values.std()
		except ValueError as e:
			# ValueError when the shapefile is empty I think
			return
		
		if return_masked_array == True:
			return masked_aster_band_tb_mean, masked_aster_band_tb_max, masked_aster_band_tb_min, masked_aster_band_tb_std, masked_aster_band_tb
		else:
			return masked_aster_band_tb_mean, masked_aster_band_tb_max, masked_aster_band_tb_min, masked_aster_band_tb_std

