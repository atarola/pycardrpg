#!/usr/bin/env python

#
# Get the tiles within a radius that the unit can see.
# From: http://roguebasin.roguelikedevelopment.org/index.php?title=PythonShadowcastingImplementation
#

class FovUtil(object):
    # Multipliers for transforming coordinates to other octants, used for fov.
    mult = [
        [1,  0,  0, -1, -1,  0,  0,  1],
        [0,  1, -1,  0,  0, -1,  1,  0],
        [0,  1,  1,  0,  0, -1, -1,  0],
        [1,  0,  0,  1, -1,  0,  0, -1]
    ]

    def __init__(self, map):
        self.map = map
        self.flag = 0

    def do_fov(self, pos, radius):
        x, y = pos
        self.lit_positions = [pos]

        self.flag += 1
        for oct in range(8):
            self._cast_light(x, y, 1, 1.0, 0.0, radius,
                             FovUtil.mult[0][oct], FovUtil.mult[1][oct],
                             FovUtil.mult[2][oct], FovUtil.mult[3][oct], 0)

        return set(self.lit_positions)

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius + 1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                # Translate the dx, dy coordinates into map coordinates:
                pos = (cx + dx * xx + dy * xy, cy + dx * yx + dy * yy)

                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)

                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self._set_lit(pos)

                    if blocked:
                        # we're scanning a row of blocked squares:
                        if self._is_blocked(pos):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self._is_blocked(pos) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self._cast_light(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope

            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break

    def _is_blocked(self, pos):
        return self.map[pos].opaque

    def _set_lit(self, pos):
        self.lit_positions.append(pos)

