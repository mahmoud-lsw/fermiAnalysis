# N.B Before running, make sure:
#       - all photon files are in a folder called 'photon'
#       - the spacecraft file is named 'spacecraft.fits' and is in a folder called 'spacecraft'
#       You have these 5 files in a folder called model:
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
###### Adjustable paramaters #######
minE=100
maxE=300000
irfsType='CALDB'       # or 'P7REP_SOURCE_V15' ?
##### Naming stuff #####
file = open('filelist.list', 'r')
name_temp=file.readline()
file.close()
name_type= name_temp[9:12]                                                      # Usually LAT
name_energy=str(long(minE/1000))+'-'+str(int(maxE/1000))+'GeV'                   # i.e 100GeV

gtselectOutfile=name_type+'_allphotondata_'+name_energy+'.fits'
filteredLATFile = name_type+'_final_'+name_energy+'.fits'
expCubeFile=name_type+'_expCube_'+name_energy+'.fits'
expMapFile=name_type+'_expMap_'+name_energy+'_'+irfsType+'.fits'

modelFile=name_type+'_'+name_energy+'_model.xml'
########################

# Start analysis

# Make an exposure map
print filteredLATFile
my_apps.expMap['evfile'] = filteredLATFile
print spacecraftFile
my_apps.expMap['scfile'] =spacecraftFile
print expCubeFile
my_apps.expMap['expcube'] =expCubeFile
print expMapFile
my_apps.expMap['outfile'] =expMapFile
my_apps.expMap['irfs'] =irfsType
my_apps.expMap['srcrad'] =20
my_apps.expMap['nlong'] =120
my_apps.expMap['nlat'] =120
my_apps.expMap['nenergies'] =20
my_apps.expMap.run()



# Generate XML Model File
from make2FGLxml import *
mymodel = srcList('model/gll_psc_v08.fit',filteredLATFile,modelFile)
mymodel.makeModel('model/gll_iem_v05_rev1.fit', 'gll_iem_v05_rev1', 'model/iso_source_v05_rev1.txt', 'iso_source_v05_rev1')

# There should now be a modelFile with a name SIMILAR to LAT_modelFile.xml

# Run the Diffuse response (Only if you are NOT using CALDB)

# Each event must have a separate response precomputed for each diffuse component in the source model. The precomputed responses for Pass 7 (V6) data are for the gll_iem_v05, iso_source_v05.txt, and iso_clean_05.txt diffuse models.

if not irfsType=='CALDB':
	my_apps.diffResps['evfile']=filteredLATFile
	my_apps.diffResps['scfile']=spacecraftFile
	my_apps.diffResps['srcmdl']=modelFile
	my_apps.diffResps['irfs']=irfsType
	my_apps.diffResps.run()

# Run the Likelihood Analysis
import pyLikelihood
from UnbinnedAnalysis import *
obs = UnbinnedObs(filteredLATFile,spacecraftFile,expMap=expMapFile,expCube=ltCubeFile,irfs=irfsType)
like = UnbinnedAnalysis(obs,modelFile,optimizer='Minuit')

# Analysis Complete
print "################ Analysis Complete ################"
print obs
print like
print "###################################################"

# Some plots!

like.tol
like.tolType
like.tol = 0.0001
likeobj = pyLike.Minuit(like.logLike)
like.fit(verbosity=0,covar=True,optObject=likeobj)                 # Warning: This takes VERY long ~ 30 minutes

# Get all the TS values of the sources in the model
sourceDetails = {}
for source in like.sourceNames():
   sourceDetails[source] = like.Ts(source)

# Output for data
os.system('mkdir results')

# N.B A source with a TS value less than 0 should never happen unless the minimization failed. Remove that source and try fitting again and check the return code again.
print "Zero?: %d" %(likeobj.getRetCode()) # This value should be zero, refit using the method below if not

# Delete useing like.deleteSource('_2FGLJ1625.2-0020')

# Protip, you can really simplify the model by removing sources with TS levels below 9 (about 3 sigma)
for source,TS in sourceDetails.iteritems():
	print source, TS
	if (TS < 9.0):
		print "Deleting..."
		like.deleteSource(source)
# Refit
like.fit(verbosity=0,covar=True,optObject=likeobj)

print "Zero?: %d" %(likeobj.getRetCode()) 

sourceDetails = {}
for source in like.sourceNames():
   sourceDetails[source] = like.Ts(source)

printDictionaryToFile(sourceDetails)

# Make some plots!

import matplotlib.pyplot as plt
import numpy as np

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
for sourceName in like.sourceNames():
	fid.write(str(like.model[sourceName]))
	fid.write('Flux: '+str(like.flux(sourceName,emin=eMin))+'\n')
	fid.write('Flux Error: '+str(like.fluxError(sourceName,emin=eMin))+'\n')
	fid.write('TS: '+str(like.Ts(sourceName))+'\n')
	fid.write('Sigma: '+str(np.sqrt(like.Ts(sourceName)))+'\n')
	fid.write('\n=====================================\n')
fid.close()

# Save .xml
like.logLike.writeXml('results/'+name_type+'_results.xml')

