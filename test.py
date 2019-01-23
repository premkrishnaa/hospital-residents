from graph_class import Graph
from generate_lp import generate_max_card_lp
import cplex

def verification():
    g = Graph()
    g.create_graph('16Jan-PK-generator')
    generate_max_card_lp(g, 'output/temp.txt')
    print(len(g.edges))
    # g.print_format_terminal()
    # print(len(g.residents), len(g.hospitals))
    # g.verify_blocking_pairs('16Jan-PK-generator')
    # print(g.verify_feasible_matching())
    # g.verify_exchange_blocking_pairs()

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
    verification()
    run_lp('output/temp.txt', 'output/output.csv')

if __name__ == '__main__':
    main()