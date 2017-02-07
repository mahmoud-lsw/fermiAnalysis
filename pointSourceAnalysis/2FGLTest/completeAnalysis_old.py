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

photonFolder='./photon'						# This is how I find the photon file
while not os.path.isdir(photonFolder):
	photonFolder='../'+photonFolder
bashCommand = "ls -1 "+photonFolder +"/*.fits > filelist.list"
os.system(bashCommand)
photonFile='@'+photonFolder+'/filelist.list'

spacecraftFolder='./spacecraft'						# This is how I find the spacecraft file
while not os.path.isdir(spacecraftFolder):
	spacecraftFolder='../'+spacecraftFolder
bashCommand = "ls -1 "+spacecraftFolder +"/*.fits > spacelist.list"
os.system(bashCommand)
spacecraftFile='@'+spacecraftFolder+'/spacelist.list'

pathToModelFolder='model/'						# This is how I find the model file
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

###############################################

# Quick check to see if any files already exist
normalFiles_temp=[gtselectOutfile,filteredLATFile,ltCubeFile,expMapFile,modelFile,filteredLATFile_withDiffResps]
#binningFiles_temp=[gtbinnedFile,expCubeFile,farithOutfile,fimgtrimOutfile,fcarithOutfile]

normalFiles=[]
#binningFiles=[]
for x in normalFiles_temp:
	if os.path.isfile(x):
		normalFiles.append(x)

#for y in binningFiles_temp:
#	if os.path.isfile(y):
#		binningFiles.append(y)

if len(normalFiles)>0: #or len(binningFiles)>0:
	if overWriteFiles:
		print colors.FAIL +"!!!!! WARNING: THESE FILES WILL BE OVERWRITTEN !!!!!:"
	if not overWriteFiles:
		print colors.WARNING+ "CAREFULL: These previous files will be used:"
	if len(normalFiles)>0:
		print '############# Analysis Files #############'
		for x in normalFiles:
			print x
#	if len(binningFiles)>0:
#		print '############# Binning Files #############'
#		for x in binningFiles:
#			print x
	print colors.ENDC
	print 'MAKE SURE YOU ARE USING THE RIGHT ONES/NOT OVERWRITING ANYTHING IMPORTANT!' 
	doIContinue = raw_input('Do you want to continue? (y/n):')

	if not (doIContinue=='y' or doIContinue=='Y' or doIContinue=='yes' or doIContinue=='Yes' or doIContinue=='YES'):
		print 'Exiting'
		exit ()
###############################################

def printDictionaryToFile(dictionary,filename):
	fid=open(filename,'w')
	for source,TS in dictionary.iteritems():
		fid.write("%s : %f\n" %(source,TS))
	fid.close()
	os.system('mv '+filename+' results')

################################################################################################
######################################## Start the cuts ########################################
################################################################################################

if not os.path.isfile(gtselectOutfile) or overWriteFiles:
	#Run gtselect
	my_apps.filter['evclass'] = evClass
	my_apps.filter['ra'] = RA
	my_apps.filter['dec'] = DEC
	my_apps.filter['rad'] = ROI
	my_apps.filter['emin'] = eMin
	my_apps.filter['emax'] = eMax
	my_apps.filter['zmax'] = 100
	my_apps.filter['tmin'] = tMin
	my_apps.filter['tmax'] = tMax
	my_apps.filter['infile'] = photonFile
	my_apps.filter['outfile'] = gtselectOutfile
	my_apps.filter.run()

if not os.path.isfile(filteredLATFile) or overWriteFiles:
	#Run gtmktime
	my_apps.maketime['scfile'] = spacecraftFile
	my_apps.maketime['filter'] = spacecraftFilter
	my_apps.maketime['roicut'] = 'yes'
	my_apps.maketime['evfile'] = gtselectOutfile
	my_apps.maketime['outfile'] = filteredLATFile
	my_apps.maketime.run()

