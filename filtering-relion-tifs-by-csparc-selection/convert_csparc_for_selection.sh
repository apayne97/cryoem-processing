#!/bin/bash
particle_cs=$1
passthrough_cs=$2

## this is really the only necessary line, and even this could be simpler
csparc2star.py --swapxy --inverty $(ls $particle_cs | sort -r --version-sort | head -1) $2 pre.star

awk '{if(NF<10){print}}' pre.star > post.star

awk '$12 *= -1' pre.star >> post.star

awk '{if(NF>10){print}}' post.star > no_header.star
awk '{print $2}' no_header.star | sort -u > micrographs_only.txt

