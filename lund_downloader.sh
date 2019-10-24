#!/bin/bash

# Downloads lund file from the specified location to the specified directory

lundOnlineLocation=$1
lundDestination=$2


mkdir -p $lundDestination
cd $lundDestination

echo
echo Downloading $lundDestination"..."
echo

