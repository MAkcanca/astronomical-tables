from skyfield.api import load, Star
from skyfield.data import hipparcos
from skyfield.units import Angle

ts = load.timescale()
eph = load('de421.bsp')
earth = eph['earth']
mars = eph['mars']

# get the time we want to observe
t = ts.utc(2030, 1, 1)

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) # loading hipparcos catalog

# df = df[df['magnitude'] < 10] 

count = 0
for index, row in df.iterrows():
    star = Star.from_dataframe(row)
    ra, dec, _ = mars.at(t).observe(star).apparent().radec(epoch='date')
    #print(ra, dec, row["magnitude"])
    count += 1

print(count)

