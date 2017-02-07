
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


# First find minimum source Name

minROI=9999		# Arbitrarily large number
import re
with open(modelFile_TSMap_resid, 'r') as inF:
	for line in inF:
		if "<!-- Diffuse Sources -->" in line:
			break
		if "<source name=" in line:		
			currentName= re.findall('<source name=\"(.*?)"', line)[0]

		if "degrees away from ROI center -->" in line:
			currentROI=float(re.findall("Source is (.*?) degrees", line)[0])

		# Check if minimum
		if "</source>" in line and currentROI<minROI:
			minName=currentName			
			minROI=currentROI
# Now delete it!


findSrcFile='results/'+name_type+'_findSrc_'+minName+'_'+optimizerType+'.txt'
if not os.path.isfile(findSrcFile) or overWriteFiles:
	from GtApp import GtApp
	gtfindsrc = GtApp('gtfindsrc','Likelihood')
	gtfindsrc['evfile']=filteredLATFile_withDiffResps
	gtfindsrc['scfile']=spacecraftFile
	gtfindsrc['srcmdl']=modelFile
	gtfindsrc['outfile']=findSrcFile
	gtfindsrc['irfs']=irfsType
	gtfindsrc['optimizer']=optimizerType
	gtfindsrc['expcube']=ltCubeFile
	gtfindsrc['expmap']=expMapFile
	gtfindsrc['target']=minName
	gtfindsrc['coordsys']= 'CEL'
	gtfindsrc['ra']=RA
	gtfindsrc['dec']=DEC
	gtfindsrc['ftol']=0.0001
	gtfindsrc['atol']=0.001		# Default Value
	gtfindsrc.run()
