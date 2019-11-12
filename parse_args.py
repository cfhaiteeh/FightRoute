import sys
args = sys.argv

import os
import argparse

def interpret_args():
    """ Interprets the command line arguments, and returns a dictionary. """
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha1", type=int, default=25)
    parser.add_argument("--alpha2", type=int, default=15)
    parser.add_argument("--beta1", type=int, default=20)
    parser.add_argument("--beta2", type=int, default=25)
    parser.add_argument("--thet", type=int, default=30)
    parser.add_argument("--delta", type=float, default=0.001)
    parser.add_argument("--max_point", type=int, default=270000)
    parser.add_argument("--prob", type=bool, default=False)
    parser.add_argument("--top5", type=bool, default=False)


    parser.add_argument(
        '--data_path',
        type=str,
        default='data/data1.csv')





    args = parser.parse_args()

    print(args)
    return args
