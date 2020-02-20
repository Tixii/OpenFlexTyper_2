import sys
import argparse


def parse_arguments():
	"""Parses inputted arguments as described"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-V", "--VCF", help="Merged to Split Genotypes",required=True)
	args = parser.parse_args()
	return args

def StripMergedVCF2GT(infilename):
	"""
	Function to strip the VCF file down to genotypes in the form of, chrom_pos_ref_alt_GT
	Assumes ERR1955491_SProbe_FlexTyper	ERR1955491_SProbe_BamCoverage	ERR1955491_DeepVariant for the variant columns
	in cols[9],cols[10],cols[11]
	"""
	FlexGToutfile = open("ERR1955491_SProbe_FlexTyper_Genotypes.txt",'w')
	BamCovGToutfile = open("ERR1955491_SProbe_BamCoverage_Genotypes.txt",'w')
	DeepVariantGToutfile = open("ERR1955491_SProbe_DeepVariant_Genotypes.txt",'w')

	snps = []
	infile = open(infilename,'r')
	chrom_pos_snps = []
	for line in infile:
		if line[0]=='#':
			continue
		cols=line.strip('\n').split('\t')
		chrom=cols[0]
		pos=cols[1]
		ref=cols[3]
		alt=cols[4]

		GTflex=cols[9].split(':')[0]
		flexsite = '%s_%s_%s_%s_%s'%(chrom,pos,ref,alt,GTflex)
		FlexGToutfile.write("%s\n"%flexsite)

		GTbamcov=cols[10].split(':')[0]
		bamcovsite = '%s_%s_%s_%s_%s'%(chrom,pos,ref,alt,GTbamcov)
		BamCovGToutfile.write("%s\n"%bamcovsite)
		
		GTdeepvar=cols[11].split(':')[0]
		deepvarsite = '%s_%s_%s_%s_%s'%(chrom,pos,ref,alt,GTdeepvar)
		DeepVariantGToutfile.write("%s\n"%deepvarsite)

def main():
	args = parse_arguments()
	StripMergedVCF2GT(args.VCF)

if __name__ == "__main__":
	main()
