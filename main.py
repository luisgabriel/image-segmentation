import argparse
import logging
import time
from graph import build_graph, segment_graph
from random import random
from PIL import Image, ImageFilter
from skimage import io
import numpy as np


def diff(img, x1, y1, x2, y2):
    _out = np.sum((img[x1, y1] - img[x2, y2]) ** 2)
    return np.sqrt(_out)


def threshold(size, const):
    return (const * 1.0 / size)


def generate_image(forest, width, height):
    random_color = lambda: (int(random()*255), int(random()*255), int(random()*255))
    colors = [random_color() for i in range(width*height)]

    img = Image.new('RGB', (width, height))
    im = img.load()
    for y in range(height):
        for x in range(width):
            comp = forest.find(y * width + x)
            im[x, y] = colors[comp]

    return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)


def get_segmented_image(sigma, neighbor, K, min_comp_size, input_file, output_file):
    if neighbor != 4 and neighbor!= 8:
        logger.warn('Invalid neighborhood choosed. The acceptable values are 4 or 8.')
        logger.warn('Segmenting with 4-neighborhood...')
    start_time = time.time()
    image_file = Image.open(input_file)

    size = image_file.size  # (width, height) in Pillow/PIL
    logger.info('Image info: {} | {} | {}'.format(image_file.format, size, image_file.mode))

    # Gaussian Filter
    smooth = image_file.filter(ImageFilter.GaussianBlur(sigma))
    smooth = np.array(smooth)
    
    logger.info("Creating graph...")
    graph_edges = build_graph(smooth, size[1], size[0], diff, neighbor==8)
    
    logger.info("Merging graph...")
    forest = segment_graph(graph_edges, size[0]*size[1], K, min_comp_size, threshold)

    logger.info("Visualizing segmentation and saving into: {}".format(output_file))
    image = generate_image(forest, size[1], size[0])
    image.save(output_file)

    logger.info('Number of components: {}'.format(forest.num_sets))
    logger.info('Total running time: {:0.4}s'.format(time.time() - start_time))


if __name__ == '__main__':
    # argument parser
    parser = argparse.ArgumentParser(description='Graph-based Segmentation')
    parser.add_argument('--sigma', type=float, default=1.0, 
                        help='a float for the Gaussin Filter')
    parser.add_argument('--neighbor', type=int, default=8, choices=[4, 8],
                        help='choose the neighborhood format, 4 or 8')
    parser.add_argument('--K', type=float, default=10.0, 
                        help='a constant to control the threshold function of the predicate')
    parser.add_argument('--min-comp-size', type=int, default=2000, 
                        help='a constant to remove all the components with fewer number of pixels')
    parser.add_argument('--input-file', type=str, default="./assets/seg_test.jpg", 
                        help='the file path of the input image')
    parser.add_argument('--output-file', type=str, default="./assets/seg_test_out.jpg", 
                        help='the file path of the output image')
    args = parser.parse_args()

    # basic logging settings
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
    logger = logging.getLogger(__name__)

    get_segmented_image(args.sigma, args.neighbor, args.K, args.min_comp_size, args.input_file, args.output_file)
