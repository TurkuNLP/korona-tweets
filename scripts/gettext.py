#!/usr/bin/env python3

import sys
import json
import gzip

from argparse import ArgumentParser


def argparser():
    ap = ArgumentParser()
    ap.add_argument('-d', '--dedup', default=False, action='store_true')
    ap.add_argument('-i', '--ids', default=False, action='store_true')
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
            try:
                text = data['extended_tweet']['full_text']
            except:
                text = data['text']
            text = normalize(text)
            if options.dedup:
                if text in seen:
                    continue
                else:
                    seen.add(text)
            if options.ids:
                print('{}\t{}'.format(data['id'], text))
            else:
                print(text)
        except Exception as e:
            print('failed {}: {}'.format(e, l), file=sys.stderr)


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        if fn.endswith('.gz'):
            with gzip.open(fn, 'rt', encoding='utf-8') as f:
                process(f, fn, args)
        else:
            with open(fn) as f:
                process(f, fn, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
