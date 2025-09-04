# perlin.py
# Perlin noise generator.
# Based on the implementation by Casey Duncan, found at:
# https://github.com/caseman/noise/blob/master/noise.py
# Which is under the MIT license.
# Adapted for simplicity and to be a standalone module.

import math
import random

class PerlinNoise:
    """
    A standalone Perlin Noise generator.
    """
    def __init__(self, octaves=1, seed=None):
        if seed is None:
            seed = random.randint(0, 1000000)
        self.octaves = octaves
        self.p = list(range(256))
        random.seed(seed)
        random.shuffle(self.p)
        self.p += self.p

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a, b, x):
        return a + x * (b - a)

    def _grad(self, hash_val, x, y, z):
        h = hash_val & 15
        u = x if h < 8 else y
        v = y if h < 4 else (x if h in (12, 14) else z)
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def noise(self, x, y, z=0.0):
        """
        Calculates the Perlin noise value for a given 2D or 3D coordinate.
        """
        total = 0.0
        frequency = 1.0
        amplitude = 1.0
        max_amplitude = 0.0

        for _ in range(self.octaves):
            total += self._noise(x * frequency, y * frequency, z * frequency) * amplitude
            max_amplitude += amplitude
            amplitude *= 0.5  # persistence
            frequency *= 2.0  # lacunarity

        return total / max_amplitude if max_amplitude > 0 else 0

    def _noise(self, x, y, z):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        Z = int(math.floor(z)) & 255

        x -= math.floor(x)
        y -= math.floor(y)
        z -= math.floor(z)

        u = self._fade(x)
        v = self._fade(y)
        w = self._fade(z)

        p = self.p
        A = p[X] + Y
        AA = p[A] + Z
        AB = p[A + 1] + Z
        B = p[X + 1] + Y
        BA = p[B] + Z
        BB = p[B + 1] + Z

        return self._lerp(
            self._lerp(
                self._lerp(self._grad(p[AA], x, y, z), self._grad(p[BA], x - 1, y, z), u),
                self._lerp(self._grad(p[AB], x, y - 1, z), self._grad(p[BB], x - 1, y - 1, z), u),
                v,
            ),
            self._lerp(
                self._lerp(self._grad(p[AA + 1], x, y, z - 1), self._grad(p[BA + 1], x - 1, y, z - 1), u),
                self._lerp(self._grad(p[AB + 1], x, y - 1, z - 1), self._grad(p[BB + 1], x - 1, y - 1, z - 1), u),
                v,
            ),
            w,
        )
