"""
@author: zhshj0110@gmail.com
"""

import struct
import argparse


class ImageSize:
    def __init__(self, image_path):
        self.image_path = image_path
    
    def _get_size_(self):
        with open(self.image_path, "rb") as f:
            header = f.read(24)
            if len(header) < 24:
                return None

            # JPEG format
            if header[:2] == b'\xff\xd8':
                return self._get_jpg_size_(f)
            
            # PNG format
            elif header[:8] == b'\x89PNG\r\n\x1a\n':
                return self._get_png_size_(header)
        

    def _get_jpg_size_(self, f):
        while True:
            while f.read(1) != b'\xff':
                pass
            marker = f.read(1)
            if marker == b'\xda':  # SOS (Start of Scan) flag
                return None
            if marker[0] >= 0xc0 and marker[0] <= 0xc3:  # SOF (Start of Frame) flag
                f.read(3)  
                height, width = struct.unpack('>HH', f.read(4))
                return width, height
            else:
                size = struct.unpack('>H', f.read(2))[0]
                if size < 2:
                    return None
                f.read(size - 2)
    

    def _get_png_size_(self, header):
        width, height = struct.unpack('>II', header[16:24])
        return width, height


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=str, nargs="+")
    args = parser.parse_args()

    for image_path in args.inputs:
        size = ImageSize(image_path)._get_size_()
        print(f"The resolution of the {image_path} is {size}.")