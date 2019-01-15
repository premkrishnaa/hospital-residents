class Resident:
    def __init__(self, name, uq=0):
        self.name = name
        self.pref = []
        self.matched = None
        self.prefPtr = 0
        self.lq = 0
        self.uq = uq
        self.classes = []

    def get_index(self):
        return self.name[1:]

    def get_pref_size(self):
        return len(self.pref)

    def get_rank(self, hosp_name):
        for i, h in enumerate(self.pref):
            if(h.name == hosp_name):
                return i+1

class Hospital:
    def __init__(self, name, lq, uq, credits=10):
        self.name = name
        self.pref = []
        self.lq = lq
        self.uq = uq
        self.matched = []
        self.worstRankRes = None
        self.credits = credits

    def get_index(self):
        return self.name[1:]

    def get_pref_size(self):
        return len(self.pref)

    def get_rank(self, res_name):
        for i, r in enumerate(self.pref):
            if(r.name == res_name):
                return i+1

    def compute_worst_rank_res(self):
        worstRank = -1
        worstRankResident = None
        for r in self.matched:
            curRank = self.getRank(r.name)
            if(curRank > worstRank):
                worstRank = curRank
                worstRankResident = r
        self.worstRankRes = worstRankResident

class Edge:
    def __init__(self, r_ind, h_ind):
        self.name = 'x_' + r_ind + '_' + h_ind
        self.r_ind = r_ind
        self.h_ind = h_ind

class Classification:
    def __init__(self):
        self.class_list = []
        self.cap = 0

    def get_class_str(self):
        s = str(self.cap)
        for hosp in self.class_list:
            s += ',' + hosp
        return s

    def print_class(self):
        print('{(', end='', flush=True)
        for i, e in enumerate(self.class_list):
            if(i != len(self.class_list)-1):
                print(e + ', ', end='', flush=True)
            else:
                print(e + ') - ' + str(self.cap) +'}', end='', flush=True)