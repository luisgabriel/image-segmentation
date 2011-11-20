import Image, ImageFilter
import sys
from graph import build_graph, segment_graph
from smooth_filter import GAUSSIAN
from random import random
from numpy import sqrt

def diff(img, x1, y1, x2, y2):
    r = (img[x1, y1][0] - img[x2, y2][0]) ** 2
    g = (img[x1, y1][1] - img[x2, y2][1]) ** 2
    b = (img[x1, y1][2] - img[x2, y2][2]) ** 2
    return sqrt(r + g + b)

def threshold(size, const):
    return (const / size)

def generate_image(forest, width, height):
    random_color = lambda: (int(random()*255), int(random()*255), int(random()*255))
    colors = [random_color() for i in xrange(width*height)]

    img = Image.new('RGB', (width, height))
    im = img.load()
    for y in xrange(height):
        for x in xrange(width):
            comp = forest.find(y * width + x)
            im[x, y] = colors[comp]

    return img

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Invalid number of arguments passed'
        print 'Correct usage: python main.py k min_component_size input_file output_file'
    else:
        image_file = Image.open(sys.argv[3])
        size = image_file.size
        print 'Image info:', image_file.format, size, image_file.mode

        K = float(sys.argv[1])
        min_size = int(sys.argv[2])

        smooth = image_file.filter(GAUSSIAN)
        #smooth.save('data/testfiltered.png')

        graph = build_graph(image_file, diff)
        forest = segment_graph(graph, size[0]*size[1], K, min_size, threshold)

        image = generate_image(forest, size[0], size[1])
        image.save(sys.argv[4])

        print 'Number of components: %d' % forest.num_sets
