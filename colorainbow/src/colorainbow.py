#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: eis
Created on 23/12/11
"""
from collections import namedtuple
import colorsys
import re

import random
random.seed()
rnd = lambda f, t: f + random.random() * (t-f)

_re_template = r'^(?P<pre>\s*<option\s+name\s*=\s*"\S*?%s"\s+value\s*=\s*")(?P<color_val>[0-9a-fA-F]{6})(?P<post>"\s*/>\s*)$'

_re_background_color = re.compile(_re_template % 'BACKGROUND')
_re_foreground_color = re.compile(_re_template % 'FOREGROUND')
_re_color = re.compile(_re_template % 'COLOR')
_re_scheme_name = re.compile(r'^\s*(?P<pre>\<scheme\s+name\s*=\s*")(?P<name>\S*?)(?P<post>".*)$')

RGB = namedtuple('RGB', ['r', 'g', 'b'])
HSV = namedtuple('HSV', ['r', 'g', 'b'])

def rgb_for_hsv(hsv):
    """
    >>> rgb_for_hsv(HSV(1.0, 1.0, 1.0))
    RGB(r=1.0, g=0.0, b=0.0)
    """
    return RGB(*colorsys.hsv_to_rgb(*hsv))

def rgb_for_str(s):
    """
    >>> rgb_for_str('ffeedd')
    RGB(r=1.0, g=0.9333333333333333, b=0.8666666666666667)
    """
    return RGB(*[int(s, 16)/255.0 for s in [s[0:2], s[2:4], s[4:6]]])

def hsv_for_rgb(rgb):
    return HSV(*colorsys.rgb_to_hsv(*rgb))
    
def str_for_rgb(rgb):
    """
    >>> str_for_rgb(RGB(1.0, 0.9333333333333333333, 0.866666666666666666666666666666667))
    'ffeedd'
    """
    return '{0:02x}{1:02x}{2:02x}'.format(*[int(v*255) for v in rgb])

def pick_editor_background_color():
    return str_for_rgb(rgb_for_hsv(HSV(
        random.random(),
        rnd(0.4, 0.6),
        rnd(0.05, 0.20),
    )))

def pick_random_background_color():
    return str_for_rgb(rgb_for_hsv(HSV(
        random.random(),
        rnd(0.5, 0.8),
        rnd(0.35, 0.7),
    )))

def pick_random_text_color():
    return str_for_rgb(rgb_for_hsv(HSV(
        random.random(),
        rnd(0.05, 0.4),
        rnd(0.7, 0.9),
    )))

def process_line(s, scheme_name):
    return reduce(lambda acc, v: v[0].sub(r'\g<pre>%s\g<post>' % v[1], acc), [
        (_re_color, pick_random_text_color()),
        (_re_background_color, pick_random_background_color()),
        (_re_foreground_color, pick_random_text_color()),
        (_re_scheme_name, scheme_name),
    ], s)
    
def colorize(infile, outfile=None, background_color=None):
    """Main color scheme processing function."""
    background_color = background_color or pick_editor_background_color()

#    outfile = outfile or os.path.abspath('./{0}.colorainbow.{1}.xml'.format(
#        infile[:-(len(infile.split('.')[-1]) + 1)],
#        str(datetime.datetime.now()).replace(':', ''))
#    )
    outfile = outfile or (background_color + '.xml')

    print 'Colorizing {0} --> {1}...'.format(infile, outfile)
    print 'Your background color is: * {0} *.\nNOTE: YOU STILL HAVE TO SET THIS COLOR MANUALLY. OK.'.format(background_color)
    
    with open(outfile, 'w') as outs, open(infile, 'r') as ins:
        outs.writelines([process_line(l, background_color) for l in ins.readlines()])
        
    print 'All done!'
    
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])

    parser.add_argument('template_file', type=str, default=None,
        help='''Template scheme file.''')
    parser.add_argument('how_much', nargs='?', type=int, default=1,
        help='''How many schemes to generate. Default is 1.''')
    parser.add_argument('output_file', nargs='?', type=str, default=None,
        help='''Output file path. If not specified will default to <editor_background_color>.xml.''')
    parser.add_argument('background_color', nargs='?', type=str, default=None,
        help='''Your desired background color. If not specified -- randomized. It still has to be set manually after you load the scheme.''')

    args = parser.parse_args()
    
    for _ in xrange(args.how_much):    
        colorize(args.template_file, outfile=args.output_file, background_color=args.background_color)
