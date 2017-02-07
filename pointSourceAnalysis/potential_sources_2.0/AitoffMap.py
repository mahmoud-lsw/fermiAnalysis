# N.B Before running, make sure:
#       - all photon files are in a folder called 'photon'
#       - the spacecraft file is named 'spacecraft.fits' and is in a folder called 'spacecraft'
#	- a file called 'variables.py' is in the current directory. The file should contain all the variables for the specific cut
#       You have these 4 files in a folder called model:	# Note: This folder can be in any parent directory (program will keep going up until it finds it)
#              i) gll_iem_v05.fits				For details look at the code there 	
#              ii) gll_iem_v05_rev1.fit								  |
#              iii) gll_psc_v08.fit								  V
#              iv) iso_source_v05_rev1.txt
#              v) iso_clean_v05.txt

###### DONT CHANGE #######
if not 'overWriteFiles' in locals():
	overWriteFiles=False			# If you cant to change these, do it in 'variables.py' or in the interactive python shell. NOT HERE!!

if not 'createTSMaps' in locals():
	createTSMaps=True

if not 'mySources' in locals():
	mySources=False

if not 'createAitoff' in locals():
	createAitoff=0
##########################

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


import gt_apps as my_apps
import os
bashCommand = "ls -1 ./photon/*.fits > filelist.list"
os.system(bashCommand)
spacecraftFile='./spacecraft/spacecraft.fits'						# This is how I find the spacecraft file
while not os.path.isfile(spacecraftFile):
	spacecraftFile='../'+spacecraftFile


pathToModelFolder='model/'								# This is how I find the model file
while not os.path.isdir(pathToModelFolder):
	pathToModelFolder='../'+pathToModelFolder
###############################################
############ Adjustable paramaters ############
###############################################

if os.path.isfile("variables.py"):
	print colors.OKBLUE
	print "\n##### 'variables.py' was found. Using the variables outlined in file. ##### \n\n"
	execfile("variables.py")
	print '''Using values:
			
		overWriteFiles=%s	
		createTSMaps=%s
		mySources=%s
		createAitoff=%s
	''' %(overWriteFiles,createTSMaps,mySources,createAitoff)
else:
	print colors.FAIL
	print "'variables.py' was not found. It is now a required file."
	print "Please create the file."
	print '''These are the current variables:
evClass

RA
DEC
roi

eMin
eMax
tMin (ex. 239557417	# This is the earliest Fermi MET)
tMax (ex. 'INDEF'	# This will make tMax the maximun possible time)

irfsType (ex. sugested: 'P7REP_SOURCE_V15' , other : 'P7REP_CLEAN_V15' or $CALDB  )
optimizerType (ex. sugested: 'NewMinuit' other: 'Minuit' )
TSThreshold

createAitoff
		'''
	exit ()
print colors.ENDC
###############################################

########################
##### Naming stuff #####
########################
file = open('filelist.list', 'r')
name_temp=file.readline()
file.close()
name_type= name_temp[9:12]                                                      # Usually LAT
if (float(eMin/1000.0)).is_integer():                                                      # Usually LAT
	name_energy=str(int(eMin/1000.0))+'-'+str(int(eMax/1000.0))+'GeV' 
else:
	name_energy=str(float(eMin/1000.0)).replace('.', ',')+'-'+str(int(eMax/1000.0))+'GeV'                   # i.e 100Ge

gtselectOutfile=name_type+'_allphotondata_'+name_energy+'.fits'
filteredLATFile = name_type+'_filtered_'+name_energy+'.fits'
gtbinnedFile = name_type+'_binned3600_'+name_energy+'.fits'
ltCubeFile=name_type+'_ltCube_'+name_energy+'.fits'
expMapFile=name_type+'_expMap_'+name_energy+'_'+irfsType+'.fits'
filteredLATFile_withDiffResps = name_type+'_filtered_wDiffResps_'+irfsType+'_'+name_energy+'.fits'

modelFile=name_type+'_'+name_energy+'_model.xml'

#Results
xmlFile='results/'+name_type+'_results_'+optimizerType+'.xml'

modelFile_TSMap_resid='results/'+name_type+'_TSMap_resid_'+optimizerType+'.xml'
modelFile_TSMap_withSource='results/'+name_type+'_TSMap_withSource_'+optimizerType+'.xml'
TSMapResid='results/'+name_type+'_TSMap_resid_'+optimizerType+'.fits'
TSMapWithSource='results/'+name_type+'_TSMap_withSource_'+optimizerType+'.fits'
########################

my_apps.evtbin['algorithm'] = 'CMAP'
my_apps.evtbin['evfile'] = filteredLATFile
my_apps.evtbin['outfile'] = gtbinnedFile
my_apps.evtbin['scfile'] = spacecraftFile
my_apps.evtbin['emin'] = eMin
my_apps.evtbin['emax'] = eMax
my_apps.evtbin['nxpix'] = 3600
my_apps.evtbin['nypix'] = 1800
my_apps.evtbin['binsz'] = 0.1
my_apps.evtbin['coordsys'] = 'GAL'
my_apps.evtbin['xref'] = 0
my_apps.evtbin['yref'] = 0
my_apps.evtbin['axisrot'] = 0.0
my_apps.evtbin['proj'] = 'AIT'
my_apps.evtbin.run()



