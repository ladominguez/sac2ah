#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from obspy import read, write

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', type=str, help='input file (sac).')
    parser.add_argument('-o','--output', type=str, help='output file (sac).')
    args = parser.parse_args()
    input=args.input
    output=args.output

    sac=read(input)
    sac.write(output,format='AH')