if (not os.path.isfile(gtbinnedFile) or overWriteFiles):
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

if not os.path.isfile(ltCubeFile) or overWriteFiles:
	# Make livetime cube
	my_apps.expCube['evfile'] = filteredLATFile
	my_apps.expCube['scfile'] = spacecraftFile
	my_apps.expCube['outfile'] = ltCubeFile
	my_apps.expCube['dcostheta'] = 0.025
	my_apps.expCube['binsz'] = 1
	my_apps.expCube.run()

if not os.path.isfile(expMapFile) or overWriteFiles:
	# Make an exposure map
	my_apps.expMap['evfile'] = filteredLATFile
	my_apps.expMap['scfile'] =spacecraftFile
	my_apps.expMap['expcube'] =ltCubeFile
	my_apps.expMap['outfile'] =expMapFile
	my_apps.expMap['irfs'] =irfsType
	my_apps.expMap['srcrad'] =min(max(1.5*ROI,ROI+10),180)    # Source Region should be larger than the Region of Interest by ~50% (or 10 degrees for smaller numbers). BUT NEVER BIGGER THEN 180!
# Get half degree pixels
	halfDegPix=4*min(max(1.5*ROI,ROI+10),180)
	my_apps.expMap['nlong'] =halfDegPix
	my_apps.expMap['nlat'] =halfDegPix
	my_apps.expMap['nenergies'] =20
	my_apps.expMap.run()


if not os.path.isfile(modelFile) or overWriteFiles:
	from make2FGLxml import *
	print colors.OKBLUE+"Making Source Model"+colors.ENDC
	# Generate XML Model File
	mymodel = srcList(pathToModelFolder+'gll_psc_v08.fit',filteredLATFile,modelFile)
	mymodel.makeModel(pathToModelFolder+'gll_iem_v05_rev1.fit', 'gll_iem_v05_rev1', pathToModelFolder+'iso_source_v05_rev1.txt', 'iso_source_v05_rev1')

# There should now be a modelFile with a name SIMILAR to LAT_modelFile.xml

if not os.path.isfile(filteredLATFile_withDiffResps) or overWriteFiles:
	# Run the Diffuse response (Only if you are NOT using CALDB)

	# Each event must have a separate response precomputed for each diffuse component in the source model. The precomputed responses for Pass 7 (V6) data are for the gll_iem_v05, iso_source_v05.txt, and iso_clean_05.txt diffuse models.

	os.system('cp '+filteredLATFile+' '+filteredLATFile_withDiffResps)	#Make a copy of the filteredLATFile
	my_apps.diffResps['evfile']=filteredLATFile_withDiffResps
	my_apps.diffResps['scfile']=spacecraftFile
	my_apps.diffResps['srcmdl']=modelFile
	my_apps.diffResps['irfs']=irfsType
	my_apps.diffResps.run()
	
# Run the Likelihood Analysis
print colors.OKBLUE+"Performing Liklihood Analysis"+colors.ENDC
import pyLikelihood
from UnbinnedAnalysis import *
obs = UnbinnedObs(filteredLATFile_withDiffResps,spacecraftFile,expMap=expMapFile,expCube=ltCubeFile,irfs=irfsType)
like = UnbinnedAnalysis(obs,modelFile,optimizer=optimizerType)

# Cuts Complete
print colors.OKGREEN+"################ Analysis Complete ################"
print obs
print like
print "###################################################"+colors.ENDC

################################
###### Adjust Source Model #####
################################

like.tol
like.tolType
like.tol = 0.0001
if optimizerType=='Minuit':
	likeobj = pyLike.Minuit(like.logLike)
elif optimizerType=='NewMinuit':
	likeobj = pyLike.NewMinuit(like.logLike)
else:
	print "Error: Bad Optimizer. Exiting"
	exit()
like.fit(verbosity=0,covar=True,optObject=likeobj)                 # Warning: This takes VERY long ~ 30 minutes

