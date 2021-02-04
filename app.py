from datetime import datetime, timedelta

import pytz
from skyfield.api import EarthSatellite, load, wgs84


ccsfs = wgs84.latlon(+28.4889, -80.5778)
tz = pytz.timezone("US/Eastern")

satellite = EarthSatellite(
    "1 25544U 98067A   21034.93850296  .00000995  00000-0  26262-4 0  9997",
    "2 25544  51.6455 281.7841 0002223 334.9147 115.4374 15.48938034267947",
)

position = satellite - ccsfs

now = datetime.now(pytz.utc)
t = load.timescale().from_datetimes([now, now + timedelta(hours=24)])

t, events = satellite.find_events(ccsfs, *t)
for ti, event in zip(t, events):
    alt, az, distance = position.at(ti).altaz()
    print(
        ti.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S %Z"),
        ("rises", "culminates", "sets")[event],
        alt if alt.degrees > 1 else "",
    )
