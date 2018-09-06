from __future__ import print_function

import json
import os
import cProfile
import pstats
import numpy as np

from examples.pybullet.utils.pybullet_tools.utils import connect, dump_body, disconnect, wait_for_interrupt, \
    get_movable_joints, get_sample_fn, set_joint_positions, get_joint_name, link_from_name, set_point, set_quat, \
    add_line, quat_from_euler, Euler, HideOutput, create_cylinder, load_pybullet, inverse_kinematics, \
    get_link_pose, Pose, multiply, set_pose, Point, workspace_trajectory, pairwise_collision, wait_for_duration, \
    get_pose, invert, point_from_pose, get_distance, get_joint_positions, wrap_angle, get_collision_fn, load_model, set_color

from pddlstream.utils import read, get_file_path, print_solution, user_input, get_length
from pddlstream.language.constants import PDDLProblem, And
from pddlstream.algorithms.focused import solve_focused
from pddlstream.language.generator import from_test
from pddlstream.algorithms.incremental import solve_exhaustive

JSON_FILENAME = 'voronoi_S1.0_09-05-2018.json'
#KUKA_PATH = 'framefab_kr6_r900_support/urdf/kr6_r900_workspace.urdf'
KUKA_PATH = 'framefab_kr6_r900_support/urdf/kr6_r900.urdf'
TOOL_NAME = 'eef_tcp_frame'

disabled_collisions = [
    # ('robot_link_1', 'workspace_objects'),
    # ('robot_link_2', 'workspace_objects'),
    # ('robot_link_3', 'workspace_objects'),
    # ('robot_link_4', 'workspace_objects'),
    ('robot_link_5', 'eef_base_link'),
]

# [u'base_frame_in_rob_base', u'element_list', u'node_list', u'assembly_type', u'model_type', u'unit']

def parse_point(json_point):
    return np.array([json_point['X'], json_point['Y'], json_point['Z']]) / 1e3 # / 1e3

def parse_origin(json_data):
    return parse_point(json_data['base_frame_in_rob_base']['Origin'])

def parse_elements(json_data):
    return [tuple(json_element['end_node_ids'])
            for json_element in json_data['element_list']] # 'layer_id

def parse_node_points(json_data):
    origin = parse_origin(json_data)
    return [origin + parse_point(json_node['point']) for json_node in json_data['node_list']]

def parse_ground_nodes(json_data):
    return {i for i, json_node in enumerate(json_data['node_list']) if json_node['is_grounded'] == 1}

def sample_confs(robot, num_samples=10):
    joints = get_movable_joints(robot)
    print('Joints', [get_joint_name(robot, joint) for joint in joints])
    sample_fn = get_sample_fn(robot, joints)
    for i in range(num_samples):
        print('Iteration:', i)
        conf = sample_fn()
        set_joint_positions(robot, joints, conf)
        wait_for_interrupt()

def draw_element(node_points, element, color=(1, 0, 0, 1)):
    n1, n2 = element
    p1 = node_points[n1]
    p2 = node_points[n2]
    return add_line(p1, p2, color=color[:3])

def create_elements(node_points, elements, radius=0.0005, color=(1, 0, 0, 1)):
    element_bodies = []
    for (n1, n2) in elements:
        p1 = node_points[n1]
        p2 = node_points[n2]
        height = np.linalg.norm(p2 - p1)
        if height == 0:
            continue
        center = (p1 + p2) / 2
        # extents = (p2 - p1) / 2
        body = create_cylinder(radius, height, color=color)
        set_point(body, center)
        element_bodies.append(body)

        delta = p2 - center
        x, y, z = delta
        phi = np.math.atan2(y, x)
        theta = np.math.acos(z / np.linalg.norm(delta))

        euler = Euler(pitch=theta, yaw=phi)
        # euler = Euler() # Default is vertical
        quat = quat_from_euler(euler)
        set_quat(body, quat)
    return element_bodies

def check_trajectory_collision(robot, trajectory, bodies):
    movable_joints = get_movable_joints(robot)
    for q in trajectory:
        set_joint_positions(robot, movable_joints, q)
        if any(pairwise_collision(robot, body) for body in bodies):
            return True
    return False

def get_test_cfree(element_bodies):
    def test(traj, element):
        return not check_trajectory_collision(traj.robot, traj.trajectory, [element_bodies[element]])
    return test


