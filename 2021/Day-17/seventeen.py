from math import floor, ceil, sqrt

# puzzle input: target area: x=96..125, y=-144..-98
target_x = (96,125)
target_y = (-144, -98)

# target_x = (20,30)
# target_y = (-10,-5)

# gauss tells us that the probe will travel to the x coordinate (xi*(xi+1))/2
# before stopping. Thus, we should set xi < +/- sqrt(8 * Xmax)/2 where Xmax is
# the max x coordinate of the target area. Positive or negative depending on
# position of the target area relative to origin. Similarly, xi > +/- sqrt(8 *
# Xmin)/2 where Xmin is the min target coord.

x_max = floor(sqrt(8 * target_x[1])/2)
x_min = ceil(sqrt(8 * target_x[0])/2)

# The y velocity gets the probe initially to a height of (y(y+1))/2. From there,
# the probe falls freely with constant acceleration of -1 y/s^2. I think it's
# safe to assume that by the time we reach our max height, the dx has become
# zero, so we can ignore it. Thus, every additional point of y velocity adds
# y + 1/2 to the height.
#
# So, now to figure out the maximum y velocity such that the probe is ever in the
# target area. The probe must take the same number of steps up as it does down,
# since its acceleration is constant. Thus, when the probe crosses zero at y, it will
# be traveling at velocity -(1 + yi) (because it has taken one additional step to get
# to zero). So the maximum that the probe can be traveling is such that:
# -(1 + yi) == Ymin, where Ymin is the lower bound on the target area. So,
# yi = -(Ymin + 1)

y_max = -(target_y[0] + 1)

# for completeness's sake

def launch_probe(dx, dy, num_steps, debug = False):
    x = 0
    y = 0
    step = 0

    positions = []

    while step < num_steps:
        x += dx
        y += dy
        positions.append((x,y))

        if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
            # just returning max_y breaks part two
            max_y = max([x[1] for x in positions])
            if max_y:
                return max_y
            else:
                return True
        elif y < target_y[0]:
            break

        if dx != 0:
            dx = dx - int(1 * dx/abs(dx))
        dy = dy - 1

        step += 1
    return False

# part one
print(launch_probe(x_max, y_max, 1000))

# part two
# not interested in being smart for this one.
#
# we can no longer trust that the x coordinate has stabilized, since we may even
# be shooting downward. So we must set the max(xi) to Xmax. The minimum required
# velocity remains the same.

x_max = target_x[1]

# the maxmimum y velocity remains the same, but the minimum is now the bottom of
# the y coordinate (e.g., shooting directly at x_max, Ymin gets you there in one step)

y_min = target_y[0]

good_shots = 0
for x in range(x_min - 1, x_max + 1):
    for y in range(y_min, y_max + 1):
        success = launch_probe(x,y,500)
        if success:
            good_shots +=1

print(good_shots)