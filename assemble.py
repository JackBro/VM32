#!/usr/bin/env python

import sys
import argparse
import logging
import pickle

from assembler.Assembler import Assembler
from assembler.Exceptions import ParseError
from assembler.Exceptions import AssemblyError

def main(argc, argv):
	parser = argparse.ArgumentParser(description='VM32 Assembler')
	parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='Display debug information (DEBUG)')

	parser.add_argument('inputFile', nargs=1, type=argparse.FileType('r'), help='The input file to assemble')
	parser.add_argument('-o', '--output', action='store', nargs=1, dest='outFileName', help='Output filename', metavar="outFileName", required=False)

	arguments = parser.parse_args(argv[1:])
	
	#enable logging
	if arguments.debug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger('Assembler Frontend')

	#create and truncate output file
	try:
		inputFile = arguments.inputFile[0]

		if arguments.outFileName != None:
			outputFile = open(arguments.outFileName[0], 'w+')
		else:
			outputFile = open('out.obj', 'w+')
		logger.debug("Writing to file %s", outputFile.name)

		#create assembler
		asm = Assembler()

		#assemble the file
		assembled = asm.assemble(inputFile.read())

		#serialize the assembled file and save it
		pickle.dump(assembled, outputFile)

		#cleanup
		outputFile.close()

	except IOError, e:
		logger.error(e)
		sys.exit(-1)
	except ParseError, e:
		logger.error(e)
		sys.exit(-1)
	except AssemblyError, e:
		logger.error(e)
		sys.exit(-1)
	#except Exception, e:
	#	logger.error(e)
	#	sys.exit(-1)


if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
