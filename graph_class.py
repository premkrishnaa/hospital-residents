from members import *
from random import randint
from random import sample
from random import shuffle
import numpy as np
import os

possible_credits = [40, 50, 60, 70]
# set up geometric distribution among above possible resident credit limits
probs = np.random.geometric(p=0.10, size=len(possible_credits))
probs = probs / np.sum(probs)
def get_res_credits():
    return list(np.random.choice(possible_credits, size=1, replace=False, p=probs))[0]

class Graph:
    def __init__(self):
        self.residents = []
        self.hospitals = []
        self.edges = []
        self.master = []

    def init_resident_capacities(self):
        res = self.residents
        for r in res:
            r.uq = get_res_credits()

    def init_resident_class(self, res):
        n = len(res.pref)
        rpref = []
        for h in res.pref:
            rpref.append(h.name)
        used_classes = []
        tot_classes = randint(0, n)
        ct = 0
        while(n > 1 and ct < tot_classes):
            cur_class_size = randint(2, n)
            cur_class = sample(rpref, cur_class_size)
            if(set(cur_class) not in used_classes):
                c = Classification()
                used_classes.append(set(cur_class))
                c.class_list = cur_class
                c.cap = randint(1, cur_class_size-1)
                res.classes.append(c)
                ct += 1;

    def init_master_classes_random(self):
        n = len(self.hospitals)
        rpref = []
        for h in self.hospitals:
            rpref.append(h.name)
        used_classes = []
        tot_classes = randint(0, n)
        ct = 0
        while(n > 1 and ct < tot_classes):
            cur_class_size = randint(2, n)
            cur_class = sample(rpref, cur_class_size)
            if(set(cur_class) not in used_classes):
                c = Classification()
                used_classes.append(set(cur_class))
                c.class_list = cur_class
                # c.cap = randint(1, cur_class_size-1)
                c.cap = min(randint(1, 3), len(cur_class)-1)
                if(c.cap > 0):
                    self.master.append(c)
                ct += 1;

    def init_master_classes_disjoint(self):
        rpref = []
        for h in self.hospitals:
            rpref.append(h.name)
        n = len(rpref)
        if(n < 40):
            return
        shuffle(rpref)
        tot_classes = 20
        class_size = int(np.ceil(float(n)/tot_classes))
        ct = 0
        while(ct < tot_classes):
            cur_class = rpref[ct*class_size : (ct+1)*class_size]
            if(len(cur_class) > 0):
                c = Classification()
                c.class_list = cur_class
                c.cap = min(randint(1, 3), len(cur_class)-1)
                if(c.cap > 0):
                    self.master.append(c)
            ct += 1;

    def init_all_resident_class(self):
        for res in self.residents:
            self.init_resident_class(res)

    def print_format(self, outputfolder="output"):
        # create generated files in specific format in the output folder
        if not os.path.exists(outputfolder):
        	os.makedirs(outputfolder)

        ofile = open(outputfolder+"/studentList.csv", "w")
        ofile.write("Rollno,MaxCredits\n")
        res = self.residents
        for r in res:
            ofile.write(r.name+","+str(r.uq)+"\n")
        ofile.close()

        ofile = open(outputfolder+"/courseList.csv", "w")
        ofile.write("CourseNo,MaxStrength,Credit\n")
        hosp = self.hospitals
        for h in hosp:
            ofile.write(h.name+","+str(h.uq)+","+str(h.credits)+"\n")
        ofile.close()

        ofile = open(outputfolder+"/studentPreferenceList.csv", "w")
        ofile.write("Rollno,Preferences\n")
        res = self.residents
        for r in res:
            ofile.write(r.name)
            for h in r.pref:
                ofile.write(', ' + h.name)
            ofile.write('\n')
        ofile.close()

        ofile = open(outputfolder+"/coursePreferenceList.csv", "w")
        ofile.write("CourseNo,Preferences\n")
        hosp = self.hospitals
        for h in hosp:
            ofile.write(h.name)
            for r in h.pref:
                ofile.write(', ' + r.name)
            ofile.write('\n')
        ofile.close()

        ofile = open(outputfolder+"/studentClassSpecification.csv", "w")
        ofile.write("RollNo,MaxCoursesFromThisClass,Courses\n")
        res = self.residents
        for r in res:
            if(len(r.classes) > 0):
                for c in r.classes:
                    s = r.name + ','
                    s += c.get_class_str()
                    ofile.write(s + '\n')
        ofile.close()

        ofile = open(outputfolder+"/masterClassSpecification.csv", "w")
        ofile.write("MaxCoursesFromThisClass,Courses\n")
        if(len(self.master) > 0):
            for c in self.master:
                s = c.get_class_str()
                ofile.write(s + '\n')
        ofile.close()

        ofile = open(outputfolder+"/cli-iterativeHR", "w")
        ofile.write(outputfolder+"/studentList.csv\n")
        ofile.write(outputfolder+"/courseList.csv\n")
        ofile.write(outputfolder+"/studentPreferenceList.csv\n")
        ofile.write(outputfolder+"/coursePreferenceList.csv\n")
        ofile.write(outputfolder+"/masterClassSpecification.csv\n")
        ofile.write(outputfolder+"/studentClassSpecification.csv\n")
        ofile.write("1\n")
        ofile.write(outputfolder+"/iterativeHR")
        ofile.close()

        ofile = open(outputfolder+"/cli-firstPreference", "w")
        ofile.write(outputfolder+"/studentList.csv\n")
        ofile.write(outputfolder+"/courseList.csv\n")
        ofile.write(outputfolder+"/studentPreferenceList.csv\n")
        ofile.write(outputfolder+"/coursePreferenceList.csv\n")
        ofile.write(outputfolder+"/masterClassSpecification.csv\n")
        ofile.write(outputfolder+"/studentClassSpecification.csv\n")
        ofile.write("2\n")
        ofile.write(outputfolder+"/firstPreference")
        ofile.close()
	
    def print_format_terminal(self):
        print('@PartitionA')
        res = self.residents
        rlen = len(res)
        for i, r in enumerate(res):
            if(i != rlen-1):
                print(r.name + ' (' + str(r.uq) + '), ', end='', flush=True)
            else:
                print(r.name + ' (' + str(r.uq) + ') ;')
        print('@End\n')

        print('@PartitionB')
        hosp = self.hospitals
        hlen = len(hosp)
        for i, h in enumerate(hosp):
            if(i != hlen-1):
                print(h.name + ' (' + str(h.uq) + ', ' + str(h.credits) + '), ', end='', flush=True)
            else:
                print(h.name + ' (' + str(h.uq) + ', ' + str(h.credits) + ') ;')
        print('@End\n')

        print('@PreferenceListsA')
        for r in res:
            print(r.name + ' : ', end='', flush=True)
            for i, h in enumerate(r.pref):
                if(i != len(r.pref)-1):
                    print(h.name + ', ', end='', flush=True)
                else:
                    print(h.name + ' ;')
        print('@End\n')

        print('@PreferenceListsB')
        for h in hosp:
            print(h.name + ' : ', end='', flush=True)
            for i, r in enumerate(h.pref):
                if(i != len(h.pref)-1):
                    print(r.name + ', ', end='', flush=True)
                else:
                    print(r.name + ' ;')
        print('@End\n')

        print('@ClassificationA')
        for r in res:
            if(len(r.classes) > 0):
                print(r.name + ' : ', end='', flush=True)
                for i, c in enumerate(r.classes):
                    if(i != len(r.classes)-1):
                        c.print_class() 
                        print(', ', end='', flush=True)
                    else:
                        c.print_class() 
                        print(';')
        print('@End\n')

        print('@ClassificationMaster')
        if(len(self.master) > 0):
            print('master : ', end='', flush=True)
            for i, c in enumerate(self.master):
                if(i != len(self.master)-1):
                    c.print_class() 
                    print(', ', end='', flush=True)
                else:
                    c.print_class() 
                    print(';')
        print('@End')

    def get_resident(self, name):
        for r in self.residents:
            if(r.name == name):
                return r
        return None

    def get_hospital(self, name):
        for h in self.hospitals:
            if(h.name == name):
                return h
        return None

    def create_graph(self, dir_path):
        # parse input files in dir_path to create a Graph object
        f = open(dir_path + '/studentList.csv')
        line_ct = 0
        for line in f.readlines():
            if(line_ct != 0):
                line_split = line.split(',')
                self.residents.append(Resident(line_split[0], int(line_split[1])))
            line_ct += 1
        f.close()

        f = open(dir_path + '/courseList.csv')
        line_ct = 0
        for line in f.readlines():
            if(line_ct != 0):
                line_split = line.split(',')
                self.hospitals.append(Hospital(line_split[0], 0, int(line_split[1]), int(line_split[2])))
            line_ct += 1
        f.close()

        f = open(dir_path + '/studentPreferenceList.csv')
        line_ct = 0
        for line in f.readlines():
            line = line.replace(' ', '')
            line = line.strip()
            if(line_ct != 0):
                line_split = line.split(',')
                r_name = line_split[0]
                r = self.get_resident(r_name)
                for h_name in line_split[1:]:
                    hosp = self.get_hospital(h_name)
                    r.pref.append(hosp)
                    self.edges.append(Edge(r_name[1:], h_name[1:]))
            line_ct += 1
        f.close()

        f = open(dir_path + '/coursePreferenceList.csv')
        line_ct = 0
        for line in f.readlines():
            line = line.replace(' ', '')
            line = line.strip()
            if(line_ct != 0):
                line_split = line.split(',')
                h_name = line_split[0]
                h = self.get_hospital(h_name)
                for r_name in line_split[1:]:
                    res = self.get_resident(r_name)
                    h.pref.append(res)
            line_ct += 1
        f.close()

        f = open(dir_path + '/studentClassSpecification.csv')
        line_ct = 0
        for line in f.readlines():
            line = line.strip()
            if(line_ct != 0):
                line_split = line.split(',')
                r_name = line_split[0]
                r = self.get_resident(r_name)
                c = Classification()
                c.cap = int(line_split[1])
                for h_name in line_split[2:]:
                    c.class_list.append(h_name)
                r.classes.append(c)
            line_ct += 1
        f.close()

        f = open(dir_path + '/masterClassSpecification.csv')
        line_ct = 0
        for line in f.readlines():
            line = line.strip()
            if(line_ct != 0):
                line_split = line.split(',')
                c = Classification()
                c.cap = int(line_split[0])
                for h_name in line_split[1:]:
                    c.class_list.append(h_name)
                self.master.append(c)
            line_ct += 1
        f.close()

    def check_feasible(self, r, h, wh):
        # utility function to check if a matching is feasible in the instance
        wh_creds = 0
        if(wh != None):
            wh_creds = wh.credits
        if((r.get_total_allotted_credits() - wh_creds + h.credits) > r.uq):
            return False
        for c in r.classes:
            if(h.name in c.class_list):
                if((wh == None or wh.name not in c.class_list) and c.cap == c.intersection_with_matching(r.matched)):
                    return False
        for c in self.master:
            if(h.name in c.class_list):
                if((wh == None or wh.name not in c.class_list) and c.cap == c.intersection_with_matching(r.matched)):
                    return False
        return True

    def verify_blocking_pairs(self):
        # utility function to print the number of blocking pairs in a given matching
        for h in self.hospitals:
            h.compute_worst_rank_res()

        bps_calc = set()
        counts = [0,0,0,0]
        for r in self.residents:
            for h in r.pref:
                if(not r.is_matched_to(h)):
                    wr = h.worstRankRes
                    if(self.check_feasible(r, h, None)):
                        if(len(h.matched) < h.uq):
                            s = r.name + ',' + h.name
                            bps_calc.add(s)
                            counts[0] += 1
                            continue
                        elif(wr != None and h.is_better_preferred(r.name, wr.name)):
                            s = r.name + ',' + h.name + ',' + wr.name
                            bps_calc.add(s)
                            counts[1] += 1
                            continue

                    for wh in r.matched:
                        flag = 0
                        if(r.is_better_preferred(h.name, wh.name) and self.check_feasible(r, h, wh)):
                            if(len(h.matched) < h.uq):
                                s = r.name + ',' + h.name
                                bps_calc.add(s)
                                flag = 1
                                counts[2] += 1
                            elif(wr != None and h.is_better_preferred(r.name, wr.name)):
                                s = r.name + ',' + h.name + ',' + wr.name
                                bps_calc.add(s)
                                flag = 1
                                counts[3] += 1
                        if(flag == 1):
                            break

        print(len(bps_calc))

    def verify_feasible_matching(self):
        for r in self.residents:
            if(not r.is_feasible_matching(self.master)):
                return False

        for h in self.hospitals:
            if(not h.is_feasible_matching()):
                return False

        return True

    def verify_exchange_blocking_pairs(self):
        # utility function to print the list of exchange blocking pairs for a given matching
        n = len(self.residents)
        for i in range(n):
            for j in range(i+1, n):
                r1 = self.residents[i]
                r2 = self.residents[j]
                for h1 in r1.matched:
                    flag = 0
                    for h2 in r2.matched:
                        if((not r1.is_matched_to(h2)) and r1.is_better_preferred(h2.name, h1.name) and self.check_feasible(r1, h2, h1)
                            and (not r2.is_matched_to(h1)) and r2.is_better_preferred(h1.name, h2.name) and self.check_feasible(r2, h1, h2)):
                            print(r1.name + ',' + h1.name + ',' + r2.name + ',' + h2.name)
                            flag = 1
                            break
                    if(flag == 1):
                        break
