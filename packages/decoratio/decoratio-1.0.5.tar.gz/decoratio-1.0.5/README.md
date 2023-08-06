
NAME
==========

**decoratio** — estimate the DEpth-COmplexity RATIO and amplification noisiness
of a sequencing experiment based on the PCR clone size histogram.

INSTALLATION
==========

```sh
python3 -m pip decoratio
```

Decoratio depends on `numpy`, `scipy`, and `matplotlib`.

SYNOPSIS
==========

```sh
python3 -m decoratio [--model=MODEL] [...] CLONE_SIZE_HISTOGRAM.tsv
```

AUTHORS & CITATION
==========

Nicolas C. Rochette, Angel G. Rivera-Colón, Julian M. Catchen

If you use Decoratio, please cite:

Rochette NC, Rivera-Colón AG, Walsh J, Sanger TJ, Campbell-Staton SC, Catchen JM
(2022). On the causes, consequences, and avoidance of PCR duplicates: towards a
theory of library complexity. bioRxiv. https://doi.org/10.1101/2022.10.10.511638

DESCRIPTION
==========

PCR duplicates become prevalent in sequencing experiments when the sequencing
effort exceeds the number of molecules the library was originally prepared from.
The precise duplicates rate that is observed depends primarily on the ratio
between the sequencing depth and the complexity of the library, as well as
secondarily on the variance of the amplification factor among the original
template molecules the library.

This program leverages PCR duplicate patterns (namely, the relative occurrence
of duplication clones of various sizes) in a sequencing dataset to jointly
estimate (1) the depth-complexity ratio, and (2) a variance model for the PCR
amplification of the library. As the sequencing depth should be known to the
experimenter, the depth-complexity ratio is a library complexity estimate. This,
together with the amplification variance model, informs on the quality of the
library, allowing to identify failed libraries and/or to compare the performance
of a set of library preparation protocols.

Input TSV histogram
----------

The main input for the program is a TSV table giving the number of duplication
clones of each size that were observed. A duplication clone is a set of
individual reads that are all descend from the same template, and are PCR
duplicates of one another. Thus, clones of size 1 correspond to singleton reads
that do not have duplicates; clones of size 2 to pairs of duplicate reads;
clones of size 3 to read triplets; etc.

The input file should look like this:

```txt
clone_size  n_clones
1           9746142
2           7320751
3           4969106
4           3023127
5           1693158
6            893344
7            456659
...
# (Empty size classes may be omitted.)
```

For instructions on how to obtain this histogram from sequencing data (e.g., BAM
alignment files), see the EXAMPLES section below.

Options
----------

`--model`
: an amplification model specifier such as "logskewnormal" (default),
"lognormal", or "inheffbeta:12"; see AMPLIFICATION MODELS below

`--output-prefix`
: defaults to `CLONE_SIZE_HISTOGRAM.tsv.decoratio.*`

`--ratio-min`, `--ratio-max`
: constrains the optimization range for the depth-complexity ratio

`--no-plots`, `--tsv-out`, `--log-level`
: miscelaneous output control

Amplification models
----------

Default settings should work well in most cases.

Three models are currently implemented for the amplification: log-skew-normal
(`logskewnormal`, default), log-normal (`lognormal`), and the empirical
inherited efficiency model (`inheff` and `inheffbeta` for the original and beta
distribution-based versions respectively). All models may be specified without
parameters, in which case their parameters will be jointly optimized with the
depth-complexity ratio, or with user-specified parameters, in which case only
the depth-complexity ratio will be optimized.

#### Log-skew-normal and log-normal models

The PCR duplicate rate is only sensitive to the variance in relative
amplification factors, and not to the mean amplification factor. As a result,
the log-normal model has only one parameter (a standard deviation) and
log-skew-normal two (a standard deviation and a skew). Thus, for these models
the possible values take the form:

```txt
--model=lognormal
--model=lognormal:0.54
--model=logskewnormal
--model=logskewnormal:0.72:-3.4
```

All numerical values are given in units of the natural logarithm (this is
important as e.g., an amplification factor log-distribution with a standard
deviation of 0.54 in base *e* has a standard deviation of 0.78 in base 2).

#### Inherited efficiency models

This is the empirical model of (Best et al., 2015). We provide two closely
related versions, the normal distribution-based model and a stabilized model
based on the beta distribution, which we recommend.

A number of PCR cycles (e.g., 12) must always be provided. The models then
depend on two additional parameters, the mean efficiency of the PCR process and
its standard deviation across clones. Thus, possible values take the form:

```txt
--model=inheff:12
--model=inheffbeta:12
--model=inheffbeta:12:0.76:0.14
```

