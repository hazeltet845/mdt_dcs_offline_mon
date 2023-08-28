from EndcapChart import *
from PIL import Image, ImageDraw, ImageFont
import SiteConfiguration

class EndcapInnerChart(EndcapChart):

#station names in the region
	StationNames=set(['EIS', 'EIL', 'EES', 'EEL'])
#etas per station names
	StationEtas={	'EIS' : [1, 2],\
			'EIL' : range(1, 6),\
			'EES' : [1, 2],\
			'EEL' : [1, 2]}
			
#phis per station names
	StationPhis={	'EIS' : range(1, 9),\
			'EIL' : range(1, 9),\
			'EES' : range(1, 9),\
			'EEL' : range(1, 9)}
#non existing stations	
	ExcludedStations=set([('EIL', 2, 5), ('EIL', 3, 5), ('EIL', 4, 5), ('EIL', 6, 5), ('EIL', 7, 5), ('EIL', 8, 5), ('EEL', 3, 1), ('EEL', 3, -1)])
	
#ranges
	RRange=(0, 7)


	def DrawDecoration(self, image):
		width=min(image.size[0], image.size[1])
		draw=ImageDraw.Draw(image)
		font = ImageFont.truetype(SiteConfiguration.TrueTypeFont,width//(self.RRange[1] + 3))
		for i in range(0,8):
			coords=self._get_coordinates(width, self.RRange[1] + 1, 2*i)
			draw.line(xy=[int(0.5 * image.size[0]) ,int(0.5 * image.size[1]) , coords[0], coords[1]], fill="#0000aa")
			coords=self._get_coordinates(width, self.RRange[1] - 4, 2*i + 1)
			fontsize=font.getsize(str(i+1))
			draw.text((int(coords[0]-0.5*fontsize[0]), int(coords[1] - 0.5 * fontsize[1])) , str(i+1), "#0000aa", font=font)
		fontsize=font.getsize("EEL/EES")	
		draw.text((int(image.size[0] * 0.5 - 0.5 * fontsize[0]), 0), "EEL/EES", "#0000aa", font=font)

		
	
	def _get_index_for(self, station, eta, phi):
		seg=2*(phi-1)
		if station[-1]=='S':
			seg+=1
		r=eta-1
		if station[:2]=='EE':
			r+=6
			if phi==3 and station[-1]=='L':
				r-=0.5
				
		return r, seg


	
	
