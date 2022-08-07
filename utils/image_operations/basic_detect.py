import numpy as np
import crossbow_manga_lib
from PIL import Image

def RGB2YUV(rgb):
    m = np.array([[0.29900, -0.16874, 0.50000],
                  [0.58700, -0.33126, -0.41869],
                  [0.11400, 0.50000, -0.08131]])
    yuv = np.dot(rgb, m)
    yuv[:, :, 1:] += 128.0
    return yuv

def magic_wand(rgb: 'np.array', pos_x: int, pos_y: int):
    # input: np.array(np.uint8)[w,h,3]-> out:np.array(np.uint8)[w,h,3] + Image()
    yuv = RGB2YUV(rgb)
    luma = yuv[:, :, 0]
    luma = np.minimum(np.maximum(np.round(luma.astype(np.int16)), 0), 255)
    f_y, f_x = luma.shape
    vmax = max(f_y, f_x) * 0.03
    rand_pos_orn = (np.random.normal(0, 20, size=(121, 2)) * vmax / 30).astype(np.int16)
    rand_pos = rand_pos_orn.copy()
    rand_pos[:, 0] += pos_x
    rand_pos[:, 1] += pos_y
    rand_pos[rand_pos < 0] = 0
    lim_x = rand_pos > (f_x - 1)
    lim_x[:, 1] = False
    rand_pos[lim_x] = f_x - 1
    lim_y = rand_pos > (f_y - 1)
    lim_y[:, 0] = False
    rand_pos[lim_y] = f_y - 1
    rand_color = luma[rand_pos[:, 1], rand_pos[:, 0]]
    histogram = [0, ] * 256
    for val in rand_color.tolist():
        histogram[val] += 1
    majority = histogram.index(max(histogram))
    rand_distance = np.sqrt(np.sum(np.power(rand_pos_orn, 2), axis=1)).reshape((-1, 1))
    rand_combat = np.hstack([rand_pos, rand_distance, rand_color.reshape((-1, 1))])
    rand_combat = rand_combat[rand_combat[:, 2].argsort()].astype(np.int16)
    for s_x, s_y, _, color in rand_combat:
        if (color - majority) < 0.1:
            break
    targ = luma.copy()
    targ[:, :] = 0

    avg_color = crossbow_manga_lib.region_grow(luma, targ, s_x, s_y, color, 15)
    if np.max(targ) <= 0:
        return Image.fromarray(rgb), None;
    # else
    for y1, _ in enumerate(targ):
        if np.max(_) > 0:
            break
    for y2, _ in enumerate(targ[::-1, :]):
        if np.max(_) > 0:
            break
    y2 = f_y - 1 - y2
    for x1, _ in enumerate(targ.T):
        if np.max(_) > 0:
            break
    for x2, _ in enumerate((targ.T)[::-1, :]):
        if np.max(_) > 0:
            break
    x2 = f_x - 1 - x2
    cut_img = rgb[y1:y2, x1:x2, :].copy()

    # find avg rgb color
    tmask = targ > 0
    targ_rgb = rgb[tmask]
    new_color = np.array([
        np.argmax(np.bincount(targ_rgb[:, 0])),
        np.argmax(np.bincount(targ_rgb[:, 1])),
        np.argmax(np.bincount(targ_rgb[:, 2])),
    ])
    rgb[tmask] = new_color
    return rgb, Image.fromarray(cut_img)