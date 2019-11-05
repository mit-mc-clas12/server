# Job finish up:
# Logs statistic, each prepended by "====" for better retrieval later

def F_runScriptFooter(scard,**kwargs):

        # Try getting these options from the scard, if they don't 
        # exist, return the default value (yes).
        generator_out = scard.data.get('generatorOUT', 'yes')
        gemc_evio_out = scard.data.get('gemcEvioOUT', 'yes')
        gemc_hipo_out = scard.data.get('gemcHipoOUT', 'yes')
        reconstruction_out = scard.data.get('reconstructionOUT', 'yes')
        dst_out = scard.data.get('dstOUT', 'yes')

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