def get_pddlstream_test(node_points, elements, ground_nodes):
    # stripstream/lis_scripts/run_print.py
    # stripstream/lis_scripts/print_data.txt

    domain_pddl = read(get_file_path(__file__, 'domain.pddl'))
    constant_map = {}

    stream_pddl = read(get_file_path(__file__, 'stream.pddl'))
    #stream_pddl = None
    stream_map = {
        'test-cfree': from_test(get_test_cfree({})),
    }

    nodes = list(range(len(node_points))) # TODO: sort nodes by height?

    init = []
    for n in nodes:
        init.append(('Node', n))
    for n in ground_nodes:
        init.append(('Connected', n))
    for e in elements:
        init.append(('Element', e))
        n1, n2 = e
        t = None
        init.extend([
            ('Connection', n1, e, t, n2),
            ('Connection', n2, e, t, n1),
        ])
        #init.append(('Edge', n1, n2))

    goal_literals = [('Printed', e) for e in elements]
    goal = And(*goal_literals)

    return PDDLProblem(domain_pddl, constant_map, stream_pddl, stream_map, init, goal)


def get_pddlstream(trajectories, element_bodies, ground_nodes):
    domain_pddl = read(get_file_path(__file__, 'domain.pddl'))
    constant_map = {}

    stream_pddl = read(get_file_path(__file__, 'stream.pddl'))
    stream_map = {
        'test-cfree': from_test(get_test_cfree(element_bodies)),
    }

    init = []
    for n in ground_nodes:
        init.append(('Connected', n))
    for t in trajectories:
        e = t.element
        n1, n2 = e
        init.extend([
            ('Node', n1),
            ('Node', n2),
            ('Element', e),
            ('Traj', t),
            ('Connection', n1, e, t, n2),
            ('Connection', n2, e, t, n1),
        ])

    goal_literals = [('Printed', e) for e in element_bodies]
    goal = And(*goal_literals)

    return PDDLProblem(domain_pddl, constant_map, stream_pddl, stream_map, init, goal)


def test_ik(robot, node_order, node_points):
    link = link_from_name(robot, TOOL_NAME)
    movable_joints = get_movable_joints(robot)
    sample_fn = get_sample_fn(robot, movable_joints)
    for n in node_order:
        point = node_points[n]
        set_joint_positions(robot, movable_joints, sample_fn())
        conf = inverse_kinematics(robot, link, (point, None))
        if conf is not None:
            set_joint_positions(robot, movable_joints, conf)
            continue
        link_point, link_quat = get_link_pose(robot, link)
        #print(point, link_point)
        #user_input('Continue?')
        wait_for_interrupt()
    # TODO: draw the transforms

def test_grasps(robot, node_points, elements):
    elements = [elements[0]]
    elements = [elements[-1]]
    element_bodies = create_elements(node_points, elements)
    element_body = element_bodies[0]
    #print('Bodies: {}'.format(len(elements)))

    phi = 0
    grasp_poses = [Pose(euler=Euler(roll=np.pi/2, pitch=phi, yaw=theta))
                   for theta in np.linspace(0, 2*np.pi, 10, endpoint=False)]

    link_pose = get_link_pose(robot, link_from_name(robot, TOOL_NAME))
    wait_for_interrupt()
    for grasp_rotation in grasp_poses:
        n1, n2 = elements[0]
        length = np.linalg.norm(node_points[n2] - node_points[n1])
        for t in np.linspace(-length/2, length/2, 10):
            element_translation = Pose(point=Point(z=t))
            grasp_pose = multiply(grasp_rotation, element_translation)
            element_pose = multiply(link_pose, grasp_pose)
            set_pose(element_body, element_pose)
            #wait_for_interrupt()
            user_input('Continue?')

def test_print(robot, node_points, elements):
    #elements = [elements[0]]
    elements = [elements[-1]]
    [element_body] = create_elements(node_points, elements)
    wait_for_interrupt()

    phi = 0
    #grasp_poses = [Pose(euler=Euler(roll=np.pi/2, pitch=phi, yaw=theta))
    #               for theta in np.linspace(0, 2*np.pi, 10, endpoint=False)]
    grasp_poses = [Pose(euler=Euler(roll=np.pi/2, pitch=theta, yaw=phi))
                   for theta in np.linspace(0, 2*np.pi, 10, endpoint=False)]

    link = link_from_name(robot, TOOL_NAME)
    movable_joints = get_movable_joints(robot)
    sample_fn = get_sample_fn(robot, movable_joints)
    for grasp_rotation in grasp_poses:
        n1, n2 = elements[0]
        length = np.linalg.norm(node_points[n2] - node_points[n1])
        set_joint_positions(robot, movable_joints, sample_fn())
        for t in np.linspace(-length/2, length/2, 10):
            element_translation = Pose(point=Point(z=t))
            grasp_pose = multiply(grasp_rotation, element_translation)
            element_pose = get_pose(element_body)
            link_pose = multiply(element_pose, invert(grasp_pose))
            conf = inverse_kinematics(robot, link, link_pose)
            #wait_for_interrupt()
            user_input('Continue?')

