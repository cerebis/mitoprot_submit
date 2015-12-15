#!/usr/bin/env python

from Bio import SeqIO
import argparse
import urllib2
import time
import sys

parser = argparse.ArgumentParser(description='Submit sequences to MitoprotII server')
parser.add_argument('-w', '--wait', dest='wait', metavar='SECONDS', default=2, type=int,
                    help='Wait N seconds between requests')
parser.add_argument('seq', metavar='FASTA', nargs=1, help='Multi-fasta format sequence file')
parser.add_argument('out', metavar='FILE', nargs=1, help='Output file')

output = None

try:
    args = parser.parse_args()

    if args.wait < 1:
        raise RuntimeError('Error: the minimum wait time is 1 second')

    output = open(args.out[0], 'w')

    template_url = 'http://ihg.gsf.de/cgi-bin/paolo/mitofilter?seq={0}&seqname={1}'

    with open(args.seq[0], 'r') as input_file:
        for n, seq in enumerate(SeqIO.parse(input_file, 'fasta'), start=1):
            print 'Submitting sequence #{0} named {1}'.format(n, seq.id)
            url = template_url.format(str(seq.seq), str(seq.id))
            response = urllib2.urlopen(url)
            output.write(str(response.read()))
            output.write('\n')
            time.sleep(args.wait)

except Exception as ex:
    print 'An error occured: {0}'.format(ex.message)
    sys.exit(1)

finally:
    if output is not None:
        output.close()