# Buoy Math

Buoyancy arithmetic. A 12 kg body in 20 L has a density of 600 kg/m³. In a 1000 kg/m³ fluid it sits 60% under the surface and can take 8 kg more before it is awash.

## What it computes

- **The density truth** - density from a body's mass (0.01 to 100000 kg) and volume (0.01 to 100000 L) against the fluid's density (1 to 5000 kg/m³), and which is denser.
- **The draft truth** - the share of a freely floating body's volume under the surface, or a plain statement that the fluid alone does not hold it up.
- **The lift truth** - what the fluid buoys at full submersion and the spare lift before the body sits awash, or how far short it falls.

## Boundary

Arithmetic only. The mass, volume and fluid density are the owner's own entries, every body is treated as uniform and every fluid as still. It has not seen any setup and does not know a body's shape, balance, leaks or condition, the water's movement, or how anything is loaded or rigged, and it gives no verdict that anything is safe to float, ride, tow or load. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a kg and of a liter, whole kg/m³, half-up rounding).
- `oracle.py` - the Python mirror (Fractions of the entered numbers) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/buoymath/
Repo: https://github.com/iLanis-agent/buoymath
