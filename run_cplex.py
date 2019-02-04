from graph_class import Graph
from generate_lp import generate_max_card_lp
import cplex
import sys

def verification(directory):
    g = Graph()
    g.create_graph(directory)
    generate_max_card_lp(g, directory+'/max_card_lp.txt')
    print(len(g.edges))

def run_lp(in_dir, out_dir):
    model = cplex.Cplex(in_dir)
    model.solve()
    edges = model.variables.get_names()
    print('Tot variables: ', len(edges))
    print('Objective: ', model.solution.get_objective_value())
    f = open(out_dir, 'w')
    f.write('Student Roll Number, Course ID \n')
    for e in edges:
        if(model.solution.get_values(e) == 1.0):
            e_split = e.split('_')
            r_name = 'r' + e_split[1]
            h_name = 'h' + e_split[2]
            f.write(r_name + ',' + h_name + ' \n')

def main():
    directory = sys.argv[1]
    verification(directory)
    run_lp(directory+'/max_card_lp.txt', directory+'/output.csv')

if __name__ == '__main__':
    main()
