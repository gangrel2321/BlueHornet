import argparse
import multiprocessing
from multiprocessing import Pool

class Hornet(object):

    def __init__(self):
        pass

    @staticmethod
    def crop_glob():
        pass

    @staticmethod
    def resize_glob():
        pass

    @staticmethod
    def get_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('command', nargs='?', type=str,
                            choices=['crop','resize'], 
                            help='crop: Crop images in the dataset to desired size\n'
                            'resize: Resize images to desired size')
        parser.add_argument('--in_dir', type=str, help='Path to input direcotry of images')
        parser.add_argument('--out_dir', type=str, help='Path to directory where processed images will go')
        parser.add_argument('--num_cores', type=int, help='Number of CPU cores to utilize')

        args = parser.parse_args()
        return args

def main():
    args = Hornet.get_arg_parser()
    


if __name__ == '__main__':
    main()