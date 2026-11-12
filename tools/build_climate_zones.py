#!/usr/bin/env python3
"""Köppen climate zones of the last 540 million years for the "environment" map style (docs/climate.png, climate.json).

Usage: python3 tools/build_climate_zones.py <folder with <age>Ma_Pohletal2022_DIB_PhaneroContinentalClimate.nc>
         <1991_2020/koppen_geiger_0p5.tif> docs
       (needs numpy and Pillow)

Source: Pohl, A., Wong Hearing, T., Franc, A., Sepulchre, P. & Scotese, C.R. (2022) Dataset of Phanerozoic continental
climate and Köppen–Geiger climate classes. Data in Brief 43, 108424, doi:10.1016/j.dib.2022.108424 — FOAM (slab ocean)
on the Scotese & Wright PALEOMAP paleogeography, 28 slices every 20 Myr from 540 Ma to today, 2.8° × 1.4°.
Data: Zenodo 6620748 (doi:10.5281/zenodo.6620748), CC BY 4.0. FOAM runs have no ice sheets, so polar land is cold or
tundra even today.

Today (0 Ma) uses the observed map instead: Beck, H.E. et al. (2023) High-resolution (1 km) Köppen-Geiger maps for
1901–2099 based on constrained CMIP6 projections. Scientific Data 10, 724, doi:10.1038/s41597-023-02549-6 — 1991–2020,
0.5° (koppen_geiger_0p5.tif), figshare 21789074, CC BY 4.0. Beck codes: 1–2 Af Am, 3 Aw, 4–5 BW, 6–7 BS, 8–16 C,
17–28 D, 29 ET, 30 EF. The app blends from it to the 20 Ma model slice, and adds the ice of Antarctica (from 34 Ma)
and Greenland (from 2.7 Ma) that the ice-free model runs lack.

Köppen codes in the files (Table 3 of the article) → 8 groups that read on a small globe:
  1 tropical rainforest  Af 13, Am 12          5 temperate  Cf 8, Cs 7, Cw 6
  2 savanna              Aw 11                 6 cold       Df 5, Ds 4, Dw 3
  3 desert               BW 9                  7 tundra     ET 1
  4 steppe               BS 10                 8 ice cap    EF 2
Sea cells take the class of the nearest land cell of the same slice (great-circle distance) (the app decides what is land from its own
elevation frames). The 2.8° cells are upsampled to 0.5° by softening each group's share (1-2-1 blur), interpolating it bilinearly and taking the
largest, so borders are smooth lines instead of steps.

Output: climate.png — 720 × (360 × 28) 8-bit grey, value = group 1–8, slices from today (top) to 540 Ma, rows 89.75°N …
89.75°S, columns from 179.75°W; climate.json — slice ages (Ma) and the grid.
"""
import glob
import json
import os
import re
import struct
import sys

import numpy as np
from PIL import Image

src, beck, out = sys.argv[1], sys.argv[2], sys.argv[3]
GROUP = np.zeros(16, np.uint8)
for k, v in {13: 1, 12: 1, 11: 2, 9: 3, 10: 4, 8: 5, 7: 5, 6: 5, 5: 6, 4: 6, 3: 6, 1: 7, 2: 8}.items():
    GROUP[k] = v
NG = 8


def read_nc(path):
    """minimal reader for classic netCDF: {name: array} for fixed-size numeric variables"""
    b = open(path, 'rb').read(); assert b[:3] == b'CDF'; ver = b[3]; p = 4
    def i4():
        nonlocal p; v = struct.unpack('>i', b[p:p + 4])[0]; p += 4; return v
    def off():
        nonlocal p
        if ver == 2: v = struct.unpack('>q', b[p:p + 8])[0]; p += 8; return v
        return i4()
    def name():
        nonlocal p; n = i4(); s = b[p:p + n].decode('latin-1'); p += (n + 3) // 4 * 4; return s
    SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 4, 6: 8}; FMT = {1: 'b', 2: 'c', 3: 'h', 4: 'i', 5: 'f', 6: 'd'}
    def atts():
        nonlocal p; tag = i4(); n = i4()
        if tag == 0: return
        for _ in range(n): name(); t = i4(); cnt = i4(); p += (cnt * SIZE[t] + 3) // 4 * 4
    i4(); tag = i4(); nd = i4(); dims = [(name(), i4()) for _ in range(nd if tag else 0)]
    atts(); tag = i4(); nv = i4(); res = {}
    for _ in range(nv if tag else 0):
        vn = name(); n = i4(); ids = [i4() for _ in range(n)]; atts(); t = i4(); i4(); begin = off()
        shape = [dims[k][1] for k in ids]
        if any(s == 0 for s in shape): continue
        cnt = int(np.prod(shape)) if shape else 1
        if t in (3, 4, 5, 6): res[vn] = np.array(struct.unpack('>%d%s' % (cnt, FMT[t]), b[begin:begin + cnt * SIZE[t]])).reshape(shape)
    return res


