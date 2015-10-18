#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time
import re
import shutil
import requests
from bs4 import BeautifulSoup

def getArgParser():
    parser = argparse.ArgumentParser(
             description="Crawl given imgur album and save all images within.",
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", metavar="url", type=str,
                        help="the source URL of imgur")
    parser.add_argument("dest", metavar="dest", type=str, nargs='?', default=".",
                        help="the destination folder to save image")
    parser.add_argument("-n", "--nitem", metavar="N", type=int, action="store",
                        help="the maximum number of images to save")
    parser.add_argument("-s", "--show-status", action="store_true", default=False,
                        help="optionally show download status")
    return parser

def crawlImgur(src_url, dest_path, nitem, show_status=True):
    soup = BeautifulSoup(requests.get(src_url).content, "lxml")
    tlist = soup.findAll("meta", {"property": "og:image"})
    
    if nitem is not None:
        tlist = tlist[:nitem+1]

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    
    for t in tlist:
        img_src = t.get("content")
        if re.search("\.jpg$", img_src):
            r = requests.get(img_src, stream=True)
            outfname = os.path.join(dest_path, os.path.basename(img_src))
            with open(outfname, "wb") as outfile:
                if show_status:
                    print "download %s..." % img_src,
                    size_downloaded = 0
                    size_total = len(r.content)
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            outfile.write(chunk)
                            size_downloaded += len(chunk)
                            status = r"%10d  [%3.2f%%]" % (size_downloaded, size_downloaded * 100. / size_total)
                            status = status + chr(8)*(len(status)+1)
                            print status,
                            sys.stdout.flush()
                    print ''
                else:
                    print "download %s..." % img_src,
                    shutil.copyfileobj(r.raw, outfile)
                    print "done"

    return None

def main():
    parser = getArgParser()
    args = parser.parse_args()
    crawlImgur(args.url, args.dest, args.nitem, args.show_status)

if __name__ == "__main__":
    main()



