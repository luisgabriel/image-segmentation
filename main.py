import Image
from smooth_filter import GAUSSIAN
from numpy import sqrt

def diff(img, x1, y1, x2, y2):
    r = (img[x1, y1][0] - img[x2, y2][0]) ** 2
    g = (img[x1, y1][1] - img[x2, y2][1]) ** 2
    b = (img[x1, y1][2] - img[x2, y2][2]) ** 2
    return sqrt(r + g + b)

def build_graph(image):
    img = image.load()
    width = image.size[0]
    height = image.size[1]

    graph = []
    for y in xrange(height):
        for x in xrange(width):
            if x < width-1:
                w = diff(img, x, y, x+1, y) 
                graph.append((y * width + x, y * width + (x+1), w))

            if y < height-1:
                w = diff(img, x, y, x, y+1) 
                graph.append((y * width + x, (y+1) * width + x, w))

            if x < width-1 and y < height-1:
                w = diff(img, x, y, x+1, y+1) 
                graph.append((y * width + x, (y+1) * width + (x+1), w))

            if x < width-1 and y > 0:
                w = diff(img, x, y, x+1, y-1) 
                graph.append((y * width + x, (y-1) * width + (x+1), w))

    return graph


if __name__ == '__main__':
    image_file = Image.open('data/beach.PPM')
    print image_file.format, image_file.size, image_file.mode

    smooth = image_file.filter(GAUSSIAN)
    #smooth.save('data/testfiltered.png')

    graph = build_graph(smooth)
    for edge in graph:
        print '(%s, %s, %.2f)' % (edge[0], edge[1], edge[2])
