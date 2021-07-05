from OSMnx import OSMnx
from CalcFractalDim import fractal_dimension as fd

fname = OSMnx().save()
# fname = "./images/syeru.png"
d = fd(fname, "./result/fractalDim.csv")
d.run()
d.output()
print("Fractal Dimentioin:", d.get_dim())
