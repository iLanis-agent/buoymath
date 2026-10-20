# Buoy Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

MASS = "the mass must be from 0.01 to 100000 kg with at most two decimal places"
VOL = "the volume must be from 0.01 to 100000 L with at most two decimal places"
FLUID = "the fluid density must be a whole number from 1 to 5000 kg/m³"

def p(t, err, places, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > places)):
        raise ValueError(err)
    v = int(parts[0]) * 10**places + int(parts[1].ljust(places, "0") or 0) if len(parts) == 2 else int(parts[0]) * 10**places
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def pf(t):
    t = t.strip()
    if not t.isdigit() or len(t) > 4:
        raise ValueError(FLUID)
    v = int(t)
    if v < 1 or v > 5000:
        raise ValueError(FLUID)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v, places):
    base = 10**places
    s, f = str(v // base), str(v % base).rjust(places, "0").rstrip("0")
    return s + "." + f if f else s

def kg(m): return dec(m, 2) + " kg"
def l(v): return dec(v, 2) + " L"

def inn(mass, vol, fluid):
    return p(mass, MASS, 2, 1, 10000000), p(vol, VOL, 2, 1, 10000000), pf(fluid)

def densityTruth(mass, vol, fluid):
    m, v, f = inn(mass, vol, fluid)
    d = hu(1000 * m, v)
    s = "A " + kg(m) + " body in " + l(v) + " has a density of " + str(d) + " kg/m³. The fluid is " + str(f) + " kg/m³, so "
    c = 1000 * m - v * f
    if c == 0: return s + "the body is exactly as dense as the fluid."
    return s + ("the body is less dense than the fluid." if c < 0 else "the body is denser than the fluid.")

def draftTruth(mass, vol, fluid):
    m, v, f = inn(mass, vol, fluid)
    c = 1000 * m - v * f
    s = "A " + kg(m) + " body in " + l(v) + ", in a " + str(f) + " kg/m³ fluid: "
    if c == 0: return s + "its density matches the fluid's, so it sits fully submerged, neither rising nor needing support."
    if c > 0: return s + "it is denser than the fluid, so the fluid alone does not hold it up."
    under = hu(100000 * m, v * f)
    return s + str(under) + "% of its volume sits under the surface and " + str(100 - under) + "% above it."

def loadTruth(mass, vol, fluid):
    m, v, f = inn(mass, vol, fluid)
    cap = hu(f * v, 1000)
    s = "Fully under, the " + str(f) + " kg/m³ fluid buoys " + kg(cap) + " against the " + kg(m) + " body. "
    if cap == m: return s + "That exactly matches its mass, so it sits awash with nothing to spare."
    if cap > m: return s + "That leaves " + kg(cap - m) + " of spare lift before it sits awash."
    return s + "That is " + kg(m - cap) + " short of holding it up."

FNS = {"densityTruth": densityTruth, "draftTruth": draftTruth, "loadTruth": loadTruth}

cases = []
masses = ["0.01", "12", "20", "250", "100000"]
vols = ["0.01", "20", "999.99", "100000"]
fluids = ["1", "1000", "5000"]
for m in masses:
    for v in vols:
        for f in fluids:
            cases.append((m, v, f))
cases += [("100000", "0.01", "5000"), ("20", "20", "1000"), ("12", "20", "600"), ("1", "1", "1000")]
out = []
for args in cases:
    for name, fn in FNS.items():
        try:
            exp = fn(*args)
        except ValueError as e:
            exp = "ERR:" + str(e)
        out.append({"fn": name, "args": list(args), "expected": exp})
errs = [("0", "20", "1000"), ("100001", "20", "1000"), ("12", "0", "1000"), ("12", "100001", "1000"),
        ("12", "20", "0"), ("12", "20", "5001"), ("12", "20", "10.5"), ("1.234", "20", "1000"),
        ("abc", "20", "1000"), ("12", "", "1000")]
for args in errs:
    for name, fn in FNS.items():
        try:
            exp = fn(*args)
        except ValueError as e:
            exp = "ERR:" + str(e)
        out.append({"fn": name, "args": list(args), "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
