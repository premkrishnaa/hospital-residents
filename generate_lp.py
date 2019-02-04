from graph_class import *

def generate_max_card_lp(g, path):
    # write the max cardinality matching LP constraints to output file in path
    f = open(path, "w")

    # Objective function
    f.write("maximize\nsize: ")
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    # resident wise credit capacity constraints
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ' (uq): ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write(str(h.credits) + ' x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= ' + str(r.uq) + '\n')

    # hospital wise capacity constraints
    for h in g.hospitals:
        h_ind = h.name[1:]
        if(len(h.pref) > 0):
            f.write(h.name + ' (uq): ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.uq) + '\n')

    # resident wise class constraints
    for r in g.residents:
        r_ind = r.name[1:]
        if(len(r.classes) > 0):
            for i, c in enumerate(r.classes):
                f.write(r.name + '_' + str(i) + ' (class): ')
                for j, h_name in enumerate(c.class_list):
                    h_ind = h_name[1:]
                    f.write('x_' + r_ind + '_' + h_ind + ' ')
                    if(j != len(c.class_list)-1):
                        f.write('+ ')
                f.write('<= ' + str(c.cap) + '\n')

    # master class constraints for each resident
    for r in g.residents:
        r_ind = r.name[1:]
        for i, c in enumerate(g.master):
            s = ''
            s += (r.name + '_' + str(i) + ' (master_class): ')
            trimmed_class_list = []
            for h_name in c.class_list:
                if(r.get_rank(h_name) <= len(r.pref)):
                    trimmed_class_list.append(h_name)
            if(len(trimmed_class_list) > c.cap):
                for j, h_name in enumerate(trimmed_class_list):
                    h_ind = h_name[1:]
                    s += ('x_' + r_ind + '_' + h_ind + ' ')
                    if(j != len(trimmed_class_list)-1):
                        s += ('+ ')
                s += ('<= ' + str(c.cap) + '\n')
                f.write(s)

    # specifying that all decision variables are binary (0/1)
    f.write('\nbin\n')
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i%31 == 0 and i != 0):
            f.write('\n')
    f.write('\n')

    f.write('\nend')
    f.close()
