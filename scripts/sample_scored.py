#!/usr/bin/env python3

import sys
import random

from statistics import mean, median


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--seed', default=None, type=float)
    ap.add_argument('file')
    return ap


def load_scored(fn):
    scored_data = []
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            fields = l.split('\t')
            score, rest = fields[0], fields[1:]
            score = float(score)
            scored_data.append((score, rest))
    print('Loaded {} items from {}'.format(len(scored_data), fn),
          file=sys.stderr)
    return scored_data


def sampling_probability(rank, total_count):
    scaled = (100.0 * rank) / total_count
    return min(1.0, 1.0/scaled)


def sample_scored(fn):
    scored_data = load_scored(fn)
    total_count = len(scored_data)
    sampled = []
    for rank, (score, data) in enumerate(sorted(scored_data), start=1):
        prob = sampling_probability(rank, total_count)
        if random.random() < prob:
            sampled.append((prob, rank, score, data))
    ranks = [s[1] for s in sampled]
    print('Sampled {}/{} ({:.1%}), mean rank {:.1f}, median rank {}'.format(
        len(sampled), len(scored_data), len(sampled)/len(scored_data),
        mean(ranks), median(ranks)), file=sys.stderr)
    return sampled


def main(argv):
    args = argparser().parse_args(argv[1:])
    random.seed(args.seed)
    sampled = sample_scored(args.file)
    for prob, rank, score, data in sampled:
        print('\t'.join([str(prob), str(rank), str(score)]+data))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
