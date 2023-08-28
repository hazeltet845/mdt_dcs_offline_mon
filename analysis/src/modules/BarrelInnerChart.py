from BarrelChart import *
from PIL import Image, ImageDraw, ImageFont
import SiteConfiguration

class BarrelInnerChart(BarrelChart):

	StationNames=set(['BIL', 'BIS', 'BEE', 'BIM', 'BIR'])
	
	StationEtas={	'BIL' : [*range(-6, 0),* range(1, 7)],\
			'BIS' : [*range(-8, 0), * range(1, 9)],\
			'BEE' : [-2, -1, 1, 2],\
			'BIM' : [*range(-5, 0),*range(1, 6)],\
			'BIR': [*range(-6, 0),*range(1, 7)]}
	StationPhis={ 	'BIL': [*range(1,6),*[7]],\
			'BIS' : range(1, 9),\
			'BEE' : range(1,9),\
			'BIM': [6, 8],\
			'BIR': [6,8]}
	ExcludedStations = set([])

#ranges
	ColumnRange = (-11, 11)
	RowRange=(-2, 18)

	
	def DrawDecoration(self, image):
		draw=ImageDraw.Draw(image)
		x, y, x_size, y_size=self._get_geometry_params(image.size)
		titlefont = ImageFont.truetype(SiteConfiguration.TrueTypeFont, 2*y_size)
		labelfont = ImageFont.truetype(SiteConfiguration.TrueTypeFont, y_size)
		cntr = .5 * x_size - 5
		negmargin = 0.4 * y_size
		draw.text((x[5], y[0] - negmargin), "BIS, BIL",  "#000099", font=titlefont)
		draw.text((x[13], y[0] - negmargin), "BIS, BIL",  "#000099", font=titlefont)
		draw.text((x[0], y[0] - negmargin), "BEE",  "#000099", font=titlefont)
		draw.text((x[21], y[0] - negmargin), "BEE",  "#000099", font=titlefont)

		# row 6
		draw.text((x[12] + cntr, y[12]), "BIM",  "#000099", font=labelfont)
		draw.text((x[12] + cntr, y[13]), "BIR",  "#000099", font=labelfont)
		draw.text((x[10] + cntr, y[12]), "BIM",  "#000099", font=labelfont)
		draw.text((x[10] + cntr, y[13]), "BIR",  "#000099", font=labelfont)
		#row 8 
		draw.text((x[12] + cntr, y[17]), "BIR",  "#000099", font=labelfont)
		draw.text((x[12] + cntr, y[18]), "BIM",  "#000099", font=labelfont)

		draw.text((x[10] + cntr, y[17]), "BIR",  "#000099", font=labelfont)
		draw.text((x[10] + cntr, y[18]), "BIM",  "#000099", font=labelfont)
		
		for i in range(0, 8):
			draw.text((x[11] + 0.2 * x_size, y[self.__phi_to_row[i]+2]), str(i+1), "#000099", font=titlefont)
			
		
	
	def _get_index_for(self, station, eta, phi):
		row=self.__phi_to_row[ phi -1 ]
		if station=='BIS':
			if phi==6 or phi==8:
				row += 2
			else:
				row += 1
		if phi==6 and station=='BIR':
			row+=1
		if phi==8 and station=='BIM':
			row+=1
			
		
		eta_offset=0
		if station=='BEE':
			row += 1
			if phi==6 or phi==8:
				row += 1
		if station=="BEE" and eta>0:
			eta_offset=9
		if station=="BEE" and eta<0:	
			eta_offset=-9
		
		return eta+eta_offset, row
			
	
	_line_scips=set([2, 4, 6, 8, 10, 13, 15])

	
	__phi_to_row = [0, 2, 4, 6, 8, 10, 13, 15]

	
