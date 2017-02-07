# N.B Before running, make sure:
#       - all photon files are in a folder called 'photon'
#       - the spacecraft file is named 'spacecraft.fits' and is in a folder called 'spacecraft'
#       You have these 4 files in a folder called model:
#              i) gll_iem_v05.fits
#              ii) gll_iem_v05_rev1.fit
#              iii) gll_psc_v08.fit
#              iv) iso_source_v05_rev1.txt
#              v) iso_clean_v05.txt


import gt_apps as my_apps
import os
bashCommand = "ls -1 ./photon/*.fits > filelist.list"
os.system(bashCommand)
spacecraftFile='./spacecraft/spacecraft.fits'
###############################################
############ Adjustable paramaters ############
###############################################
evClass=2
eMin=100
eMax=300000
tMax=256970880
roi=10
irfsType='P7REP_CLEAN_V15'       # or 'P7REP_SOURCE_V15' ?
###############################################

##### Naming stuff #####
file = open('filelist.list', 'r')
name_temp=file.readline()
file.close()
name_type= name_temp[9:12]                                                      # Usually LAT
name_energy=str(int(eMin/1000))+'-'+str(int(eMax/1000))+'GeV'                   # i.e 100GeV

gtselectOutfile=name_type+'_allphotondata_'+name_energy+'.fits'
filteredLATFile = name_type+'_final_'+name_energy+'.fits'
expCubeFile=name_type+'_expCube_'+name_energy+'.fits'
expMapFile=name_type+'_expMap_'+name_energy+'_'+irfsType+'.fits'

modelFile=name_type+'_'+name_energy+'_model.xml'
###############################################

def printDictionaryToFile(dictionary):
	fid=open('TSValues.txt','w')
	for source,TS in dictionary.iteritems():
		fid.write("%s : %f\n" %(source,TS))
	fid.close()
	os.system('mv TSValues.txt data')

# Start analysis

# Make an exposure map
my_apps.expMap['evfile'] = filteredLATFile
my_apps.expMap['scfile'] =spacecraftFile
my_apps.expMap['expcube'] =expCubeFile
my_apps.expCube['outfile'] = expCubeFile
my_apps.expMap['outfile'] =expMapFile
my_apps.expMap['irfs'] =irfsType
my_apps.expMap['srcrad'] =1.5*roi    # Source Region should be larger than the Region of Interest by ~50%.
my_apps.expMap['nlong'] =120
my_apps.expMap['nlat'] =120
my_apps.expMap['nenergies'] =20
my_apps.expMap.run()
