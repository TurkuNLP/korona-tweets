# korona-tweets

stuff for our korona-tweets

## Data selection for batches 2+

Files in `annotation/`:

- `batch-01.tsv`: unannotated initial batch of data
- `batch-01-annotated.tsv`: manually annotated version of `batch-01.tsv`
- `tweets-170420-scored.tsv`: unannotated tweets not in `batch-01.tsv` with scores predicted based on FinBERT trained on `batch-01-annotated.tsv`

Sampling:

```
$ python3 scripts/sample_scored.py --seed 1234 annotation/tweets-170420-scored.tsv > annotation/tweets-170420-sampled.tsv
Loaded 68504 items from annotation/tweets-170420-scored.tsv
Sampled 3795/68504 (5.5%), mean rank 12385.1, median rank 4205
```

Split first 2000 into batches of 250 tweets

```
head -n 2000 annotation/tweets-170420-sampled.tsv | shuf | gsplit - -l 250 --numeric-suffixes=02 --additional-suffix=.tsv annotation/batch-
for f in annotation/batch-0[23456789].tsv; do cut -f 4- $f > tmp; mv tmp $f; done
```

