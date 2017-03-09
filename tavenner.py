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

        # Note the time at which we started reading this record, to make sure that we don't make
        # more than one request per second. (Too-frequent requests result in being blocked.)
        start_time = time.time()

        req = Request(url_base + str(i))

        try:
            f = urlopen(req)
            sys.stdout.write('.')
            sys.stdout.flush()

            errors = 0
            
            local_file = open(str(i) + '.html', 'w')
            local_file.write(f.read())
            local_file.close()

        # If there's an HTTP error, record that.
        except HTTPError as e:
            sys.stdout.write(' ')
            sys.stdout.flush()

            errors += 1

        # Increment our counter.
        i += 1

        # If we get 100 errors in a row, stop.
        if errors = 100:
            break

        # Don't query more than once every half-second.
        if time.time() - start_time < 0.5:
            time.sleep(0.5 - (time.time() - start_time))

if __name__ == "__main__":
    main()
