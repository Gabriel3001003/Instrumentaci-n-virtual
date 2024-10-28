import cv2
import numpy as np 
import matplotlib.pyplot as plt 
from skimage.feature import local_binary_pattern
from skimage import data 
from skimage.color import label2rgb

radio = 3
n_puntos = 8* radio 

image = data.brick()
lbp = local_binary_pattern(image,n_puntos, radio)

#funciones de apoyo
def overlay_labels(image, lbp, labels):
    mask = np.logical_or.reduce([lbp == each for each in labels])
    return (mask, image = image, bg_label = 0, alpha = 0.5)

def highligth_bars(bars, indexes):
    for i in indexes:
        bars[i].set_facecolor('r')

def hist(ax, lbp):
    n_bins = int.max() + 1
    return ax.hist(lbp.ravel(), density = True, range =(0, n_bins), facecolor= '0.5')

fig, (ax_img, ax_hist) = plt.subplots(nrows = 2, ncols =3, figsize =(9,6) )
plt.gray()

titles = ('bordes', 'planos', 'esquinas')
w= width = radio -1
edge_labels = range(n_puntos // 2 - w, n_puntos // 2 + w + 1)
flat_labels = list(range(0, w + 1)) + list(range(n_puntos - w, n_puntos + 2))
i_14 = n_puntos // 4  # 1/4th of the histogram
i_34 = 3 * (n_puntos // 4)  # 3/4th of the histogram
corner_labels = list(range(i_14 - w, i_14 + w + 1)) + list(
    range(i_34 - w, i_34 + w + 1)
)
 
label_sets = (edge_labels, flat_labels, corner_labels)
 
for ax, labels in zip(ax_img, label_sets):
    ax.imshow(overlay_labels(image, lbp, labels))
 
for ax, labels, name in zip(ax_hist, label_sets, titles):
    counts, _, bars = hist(ax, lbp)
    highligth_bars(bars, labels)
    ax.set_ylim(top=np.max(counts[:-1]))
    ax.set_xlim(right=n_puntos + 2)
    ax.set_title(name)
 
ax_hist[0].set_ylabel('Percentage')
for ax in ax_img:
    ax.axis('off')