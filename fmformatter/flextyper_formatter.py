import sys
import argparse
import os
import statistics


def parse_arguments():
	"""Parses inputted arguments as described"""
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-0', '--ZeroBased', help="Set this option if the query file is 0 based", action='store_true')
	parser.add_argument(
		'-f', '--Format', help="format of output", type=str, required=True,
		choices=["VCF", "23_and_me", "ancestry"])
	parser.add_argument(
		'-i', '--Input', help='input tsv ', type=str, required=True)
	parser.add_argument('-n', '--name',
						help='name of save file', required=True)
	parser.add_argument("-m", "--minSuppReads", help="Minimum supporting reads for a genotype call", default=1, type=int)
	args = parser.parse_args()
	return args

def flextyper_2_vcf(infilename, name, minSuppReads, zerobased):
	"""
	This function creates a VCF from output query file.

	It determines genotypes as follows:
		het site: alt>minSuppReads and ref>minSuppReads
		homo alt: alt>minSuppReads and ref<minSuppReads
		homo ref: alt<minSuppReads and ref>minSuppReads
	"""
	
	infile = open(infilename,'r')
	outfile = open("%s.vcf"%name,'w')
	# write the header
	outfile.write("##fileformat=VCFv4.2\n")	
	outfile.write("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n")
	outfile.write("##FORMAT=<ID=AO,Number=A,Type=Integer,Description=\"Alternate allele observation count\">\n")
	outfile.write("##FORMAT=<ID=RO,Number=1,Type=Integer,Description=\"Reference allele observation count\">\n")
	outfile.write("##FORMAT=<ID=DP,Number=1,Type=Integer,Description=\"Read depth\">\n")
	outfile.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s\n"%name)
	for line in infile:
		if line[0]=='#':
			continue
		cols = line.strip('\n').split('\t')
		chrom = cols[3]
		pos = int(cols[4]) 
		if zerobased:
			pos+=1  # fixed for 0-based FlexTyper query file format
		ref = cols[5]
		alt = cols[6]
		ID = cols[7]
		ref_count = int(cols[9])
		alt_count = int(cols[10])
		depth = ref_count + alt_count
		if alt_count >= minSuppReads:
			if ref_count >= minSuppReads:
				zygosity = '0/1'
			elif ref_count < minSuppReads:
				zygosity = '1/1'
		else:
			zygosity = '0/0'
		outfile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s:%d:%d:%d\n"%(chrom,pos,ID,ref,alt,'.','.','.','GT:RO:AO:DP',zygosity,ref_count,alt_count,depth))
		

def flextyper_2_array(data, name, format, zerobased):
	if format == "23_and_me":
		new = open(name+"23_and_me.txt", "w+")
		new.write("#rsid\tchromosome\tposition\tgenotype")
	if format == "ancestry":
		new = open(name+"ancestry.txt", "w+")
		new.write("#rsID\tChromosome\tPosition\tAllele 1\tAllele 2\n")
	with open(data) as f:
		for line in f:
			if not line.startswith("#"):
				ln = line.split("\t")
				ln[-1] = ln[-1].rstrip()
				chrom = ln[3]
				if zerobased:
					pos = str(int(ln[4]) + 1)  # making 1 based
				else:
					pos = str(int(ln[4]))
				ID = ln[7]
				ref = ln[5]
				alt = ln[6]
				ref_count = int(ln[9])
				alt_count = int(ln[10])
				if alt_count > 0 or ref_count > 0:
					if alt_count > 0 and ref_count == 0:  # homozygous alt
						allele1 = alt
						allele2 = alt
					elif alt_count == 0 and ref_count > 0:  # homozygous ref
						allele1 = ref
						allele2 = ref
					elif alt_count > 0 and ref_count > 0:  # het
						allele1 = ref
						allele2 = alt
					if format == "23_and_me":
						output = "\t".join([ID, chrom, pos, allele1+allele2])
					if format == "ancestry":
						output = "\t".join([ID, chrom, pos, allele1, allele2])
					new.write(output + "\n")
	new.close()


def main():
	args = parse_arguments()
	Format = args.Format
	Input = args.Input
	minSuppReads = args.minSuppReads
	name = args.name
	Zerobased = args.ZeroBased

	if Format == "VCF":
		flextyper_2_vcf(Input, name, minSuppReads,Zerobased)
	if Format == "23_and_me":
		flextyper_2_array(Input, name, "23_and_me", Zerobased)
	if Format == "ancestry":
		flextyper_2_array(Input, name, "ancestry", Zerobased)


if __name__ == "__main__":
	main()