# Get all the TS values of the sources in the model
sourceDetails = {}
for source in like.sourceNames():
   sourceDetails[source] = like.Ts(source)

# Output for data
os.system('mkdir results')

printDictionaryToFile(sourceDetails,'TSValues_preDelete.txt')

# N.B A source with a TS value less than 0 should never happen unless the minimization failed. Remove that source and try fitting again and check the return code again.

converganceCheckOne="Zero?: %d" %(likeobj.getRetCode())
converganceCheckTwo="NA"
print converganceCheckOne # This value should be zero, refit using the method below if not

if not likeobj.getRetCode() ==0 or eMin<100000:	# If energy is too high, just don't refit because it causes problems

	print colors.OKBLUE+"Minimization Failed. Removing sources with TS < 9.0 and refitting!"
	# Protip, you can really simplify the model by removing sources with TS levels below 9 (about 3 sigma)
	for source,TS in sourceDetails.iteritems():
		print source, TS
		if (TS < TSThreshold):
			print "Deleting..."
			like.deleteSource(source)
	# Refit
	like.fit(verbosity=0,covar=True,optObject=likeobj)

	converganceCheckTwo="Zero?: %d" %(likeobj.getRetCode())

	print converganceCheckTwo

	sourceDetails = {}
	for source in like.sourceNames():
	   sourceDetails[source] = like.Ts(source)
	
	print colors.ENDC
printDictionaryToFile(sourceDetails,'TSValues.txt')

########################################
########### Make some plots! ###########
########################################
import matplotlib.pyplot as plt
import numpy as np
if eMin<100000:

	E = (like.energies[:-1] + like.energies[1:])/2.
	# The 'energies' array are the endpoints so we take the midpoint of the bins.

	plt.figure(figsize=(9,9))
	plt.ylim((0.4,1e4))
	plt.xlim((200,300000))
	sum_model = np.zeros_like(like._srcCnts(like.sourceNames()[0]))

	for sourceName in like.sourceNames():
	   sum_model = sum_model + like._srcCnts(sourceName)
	   plt.loglog(E,like._srcCnts(sourceName),label=sourceName[1:])

	plt.loglog(E,sum_model,label='Total Model')
	plt.errorbar(E,like._Nobs(),yerr=np.sqrt(like._Nobs()), fmt='o',label='Counts')
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
	plt.savefig('results/1.eps',format='eps', bbox_inches='tight')                       # Save figure!


	# Plot residuals
	sum_counts=sum_model                                        # Is this right? Probably not :/
	resid = (like._Nobs() - sum_counts)/sum_counts
	resid_err = (np.sqrt(like._Nobs())/sum_counts)
	plt.figure(figsize=(9,9))
	plt.xscale('log')
	plt.errorbar(E,resid,yerr=resid_err,fmt='o')
	plt.axhline(0.0,ls=':')
	plt.savefig('results/2.eps',format='eps', bbox_inches='tight')

# Get indexes and stuff
fid=open('results/'+name_type+'_results.txt','w')
fid.write(converganceCheckOne+'\n')
if not 'overWriteFiles' in locals():
	fid.write('None\n\n')
else:
	fid.write(converganceCheckTwo+'\n\n')

for sourceName in like.sourceNames():
	fid.write(str(like.model[sourceName]))
	fid.write('Flux: '+str(like.flux(sourceName,emin=eMin,emax=eMax))+'\n')
	fid.write('TS: '+str(like.Ts(sourceName))+'\n')
	if like.Ts(sourceName) >= 0:
		fid.write('Sigma: '+str(np.sqrt(like.Ts(sourceName)))+'\n')		# This is to avoid negatives going cray
	else:
		fid.write('Sigma: NA')
	fid.write('\n=====================================\n')
fid.close()

# Save .xml
like.logLike.writeXml(xmlFile)


#############################################
############### Create TS map ###############
#############################################


# Prepare source file
infile = open(modelFile)
outfile = open(modelFile_TSMap_withSource, 'w')

