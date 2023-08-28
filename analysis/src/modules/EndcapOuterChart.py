from EndcapChart import *


class EndcapOuterChart(EndcapChart):

#station names in the region
	StationNames=set(['EOL', 'EOS'])
#etas per station names
	StationEtas={	'EOS' : range(1, 7),\
			'EOL' : range(1, 7),}
			
#phis per station names
	StationPhis={	'EOS' : range(1, 9),\
			'EOL' : range(1, 9),}
#non existing stations	
	ExcludedStations=set([])
	
#ranges
	RRange=(0, 5)
	
	def _get_index_for(self, station, eta, phi):
		seg=2*(phi-1)
		if station[-1]=='S':
			seg+=1
		r=eta-1
		return r, seg

	
	
