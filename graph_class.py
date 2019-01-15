from members import *
from random import randint
from random import sample
import numpy as np

possibile_credits = [40, 50, 60, 70]
probs = np.random.geometric(p=0.10, size=len(possibile_credits))
probs = probs / np.sum(probs)
def get_res_credits():
    return list(np.random.choice(possibile_credits, size=1, replace=False, p=probs))[0]

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
                c.cap = randint(1, cur_class_size-1)
                self.master.append(c)
                ct += 1;

    def init_all_resident_class(self):
        for res in self.residents:
            self.init_resident_class(res)

    def print_format(self):

        ofile = open("output/studentList.csv", "w")
        ofile.write("Rollno,MaxCredits\n")
        res = self.residents
        for r in res:
            ofile.write(r.name+","+str(r.uq)+"\n")
        ofile.close()

        ofile = open("output/courseList.csv", "w")
        ofile.write("CourseNo,MaxStrength,Credit\n")
        hosp = self.hospitals
        for h in hosp:
            ofile.write(h.name+","+str(h.uq)+","+str(h.credits)+"\n")
        ofile.close()

        ofile = open("output/studentPreferenceList.csv", "w")
        ofile.write("Rollno,Preferences\n")
        res = self.residents
        for r in res:
            ofile.write(r.name)
            for h in r.pref:
                ofile.write(', ' + h.name)
            ofile.write('\n')
        ofile.close()

        ofile = open("output/coursePreferenceList.csv", "w")
        ofile.write("CourseNo,Preferences\n")
        hosp = self.hospitals
        for h in hosp:
            ofile.write(h.name)
            for r in h.pref:
                ofile.write(', ' + r.name)
            ofile.write('\n')
        ofile.close()

        ofile = open("output/studentClassSpecification.csv", "w")
        ofile.write("RollNo,MaxCoursesFromThisClass,Courses\n")
        res = self.residents
        for r in res:
            if(len(r.classes) > 0):
                for c in r.classes:
                    s = r.name + ','
                    s += c.get_class_str()
                    ofile.write(s + '\n')
        ofile.close()

        ofile = open("output/masterClassSpecification.csv", "w")
        ofile.write("MaxCoursesFromThisClass,Courses\n")
        if(len(self.master) > 0):
            for c in self.master:
                s = c.get_class_str()
                ofile.write(s + '\n')
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
