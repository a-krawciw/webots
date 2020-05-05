import re
import sys
import argparse
from string import Template


bbox = """
boundingObject Transform {
    translation $x $y $z
    children [
        Box {
            size $x_width $y_width $z_width
        }
    ]
}
"""

class Interval:
    
    def __init__ (self, low=0, high = 0):
        self.min = low
        self.max = high
    
    def inspect_value(self, value):
        if value < self.min:
            self.min = value
        elif value > self.max:
            self.max = value
            
    def width (self):
        return (self.max - self.min)
    
    def mean (self):
        return (self.max + self.min)/2
            
def parse_point (string):
    nums = string.split(' ')
    return [float(n) for n in nums]
    
def add_bounding_box (file):
    x_int = Interval()
    y_int = Interval()
    z_int = Interval()
    
    coords = re.finditer(r"point \[(.*?)\]", file, flags=re.DOTALL|re.MULTILINE)
    
    for coord_arr in coords:
        points = coord_arr.group(1).split(',')
        for point in points:
            [x, y, z] = parse_point(point.strip())
            x_int.inspect_value(x)
            y_int.inspect_value(y)
            z_int.inspect_value(z)
    
    
    f = Template(bbox)
    return  f.substitute(x = x_int.mean(), y=y_int.mean(), z=z_int.mean(), x_width=x_int.width(), y_width=y_int.width(), z_width=z_int.width())
    
    
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filename')
    parser.add_argument('--outname')
    args = parser.parse_args()
    
    
    
    file = ''
    f = open(args.filename, mode='r')
    for line in f:
        file += line
    f.close()
    
    bounds = add_bounding_box(file)
    
    if args.outname:
        out = open(args.outname, 'w')
        out.write(bounds)
        out.close()
    else:
        print(bounds)


if __name__ == "__main__":
    main()