def get_grasp_rotation(direction, angle):
    return Pose(euler=Euler(roll=np.pi / 2, pitch=direction, yaw=angle))

def get_grasp_pose(translation, direction, angle):
    return multiply(get_grasp_rotation(direction, angle), Pose(point=Point(z=translation)))

def optimize_angle(robot, link, element_pose, translation, direction, initial_angles, collision_fn, max_error=1e-2):
    movable_joints = get_movable_joints(robot)
    initial_conf = get_joint_positions(robot, movable_joints)
    best_error, best_angle, best_conf = max_error, None, None
    for angle in initial_angles:
        grasp_pose = get_grasp_pose(translation, direction, angle)
        target_pose = multiply(element_pose, invert(grasp_pose))
        set_joint_positions(robot, movable_joints, initial_conf)
        conf = inverse_kinematics(robot, link, target_pose)
        # if conf is None:
        #    continue
        #if pairwise_collision(robot, robot):
        conf = get_joint_positions(robot, movable_joints)
        if collision_fn(conf):
            continue
        link_pose = get_link_pose(robot, link)
        error = get_distance(point_from_pose(target_pose), point_from_pose(link_pose))
        if error < best_error:  # TODO: error a function of direction as well
            best_error, best_angle, best_conf = error, angle, conf
        # wait_for_interrupt()
    #print(best_error, translation, direction, best_angle)
    #if best_conf is not None:
    #    set_joint_positions(robot, movable_joints, best_conf)
    #    wait_for_interrupt()
    return best_angle, best_conf

def compute_direction_path(robot, p1, p2, element_body, direction, collision_fn):
    step_size = 0.0025 # 0.005
    #angle_step_size = np.pi / 128
    angle_step_size = np.math.radians(0.25)
    angle_deltas = [-angle_step_size, 0, angle_step_size]
    num_initial = 12

    length = np.linalg.norm(p2 - p1) # 5cm
    start, end = -length / 2, length / 2
    steps = np.append(np.arange(start, end, step_size), [end])
    #print('Length: {} | Steps: {}'.format(length, len(steps)))

    #initial_angles = [wrap_angle(angle) for angle in np.linspace(0, 2*np.pi, num_initial, endpoint=False)]
    initial_angles = [wrap_angle(angle) for angle in np.random.uniform(0, 2*np.pi, num_initial)]
    movable_joints = get_movable_joints(robot)
    sample_fn = get_sample_fn(robot, movable_joints)
    set_joint_positions(robot, movable_joints, sample_fn())
    link = link_from_name(robot, TOOL_NAME)
    element_pose = get_pose(element_body)
    current_angle, current_conf = optimize_angle(robot, link, element_pose,
                                                 steps[0], direction, initial_angles, collision_fn)
    if current_conf is None:
        return None
    # TODO: constrain maximum conf displacement
    # TODO: alternating minimization for just position and also orientation
    trajectory = [current_conf]
    for translation in steps[1:]:
        set_joint_positions(robot, movable_joints, current_conf)
        initial_angles = [wrap_angle(current_angle + delta) for delta in angle_deltas]
        current_angle, current_conf = optimize_angle(robot, link, element_pose,
                                                     translation, direction, initial_angles, collision_fn)
        if current_conf is None:
            return None
        trajectory.append(current_conf)
    return trajectory

def sample_print_path(robot, node_points, element, element_body, collision_fn):
    #max_directions = 10
    max_directions = 16
    #for direction in np.linspace(0, 2*np.pi, 10, endpoint=False):
    for direction in np.random.uniform(0, 2*np.pi, max_directions):
        n1, n2 = element
        trajectory = compute_direction_path(robot, node_points[n1], node_points[n2],
                                            element_body, direction, collision_fn)
        if trajectory is not None:
            return trajectory
    return None

def load_world():
    root_directory = os.path.dirname(os.path.abspath(__file__))
    floor = load_model('models/short_floor.urdf')
    with HideOutput():
        robot = load_pybullet(os.path.join(root_directory, KUKA_PATH))
    set_point(floor, Point(z=-0.01))
    return floor, robot

def plan_sequence_test(node_points, elements, ground_nodes):
    pr = cProfile.Profile()
    pr.enable()
    pddlstream_problem = get_pddlstream_test(node_points, elements, ground_nodes)
    #solution = solve_focused(pddlstream_problem, planner='goal-lazy', max_time=10, debug=False)
    solution = solve_exhaustive(pddlstream_problem, planner='goal-lazy', max_time=10, debug=False)
    print_solution(solution)
    pr.disable()
    pstats.Stats(pr).sort_stats('tottime').print_stats(10)
    plan, _, _ = solution
    return plan

