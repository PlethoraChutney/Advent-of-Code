with open('test.txt', 'r') as f:
    particles = [x.rstrip() for x in f]

min_accel = 1e9

def calc_length(accel):
    return sum(x**2 for x in accel)**0.5

min_accel_particles = {}

for i in range(len(particles)):
    particle = particles[i]
    # rather arcane splits to get the third set of ints
    accel = particle.split('<')[-1][:-1].split(',')
    accel = [int(x) for x in accel]
    accel = calc_length(accel)

    if accel < min_accel:
        min_accel = accel
        min_accel_particles = {i: particle}

    elif accel == min_accel:
        min_accel_particles[i] = particle

print('Part one:', min_accel_particles)

class Particle(object):
    def __init__(self, line) -> None:
        position, vel, accel = line.split(', ')
        position = [int(x) for x in position[3:-1].split(',')]
        vel = [int(x) for x in vel[3:-1].split(',')]
        accel = [int(x) for x in accel[3:-1].split(',')]

        self.position_vec = position
        self.vel_vec = vel
        self.accel_vec = accel

    def position(self, t):
        pos = [None, None, None]
        for coord in (0, 1, 2):
            pos[coord] = self.accel_vec[coord] * t**2 + self.vel_vec[coord] * t + self.position_vec[coord]
        
        return pos

parts = {x: Particle(particles[x]) for x in range(len(particles))}

t = 0
parts[0].position(0)

while True:
    to_remove = []
    for i in range(len(parts)):
        if i in to_remove:
            continue
        test_pos = parts[i].position(t)
        for j in range(i+1, len(parts)):
            if parts[j].position(t) == test_pos:
                to_remove.extend((i,j))

    to_remove = set(to_remove)
    for i in to_remove:
        del parts[i]

    t += 1
    if t % 10 == 0:
        print(f'At t {t}, {len(parts)} particles remain', end = '\r')