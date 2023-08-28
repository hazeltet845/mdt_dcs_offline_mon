from EndcapChart import *


class EndcapMiddleChart(EndcapChart):

#station names in the region
	StationNames=set(['EML', 'EMS'])
#etas per station names
	StationEtas={	'EMS' : range(1, 6),\
			'EML' : range(1, 6),}
			
#phis per station names
	StationPhis={	'EMS' : range(1, 9),\
			'EML' : range(1, 9),}
#non existing stations	
	ExcludedStations=set([])
	
#ranges
	RRange=(0, 4)
	
	
	def _get_index_for(self, station, eta, phi):
		seg=2*(phi-1)
		if station[-1]=='S':
			seg+=1
		r=eta-1
		return r, seg

	
	
