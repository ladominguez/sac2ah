#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from obspy.core import read
from obspy.core.inventory import read_inventory

instrument_response='/Users/antonio/Dropbox/espectrosGolfo/InstrumentResponse'
type = {5:'Unknown',6:'Disp (nm)', 7:'Vel (nm/s)', 8:'Acc (nm/s/s)'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input file (sac).')
    parser.add_argument('-o', '--output', type=str, help='output file (sac).')
    parser.add_argument('-r', '--response', type=str, default=instrument_response, help='output file (sac).')
    args = parser.parse_args()
    input = args.input
    output = args.output
    resp_file = args.response	
    sac = read(input)
    stnm =sac[0].stats.sac.kstnm.strip() 
    if os.path.isfile(resp_file):
        inv = read_inventory(resp_file, format='RESP')
    elif os.path.isdir(resp_file):
        inv = read_inventory(resp_file + '/*' + stnm + '*', format='RESP')
    response=inv.get_response(sac[0].get_id(),sac[0].stats.starttime)
    paz=response.get_paz()
    normalization_factor=paz.normalization_factor
    gain=response.instrument_sensitivity.value
    poles=paz.poles
    zeros=paz.zeros
    try:
        idep=sac[0].stats.sac.idep
    except:
        idep=5
    with open(output, 'w') as fout:
        fout.write('station information\n')
        fout.write('code:\t' + sac[0].stats.sac.kstnm.strip() + '\n')
        fout.write('channel:\t' + sac[0].stats.sac.kcmpnm.strip() + '\n')
        fout.write('type:\tmex\n')
        fout.write('latitude:\t'+str(sac[0].stats.sac.stla)+'\n')
        fout.write('longitude:\t'+str(sac[0].stats.sac.stlo)+'\n')
        fout.write('elevation:\t'+str(sac[0].stats.sac.stel)+'\n')
        fout.write('gain:\t'+str(gain)+'\n')
        fout.write('normaliztion:\t'+'%.2f'%normalization_factor+'\n')
        fout.write('calibration information\n')
        fout.write('pole.re		pole.im		zero.re		zero.im \n')
        fout.write('%8.6e' % len(poles)+'\t'+'0.000000e+00'+'\t'+'%8.6e' % len(zeros)+'\t'+'0.000000e+00\n')
        for k in range(0, 29):
            try:
                pole=poles[k]
                pole_real=pole.real
                pole_imag=pole.imag
            except:
                pole_real=0
                pole_imag=0

            try:
                zero=zeros[k]
                zero_real=zero.real
                zero_imag=zero.imag
            except:
                zero_real=0
                zero_imag=0
            
            fout.write('%8.6e' % pole_real+'\t'+'%8.6e'%pole_imag+'\t'+'%8.6e' % zero_real+'\t'+'%8.6e'%zero_imag+'\n')
        fout.write('event information\n')
        fout.write('latitude:\t'+str(sac[0].stats.sac.evla)+'\n')
        fout.write('longitude:\t'+str(sac[0].stats.sac.evlo)+'\n')
        fout.write('depth:\t'+str(sac[0].stats.sac.evdp)+'\n')
        fout.write('origin_time:    0   0   0   0   0   0.000000\n')
        fout.write('comment:    null\n')
        fout.write('record information\n')
        fout.write('type:   1\n')
        fout.write('ndata:\t'+str(sac[0].stats.npts)+'\n')
        fout.write('delta:\t'+str(sac[0].stats.delta)+'\n')
        fout.write('max_amplitude:\t' + '%8.6e' % sac[0].stats.sac.depmax+'\n')
        fout.write('start_time: '+str(sac[0].stats.starttime.year)+'\t'+str(sac[0].stats.starttime.month)+'\t'+str(sac[0].stats.starttime.day)+'\t'+str(
            sac[0].stats.starttime.hour)+'\t'+str(sac[0].stats.starttime.minute)+'\t'+'%8.6f' % sac[0].stats.starttime.second+'\n')
        fout.write('abscissa_min:\t0.000000e+00\n')
        fout.write('comment:\tComp azm=%4.1f,inc=%4.1f; ' %(sac[0].stats.sac.cmpaz,sac[0].stats.sac.cmpinc) + type[idep] +'\n')
        fout.write('log:\tnull\n')
        fout.write('extras:\n')
        for k in range(21):
            fout.write(str(k) + ':\t0.000000e+00\n')
        fout.write('data:\n')
        for data in sac[0].data:
            fout.write('%8.6e\n'%data)

    fout.close()

    # sac=read(input)
    # sac.write(output,format='AH')
