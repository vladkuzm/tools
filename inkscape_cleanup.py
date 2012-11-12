#!/usr/bin/python3
import sys
import gzip

from lxml import etree

DEBUG = True

def get_opts(raw_str):
    opt_list = raw_str.strip(";").split(";")
    opt_list = [(x + ';') for x in opt_list]
    return opt_list

def get_new_style(raw_str):
    opt_list = get_opts(raw_str)
    for opt in opt_list:
        if (opt.startswith("color:")):
            opt_list.remove(opt)
    return ''.join(opt_list)

def is_target(elm):
    style_attr = elm.get("style")
    if (style_attr is not None and
        "fill:currentColor" in get_opts(style_attr)):
        opts = get_opts(style_attr)
        for opt in opts:
            if (opt.startswith("color:")):
                return True
        
    return False

def set_proper_style(elm):
    new_style = get_new_style(elm.get("style"))
    elm.set("style", new_style)
    if (DEBUG):
        print("Removing from element - class: %s | %s" % 
              (elm.get("class"), elm.get("style")))

def main():
    is_gzipped = False
    if (len(sys.argv) < 2):
        sys.exit("Usage: %s <SVG-FILE-PATH>" % sys.argv[0])
    if (sys.argv[1].endswith(".svgz")):
        is_gzipped = True

    if (is_gzipped):
        fobj = gzip.open(sys.argv[1], "rb")
    else:
        fobj = open(sys.argv[1], "rb")

    tree = etree.parse(fobj)
    for elm in tree.iter():
        if (is_target(elm)):
            set_proper_style(elm)
    fobj.close()
    
    if (is_gzipped):
        fobj = gzip.open(sys.argv[1], "wb")
    else:
        fobj = open(sys.argv[1], "wb")
    fobj.write(etree.tostring(tree, encoding="UTF-8", pretty_print=True))
    fobj.close()

if __name__ == "__main__":
    main()
