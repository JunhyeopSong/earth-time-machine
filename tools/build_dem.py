"""Build the terrain frames used by the site from the PALEOMAP PaleoDEM 6-arc-minute netCDF grids.

  docs/hd/dem_XXX.png   0.25-degree frames (1440 x 721), one per 5 Myr
  docs/paleodem.png     1-degree atlas (360 x 181 per frame, stacked vertically)
  docs/hd/hd.json, docs/earth-data.json["dem"]["ages"]  updated age lists

usage: python3 tools/build_dem.py <dir with *.nc> <max age Ma> [--only-missing]
Elevation is stored as one byte: v = 100 + e/40 above sea level, 99 + e/60 below.
"""
import sys, os, re, glob, json
import numpy as np
from PIL import Image
import netCDF4

src, MAXAGE = sys.argv[1], int(sys.argv[2])
only_missing = '--only-missing' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
W, H = 1440, 721

def enc(e):
    v = np.where(e > 0, 100 + e / 40, 99 + e / 60)
    return np.clip(np.round(v), 0, 255).astype(np.uint8)

files = {}
for f in glob.glob(os.path.join(src, '**', '*.nc'), recursive=True):
    m = re.search(r'_(\d+(?:\.\d+)?)Ma\.nc$', os.path.basename(f))
    if m and float(m.group(1)) <= MAXAGE and float(m.group(1)) % 5 == 0:
        files[int(float(m.group(1)))] = f
ages = sorted(files)
assert ages == list(range(0, MAXAGE + 1, 5)), 'missing ages: %s' % sorted(set(range(0, MAXAGE + 1, 5)) - set(ages))

lon_t = np.arange(W) * 0.25 - 180.0
lat_t = 90.0 - np.arange(H) * 0.25
atlas = []
for a in ages:
    out = os.path.join(DOCS, 'hd', 'dem_%03d.png' % a)
    if only_missing and os.path.exists(out):
        g = np.array(Image.open(out)).astype(float)
        g = np.where(g >= 100, (g - 100) * 40 + 20, (g - 99) * 60)
    else:
        ds = netCDF4.Dataset(files[a])
        lon = ds.variables['longitude'][:].astype(float); lat = ds.variables['latitude'][:].astype(float)
        z = np.ma.filled(ds.variables['z'][:].astype(float), np.nan); ds.close()
        if lat[0] > lat[-1]: lat = lat[::-1]; z = z[::-1]
        fx = np.interp(lon_t, lon, np.arange(len(lon))); fy = np.interp(lat_t, lat, np.arange(len(lat)))
        x0 = np.floor(fx).astype(int); y0 = np.floor(fy).astype(int)
        x1 = np.minimum(x0 + 1, len(lon) - 1); y1 = np.minimum(y0 + 1, len(lat) - 1)
        tx = (fx - x0)[None, :]; ty = (fy - y0)[:, None]
        g = (z[y0][:, x0] * (1 - tx) * (1 - ty) + z[y0][:, x1] * tx * (1 - ty) + z[y1][:, x0] * (1 - tx) * ty + z[y1][:, x1] * tx * ty)
        g = np.where(np.isnan(g), -4000, np.clip(g, -6000, 6200))
        Image.fromarray(enc(g), 'L').save(out, optimize=True)
        print('frame', a, os.path.getsize(out) // 1024, 'KB')
    # 1-degree frame: average of the 0.25-degree cells around each whole degree
    k = np.ones(5) / 5
    sm = np.apply_along_axis(lambda r: np.convolve(np.concatenate([r[-2:], r, r[:2]]), k, 'valid'), 1, g)
    sm = np.apply_along_axis(lambda c: np.convolve(np.concatenate([c[:1], c[:1], c, c[-1:], c[-1:]]), k, 'valid'), 0, sm)
    atlas.append(enc(sm[::4, ::4]))

Image.fromarray(np.vstack(atlas), 'L').save(os.path.join(DOCS, 'paleodem.png'), optimize=True)
hd = json.load(open(os.path.join(DOCS, 'hd', 'hd.json'))); hd['ages'] = ages
json.dump(hd, open(os.path.join(DOCS, 'hd', 'hd.json'), 'w'))
d = json.load(open(os.path.join(DOCS, 'earth-data.json'))); d['dem']['ages'] = ages
json.dump(d, open(os.path.join(DOCS, 'earth-data.json'), 'w'), separators=(',', ':'))
print('ages', ages[0], '...', ages[-1], len(ages), 'atlas', os.path.getsize(os.path.join(DOCS, 'paleodem.png')) // 1024, 'KB')
