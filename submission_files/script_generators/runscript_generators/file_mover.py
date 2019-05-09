#****************************************************************
"""
# Commentary for this file does not yet exist
"""
#****************************************************************

def file_mover(scard,**kwargs):
  strn = """ls -l \n
echo Moving file
echo $ClusterId
mv out.ev out.$ProcId.ev
mv gemc.hipo gemc.$ProcId.hipo
mv {0} {0}.$ProcId
echo File moved
echo `basename {0}.$ProcId`
echo `basename out.$ProcId.ev`
echo `basename gemc.$ProcId.hipo`
echo `basename out_gemc.$ProcId.hipo` \n \n
echo creating directory

mkdir out_`basename $ClusterId`_n{1}
echo moving file
mv {0}.$ProcId out_`basename $ClusterId`_n{1}
mv out.$ProcId.ev out_`basename $ClusterId`_n{1}
mv gemc.$ProcId.hipo out_`basename $ClusterId`_n{1}
mv out_gemc.hipo out_gemc.$ProcId.hipo
mv out_gemc.$ProcId.hipo out_`basename $ClusterId`_n{1}

echo copying gcard and scard
cp {2} out_`basename $ClusterId`_n{1}
cp {3} out_`basename $ClusterId`_n{1}

#final job log
printf "Job finished time: "; /bin/date

echo "script started at" $script_start
echo "generator started at" $generator_start
echo "gemc started at" $gemc_start
echo "evio2hipo started at" $evio2hipo_start
echo "notsouseful started at" $notsouseful_start""".format(scard.data['genOutput'],scard.data['nevents'],scard.data['gcards'],'scard_name')
  return strn
