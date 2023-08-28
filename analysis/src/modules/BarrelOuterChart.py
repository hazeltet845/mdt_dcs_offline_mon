from BarrelChart import *
from PIL import Image, ImageDraw, ImageFont
import SiteConfiguration


class BarrelOuterChart(BarrelChart):

#station names in the region
	StationNames=set(['BOL', 'BOS', 'BOF', 'BOG','BOE'])
#etas per station names
	StationEtas={	'BOL' : [*range(-7, 0),*range(1, 8)],\
			'BOS' : [*range(-6, 0),*range(1, 7)],\
			'BOF' : [-7,-5,-3,-1,1,3,5,7],\
			'BOG' : [-8,-6,-4,-2,0,2,4,6,8],'BOE' : [-3,3]}
#phis per station names
	StationPhis={	'BOL' : range(1, 9),\
			'BOS' : [*range(1, 6),* [ 8 ]],\
			'BOF' : [6, 7],\
			'BOG' : [6, 7], 'BOE' : [7]}
#non existing stations	
	ExcludedStations=set([ ('BOL', 1, -7), ('BOL', 1, 7), ('BOL', 2, -7), ('BOL', 2, 7), ('BOL', 3, -7), ('BOL', 3, 7),('BOL', 4, -7), ('BOL', 4, 7),('BOL', 5, -7), ('BOL', 5, 7),('BOL', 6, -7), ('BOL', 6, 7),('BOL', 8, -7), ('BOL', 8, 7),('BOL',7,-7),('BOL',7,7) ])
	
#ranges
	ColumnRange = (-8, 8)
	RowRange=(-2, 16)

	def DrawDecoration(self, image):
		draw=ImageDraw.Draw(image)
		x, y, x_size, y_size=self._get_geometry_params(image.size)
		titlefont = ImageFont.truetype(SiteConfiguration.TrueTypeFont, 2*y_size)
		labelfont = ImageFont.truetype(SiteConfiguration.TrueTypeFont, y_size)
		cntr = .5 * x_size - 5
		draw.text((x[5], y[0] ), "BOS, BOL",  "#000099", font=titlefont)
		draw.text((x[10], y[0]), "BOS, BOL",  "#000099", font=titlefont)
		draw.text((x[9] + cntr, y[13]), "BOF",  "#000099", font=labelfont)
		draw.text((x[10] + cntr, y[13]), "BOG",  "#000099", font=labelfont)
		draw.text((x[6] + cntr, y[13]), "BOG",  "#000099", font=labelfont)
		draw.text((x[7] + cntr, y[13]), "BOF",  "#000099", font=labelfont)
		draw.text((x[6] + cntr, y[15]), "BOG",  "#000099", font=labelfont)
		draw.text((x[7] + cntr, y[15]), "BOF",  "#000099", font=labelfont)
		draw.text((x[9] + cntr, y[15]), "BOF",  "#000099", font=labelfont)
		draw.text((x[10] + cntr, y[15]), "BOG",  "#000099", font=labelfont)
		draw.text((x[15] + cntr, y[14]), "BOE",  "#000099", font=labelfont)
		draw.text((x[1] + cntr, y[14]), "BOE",  "#000099", font=labelfont)
		for i in range(0, 8):
			draw.text((x[8] + 0.3 * x_size, y[2*i+2]), str(i+1), "#000099", font=titlefont)

	def _get_index_for(self, station, eta, phi):
		row=2*(phi-1)
		if station=='BOS' or station=='BOF' or station=='BOG':
			row += 1
		column=eta
		if station=='BOF' or station=='BOG':
			column = eta
		if station == 'BOE':
			if eta > 0:
				column += 4
			else:
				column -= 4
		return column, row
			
	
	_line_scips=[0, 2, 4, 6, 8, 10, 12, 14]

	
	
