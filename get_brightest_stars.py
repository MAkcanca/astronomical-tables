from math import log10
from skyfield.api import load, Star
from skyfield.data import hipparcos
from skyfield.units import Angle

ts = load.timescale()
eph = load('de440s.bsp')
earth = eph[3]
mars = eph[4]
sun = eph['Sun']

# get the time we want to observe
t = ts.utc(2030, 1, 1)

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f) # loading hipparcos catalog

df = df[df['magnitude'] < 4]
df = df[df['ra_degrees'].notnull()]

def get_brightest_stars():
    stars = []
    for index, row in df.iterrows():
        star = Star.from_dataframe(row)
        earth_dis = earth.at(t).observe(star).distance().au
        mars_dis = mars.at(t).observe(star).distance().au
        distance_modulus = 5 * log10(earth_dis) - 5 * log10(mars_dis)
        earth_mag = row["magnitude"]
        mars_mag = earth_mag + distance_modulus
        ra, dec, _ = mars.at(t).observe(star).apparent().radec(epoch='date')
        stars.append([ra._degrees, dec._degrees, mars_mag])
    return stars

def get_brightest_stars_for_earth():
    stars = []
    for index, row in df.iterrows():
        star = Star.from_dataframe(row)
        ra, dec, _ = earth.at(t).observe(star).apparent().radec(epoch='date')
        stars.append([ra._degrees, dec._degrees, row['magnitude']])
    return stars

def get_sun():
    astrometric = mars.at(t).observe(sun)
    ra_sun, dec_sun, distance = astrometric.radec()
    print('The sun is located at RA/DEC',ra_sun._degrees ,dec_sun._degrees ,'on',t.utc_strftime())
    # get the distance between the observer (Mars) and the Sun
    d_mars = mars.at(t).observe(sun).apparent().distance().au 
    d_earth = earth.at(t).observe(sun).apparent().distance().au

    # visual magnitude of sun from earth
    V_earth = -26.71

    #sun magnitude from mars
    distance_modulus = 5 * log10(d_mars) - 5 * log10(d_earth)
    V_mars = V_earth + distance_modulus
    print(V_mars)
    return [ra_sun._degrees, dec_sun._degrees, V_mars]





if __name__ == '__main__':
    get_sun()
    #print(get_brightest_stars())
