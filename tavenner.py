#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno
import zipfile
import sys
import hashlib

output_dir = 'output'

def main():

    # Make our output directory, if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    from urllib2 import Request, urlopen, HTTPError
    url_base = 'http://ethicssearch.dls.virginia.gov/ViewFormBinary.aspx?filingid='

    errors = 0
    i = 1
    while True:

        req = Request(url_base + str(i))

        try:
            f = urlopen(req)
            sys.stdout.write('.')
            sys.stdout.flush()

            errors = 0
            
            local_file = open(str(i) + '.html', 'w')
            local_file.write(f.read())
            local_file.close()

        except HTTPError as e:
            sys.stdout.write(' ')
            sys.stdout.flush()

            errors += 1

        i += 1

        if errors >= 100:
            break

if __name__ == "__main__":
    main()
