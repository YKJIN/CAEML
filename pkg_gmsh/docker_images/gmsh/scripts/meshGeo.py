#!/usr/bin/env python3
__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import argparse
import subprocess

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('geo_file')
    parser.add_argument('step_file')
    parser.add_argument('--clscale', metavar='clscale', required=False, default=1.0, type=float)
    parser.add_argument('--out_file_format', metavar='out_file_format', required=False, default="vtk", type=str)

    args = parser.parse_args()
    subprocess.Popen("gmsh  {} -3 -format {} -clscale {:f} -o /data/gmsh_out.{}".format(args.geo_file, args.out_file_format, args.clscale, args.out_file_format), shell=True).wait()