for line in infile:
    line = line.replace("free=\"0\"", "free=\"1\"")
    outfile.write(line)

infile.close()
outfile.close()

# Prepare sourcefile with source removed 

os.system("cat "+modelFile_TSMap_withSource+" > "+modelFile_TSMap_resid)

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
if minROI < 0.25:
	os.system("sed -i '/%s/,/source>/d' %s" %(minName,modelFile_TSMap_resid))

# If it's greater, this is not the source, so just make a copy

def TSMapPartOne():
	my_apps.TsMap['statistic'] = "UNBINNED"
	my_apps.TsMap['scfile'] = spacecraftFile
	my_apps.TsMap['evfile'] = filteredLATFile_withDiffResps
	my_apps.TsMap['expmap'] = expMapFile
	my_apps.TsMap['expcube'] = ltCubeFile
	my_apps.TsMap['srcmdl'] = modelFile_TSMap_resid
	my_apps.TsMap['irfs'] = irfsType
	my_apps.TsMap['optimizer'] = optimizerType
	my_apps.TsMap['outfile'] = TSMapWithSource		# Yes, its the opposite. Yes, its right
	my_apps.TsMap['nxpix'] = 25
	my_apps.TsMap['nypix'] = 25
	my_apps.TsMap['binsz'] = 0.5
	my_apps.TsMap['coordsys'] = "CEL"
	my_apps.TsMap['xref'] = RA
	my_apps.TsMap['yref'] = DEC
	my_apps.TsMap['proj'] = 'STG'
	my_apps.TsMap.run()

def TSMapPartTwo():
	my_apps.TsMap['statistic'] = "UNBINNED"
	my_apps.TsMap['scfile'] = spacecraftFile
	my_apps.TsMap['evfile'] = filteredLATFile_withDiffResps
	my_apps.TsMap['expmap'] = expMapFile
	my_apps.TsMap['expcube'] = ltCubeFile
	my_apps.TsMap['srcmdl'] = modelFile_TSMap_withSource
	my_apps.TsMap['irfs'] = irfsType
	my_apps.TsMap['optimizer'] = optimizerType
	my_apps.TsMap['outfile'] = TSMapResid		# Yes, its the opposite. Yes, its right
	my_apps.TsMap['nxpix'] = 25
	my_apps.TsMap['nypix'] = 25
	my_apps.TsMap['binsz'] = 0.5
	my_apps.TsMap['coordsys'] = "CEL"
	my_apps.TsMap['xref'] = RA
	my_apps.TsMap['yref'] = DEC
	my_apps.TsMap['proj'] = 'STG'
	my_apps.TsMap.run()

# This is a work around to make both processes run at the same time. This takes ~ 3 hours!!

if createTSMaps and (not os.path.isfile(TSMapResid) or overWriteFiles):
	print colors.OKBLUE+"Creating TS Maps" +colors.ENDC
	from multiprocessing import Process

	p1 = Process(target=TSMapPartOne)
	p1.start()
	p2 = Process(target=TSMapPartTwo)
	p2.start()
	p1.join()
	p2.join()

	TSMapPartOne()
	import pyfits
	residHDU = pyfits.open(TSMapResid)
	sourceHDU = pyfits.open(TSMapWithSource)
	fig = plt.figure(figsize=(16,8))
	plt.imshow(residHDU[0].data)
	plt.colorbar()
	plt.savefig('results/TSMapsResid.eps',format='eps', bbox_inches='tight')

	fig = plt.figure(figsize=(16,8))
	plt.imshow(sourceHDU[0].data)
	plt.colorbar()
	plt.savefig('results/TSMapWithSource.eps',format='eps', bbox_inches='tight')

#############################################
############ Find Source Center #############
#############################################
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
	gtfindsrc['ftol']=like.tol
	gtfindsrc['atol']=0.001		# Default Value
	gtfindsrc.run()