def plan_sequence(trajectories, element_bodies, ground_nodes):
    pr = cProfile.Profile()
    pr.enable()
    pddlstream_problem = get_pddlstream(trajectories, element_bodies, ground_nodes)
    #solution = solve_focused(pddlstream_problem, planner='goal-lazy', max_time=10, debug=False)
    solution = solve_exhaustive(pddlstream_problem, planner='goal-lazy', max_time=30, debug=True)
    print_solution(solution)
    pr.disable()
    pstats.Stats(pr).sort_stats('tottime').print_stats(10)
    plan, _, _ = solution
    return plan

class PrintTrajectory(object):
    def __init__(self, robot, trajectory, element):
        self.robot = robot
        self.trajectory = trajectory
        self.element = element
    def __repr__(self):
        return 't{}'.format(self.element)


def who_even_knows(robot, obstacles, node_points, element_bodies):
    disabled = {tuple(link_from_name(robot, link) for link in pair) for pair in disabled_collisions}
    collision_fn = get_collision_fn(robot, get_movable_joints(robot), obstacles, [],
                                    self_collisions=True, disabled_collisions=disabled, use_limits=False)
    trajectories = {}
    for element, element_body in element_bodies.items():
        trajectory = sample_print_path(robot, node_points, element, element_body, collision_fn)
        print(element, get_length(trajectory))
        if trajectory is None:
            continue
        trajectories[element] = PrintTrajectory(robot, trajectory, element)
        #print(sum(check_trajectory_collision(robot, trajectory, [body])
        #          for body in element_bodies.values()))
    return trajectories

def display(elements, trajectories):
    connect(use_gui=True)
    floor, robot = load_world()
    movable_joints = get_movable_joints(robot)
    #element_bodies = dict(zip(elements, create_elements(node_points, elements)))
    #for body in element_bodies.values():
    #    set_color(body, (1, 0, 0, 0))
    #for element, trajectory in trajectories.items():
    for element in elements:
        if element not in trajectories:
            continue
        trajectory = trajectories[element].trajectory
        print(element, len(trajectory))
        #wait_for_interrupt()
        #set_color(element_bodies[element], (1, 0, 0, 1))
        last_point = None
        for conf in trajectory:
            set_joint_positions(robot, movable_joints, conf)
            current_point = point_from_pose(get_link_pose(robot, link_from_name(robot, TOOL_NAME)))
            if last_point is not None:
                handle = add_line(last_point, current_point, color=(1, 0, 0))
            last_point = current_point
            wait_for_duration(0.025)
    #user_input('Finish?')
    wait_for_interrupt()
    disconnect()

def main(viewer=False):
    root_directory = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_directory, JSON_FILENAME), 'r') as f:
        json_data = json.loads(f.read())

    elements = parse_elements(json_data)
    node_points = parse_node_points(json_data)
    ground_nodes = parse_ground_nodes(json_data)

    node_order = list(range(len(node_points)))
    #np.random.shuffle(node_order)
    node_order = sorted(node_order, key=lambda n: node_points[n][2])
    elements = sorted(elements, key=lambda e: min(node_points[n][2] for n in e))

    #node_order = node_order[:100]
    ground_nodes = [n for n in ground_nodes if n in node_order]
    elements = [element for element in elements if all(n in node_order for n in element)]
    elements = elements[:25]
    #elements = elements[150:]

    print('Nodes: {} | Ground: {} | Elements: {}'.format(
        len(node_points), len(ground_nodes), len(elements)))
    #print(json_data['assembly_type']) # extrusion
    #print(json_data['model_type']) # spatial_frame
    #print(json_data['unit']) # millimeter
    #plan = plan_sequence_test(node_points, elements, ground_nodes)

    connect(use_gui=viewer)
    floor, robot = load_world()
    dump_body(robot)

    #for element in elements:
    #    draw_element(node_points, element)
    #    #user_input('Continue?')
    #for name, args in plan:
    #    n1, e, n2 = args
    #    draw_element(node_points, e)
    #    user_input('Continue?')

    #test_ik(robot, node_order, node_points)

    element_bodies = dict(zip(elements, create_elements(node_points, elements)))
    trajectories = who_even_knows(robot, [floor], node_points, element_bodies)

    plan_sequence(trajectories.values(), element_bodies, ground_nodes)


    disconnect()
    #display(elements, trajectories)


if __name__ == '__main__':
    main()