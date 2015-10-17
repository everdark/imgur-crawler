#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
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
    return parser

def crawlImgur(src_url, dest_path, nitem):
    soup = BeautifulSoup(requests.get(src_url).content, "lxml")
    tlist = soup.findAll("meta", {"property": "og:image"})
    
    if nitem is not None:
        tlist = tlist[:nitem+1]

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    
    for t in tlist:
        img_src = t.get("content")
        if re.search("\.jpg$", img_src):
            print "download %s..." % img_src,
            r = requests.get(img_src, stream=True)
            outfname = os.path.join(dest_path, os.path.basename(img_src))
            with open(outfname, 'wb') as outfile:
                shutil.copyfileobj(r.raw, outfile)
                print "done"

    return None

def main():
    parser = getArgParser()
    args = parser.parse_args()
    crawlImgur(args.url, args.dest, args.nitem)

if __name__ == "__main__":
    main()



