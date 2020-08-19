#!/usr/bin/env python2.7

from __future__ import print_function

import os
import time

from collections import defaultdict
from itertools import permutations, combinations

from pddlstream.algorithms.search import solve_from_pddl
from pddlstream.algorithms.focused import solve_focused

from pddlstream.algorithms.incremental import solve_incremental
from pddlstream.algorithms.focused import solve_focused
from pddlstream.utils import read, elapsed_time, get_mapping, str_from_object, implies
from pddlstream.language.constants import print_solution
#from pddlstream.language.optimizer import add_result_inputs, add_result_outputs

from pddlstream.language.generator import from_test, universe_test, from_gen_fn, from_gen
from pddlstream.language.constants import print_solution, PDDLProblem, And, Fact, get_args, get_prefix
from pddlstream.language.conversion import list_from_conjunction
from pddlstream.language.stream import WildOutput, StreamInfo, Stream
from pddlstream.algorithms.search import solve_from_pddl
from pddlstream.algorithms.downward import parse_sequential_domain, parse_problem, get_conjunctive_parts, get_literals
from pddlstream.algorithms.downward import get_fluents, get_precondition, parse_domain_pddl, parse_sequential_domain
from pddlstream.algorithms.algorithm import get_predicates


def read_pddl(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    return read(os.path.join(directory, filename))

##################################################

def solve_pddl():
    domain_pddl = read_pddl('domain.pddl')
    problem_pddl = read_pddl('problem.pddl')

    plan, cost = solve_from_pddl(domain_pddl, problem_pddl)
    print('Plan:', plan)
    print('Cost:', cost)

##################################################

def get_problem(num=3):
    domain_pddl = read_pddl('domain.pddl')
    constant_map = {}
    stream_pddl = None
    stream_map = {}
    others = ['b{}'.format(i) for i in range(num)]

    init = [
        ('on', 'b', 'a'),
        ('on-table', 'a'),
        ('on-table', 'c'),
        ('clear', 'b'),
        ('clear', 'c'),
        ('arm-empty',),
        ('isblock', 'a'),
        ('isblock', 'b'),
        ('isblock', 'c'),
    ]
    for block in others:
        init.extend([
            ('on-table', block),
            ('clear', block),
            ('isblock', block),
        ])

    goal = ('on', 'a', 'c')
    #goal = ('clear', 'a')

    return PDDLProblem(domain_pddl, constant_map, stream_pddl, stream_map, init, goal)

def solve_pddlstream(focused=False):
    pddlstream_problem = get_problem()
    if focused:
        solution = solve_focused(pddlstream_problem, unit_costs=True)
    else:
        solution = solve_incremental(pddlstream_problem, unit_costs=True, debug=True)
    print_solution(solution)

def extract_facts(facts, objects):
    filtered_facts = []
    for fact in facts:
        #if set(get_args(fact)) & objects:
        if set(get_args(fact)) <= objects:
            filtered_facts.append(fact)
    return filtered_facts

def identify_conditions(stream_facts, parameters, init):
    facts_from_predicate = defaultdict(set)
    for fact in init:
        facts_from_predicate[get_prefix(fact)].add(fact)
    conditions = []
    for other_predicate in facts_from_predicate:
        other_example = list(facts_from_predicate[other_predicate])[0]
        indices = sorted(parameters)
        # len(get_args(other_example)) <= len(indices)
        for assignment in permutations(indices, r=len(get_args(other_example))):
            for fact in stream_facts:
                args = get_args(fact)
                domain_fact = (other_predicate,) + tuple(args[i] for i in assignment)
                if domain_fact not in init:
                    break
            else:
                domain_predicate = (other_predicate,) + tuple(parameters[i] for i in assignment)
                conditions.append(domain_predicate)
    return conditions

def get_static_predicates(domain):
    fluent_predicates = get_fluents(domain)
    print(fluent_predicates)
    assert not domain.axioms  # TODO: axioms
    predicates = {predicate for action in domain.actions
                  for predicate in get_predicates(get_precondition(action))}  # get_literals
    return predicates - fluent_predicates

def get_gen_fn(outputs_from_input):
    return lambda *inps: iter(outputs_from_input[inps])

def reduce_initial(replace=True):
    problem = get_problem()
    #stream_pddl = None
    stream_pddl = read_pddl('stream.pddl')

    # TODO: what if there are a bunch of predicates that aren't in the goal
    all_objects = {o for fact in problem.init for o in get_args(fact)}
    goal_objects = set()
    for fact in list_from_conjunction(problem.goal):
        goal_objects.update(get_args(fact))
    unused_objects = all_objects - goal_objects
    active_objects = set(goal_objects)

    used_init = problem.init
    if replace:
        domain = parse_sequential_domain(problem.domain_pddl)
        fluent_predicates = get_fluents(domain)
        # static_predicates = get_static_predicates(domain)
        # print(static_predicates)

        all_init = problem.init
        used_init = extract_facts(all_init, goal_objects)
        print('Used:', used_init)
        unused_facts = set(all_init) - set(used_init)
        print('Unused:', unused_facts)

        facts_from_predicate = defaultdict(set)
        for fact in unused_facts: # init
            facts_from_predicate[get_prefix(fact)].add(fact)

        # Not strictly necessary to do only unused but can narrow the pool a bit
        # potential_streams = defaultdict(set)
        # for fact in unused_facts:
        #     predicate = get_prefix(fact)
        #     input_indices = frozenset(i for i, v in enumerate(get_args(fact)) if v in active_objects)
        #     output_indices = frozenset(i for i in range(len(get_args(fact))) if i not in input_indices)
        #     potential_streams[predicate, input_indices, output_indices].add(fact)
        #print(potential_streams.keys())

        predicates = {}
        for fact in unused_facts:
            predicate = get_prefix(fact)
            indices = set(range(len(get_args(fact))))
            if predicate not in predicates:
                predicates[predicate] = indices
            assert predicates[predicate] == indices

        potential_streams = []
        for predicate, indices in sorted(predicates.items()):
            for r in range(len(indices)+1):
                for combo in map(set, combinations(indices, r=r)):
                    input_indices = indices - combo
                    output_indices = tuple(sorted(indices - input_indices))
                    input_indices = tuple(sorted(input_indices))
                    potential_streams.append((predicate, input_indices, output_indices))

        streams = []
        #for (predicate, input_indices, output_indices), facts in potential_streams.items():
        for predicate, input_indices, output_indices in potential_streams:
            facts = facts_from_predicate[predicate]

            parameters = {i: '?i{}'.format(i) for i in input_indices}
            inputs = [parameters[i] for i in input_indices]
            domain_facts = {f for f in identify_conditions(facts, parameters, all_init)
                            if get_prefix(f) not in fluent_predicates}
            assert implies(inputs, domain_facts)
            parameters.update({i: '?o{}'.format(i) for i in output_indices})
            outputs = [parameters[i] for i in output_indices]
            certified_facts = set(identify_conditions(facts, parameters, all_init)) - domain_facts
            if not certified_facts:
                continue
            print()
            print(predicate, input_indices, output_indices)
            print('Domain:', domain_facts)
            print('Certified', certified_facts)

            outputs_from_input = defaultdict(list)
            for fact in sorted(facts_from_predicate[predicate]):
                args = get_args(fact)
                input_values = tuple(args[i] for i in input_indices)
                output_values = tuple(args[i] for i in output_indices)
                outputs_from_input[input_values].append(output_values)

            name = '{}({},{})'.format(predicate, str_from_object(inputs), str_from_object(outputs))
            gen_fn = get_gen_fn(outputs_from_input)
            stream = Stream(name, from_gen_fn(gen_fn), inputs, domain_facts, outputs, certified_facts, StreamInfo())
            stream.pddl_name = 'placeholder'
            streams.append(stream)
        stream_pddl = streams

    stream_map = {}
    stream_info = {}

    # def test_clear(block):
    #     fact = ('clear', block)
    #     return fact in all_init
    #
    # # TODO: the constraint satisfaction world that I did for TLPK that automatically creates streams (hpncsp)
    # def sample_on(b1):
    #     # TODO: return all other facts that are contained just to speed up the process
    #     for b2 in sorted(all_objects, reverse=True):
    #         fact = ('on', b2, b1)
    #         print(fact)
    #         if fact in all_init:
    #             active_objects.add(b2)
    #             new_facts = list(extract_facts(all_init, active_objects))
    #             # TODO: needs to be a sequence (i.e. no sets)
    #             yield WildOutput(values=[(b2,)], facts=new_facts)
    #
    # stream_map = {
    #     'sample-block': from_gen((o,) for o in unused_objects),
    #     'test-block': from_test(universe_test),
    #     'test-arm-empty': from_test(universe_test),
    #     'test-clear': from_test(test_clear),
    #     'sample-on': sample_on,
    # }
    # stream_info = {
    #     'sample-on': StreamInfo(eager=False), #, opt_gen_fn=from_gen_fn(lambda x: [(False,)])),
    # }

    start_time = time.time()
    pddlstream = PDDLProblem(problem.domain_pddl, problem.constant_map, stream_pddl, stream_map, used_init, problem.goal)
    solution = solve_incremental(pddlstream, unit_costs=True, verbose=True, debug=False)
    #solution = solve_focused(pddlstream, stream_info=stream_info, unit_costs=True, verbose=True, debug=False)
    print_solution(solution)
    print(elapsed_time(start_time))

##################################################

def main():
    #solve_pddl()
    #solve_pddlstream()
    reduce_initial()

if __name__ == '__main__':
    main()
