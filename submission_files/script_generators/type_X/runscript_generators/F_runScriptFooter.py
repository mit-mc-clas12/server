# Job finish up:
# Logs statistic, each prepended by "====" for better retrieval later

def F_runScriptFooter(scard,**kwargs):

	strn = """
#!/bin/csh

# Run Script Footer
# -----------------

set endDate = `date`

echo ==== SubMit-Job === Job Start: $startDate
echo ==== SubMit-Job === Generator Start: $generatorDate
echo ==== SubMit-Job === GEMC Start: $gemcDate
echo ==== SubMit-Job === evio2hipoDate Start: $evio2hipoDate
echo ==== SubMit-Job === Reconstruction Start: $reconstructionDate
echo ==== SubMit-Job === Job End: $endDate

# End of Run Script Footer
# ------------------------

"""

	return strn
