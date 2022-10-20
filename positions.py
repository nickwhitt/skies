import json
from datetime import datetime, timezone

from pymemcache import serde
from pymemcache.client.base import Client
from skyfield.api import load

cache = Client("localhost", serde=serde.pickle_serde)

t = load.timescale().from_datetime(
    datetime.now(timezone.utc).replace(second=30, microsecond=0)
)


def distance_of(source, dest):
    return source.at(t).observe(dest).apparent().distance()


response: list[dict] = cache.get(t.utc_iso())
if response is None:
    jpl = load("de421.bsp")

    response = [{"earth": {"sun": distance_of(jpl["earth"], jpl["sun"]).km}}]
    for p in ("mercury", "venus", "mars"):
        response.append(
            {
                p: {
                    "earth": distance_of(jpl["earth"], jpl[p]).km,
                    "sun": distance_of(jpl[p], jpl["sun"]).km,
                }
            }
        )

    cache.set(t.utc_iso(), response, expire=60)

print(t.utc_iso(), json.dumps(response))
