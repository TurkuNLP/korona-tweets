import sys
import re

from argparse import ArgumentParser


HASHTAG_RE = re.compile(r'^(#\w+).*', re.UNICODE)


def argparser():
    ap = ArgumentParser()
    ap.add_argument('-d', '--dedup', default=False, action='store_true')
    ap.add_argument('-i', '--ids', default=False, action='store_true')
    ap.add_argument('file', nargs='+')
    return ap


def get_hashtags(text):
    hashtags = []
    for t in text.split():
        m = HASHTAG_RE.match(t)
        if m:
            hashtags.append(m.group(1))
    return hashtags


def process(fn, options):
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            for t in get_hashtags(l):
                print(t)


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        process(fn, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
