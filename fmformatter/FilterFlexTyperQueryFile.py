import sys
import argparse
import pybedtools
import os


def parse_arguments():
	"""Parses inputted arguments as described"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-i', '--Input', help='input tsv ', type=str, required=True)
	parser.add_argument(
		'-o', '--Output', help='output tsv', type=str, required=True)
	parser.add_argument(
		'-f', '--Fasta', help='Fasta file corresponding to query file', type=str, required=True)
	args = parser.parse_args()
	return args

def ParseQueryFile(infilename, outfilename, fasta):
	"""
	This function scans through the query file and checks the ref base to the genome ref base

	if they match, it writes to the outfile
	"""
	infile = open(infilename,'r')
	outfile = open(outfilename,'w')
	for line in infile:
		if line[0]=='#':
			continue
		cols = line.strip('\n').split('\t')
		chrom = cols[3]
		start = int(cols[4]) -1
		end = int(cols[4])  # fixed for 0-based FlexTyper query file format
		ref = cols[5]
		alt = cols[6]
		if CheckBase(ref, chrom, start, end, fasta):
			outfile.write(line)
		else:
			print("This line had an issue")
			print(line)
		
def CheckBase(ref, chrom, start, end, fasta):
	""" 
	This function checks the ref base provided in the ref genome fasta.
	"""
	refSeq = pybedtools.BedTool.seq((chrom,start,end),fasta)
	#print(refSeq)
	#print(ref)
	if ref == refSeq:
		return True
	else:
		return False


def main():
	args = parse_arguments()
	Input = args.Input
	Output = args.Output
	Fasta = args.Fasta
	ParseQueryFile(Input, Output, Fasta)

if __name__ == "__main__":
	main()
