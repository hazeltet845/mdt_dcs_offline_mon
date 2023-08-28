from BarrelChart import *
from PIL import Image, ImageDraw, ImageFont
import SiteConfiguration

class BarrelMiddleChart(BarrelChart):

#station names in the region
	StationNames=set(['BML', 'BMS', 'BMF', 'BME', 'BMG'])
#etas per station names
	StationEtas={	'BML' : [*range(-6,0),*range(1, 7)],\
			'BMS' : [*range(-6,0),*range(1, 7)],\
			'BMF' : [-3, -2, -1, 1, 2, 3],\
			'BME' : [ -5,-4,4,5],\
			'BMG' : [-6,-4,-2,2,4,6]}
#phis per station names
	StationPhis={	'BML': range(1,9),\
			'BMS' : [*range(1, 6),*[8]],\
			'BMF' : [6, 7],\
			'BME' : [7],\
			'BMG' : [6, 7]}

#non existing stations	
	ExcludedStations=set([('BML', 7, -4), ('BML', 7, 4) ])

#ranges
	ColumnRange = (-7, 7)
	RowRange=(-2, 16)


	def DrawDecoration(self, image):
		draw=ImageDraw.Draw(image)
		x, y, x_size, y_size=self._get_geometry_params(image.size)
		font = ImageFont.truetype(SiteConfiguration.TrueTypeFont, 2*y_size)
		titlefont = ImageFont.truetype(SiteConfiguration.TrueTypeFont, 2*y_size)
		labelfont = ImageFont.truetype(SiteConfiguration.TrueTypeFont, y_size)
		cntr = .5 * x_size - 5
		draw.text((x[3], y[0]), "BMS, BML",  "#000099", font=titlefont)
		draw.text((x[8], y[0]), "BMS, BML",  "#000099", font=titlefont)
		draw.text((x[7] + cntr, y[13]), "BMF",  "#000099", font=labelfont)
		draw.text((x[5] + cntr, y[13]), "BMF",  "#000099", font=labelfont)
		draw.text((x[7] + cntr, y[15]), "BMF",  "#000099", font=labelfont)
		draw.text((x[5] + cntr, y[15]), "BMF",  "#000099", font=labelfont)
		draw.text((x[2] + cntr, y[14]), "BME",  "#000099", font=labelfont)
		draw.text((x[10] + cntr,y[14]), "BME",  "#000099", font=labelfont)
		draw.text((x[2] + cntr, y[13]), "BMG",  "#000099", font=labelfont)
		draw.text((x[2] + cntr, y[15]), "BMG",  "#000099", font=labelfont)
		draw.text((x[10] + cntr,y[13]), "BMG",  "#000099", font=labelfont)
		draw.text((x[10] + cntr,y[15]), "BMG",  "#000099", font=labelfont)
		for i in range(0, 8):
			draw.text((x[6] + 0.3 * x_size, y[2*i+2]), str(i+1), "#000099", font=font)
			


	def _get_index_for(self, station, eta, phi):
		row=2*(phi-1)
		column=eta
		if station=='BMS' or station=='BMF':
			row += 1
# Plot BMG next to BMF, in eta positions 4,5,6
		if station=='BMG':
			
			row += 1  
			if eta < 0:
				tmp = -1
			else: 
				tmp = 1
			if eta == tmp * 2:
				column = tmp*4
			elif eta == tmp*4:
				column = tmp*5
			elif eta == tmp*6:
				column = tmp*6
# This is to skip BML4x13 which does not exist
		if phi==7 and station[-1]=='L':
			if eta>3:
				column+=1
			if eta<-3:
				column-=1
#plot BME at eta=+-4 in position of non-existant BML4x13
		if station == 'BME':
			column = eta
		return column, row
				
	_line_scips=[0, 2, 4, 6, 8, 10, 12, 14]
