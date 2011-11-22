import Image
import sys
from graph import build_graph, segment_graph
from smooth_filter import gaussian_grid, filter_image
from random import random
from numpy import sqrt, asarray

def diff(img, x1, y1, x2, y2):
    r = (img[0][x1, y1] - img[0][x2, y2]) ** 2
    g = (img[1][x1, y1] - img[1][x2, y2]) ** 2
    b = (img[2][x1, y1] - img[2][x2, y2]) ** 2
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

    return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print 'Invalid number of arguments passed.'
        print 'Correct usage: python main.py sigma min_component_size input_file output_file'
    else:
        image_file = Image.open(sys.argv[4])
        sigma = float(sys.argv[1])
        K = float(sys.argv[2])
        min_size = int(sys.argv[3])

        size = image_file.size
        print 'Image info: ', image_file.format, size, image_file.mode

        image_file.load()
        r, g, b = image_file.split()

        grid = gaussian_grid(sigma)
        r = filter_image(r, grid)
        g = filter_image(g, grid)
        b = filter_image(b, grid)

        graph = build_graph((r, g, b), size[1], size[0], diff)
        forest = segment_graph(graph, size[0]*size[1], K, min_size, threshold)

        image = generate_image(forest, size[1], size[0])
        image.save(sys.argv[5])

        print 'Number of components: %d' % forest.num_sets
