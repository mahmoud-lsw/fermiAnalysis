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

RA= 0
DEC=0

eMin=1000
eMax=300000
tMax='INDEF'
roi=180
irfsType='P7REP_SOURCE_V15'       # or 'P7REP_SOURCE_V15' ?

# For binning


###############################################

##### Naming stuff #####
file = open('filelist.list', 'r')
name_temp=file.readline()
file.close()
name_type= name_temp[9:12]                                                      # Usually LAT
name_energy=str(int(eMin/1000))+'-'+str(int(eMax/1000))+'GeV'                   # i.e 100GeV

gtselectOutfile=name_type+'_allphotondata_'+name_energy+'.fits'
filteredLATFile = name_type+'_final_'+name_energy+'.fits'
ltCubeFile=name_type+'_ltCube_'+name_energy+'.fits'
expMapFile=name_type+'_expMap_'+name_energy+'_'+irfsType+'.fits'

modelFile=name_type+'_'+name_energy+'_model.xml'

# For binning
gtbinnedFile = name_type+'_binned3600_'+name_energy+'.fits'
expCubeFile=name_type+'_expCube_'+name_energy+'_'+irfsType+'.fits'
farithOutfile = name_type+'_farith_'+name_energy+'_'+irfsType+'.fits'
fimgtrimOutfile = name_type+'_fimgtrim_'+name_energy+'_'+irfsType+'.fits'
fcarithOutfile = name_type+'_corrmap_'+name_energy+'_'+irfsType+'.fits'

###############################################

# Quick check to see if any files already exist
normalFiles_temp=[gtselectOutfile,filteredLATFile,ltCubeFile,expMapFile,modelFile]
binningFiles_temp=[gtbinnedFile,expCubeFile,farithOutfile,fimgtrimOutfile,fcarithOutfile]

normalFiles=[]
binningFiles=[]
for x in normalFiles_temp:
	if os.path.isfile(x):
		normalFiles.append(x)

for y in binningFiles_temp:
	if os.path.isfile(y):
		binningFiles.append(y)

if len(normalFiles)>0 or len(binningFiles)>0:
	print "WARNING: THESE FILES EXIST:"
	if len(normalFiles)>0:
		print '############# Normal Files #############'
		for x in normalFiles:
			print x
	if len(binningFiles)>0:
		print '############# Binning Files #############'
		for x in binningFiles:
			print x
	print 'MAKE SURE YOU ARE USING THE RIGHT ONES/NOT OVERWRITING ANYTHING IMPORTANT!'

	doIContinue = raw_input('Do you want to continue? (y/n):')

	if doIContinue=='n' or doIContinue=='N':
		print 'Exiting'
		exit 1
###############################################


def printDictionaryToFile(dictionary):
	fid=open('TSValues.txt','w')
	for source,TS in dictionary.iteritems():
		fid.write("%s : %f\n" %(source,TS))
	fid.close()
	os.system('mv TSValues.txt data')

# Start analysis

#Run gtselect
if not os.path.isfile(gtselectOutfile)
	my_apps.filter['evclass'] = evClass
	my_apps.filter['ra'] = RA
	my_apps.filter['dec'] = DEC
	my_apps.filter['rad'] = roi
	my_apps.filter['emin'] = eMin
	my_apps.filter['emax'] = eMax
	my_apps.filter['zmax'] = 100
	my_apps.filter['tmin'] = 'INDEF' 	# This is the earliest Fermi MET
	my_apps.filter['tmax'] = tMax
	my_apps.filter['infile'] = '@filelist.list'
	my_apps.filter['outfile'] = gtselectOutfile
	my_apps.filter.run()

#Run gtmktime
if not os.path.isfile(filteredLATFile)
	my_apps.maketime['scfile'] = spacecraftFile
	my_apps.maketime['filter'] = '(DATA_QUAL>0)&&(LAT_CONFIG==1)'
	my_apps.maketime['roicut'] = 'no'
	my_apps.maketime['evfile'] = gtselectOutfile
	my_apps.maketime['outfile'] = filteredLATFile
	my_apps.maketime.run()

# Make livetime cube
if not os.path.isfile(ltCubeFile)
	my_apps.expCube['evfile'] = filteredLATFile
	my_apps.expCube['scfile'] = spacecraftFile
	my_apps.expCube['outfile'] = ltCubeFile
	my_apps.expCube['zmax'] = 100
	my_apps.expCube['dcostheta'] = 0.025
	my_apps.expCube['binsz'] = 1
	my_apps.expCube.run()

# Create binned map
my_apps.evtbin['algorithm'] = 'CCUBE'
my_apps.evtbin['evfile'] = filteredLATFile
my_apps.evtbin['outfile'] = gtbinnedFile
my_apps.evtbin['scfile'] = spacecraftFile
my_apps.evtbin['nxpix'] = 3600
my_apps.evtbin['nypix'] = 1800
my_apps.evtbin['binsz'] = 0.1
my_apps.evtbin['coordsys'] = 'GAL'
my_apps.evtbin['xref'] = 0
my_apps.evtbin['yref'] = 0
my_apps.evtbin['axisrot'] = 0.0
my_apps.evtbin['proj'] = 'AIT'

# Make an exposure cube

from GtApp import GtApp
expCube2 = GtApp('gtexpcube','Likelihood')

expCube2['expcube'] =ltCubeFile
expCube2['evfile'] = filteredLATFile
expCube2['cmfile'] ='NONE'
expCube2['outfile']= expCubeFile
expCube2['irfs']=irfsType
expCube2['nxpix']=3600
expCube2['nypix']=1800
expCube2['pixscale']=0.1
expCube2['coordsys']='GAL'
expCube2['xref']=0
expCube2['yref']=0
expCube2['axisrot']=0
expCube2['proj']='AIT'
expCube2['emin']=1000
expCube2['emax']=300000
expCube2['enumbins']=1
expCube2['bincalc']='CENTER'
# Correct the all-sky image for exposure and scale. Three steps

# Correct the value of each pixel for the exposure
os.system('farith infil1= %s infil2=%s ops=DIV outfil=%s' %(gtbinnedFile,expCubeFile,farithOutfile))

# Trim the pixels that were outside the Aitoff projection.
os.system('fimgtrim infile= %s threshlo=0 const_lo=0 threshup=INDEF outfile=%s' %(farithOutfile,fimgtrimOutfile))	

# Scale the image so that the maximum pixel is equal to 255
os.system('fcarith infile= %s const=6.155e9 ops=MUL outfil=%s' %(fimgtrimOutfile,fcarithOutfile))

