import ImageFilter
from numpy import *

SIGMA = 0.5

def gaussian_grid(sigma, alpha=4):
    sig = max(sigma, 0.01)
    length = int(math.ceil(sig * alpha)) + 1
    m = length / 2
    n = m + 1
    x, y = mgrid[-m:n,-m:n]
    g = exp(m ** 2) * exp(-0.5 * (x**2 + y**2))
    return g.round().astype(int)

class GAUSSIAN(ImageFilter.BuiltinFilter):
    name = "Gaussian"
    grid = gaussian_grid(SIGMA)
    g = grid.flatten().tolist()
    dim = int(math.sqrt(grid.size))
    filterargs = (dim,dim), sum(g), 0, tuple(g)
