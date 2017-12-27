import numpy as np
import argparse, os
from pyflann import *

parser = argparse.ArgumentParser(description='Computes approximated nearest neigbors for a susbset of points. Retrieves the sorted list of distances')

parser.add_argument('input_matrix', type=str, help='the numpy matrix with the data')
parser.add_argument('output_folder', type=str, help='the path where the resulting files must be stored')
parser.add_argument('--N', dest='N', type=int, default=10 ,help='the number of random points')

args = parser.parse_args()

print("loading data ...")
data = np.load(args.input_matrix)
points = data[np.random.randint(data.shape[0], size=args.N),:]

print("running FLANN...")
flann = FLANN()
set_distance_type('manhattan')
params = flann.build_index(data, algorithm="autotuned", target_precision=0.95);
result, dists = flann.nn_index(points, 200, checks=params["checks"]);

print("saving results...")
np.save(open(os.path.join(args.output_folder,"result.txt"), "w"), result)
np.save(open(os.path.join(args.output_folder,"dists.txt"), "w"), dists)