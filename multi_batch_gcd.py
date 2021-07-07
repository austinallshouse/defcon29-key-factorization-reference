import sys
from math import gcd, log2, ceil
from multiprocessing import Pool, cpu_count
from itertools import permutations

from tqdm import tqdm

def multiply_pair(x):
    return x[0] * x[1]

def div_mod_sq(x):
    result = x[0] % (x[1]**2)
    return result

def gcd_div(x):
    result = gcd(x[0] // x[1], x[1])
    return result

def calculate_remainder_level(remainders, products):
    with Pool(cpu_count()) as cpu_pool:
        return cpu_pool.map(div_mod_sq, ((remainders[i//2], products[i]) for i in range(len(products))))

def calculate_factors(product, tree):
    remainders = [product]

    for level in reversed(tree.tree[:-1]):
        remainders = calculate_remainder_level(remainders, level)

    with Pool(cpu_count()) as cpu_pool:
        return cpu_pool.map(gcd_div, zip(remainders, tree.leaves))

class ProductTree:

    def __init__(self, path):
        self.path = path
        self.tree = self.build_product_tree(self.load_modulus_file(path))
        self.product = self.tree[-1][0]
        self.leaves = self.tree[0]

    def build_product_tree(self, levels):
        """
        recursively produces a product tree from an input
        array of arrays which should initially contain one element
        representing the list of moduli to be factored
        """
        levels.append(self.calculate_product_tree_level(levels[-1]))
        if len(levels[-1]) == 1:
            return levels

        return self.build_product_tree(levels)

    @staticmethod
    def calculate_product_tree_level(products):
        """ 
        returns an array representing the pairwise products of the input,
        if an array of an odd length is provided, the last item is appended
        to the output array
        """
        with Pool(cpu_count()) as cpu_pool:
            next_level = cpu_pool.map(multiply_pair, zip(*[iter(products)]*2))
        if len(products) % 2 == 1:
            next_level.append(products[-1])

        return next_level

    @staticmethod
    def load_modulus_file(path):
        """
        returns a nested list of integers (a tree with one level) 
        from moduli stored as one hex string per line
        """
        with open(path) as fp:
            return [[int(modulus, 16) for modulus in fp]]


if __name__ == '__main__':

    paths = sys.argv[1:]
    trees = [ProductTree(path) for path in tqdm(paths, f'building {len(paths)} product trees')]

    for left_tree, right_tree in tqdm(permutations(trees, 2), 
        desc='calculating remainders', total=(len(paths)*(len(paths)-1))):
        product = left_tree.product * right_tree.product
        for idx, p in enumerate(calculate_factors(product, right_tree)):
            if p > 1:
                q, remainder = divmod(right_tree.leaves[idx], p)
                if remainder == 0:
                    print('%s:%d - %d bits - %x -> (%x * %x' % (
                        right_tree.path, idx+1, ceil(log2(right_tree.leaves[idx])), right_tree.leaves[idx], p, q)
                    )
