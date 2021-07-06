# This script gets an image of the road-network from the Open-Street-Map
import osmnx as ox
import cv2


class OSMnx:
    def __init__(self):
        # from IPython.display import Image
        ox.config(log_console=True, use_cache=True)
        print("ox version:", ox.__version__)
        print("cv2 version:", cv2.__version__)
        self.configure()

    def configure(self):
        # configure
        self.img_folder = './images/'
        self.extension = '.png'
        self.pos = (34.714, 137.414)    # (latitude,longitude)
        self.dpi = 200      # dots per inch
        self.size = 2160    # img size
        self.dist = 5000    # 5000*5000[m*m]
        self.fname = '-'.join(map(str, self.pos)) + "_dist=" + str(self.dist)

    def save(self):
        fig, ax = ox.plot_figure_ground(
            point=self.pos, fig_length=71, dist=self.dist, network_type='drive', filename=self.fname,
            dpi=self.dpi, bgcolor='#ffffff', edge_color='#000000', show=False, default_width=6)
        _img = cv2.imread(self.img_folder + self.fname + self.extension)
        img = _img[0: self.size, 0: self.size]
        f_out_name = self.img_folder + self.fname + "_" + \
            str(self.size) + "x" + str(self.size) + self.extension
        cv2.imwrite(f_out_name, img)
        return f_out_name
