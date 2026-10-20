// Buoy Math engine: density from mass and volume, the share of a freely floating body under the surface, and the spare lift before it sits awash. Exact integers (hundredths of a kg, hundredths of a liter, whole kg/m3), results rounded half up.
function _p(t, err, intDigits, places, lo, hi) { // decimal text -> integer scaled by 10^places
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _MASS = "the mass must be from 0.01 to 100000 kg with at most two decimal places";
var _VOL = "the volume must be from 0.01 to 100000 L with at most two decimal places";
var _FLUID = "the fluid density must be a whole number from 1 to 5000 kg/m³";
function _pf(t) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(_FLUID);
  var v = parseInt(t, 10);
  if (v < 1 || v > 5000) throw new Error(_FLUID);
  return v;
}
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _kg(m) { return _dec(m, 2) + " kg"; }
function _l(v) { return _dec(v, 2) + " L"; }
function _in(mass, vol, fluid) {
  return { m: _p(mass, _MASS, 6, 2, 1, 10000000), v: _p(vol, _VOL, 6, 2, 1, 10000000), f: _pf(fluid) };
}
function _dens(m, v) { return _hu(1000 * m, v); } // kg/m3, half up

function densityTruth(mass, vol, fluid) {
  var p = _in(mass, vol, fluid), d = _dens(p.m, p.v);
  var s = "A " + _kg(p.m) + " body in " + _l(p.v) + " has a density of " + d + " kg/m³. The fluid is " + p.f + " kg/m³, so ";
  var c = 1000 * p.m - p.v * p.f;
  if (c === 0) return s + "the body is exactly as dense as the fluid.";
  return s + (c < 0 ? "the body is less dense than the fluid." : "the body is denser than the fluid.");
}
function draftTruth(mass, vol, fluid) {
  var p = _in(mass, vol, fluid), c = 1000 * p.m - p.v * p.f;
  var s = "A " + _kg(p.m) + " body in " + _l(p.v) + ", in a " + p.f + " kg/m³ fluid: ";
  if (c === 0) return s + "its density matches the fluid's, so it sits fully submerged, neither rising nor needing support.";
  if (c > 0) return s + "it is denser than the fluid, so the fluid alone does not hold it up.";
  var under = _hu(100000 * p.m, p.v * p.f); // percent of volume submerged
  return s + under + "% of its volume sits under the surface and " + (100 - under) + "% above it.";
}
function loadTruth(mass, vol, fluid) {
  var p = _in(mass, vol, fluid);
  var cap = _hu(p.f * p.v, 1000); // hundredths of a kg the fluid buoys at full submersion
  var s = "Fully under, the " + p.f + " kg/m³ fluid buoys " + _kg(cap) + " against the " + _kg(p.m) + " body. ";
  if (cap === p.m) return s + "That exactly matches its mass, so it sits awash with nothing to spare.";
  if (cap > p.m) return s + "That leaves " + _kg(cap - p.m) + " of spare lift before it sits awash.";
  return s + "That is " + _kg(p.m - cap) + " short of holding it up.";
}
