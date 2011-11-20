import Image
from smooth_filter import GAUSSIAN
from graph import build_graph, segment_graph
from numpy import sqrt

def diff(img, x1, y1, x2, y2):
    r = (img[x1, y1][0] - img[x2, y2][0]) ** 2
    g = (img[x1, y1][1] - img[x2, y2][1]) ** 2
    b = (img[x1, y1][2] - img[x2, y2][2]) ** 2
    return sqrt(r + g + b)

def threshold(size, const):
    return (const / size)

if __name__ == '__main__':
    image_file = Image.open('data/beach.PPM')
    size = image_file.size
    print image_file.format, size, image_file.mode

    #small = image_file.crop((0, 0, 8, 8))
    #small.save('data/small_beach.PPM')

    smooth = image_file.filter(GAUSSIAN)
    #smooth.save('data/testfiltered.png')

    graph = build_graph(smooth, diff)
    forest = segment_graph(graph, size[0]*size[1], float(500), 50, threshold)

    print 'num sets: %d' % forest.num_sets

