from PIL import Image, ImageDraw, ImageFont
from MuonFixedIdUnpack import *
import SiteConfiguration

class EndcapChart:
	
	Side=1
	
	def Draw(self, image, colormap={}, side='A'):
		width=min(image.size[0], image.size[1])
		draw=ImageDraw.Draw(image)
		up=MuonFixedIdUnpack()
		for station in self.StationNames:
			for eta  in self.StationEtas[station]:
				for phi in self.StationPhis[station]:
					if (station, phi, eta) in self.ExcludedStations:
						continue
					color="#cccccc"
					ol="#aaaaaa"
					if ((station, phi, eta * self.Side) in colormap):
						color=colormap[(station, phi, eta * self.Side)]
						ol="#000000"
					else:
						up.InitByParam(station, phi, eta*self.Side)
						if( up.identifier ) in colormap:
							color=colormap[ up.identifier ]
							ol="#000000"
						else:
							# we used to input tube ids with certain unused bits unset - that was incorrect and has been changed
							# MuonFixedIdUnpack now translates to correct IDs but we need to accomodate the old ones still in the database
							unset_id = up.identifier ^ 7168
							if unset_id in colormap:
								color=colormap[ unset_id ]
								ol="#000000"
					r, seg = self._get_index_for(station, eta, phi)
					pol=self._get_coordinates(width, r, seg)
					draw.polygon(pol, outline=ol, fill=color)
	

	def PrintAreaMap(self, dimension, linkmap):
		ret=""
		up=MuonFixedIdUnpack()
		for ids in linkmap:
			if type(ids) == type(()):
				station, eta, phi=ids
			else:
				up.identifier=ids
				station=up.stationNameString()
				eta=up.stationEta()
				phi=up.stationPhi()
		#check if station is in range	
			if not station in self.StationNames:
				continue
			if not phi in set(self.StationPhis[station]):
				continue
			if not eta*self.Side  in set(self.StationEtas[station]):
				continue
			if (station, phi, eta*self.Side) in self.ExcludedStations:
				continue
		#get index for station
			alt='(' + station + ', ' + str(phi) + ', ' + str(eta) + ')'
			ret+= '<area shape="poly" coords="' 
			r, seg = self._get_index_for(station, eta*self.Side, phi)
			count=0
			for coord in self._get_coordinates(dimension, r, seg):
				ret += str(coord) 
				if count<7:
					ret+= ", "
				count +=1
			ret+='" href="' + linkmap[ids] + '" alt="' + alt + '" title="' + alt +'">'
		return ret
			

	def DrawDecoration(self, image):
		width=min(image.size[0], image.size[1])
		draw=ImageDraw.Draw(image)
		font = imageFont.truetype(SiteConfiguration.TrueTypeFont, width/(self.RRange[1] + 3))
		for i in range(0,8):
			coords=self._get_coordinates(width, self.RRange[1] + 1, 2*i)
			draw.line(xy=[int(0.5 * image.size[0]) ,int(0.5 * image.size[1]) , coords[0], coords[1]], fill="#0000aa")
			coords=self._get_coordinates(width, self.RRange[1] - 1, 2*i + 1)
			fontsize=font.getsize(str(i+1))
			draw.text((int(coords[0]-0.5*fontsize[0]), int(coords[1] - 0.5 * fontsize[1])) , str(i+1), "#0000aa", font=font)
		
	def GetIndexedCoordiantes(self):
		ret={}
		for station in self.StationNames:
			for eta  in self.StationEtas[station]:
				for phi in self.StationPhis[station]:
					if (station, phi, eta) in self.ExcludedStations:
						continue
					ret[self._get_index_for(station, eta, phi)] = station + " e=" + str(eta) + " p=" + str(phi) 
		return ret



	def _get_coordinates(self, size, r, phi):
		p=phi - 8
		p=p % 16
		thickness=0.5*size/(self.RRange[1] + 3)
		x1=int((r + 2) * thickness * self.__cos[p]) + int(0.5*size)
		y1=int((r + 2) * thickness * self.__sin[p]) + int(0.5*size)
		x2=int((r + 3) * thickness * self.__cos[p]) + int(0.5*size)
		y2=int((r + 3) * thickness * self.__sin[p]) + int(0.5*size)
		p=p+1
		p=p % 16
		x3=int((r + 3) * thickness * self.__cos[p]) + int(0.5*size)
		y3=int((r + 3) * thickness * self.__sin[p]) + int(0.5*size)
		x4=int((r + 2) * thickness * self.__cos[p]) + int(0.5*size)
		y4=int((r + 2) * thickness * self.__sin[p]) + int(0.5*size)
		return [ x1, y1, x2, y2, x3, y3, x4, y4]
		
			
	##lookup tables for sinus and cosinus
	
	__sin=[-0.195090322016, 0.195090322016, 0.55557023302, 0.831469612303, 0.980785280403, 0.980785280403, 0.831469612303, 0.55557023302, 0.195090322016, -0.195090322016, -0.55557023302, -0.831469612303, -0.980785280403, -0.980785280403, -0.831469612303, -0.55557023302, -0.195090322016]
	
	__cos=[0.980785280403, 0.980785280403, 0.831469612303, 0.55557023302, 0.195090322016, -0.195090322016, -0.55557023302, -0.831469612303, -0.980785280403, -0.980785280403, -0.831469612303, -0.55557023302, -0.195090322016, 0.195090322016, 0.55557023302, 0.831469612303, 0.980785280403]

		