def fill(a, lat, lon):
    """sea cells take the class of the nearest land cell (great-circle distance), so the fill has no grid streaks"""
    la, lo = np.radians(lat)[:, None] * np.ones((1, len(lon))), np.ones((len(lat), 1)) * np.radians(lon)[None, :]
    xyz = np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1).reshape(-1, 3)
    flat = a.ravel().copy(); land = np.flatnonzero(flat > 0); sea = np.flatnonzero(flat == 0)
    L = xyz[land]
    for i in range(0, len(sea), 2048):
        q = xyz[sea[i:i + 2048]]
        flat[sea[i:i + 2048]] = flat[land[np.argmax(q @ L.T, axis=1)]]
    return flat.reshape(a.shape)


def soften(I):
    """1-2-1 blur in both directions (longitude wraps), for rounder borders"""
    I = (np.roll(I, 1, 1) + 2 * I + np.roll(I, -1, 1)) / 4
    up = np.vstack([I[:1], I[:-1]]); dn = np.vstack([I[1:], I[-1:]])
    return (up + 2 * I + dn) / 4


W, H, STEP = 720, 360, 0.5
files = {int(re.match(r'(\d+)Ma_', os.path.basename(f)).group(1)): f for f in glob.glob(f'{src}/*Ma_Pohletal2022_DIB_PhaneroContinentalClimate.nc')}
ages = sorted(files)
assert len(ages) == 28, ages
slices = []
for ma in ages:
    d = read_nc(files[ma])
    lat, lon, k = d['lat'], d['lon'], d['koppen']          # koppen is stored [lon, lat]
    assert k.shape == (len(lon), len(lat)) and lat[0] < 0
    k = np.where((k > 0) & (k < 16), np.rint(k), 0).astype(int).T[::-1]   # → [lat north first, lon]
    LAT = lat[::-1]
    lon180 = ((lon + 180) % 360) - 180; order = np.argsort(lon180); lon_s = lon180[order]
    g = fill(GROUP[k][:, order], LAT, lon_s)
    # target cell centres
    tl = 89.75 - STEP * np.arange(H); tn = -179.75 + STEP * np.arange(W)
    fy = np.interp(-tl, -LAT, np.arange(len(LAT)))           # fractional source row
    dl = lon_s[1] - lon_s[0]
    fx = (tn - lon_s[0]) / dl                               # fractional source column (wraps)
    y0 = np.clip(np.floor(fy).astype(int), 0, len(LAT) - 1); y1 = np.clip(y0 + 1, 0, len(LAT) - 1); wy = (fy - np.floor(fy))[:, None]
    x0 = np.floor(fx).astype(int); wx = (fx - x0)[None, :]; x0 %= g.shape[1]; x1 = (x0 + 1) % g.shape[1]
    best = np.zeros((H, W)); arg = np.zeros((H, W), np.uint8)
    for c in range(1, NG + 1):
        I = soften((g == c).astype(float))
        v = (I[y0][:, x0] * (1 - wx) + I[y0][:, x1] * wx) * (1 - wy) + (I[y1][:, x0] * (1 - wx) + I[y1][:, x1] * wx) * wy
        m = v > best; best[m] = v[m]; arg[m] = c
    slices.append(arg)
    print(ma, 'Ma', np.bincount(GROUP[k][GROUP[k] > 0].ravel(), minlength=9)[1:])

# today: the observed 1991–2020 map on land (same 0.5° grid from 180°W, 90°N), the model's filled value at sea
BECK = np.zeros(32, np.uint8)
for k in range(1, 31):
    BECK[k] = 1 if k <= 2 else 2 if k == 3 else 3 if k <= 5 else 4 if k <= 7 else 5 if k <= 16 else 6 if k <= 28 else 7 if k == 29 else 8
obs = np.array(Image.open(beck)); assert obs.shape == (H, W), obs.shape
og = BECK[np.clip(obs, 0, 31)]
slices[0] = np.where(og > 0, og, slices[0]).astype(np.uint8)
print('0 Ma observed (Beck 2023)', np.bincount(og.ravel(), minlength=9)[1:])

Image.fromarray(np.vstack(slices), 'L').save(f'{out}/climate.png', optimize=True)
json.dump({'source': 'Pohl et al. 2022, Data in Brief 43, 108424 (doi:10.1016/j.dib.2022.108424), FOAM Köppen–Geiger classes on '
                     'Scotese & Wright paleogeography, Zenodo 6620748, CC BY 4.0; today: Beck et al. 2023 (Sci. Data 10, 724) 1991–2020, CC BY 4.0; grouped into 8, sea filled from the nearest '
                     'land class, upsampled to 0.5° with smooth borders.',
           'groups': ['tropical rainforest', 'savanna', 'desert', 'steppe', 'temperate', 'cold', 'tundra', 'ice cap'],
           'ma': ages, 'rows': H, 'cols': W, 'north': 89.75, 'west': -179.75, 'step': STEP},
          open(f'{out}/climate.json', 'w'), separators=(',', ':'))
