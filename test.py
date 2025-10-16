import datetime
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz


m31 = SkyCoord(ra=42.13*u.degree, dec=54.17*u.degree, frame='icrs')
location = EarthLocation(lon=55.05298802955941*u.deg, lat=82.90143917023106*u.deg, height=200*u.m)

time = datetime.datetime.now()
time = Time(time)

altaz_frame = AltAz(obstime=time, location=location)
m31altaz = m31.transform_to(altaz_frame)
print(m31altaz.az.degree, m31altaz.alt.degree)