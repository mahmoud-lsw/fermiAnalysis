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
	my_apps.TsMap['outfile'] = TSMapResid
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
	my_apps.TsMap['outfile'] = TSMapWithSource
	my_apps.TsMap['nxpix'] = 25
	my_apps.TsMap['nypix'] = 25
	my_apps.TsMap['binsz'] = 0.5
	my_apps.TsMap['coordsys'] = "CEL"
	my_apps.TsMap['xref'] = RA
	my_apps.TsMap['yref'] = DEC
	my_apps.TsMap['proj'] = 'STG'
	my_apps.TsMap.run()

# This is a work around to make both processes run at the same time. This takes ~ 3 hours!!
TSMapPartOne
if createTSMaps and (not os.path.isfile(TSMapResid) or overWriteFiles):
	print colors.OKBLUE+"Creating TS Maps" +colors.ENDC
	from multiprocessing import Process

	p1 = Process(target=TSMapPartOne)
	p1.start()
	p2 = Process(target=TSMapPartTwo)
	p2.start()
	p1.join()
	p2.join()

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



