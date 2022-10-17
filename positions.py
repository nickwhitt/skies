import json

from skyfield.api import load

t = load.timescale().now()
jpl = load("de421.bsp")


def distance_of(source, dest):
    return source.at(t).observe(dest).apparent().distance()


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

print(json.dumps(response))
