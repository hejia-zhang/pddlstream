from __future__ import print_function

import cProfile
import pstats
import math
import os
import numpy as np

from examples.motion.viewer import sample_box, get_distance, is_collision_free, \
    contains, create_box, draw_solution, draw_roadmap
from pddlstream.incremental import solve_incremental
from pddlstream.utils import read, print_solution, user_input
from pddlstream.stream import from_test, from_gen_fn

def scale_distance(distance):
    return int(np.ceil(1000 * distance))

def create_problem(goal, obstacles=(), regions={}, max_distance=.5):
    directory = os.path.dirname(os.path.abspath(__file__))
    domain_pddl = read(os.path.join(directory, 'domain.pddl'))
    stream_pddl = read(os.path.join(directory, 'stream.pddl'))
    constant_map = {}

    q0 = np.array([0, 0])
    init = [
        ('Conf', q0),
        ('AtConf', q0),
    ] + [('Region', r) for r in regions]

    if isinstance(goal, str):
        goal = ('In', goal)
    else:
        init += [('Conf', goal)]
        goal = ('AtConf', goal)

    np.set_printoptions(precision=3)
    samples = []
    def region_gen(region):
        while True:
            q = sample_box(regions[region])
            samples.append(q)
            yield (q,)

    # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.419.5503&rep=rep1&type=pdf
    #d = 2
    #vol_free = (1 - 0) * (1 - 0)
    #vol_ball = math.pi * (1 ** 2)
    #gamma = 2 * ((1 + 1. / d) * (vol_free / vol_ball)) ** (1. / d)

    roadmap = []
    def connected_test(q1, q2):
        #n = len(samples)
        #threshold = gamma * (math.log(n) / n) ** (1. / d)
        threshold = max_distance
        are_connected = (get_distance(q1, q2) <= threshold) and \
                is_collision_free((q1, q2), obstacles)
        if are_connected:
            roadmap.append((q1, q2))
        return are_connected

    def distance_fn(q1, q2):
        return scale_distance(get_distance(q1, q2))

    stream_map = {
        'sample-region': from_gen_fn(region_gen),
        'connect':  from_test(connected_test),
        'distance': distance_fn,
    }

    problem = (domain_pddl, constant_map, stream_pddl, stream_map, init, goal)

    return problem, roadmap


##################################################

# TODO - algorithms that take advantage of metric space (RRT)

def main(max_time=20):
    """
    Creates and solves the 2D motion planning problem.
    """

    obstacles = [
        create_box((.5, .5), (.2, .2))
    ]
    regions = {
        'env': create_box((.5, .5), (1, 1)),
        #'goal': create_box((.8, .8), (.4, .4)),
    }

    goal = np.array([1, 1])
    #goal = 'goal'

    max_distance = 0.25 # 0.2 | 0.25 | 0.5 | 1.0
    problem, roadmap = create_problem(goal, obstacles, regions, max_distance=max_distance)

    pr = cProfile.Profile()
    pr.enable()
    solution = solve_incremental(problem, unit_costs=False, max_cost=0,
        max_time=max_time, verbose=False)
    pr.disable()
    pstats.Stats(pr).sort_stats('tottime').print_stats(10)

    print_solution(solution)
    plan, cost, evaluations = solution

    print('Plan:', plan)
    if plan is None:
        return

    # TODO: use the same viewer here
    draw_roadmap(roadmap, obstacles, regions) # TODO: do this in realtime
    user_input('Continue?')

    segments = [action[1:] for action in plan]
    draw_solution(segments, obstacles, regions)
    user_input('Finish?')


if __name__ == '__main__':
    main()
