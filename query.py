from math import pi
from astroquery.jplhorizons import Horizons
import cairocffi as cairo

arcadia_planitia = {'lon': -183,
                     'lat': 48,
                     'elevation': -2,
                     'body': '499'}
obj = Horizons(id='SUN', location=arcadia_planitia, epochs={'start':'2030-01-01', 'stop':'2035-01-01','step':'10d'})
eph = obj.elements(refplane='ecliptic')
print(eph)

width, height = 640, 480

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

ctx.set_source_rgb(1,1,1)
ctx.paint()

ctx.set_source_rgb(1,0,0)

# functions to map RA and Declination to planar X and Y
def RA_to_x(RA):
    return (RA/360)*width
def DEC_to_y(DEC):
    return height-(((DEC + 90)/180)*height)

for i in range(0, len(eph), 5):
    sun_ra_deg = eph["RA"][i]
    sun_dec_deg = eph["DEC"][i]

    sun_x = RA_to_x(sun_ra_deg)
    sun_y = DEC_to_y(sun_dec_deg)

    ctx.arc(sun_x, sun_y, 1, 0, 2*pi)
    ctx.fill()

surface.write_to_png("example.png")

print(eph["RA"][-1], eph["DEC"][-1], eph["V"][-1])