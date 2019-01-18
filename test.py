from graph_class import Graph

g = Graph()
g.create_graph('16Jan-PK-generator')
# g.print_format_terminal()
# print(len(g.residents), len(g.hospitals))
g.verify_blocking_pairs('16Jan-PK-generator')
# print(g.verify_feasible_matching())
g.verify_exchange_blocking_pairs()