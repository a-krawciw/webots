import re
import sys
import argparse
from string import Template

header_string = """#VRML V2.0 utf8
# tags: static

PROTO $name [
	field SFVec3f translation 0 0 0
	field SFRotation orientation 1 0 0 0
]

{
Transform {
translation IS translation
rotation IS orientation
children [\n"""

footer = "\n]\n}\n}"

def remove_header(file):
    return re.sub(r"\#VRML.*", "", file)

def remove_colour_tag(file):
    return re.sub(r"color Color \{.*?\}", "", file, flags=re.DOTALL|re.MULTILINE ) 

def remove_colourIndex_tag(file):
    return re.sub(r"colorIndex \[.*?\]", "", file, flags=re.DOTALL|re.MULTILINE ) 
    
def remove_colorPerVertex_tag(file):
    return re.sub(r"colorPerVertex .*", "", file)
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filename')
    parser.add_argument('--outname')
    args = parser.parse_args()
    
    if not args.outname:
        args.outname = args.filename.split('.')[0]+'.proto'
    
    outname_no_ext = args.outname.split('.')[0]
    
    file = ''
    f = open(args.filename, mode='r')
    for line in f:
        file += line
    f.close()
    
    file = remove_header(file)
    file = remove_colour_tag(file)
    file = remove_colourIndex_tag(file)
    file = remove_colorPerVertex_tag(file)
    
    
    h = Template(header_string)
    
    file = h.substitute(name=outname_no_ext) + file + footer
    
    out = open(args.outname, 'w')
    out.write(file)
    out.close()


if __name__ == "__main__":
    main()
