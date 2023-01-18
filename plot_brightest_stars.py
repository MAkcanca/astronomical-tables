from matplotlib import pyplot as plt
from skyfield.data import hipparcos
from skyfield.units import Angle
from skyfield.api import load, Star

ts = load.timescale()
eph = load('de421.bsp')
earth = eph['earth']
mars = eph['mars']

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) # loading hipparcos catalog

df = df[df['magnitude'] <= 2.5]

bright_stars = Star.from_dataframe(df)
t = ts.utc(2030, 1, 1)
astrometric = mars.at(t).observe(bright_stars)
ra, dec, distance = astrometric.radec()

fig, ax = plt.subplots()
ax.scatter(ra.hours, dec.degrees, 60 - df['magnitude'], 'k')
print(sum(ra.hours) / len(ra.hours), sum(dec.degrees) / len(dec.degrees))
astrometric = earth.at(t).observe(bright_stars)
ra, dec, distance = astrometric.radec()
ax.scatter(ra.hours, dec.degrees, 20 - df['magnitude'], color=['red'])
print(sum(ra.hours) / len(ra.hours), sum(dec.degrees) / len(dec.degrees))
ax.set_xlim(7.0, 4.0)
ax.set_ylim(-20, 20)
ax.grid(True)
ax.set(title='The brightest stars in Orion, 2030, Earth and Mars, mag < 2.5')
fig.savefig('bright_stars_mars.png')
