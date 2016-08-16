"""
This script validates the objective values reported in the folder 'bkvl', by
reading the instance located in the 'instances' folder and the bitstring in the
folder 'bksol'. Every instance set should have the following three folders:
'bksol', 'bkvl' and 'instances' and each of these folders have files with
ending with '.bksol', '.bkvl' and '.mc' respectively.
"""

import os

instance_sets = ['set1', 'set2', 'set3']

class Graph(object):
    """ Undirected graph data structure """

    def __init__(self):
        """ Initialize an empty graph """
        self._graph = {}

    def add_edge(self, from_vertex, to_vertex, weight):
        """ 
        Adds an undirected edge between 'from_vertex' and 'to_vertex' with a
        weight 'weight'. This methods overwrites existing edges if there are
        any.
        """
        if from_vertex not in self._graph:
            self._graph[from_vertex] = {}
        if to_vertex not in self._graph:
            self._graph[to_vertex] = {}
        self._graph[from_vertex][to_vertex] = weight
        self._graph[to_vertex][from_vertex] = weight

    def get_edge(self, from_vertex, to_vertex):
        """ Returns the weight for the given vertex. """
        if from_vertex in self._graph:
            if to_vertex in self._graph[from_vertex]:
                return self._graph[from_vertex][to_vertex]
        return 0

    def cut(self, bitstring):
        """
        Returns the cut value for a given bisection represented by a bitstring.
        """
        
        output = 0
        for i in range(len(bitstring)):
            for j in range(i):
                if bitstring[i] != bitstring[j]:
                    output += self.get_edge(i, j)
        return output

    def __str__(self):
        return str(self._graph)

def make_graph(inst_loc):
    """ 
    Reads in a file and returns a graph object present in the file. The
    vertices in the file are one-based, but this is converted to zero-based
    vertices.
    """

    output = Graph()
    with open(inst_loc) as f:
        for line in f:
            arr = line.strip().split(' ')
            if len(arr) == 2: # contains the number of vertices and edges
                continue
            else:
                output.add_edge(int(arr[0]) - 1, int(arr[1]) - 1, int(arr[2]))
    return output

def validate_instance(inst_loc):
    """
    Returns True if and only if the correct objective value is reported in the
    '.bkvl' file for the given solution in '.bksol' for the instance in '.mc'.
    """

    sol_loc = inst_loc.replace('instances', 'bksol').replace('mc', 'bksol')
    obj_loc = inst_loc.replace('instances', 'bkvl').replace('mc', 'bkvl')
    try:
        with open(sol_loc) as f:
            sol_str = f.read().strip()
        with open(obj_loc) as f:
            obj_val = int(f.read())
    except IOError as err: 
        print 'IOError: {0}'.format(err)
        return False

    graph = make_graph(inst_loc)
    return (graph.cut(sol_str), obj_val)

def validate_set(set_name):
    """
    Returns the number of incorrect objective values and the total number of
    instances for the given set.
    """

    nr_of_instances = 0
    failures = []
    for _, _, files in os.walk(set_name + '/instances'):
        for f in files:
            actual, reported = validate_instance(set_name + '/instances/' + f)
            if actual != reported:
                failures.append(f + ' was ' + str(actual) + ', but was reported ' + str(reported))
            nr_of_instances += 1
    return (failures, nr_of_instances)

def main():
    """
    Iterates over all instance_sets and prints for each instance_set the total
    number of tested instances and the number of failures.
    """

    for set_name in instance_sets:
        (failures, total) = validate_set(set_name)
        print set_name, 
        print 'with', len(failures), 'failures and', total, 'instances'
        if len(failures) > 0:
            for failure in failures:
                print ' -', failure

if __name__ == '__main__':
    main()
