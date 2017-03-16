#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno
import zipfile
import sys
import hashlib
import time

output_dir = 'output'

def main():

    # Make our output directory, if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        dir = os.listdir(output_dir)
        if len(dir) > 0:
            resume_point = int(dir[-1].replace('.html', '')) + 1

    # If we have a resume point file, resume from that number.
    with open('.resume') as f:
        resume_point = int(f.read())
    
    from urllib2 import Request, urlopen, HTTPError
    url_base = 'http://ethicssearch.dls.virginia.gov/ViewFormBinary.aspx?filingid='

    errors = 0
    try:
        i = resume_point
    except:
        i = 2050

    print "Resuming at " + str(i)
        
    while True:

        # Note the time at which we started reading this record, to make sure that we don't make
        # more than one request per second. (Too-frequent requests result in being blocked.)
        start_time = time.time()

        req = Request(url_base + str(i))

        try:
            f = urlopen(req)

            # If the content is long enough to be legitimate.
            if int(f.headers['content-length']) > 590:
                sys.stdout.write('.')
                sys.stdout.flush()

                errors = 0

                # Save the file.
                filename = output_dir + '/' + str(i).zfill(6) + '.html'
                local_file = open(filename, 'w')
                local_file.write(f.read())
                local_file.close()

            # If the content is short, indicating a blank page.
            else:
                sys.stdout.write(' ')
                sys.stdout.flush()
                errors += 1

        # If there's an HTTP error, record that.
        except HTTPError as e:
            sys.stdout.write('X')
            sys.stdout.flush()
            errors += 1

        # Increment our counter.
        i += 1

        # If we get 50 errors in a row, count by 10s.
        if errors >= 50:
            i += 9

        # If we get 200 errors in a row, quit.
        if errors == 200:
            print "Too many consecutive errors encountered—stopping"
            break

        # Don't query more than once every two seconds.
        if time.time() - start_time < 2:
            time.sleep(2 - (time.time() - start_time))

if __name__ == "__main__":
    main()
