import argparse
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from pathlib import Path
import warnings

import lib
from PIL import Image, ImageOps

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return ' %s:%s: %s:%s' % (filename, lineno, category.__name__, message)

warnings.formatwarning = warning_on_one_line

class Hornet(object):

    def __init__(self, args):
        self.cores = min(cpu_count(), args.num_cores)
        self.dim = args.dim
        self.command = args.command 
        self.process_pool = ThreadPool(self.cores) 
        self.files = None
        self.in_dir = args.in_dir
        self.out_dir = args.out_dir
        if self.in_dir == self.out_dir: 
            warnings.warn("Output and input directories are identical.")
        if not Path(self.out_dir).exists:
            Path.mkdir(self.out_dir)

    def run(self):
        if self.files is None:
            self.extract()
        if self.command == 'crop':
            self.process_pool.map(self.crop_glob, self.files)
        elif self.command == 'resize':
            self.process_pool.map(self.resize_glob, self.files)
        elif self.command == 'fit':
            self.process_pool.map(self.fit_glob, self.files)
        elif self.command == 'smart-resize':
            self.process_pool.map(self.smart_resize_glob, self.files)
        else:
            raise RuntimeError(f"Command: {self.command} not recognized.")
    
    def crop_glob(self,file):
        img = Image.open(file)
        if not (img.size[0] >= self.dim[0] and img.size[1] >= self.dim[1]):
            warnings.warn(f"Image {file} Size less than Target Size.")
        side_cut = (img.size[0] - self.dim[0]) // 2 
        top_cut = (img.size[1] - self.dim[1]) // 2
        border = (side_cut, top_cut, side_cut, top_cut)
        img = ImageOps.crop(img, border)
        img.save(self.out_dir + file.name)

    def resize_glob(self,file):
        img = Image.open(file)
        img = img.resize((self.dim[0], self.dim[1]), Image.ANTIALIAS)
        img.save(self.out_dir + file.name)

    def fit_glob(self, file):
        img = Image.open(file)
        img = ImageOps.fit(img, (self.dim[0], self.dim[1]))
        img.save(self.out_dir + file.name)

    def smart_resize_glob(self, file):
        img = Image.open(file)
        if img.size[0] == img.size[1]:
            self.resize_glob(self, file)
        else:
            if img.size[0] > img.size[1]:
                side_cut = (img.size[0] - self.dim[0]) // 2
                border = (side_cut, 0, side_cut, 0)
                img = ImageOps.crop(img, border)
                img = img.resize((self.dim[0], self.dim[1]), Image.ANTIALIAS)
                img.save(self.out_dir + file.name)
            else:
                top_cut = (img.size[1] - self.dim[1]) // 2
                border = (0, top_cut, 0, top_cut)
                img = ImageOps.crop(img, border)
                img = img.resize((self.dim[0], self.dim[1]), Image.ANTIALIAS)
                img.save(self.out_dir + file.name)

    def extract(self):
        self.files = list(p.resolve() for p in Path(self.in_dir).rglob("*") if p.suffix in lib.image_types)

    @staticmethod
    def get_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('command', nargs='?', type=str,
                            choices=['crop','resize','fit','smart-resize'], 
                            help='crop: Crop images in the dataset to desired size\n'
                            'resize: Resize images to desired size')
        parser.add_argument('--in_dir', type=str, help='Path to input direcotry of images')
        parser.add_argument('--out_dir', type=str, help='Path to directory where processed images will go')
        parser.add_argument('--num_cores', type=int, default=cpu_count()-1, help='Number of CPU cores to utilize')
        parser.add_argument('--dim', nargs=2, metavar=('width','height'), help='Pair of "width height" values for resultant image')

        args = parser.parse_args()
        return args

def main():
    args = Hornet.get_arg_parser()
    buzz = Hornet(args)
    buzz.run()
    print("Complete.")

if __name__ == '__main__':
    main()