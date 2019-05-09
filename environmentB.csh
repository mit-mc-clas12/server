#!/bin/csh

setenv JLAB_ROOT    /jlab
setenv JLAB_VERSION 2.3
setenv CLAS12TAG    4.3.0
setenv JRE          jre1.8.0_191

# sidis, inclusive dis with rad correction, dvcs
setenv CLASDIS_PDF  /jlab/work/clasdis-nocernlib/pdf
setenv DISRAD_PDF   /jlab/work/inclusive-dis-rad
setenv CLASDVCS_PDF /jlab/work/dvcsgen

setenv GEMC /jlab/clas12Tags/$CLAS12TAG/source
setenv GEMC_VERSION $CLAS12TAG

source $JLAB_ROOT/$JLAB_VERSION/ce/jlab.csh keepmine
setenv GEMC_DATA_DIR /jlab/clas12Tags/$CLAS12TAG
setenv FIELD_DIR /jlab/noarch/data

# CLAS12 Reconstruction
setenv CLAS12_LIB $JLAB_SOFTWARE/clas12/lib
setenv CLAS12_INC $JLAB_SOFTWARE/clas12/inc
setenv CLAS12_BIN $JLAB_SOFTWARE/clas12/bin

setenv GEOMDBVAR  may_2018_engineers
setenv COATJAVA  $JLAB_SOFTWARE/clas12/coatjava
setenv JAVA_HOME $JLAB_SOFTWARE/$JRE

setenv PATH ${PATH}:${JAVA_HOME}/bin:${CLAS12_BIN}:${COATJAVA}/bin

set autolist
alias l ls -l
alias lt ls -lt
