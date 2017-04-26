#!/usr/bin/env python
# encoding: utf-8
'''
convertFromRoot -- converts the root files produced with the deepJet ntupler to the data format used by keras for the DNN training

convertFromRoot is a small program that converts the root files produced with the deepJet ntupler to the data format used by keras for the DNN training


@author:     jkiesele

'''

import sys
import os

from argparse import ArgumentParser
from pdb import set_trace
import logging
logging.getLogger().setLevel(logging.INFO)

__all__ = []
__version__ = 0.1
__date__ = '2017-02-22'
__updated__ = '2017-02-22'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = ''' ''' # optional - give further explanation about what the program does
    program_license = "Copyright 2017 user_name (organization_name) Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    
    #try:
        # setup option parser

    parser = ArgumentParser('program to convert root tuples to traindata format')
    parser.add_argument("-i", help="set input sample description (output from the check.py script)", metavar="FILE")
    parser.add_argument("-o",  help="set output path", metavar="PATH")
    parser.add_argument("-c",  help="set output class [TrainData_deepCSV, TrainData_deepCMVA_ST, TrainData_deepCSV_ST, TrainData_veryDeepJet]", metavar="Class")
    parser.add_argument("-r",  help="set path to snapshot that got interrupted", metavar="FILE", default='')
    parser.add_argument("--testdatafor", default='')
    parser.add_argument("--usemeansfrom", default='')
    parser.add_argument("--nothreads", action='store_true')
    parser.add_argument("-v", action='store_true', help='verbose')
    parser.add_argument("-q", action='store_true', help='quiet')
    
    # process options
    args=parser.parse_args()
    infile=args.i
    outPath=args.o
    Class=args.c
    Recover=args.r
    testdatafor=args.testdatafor
    usemeansfrom=args.usemeansfrom

    if args.v:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.q:
        logging.getLogger().setLevel(logging.WARNING)

    if infile:
        logging.info("infile = %s" % infile)
    if outPath:
        logging.info("outPath = %s" % outPath)

    # MAIN BODY #
    
    
    
    from DataCollection import DataCollection
    
    from TrainData import TrainData
    from TrainData_deepCSV import TrainData_deepCSV
    from TrainData_deepConvCSV import TrainData_deepConvCSV
    from TrainData_deepCMVA import TrainData_deepCMVA
    from TrainData_deepCSV_PF import TrainData_deepCSV_PF,TrainData_deepCSV_miniPF,TrainData_deepCSV_microPF,TrainData_deepCSV_softL_PF
    from TrainData_deepConvCSV import TrainData_deepConvCSV
    from TrainData_deepCSV_PF_Reg import TrainData_deepCSV_PF_Reg
    from TrainData_deepJet_Reg import TrainData_deepJet_Reg, TrainData_PF_Reg
    from TrainData_deepCSV_PF_binned import TrainData_deepCSV_PF_Binned
    dc = DataCollection(1 if args.nothreads else -1)
    
    
    traind=TrainData
    if Class == 'TrainData_deepCSV':
        traind=TrainData_deepCSV

    if Class == 'TrainData_PF_Reg':
        traind=TrainData_PF_Reg
    elif Class == 'TrainData_deepConvCSV':
        traind=TrainData_deepConvCSV
    elif Class == 'TrainData_deepJet_Reg':
        traind=TrainData_deepJet_Reg
    elif Class ==  'TrainData_deepCSV_PF':
        traind=TrainData_deepCSV_PF
    elif Class ==  'TrainData_deepCSV_PF_Reg':
        traind=TrainData_deepCSV_PF_Reg
    elif Class ==  'TrainData_deepCSV_softL_PF':
        traind=TrainData_deepCSV_softL_PF
    elif Class ==  'TrainData_deepConvCSV':
        traind=TrainData_deepConvCSV
    elif Class ==  'TrainData_deepCSV_miniPF':
        traind=TrainData_deepCSV_miniPF
    elif Class ==  'TrainData_deepCSV_microPF':
        traind=TrainData_deepCSV_microPF
    elif Class == 'TrainData_deepCMVA':
        traind=TrainData_deepCMVA
    elif Class == 'TrainData_deepCSV_PF_Binned':
        traind=TrainData_deepCSV_PF_Binned
    elif len(Recover)<1 and len(testdatafor)<1:
        raise Exception('wrong class selecton')
    
    
    
    if len(testdatafor):
        logging.info('converting test data, no weights applied')
        dc.createTestDataForDataCollection(testdatafor,infile,outPath)
    
    elif len(Recover)>0:
        dc.recoverCreateDataFromRootFromSnapshot(Recover)
        
    else:
        notdone=True
        while notdone:
            
            # testdata for.. and then pass DataCollection (for means and norms)
            
            dc.convertListOfRootFiles(infile, traind(), outPath,usemeansfrom)
            notdone=False
            #except Exception as e:
            #    print('for recovering run: convertFromRoot.py -r '+outPath+'/snapshot.dc')
            #    raise e
   

    


#if __name__ == "__main__":
if DEBUG:
    sys.argv.append("-h")
if TESTRUN:
    import doctest
    doctest.testmod()
if PROFILE:
    import cProfile
    import pstats
    profile_filename = 'convertFromRoot_profile.txt'
    cProfile.run('main()', profile_filename)
    statsfile = open("profile_stats.txt", "wb")
    p = pstats.Stats(profile_filename, stream=statsfile)
    stats = p.strip_dirs().sort_stats('cumulative')
    stats.print_stats()
    statsfile.close()
    sys.exit(0)
sys.exit(main())
