from PIL import Image, ImageDraw
from MuonFixedIdUnpack import *

class BarrelChart:


	def Draw(self, image, colormap={}):
	#create drarw object
		draw=ImageDraw.Draw(image)
		x, y, x_size, y_size=self._get_geometry_params(image.size)
		up=MuonFixedIdUnpack()
		for station in self.StationNames:
			for eta in self.StationEtas[station]:
				for phi in self.StationPhis[station]:
					if (station, phi, eta) in self.ExcludedStations:
						continue
					color="#cccccc"
					ol="#aaaaaa"
					if ((station, phi, eta) in colormap):
						color=colormap[(station, phi, eta)]
						ol="#000000"
					else:
						up.InitByParam(station, phi, eta)
						if ( up.identifier ) in colormap:
							color=colormap[ up.identifier ]
							ol="#000000"
						else:
							# we used to input tube ids with certain unused bits unset - that was incorrect and has been changed
							# MuonFixedIdUnpack now translates to correct IDs but we need to accomodate the old ones still in the database
							unset_id = up.identifier ^ 7168
							if (unset_id) in colormap:
								color=colormap[ unset_id ]
								ol="#000000"
					col, row = self._get_index_for(station, eta, phi)
					col -= self.ColumnRange[0]
					row -= self.RowRange[0]
					draw.rectangle([(x[col], y[row]), (x[col] + int(x_size), y[row] + int(y_size))], outline=ol, fill=color)

	def PrintAreaMap(self, dimensions, linkmap):
		x, y, x_size, y_size=self._get_geometry_params(dimensions)
		up=MuonFixedIdUnpack()
		ret=""
		for ids in linkmap:
			if type(ids) == type(()):
				station, eta, phi=ids
				print ("station %s phi %s eta %s <br />\n" % (station,phi,eta))
			else:
				up.identifier=ids
				station=up.stationNameString()
				eta=up.stationEta()
				phi=up.stationPhi()
		#check if station is in range	
			# print "station %s phi %s eta %s <br />\n" % (station,phi,eta)
			# station BME phi 7 eta -1  ??
			if not station in self.StationNames:
				continue
			if not phi in set(self.StationPhis[station]):
				continue
			if not eta in set(self.StationEtas[station]):
				continue
			if (station, phi, eta) in self.ExcludedStations:
				continue
		#get index for station
			col, row = self._get_index_for(station, eta, phi)
			col -= self.ColumnRange[0]
			row -= self.RowRange[0]
			alt='(' + station + ', ' + str(phi) + ', ' + str(eta) + ')'
			ret+='<area shape="rect" coords="' + str(x[col]) + ', ' + str(y[row]) + ', ' + str(x[col] + x_size) + ',' + str(y[row] + y_size) + '" href="' + linkmap[ids] + '" alt="' + alt + '" title="' + alt +'">\n'
		return ret

	def DrawDecoration(self, image):
		pass		
	
		
	def GetIndexedCoordiantes(self):
		ret={}
		for station in self.StationNames:
			for eta  in self.StationEtas[station]:
				for phi in self.StationPhis[station]:
					if (station, phi, eta) in self.ExcludedStations:
						continue
					ret[self._get_index_for(station, eta, phi)] = station + " e=" + str(eta) + " p=" + str(phi) 
		return ret


	def _get_geometry_params(self, dimensions):
		width, height = dimensions
	#calculate size of a chamber box
		n_cols=self.ColumnRange[1] - self.ColumnRange[0] + 1
		n_rows=self.RowRange[1] - self.RowRange[0]
		x_size=float(width)/float(n_cols)
		avail_height=height-8*len(self._line_scips)
		y_size=float(avail_height)/float(n_rows)
	#build y and x coordiante array
		y=[]
		line_scip_add=0
		for row in range(self.RowRange[0] ,self.RowRange[1]+1):
			if row in self._line_scips:
				line_scip_add += 8
			y.append(int(y_size * (row - self.RowRange[0])) + line_scip_add)
		x=[]
		for col in  range(self.ColumnRange[0] ,self.ColumnRange[1]+1):
			x.append(int(x_size * (col - self.ColumnRange[0])))		
		return x, y, int(x_size) , int(y_size)
