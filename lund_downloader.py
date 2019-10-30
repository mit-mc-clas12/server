""" 
Short utility script to call the function 
that downloads lund files from utils.lund_helper. 
"""

# System packages 
import os 
import sys 

# Third party 
import argparse

# Add local libraries for utils to the path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../utils')

from lund_helper import Lund_Entry as download


if __name__ == '__main__':

    ap = argparse.ArgumentParser() 
    ap.add_argument('-u', '--url', required=True, type=str) 
    ap.add_argument('-o', '--output_dir', required=True, type=str) 
    args = ap.parse_args()

    download(args.url, args.output_dir)
