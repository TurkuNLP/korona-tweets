#!/usr/bin/env python3

import sys
import json
import gzip

from argparse import ArgumentParser
from logging import warning


def argparser():
    ap = ArgumentParser()
    ap.add_argument('-r', '--no-retweets', default=False, action='store_true')
    ap.add_argument('file', nargs='+')
    return ap


def normalize(text):
    return ' '.join(text.split()).strip()


def process(f, fn, options):
    seen = set()
    for l in f:
        l = l.rstrip('\n')
        if l.isspace() or not l:
            continue
        try:
            data = json.loads(l)
            if 'retweeted_status' in data and options.no_retweets:
                continue
            try:
                text = data['user']['location']
            except:
                warning('Failed to get location for {}'.format(data['id']))
                continue
            text = normalize(text)
            print(text)
        except Exception as e:
            print('Failed with {}: {}: {}'.format(type(e).__name__, e, l),
                  file=sys.stderr)


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        try:
            if fn.endswith('.gz'):
                with gzip.open(fn, 'rt', encoding='utf-8') as f:
                    process(f, fn, args)
            else:
                with open(fn) as f:
                    process(f, fn, args)
        except Exception as e:
            warning('Error processing {}: {}: {}'.format(
                fn, type(e).__name__, e))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
