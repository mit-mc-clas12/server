# Job finish up:
# Log statistic

def runScriptFooter(scard,**kwargs):

	footerSTR = """
#!/bin/csh

# Run Script Footer
# -----------------

echo ==== SubMit-Job === Start: $startDate

# End of Run Script Footer
# ------------------------

"""

	return footerSTR