Computations based on this model are substantially slower. The default is to
perform binned simulations, as this is more computationally efficient, and the
default effort is to perform 1000 simulations for each of 1000
efficiency bins. This should work well, but can be changed with
`--inheff-n-efficiency-bins` and `--inheff-n-sims-per-bin`. Binning during
simulations can be deactivated with `--inheff-legacy-sims`. If optimizing the
parameters, the default is to optimize in a one-dimentional space, but
`--inheff-uncouple-beta-parameters` will cause the two parameters to be
optimized independently (for the beta distribution version only). This may
impact the precise shape of the amplification factor distribution.

EXAMPLES
==========

```sh
curl -O https://bitbucket.org/rochette/decoratio/raw/HEAD/examples/brown_alone.clone_sizes.tsv
# Using the default logskewnormal amplification model:
python3 -m decoratio ./brown_alone.clone_sizes.tsv
# Using the lognormal amplification model (this is faster):
python3 -m decoratio --model=lognormal ./brown_alone.clone_sizes.tsv
# Using a user-specified amplification model:
python3 -m decoratio --model=logskewnormal:0.72:-3.4 ./brown_alone.clone_sizes.tsv
```

Sample output:

```txt
decoratio-1.0.0 (python-3.8, scipy-1.5.2)
Called as: decoratio ./brown_alone.clone_sizes.tsv
Outputing to: ./brown_alone.clone_sizes.tsv.decoratio.logskewnormal.*
Reading input file...
Input data shows 60.8% PCR duplicates.
Optimizing the depth-complexity ratio & amplification noise...
Optimized:

    depth_complexity_ratio = 1.93
    model = logskewnormal:0.719:-3.4

Model fit was 99.1%; the predicted duplicate was rate 60.7% and the saturation
75.8%; the amplification model's noisiness was 0.719 and its skewness -0.72.
Writing output files...
    ./brown_alone.clone_sizes.tsv.decoratio.logskewnormal.png
    ./brown_alone.clone_sizes.tsv.decoratio.logskewnormal.ampl_factors.png
Done.
```

Obtaining the input file
----------

### Using **gstacks**

For RAD-seq datasets analyzed using STACKS, the clone sizes histogram is present
in one of the output files by default:

```sh
stacks-dist-extract ./gstacks.log.distribs pcr_clone_size_distrib > ./clone_sizes.tsv
python3 -m decoratio ./clone_sizes.tsv
# The program can actually be run directly on the distribs file:
python3 -m decoratio ./gstacks.log.distribs
```

*n.b.*, for datasets that comprise several libraries, for PCR duplicates and
library complexity purposes gstacks should be run separately on each library/set
of samples.

### Using **samtools-markdup**

```sh
prefix=./my_sample
samtools view -b -f0x3 -F0x904 $prefix.bam | 
    samtools collate -O - |
    samtools fixmate -m - - |
    samtools sort |
    samtools markdup -t - $prefix.markdup.bam
# We then extract the `do:` (presumably "duplicate of") tags in the SAM records.
samtools view -f0x40 $prefix.markdup.bam |
    sed -E 's/.*\tdo:Z:([^\t]+).*/\1/; s/\t.*//' |
    gzip > $prefix.clones.txt.gz
gzip -cd $prefix.clones.txt.gz |
    sort | uniq -c | awk '{print $1}' |
    sort -n | uniq -c |
    awk 'BEGIN{print "clone_size\tn_clones"} {print $2 "\t" $1}' \
    > $prefix.clone_sizes.tsv
python3 -m decoratio $prefix.clone_sizes.tsv
```

### Using **GATK/Picard**

```sh
prefix=./my_sample
picard=/path/to/picard.jar
# Filter for properly aligned read pairs.
samtools view -b -f0x3 -F0x904 $prefix.bam > $prefix.paired.bam
# Sort by read name.
java -jar $picard \
    SortSam \
    --SORT_ORDER queryname \
    -I $prefix.paired.bam -O $prefix.sortsam.bam \
    &> $prefix.sortsam.log
# Annotate duplicates.
java -jar $picard \
    MarkDuplicates \
    --TAG_DUPLICATE_SET_MEMBERS --READ_NAME_REGEX null \
    -I $prefix.sortsam.bam -O $prefix.markdups.bam -M $prefix.markdups.txt \
    &> $prefix.markdups.log
# Then extract the `DS:` (duplicate set size, i.e., clone size) tags in the SAM records.
samtools view -f0x40 -F0x400 $prefix.markdups.bam |
    sed -E '/\tDS:/!s/.*/1/; s/.*\tDS:i:([0-9]+).*/\1/' |
    sort -n | uniq -c |
    awk 'BEGIN{print "clone_size\tn_clones"} {print $2 "\t" $1}' \
    > $prefix.clone_sizes.tsv
python3 -m decoratio $prefix.clone_sizes.tsv
```

### Using **UMI-tools**

Handling of duplicates with UMI-tools is appropriate for experiments that make
use of unique molecular identifers (e.g., single-cell RNA-seq datasets).

Users should use the `umi_tools group` command, exporting the information about
the size of "read groups" (i.e., PCR duplication clones) to a text file with the
`--group-out` option.
