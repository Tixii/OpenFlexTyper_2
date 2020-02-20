# Cytoscan S Probe Comparison Across Methods

> Comparing the cytoscan probe genotypes for FlexTyper, BamCoverage, and DeepVariant

1. The data we are working with:
```
ERR1955491_SProbe_20190923_234544_k31_W10_centered.tsv
```
2. Convert this into VCF (Note: this file has bam coverage at cols[9,10], and FlexTyper at cols[12,13]). I adjusted the flextyper_formatter.py script for BamCoverage and FlexTyper accordingly
```
python OpenFlexTyper/fmformatter/flextyper_formatter.py -f VCF -i ERR1955491_SProbe_20190923_234544_k31_W10_centered.tsv -n ERR1955491_SProbe_BamCoverage
python OpenFlexTyper/fmformatter/flextyper_formatter.py -f VCF -i ERR1955491_SProbe_20190923_234544_k31_W10_centered.tsv -n ERR1955491_SProbe_FlexTyper
```

This produces files: 
```
ERR1955491_SProbe_BamCoverage.vcf
ERR1955491_SProbe_FlexTyper.vcf
```

I had to manually add the contigs here in order to get the VCFs into a sortable format. For those I just took the DeepVariant contig definitions
```
##contig=<ID=1,length=249250621>
##contig=<ID=2,length=243199373>
##contig=<ID=3,length=198022430>
##contig=<ID=4,length=191154276>
##contig=<ID=5,length=180915260>
##contig=<ID=6,length=171115067>
##contig=<ID=7,length=159138663>
##contig=<ID=8,length=146364022>
##contig=<ID=9,length=141213431>
##contig=<ID=10,length=135534747>
##contig=<ID=11,length=135006516>
##contig=<ID=12,length=133851895>
##contig=<ID=13,length=115169878>
##contig=<ID=14,length=107349540>
##contig=<ID=15,length=102531392>
##contig=<ID=16,length=90354753>
##contig=<ID=17,length=81195210>
##contig=<ID=18,length=78077248>
##contig=<ID=19,length=59128983>
##contig=<ID=20,length=63025520>
##contig=<ID=21,length=48129895>
##contig=<ID=22,length=51304566>
##contig=<ID=X,length=155270560>
##contig=<ID=Y,length=59373566>
##contig=<ID=MT,length=16569>
```


3. Next I convert these sites into vcf.gzs, and sort them, and index them.
```
bgzip ERR1955491_SProbe_BamCoverage.vcf 
bgzip ERR1955491_SProbe_FlexTyper.vcf
bcftools sort ERR1955491_SProbe_BamCoverage.vcf -O z -o ERR1955491_SProbe_BamCoverage.sorted.vcf.gz
bcftools sort ERR1955491_SProbe_FlexTyper.vcf -O z -o ERR1955491_SProbe_FlexTyper.sorted.vcf.gz
tabix ERR1955491_SProbe_BamCoverage.sorted.vcf.gz
tabix ERR1955491_SProbe_FlexTyper.sorted.vcf.gz
```

4. Then merge all 3 together, note the -0 option for sites missing from a sample, which will allow deepVariant easier comparison

```
bcftools merge -0 ERR1955491_SProbe_FlexTyper.sorted.vcf.gz ERR1955491_SProbe_BamCoverage.sorted.vcf.gz ERR1955491_DeepVariant0.8.noRefCalls.vcf.gz -o ERR1955491_SProbe_Merged.vcf
```

5. Then isolate lines with header, or those with rs ids (these will be the subset contained of those from the array)

```
grep -e \"^#\" -e \"rs\" ERR1955491_SProbe_Merged.vcf > ERR1955491_SProbe_Merged_ArrayOnly.vcf
```

6. Next I split-out genotypes from the merged VCF

```
python CompareVCFs.py -V ERR1955491_SProbe_Merged_ArrayOnly.vcf 
```

7. Then I run a comparison with intervene
```
intervene venn --save-overlaps --type list --names=FlexTyper,BamCoverage,DeepVariant --title GenotypeOverlaps -i ERR1955491_SProbe_FlexTyper_Genotypes.txt ERR1955491_SProbe_BamCoverage_Genotypes.txt ERR1955491_SProbe_DeepVariant_Genotypes.txt
```


