"""
Program by Ogadinma Njoku
Being a contribution to the group project.
Use: Analyze gedcom files, takes a file as input
"""

import pathlib
import unittest

import sys
from collections import defaultdict
from prettytable import PrettyTable
import datetime
from datetime import date

#define possible values as global constant
VALID_VALUES = {"0": ["INDI", "HEAD", "TRLR", "NOTE", "FAM"], "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE","CHIL","DIV"], "2": ["DATE"]}

class Gedcom:

    def __init__(self, file):
        self.file = file
        self.directory = pathlib.Path(__file__).parent
        self.output = ""
        self.userdata = defaultdict(dict)
        self.familydata = defaultdict(dict)
        self.tempdata = ""
        self.ptUsers = PrettyTable()
        self.ptFamily = PrettyTable()

    def analyze(self):
        """
        Function to check if file is valid
        """
        if self.file.endswith("ged"):
            read_lines = self.open_file()
            self.parse_file(read_lines)
            self.calc_data()
            return self.output, self.userdata, self.familydata
        else:
            return "Can only analyze gedcom files. Enter a file ending with .ged"

    def open_file(self):
        """
        Method to try and open the file
        :Return: Returns lines in the file if file is valid
        """
        try:
            with open(self.file, 'r') as ged:
                lines = ged.readlines()
        except FileNotFoundError:
            print("{}  is not exiting in {}".format(self.file, self.directory))
            sys.exit()
        return lines

    def parse_file(self, read_lines):
        """
        Function to read input file line by line and generate output
        :param read_lines: list
        :return: output as string
        """

        for offset, line in enumerate(read_lines):
            line = line.strip()
            if line == "": #if last line is reached, return output
                return self.output
            split_words = line.split(" ")
            len_split_words = len(split_words)
            if split_words[0] in ['0', '1', '2']: #splitwords[0] will get the level value and check if it is 0 or 1 or 2
                self.output += "-->" + " " + line + "\n" #append arrow to output
                if split_words[1] == "F12":
                    if 1:
                        pass
                if len_split_words > 3: # if there is a big name or date, append it to a single value in list
                    split_words[2] += " " + " ".join(split_words[3:])
                try:
                    if split_words[0] == '0': # if it is defining INDI or FAM, change order

                        if split_words[1] in ["HEAD", "TRLR"]:
                            if len_split_words > 2:
                                self.output += "<--" + " " + split_words[0] + "|" + split_words[1] + "|" + "Y" + "|" + \
                                               split_words[2] + "\n"
                                continue
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[1] + "|" + "Y" + "|" + "\n"
                            continue
                        elif split_words[2] == "INDI":
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[2] + "|" + "Y" + "|" + split_words[1] +  "\n"
                            self.userdata[split_words[1]] = {}
                            curr_id = split_words[1]
                            continue
                        elif split_words[2] == "FAM":
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[2] + "|" + "Y" + "|" + split_words[1] +  "\n"
                            self.familydata[split_words[1]] = {}
                            self.familydata[split_words[1]]["CHIL"] = []
                            curr_id = split_words[1]
                            continue
                except KeyError: # if invalid level value, throw eror
                    raise ValueError("Invalid line found on {}".format(offset + 1))
                try:
                    if split_words[1] not in VALID_VALUES[split_words[0]]: #check if splitwords[1] which is the tag value is in the global dictionary



                        if len_split_words < 3: # if no, add N after tag
                            self.tempdata = split_words[1]
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[1] + "|" + "N" + "|" + "\n"
                        else:
                            #if split_words[2] == "INDI":
                            #   self.userdata[curr_id].append({split_words[1]: split_words[2]})
                            #if split_words[2] == "FAM":
                            #   self.familydata[curr_id].append({split_words[1]: split_words[2]})
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[1] + "|" + "N" + "|" + \
                                           split_words[2] + "\n"
                    else:   #if yes add Y after tag
                        if len_split_words < 3:
                            self.tempdata = split_words[1]
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[1] + "|" + "Y" + "|" + "\n"
                        else:

                            self.output += "<--" + " " + split_words[0] + "|" + split_words[1] + "|" + "Y" + "|" + \
                                           split_words[2] + "\n"
                            if split_words[1] == "NOTE":
                                continue
                            if split_words[1] in ["HUSB", "WIFE"]:
                                self.familydata[curr_id][split_words[1]] = split_words[2]
                                continue
                            if split_words[1] == "CHIL":
                                self.familydata[curr_id][split_words[1]].append(split_words[2])
                                continue
                            if split_words[0] == "2":
                                self.userdata[curr_id][self.tempdata + split_words[1]] = split_words[2]
                                continue
                            self.userdata[curr_id][split_words[1]] = split_words[2]
                except KeyError: # if invalid level value, throw eror
                    print("Invalid line found on {}".format(offset + 1))

            else:
                return "Invalid line on {}".format(line)

        return self.output

    def calc_data(self):

        for key in self.userdata:

            today = date.today()
            try:
                birthday = self.userdata[key]["BIRTDATE"]
                born_date = datetime.datetime.strptime(birthday, '%d %b %Y')
            except ValueError:
                print("Invalid date found")
                sys.exit()
            try:
                death_date = self.userdata[key]["DEATDATE"]
                deathday = self.userdata[key]["DEATDATE"]
                death_date = datetime.datetime.strptime(deathday, '%d %b %Y')
                alive_status = False
            except KeyError:
                alive_status = True
            self.userdata[key]["ALIVE"] = alive_status
            if alive_status is True:
                age = today.year - born_date.year
            else:
                age = death_date.year - born_date.year
            self.userdata[key]["AGE"] = age

        self.prettyTablefunc()

    def maleBorn(self,ind_males, family):
        """ To determine if an individual was born before death"""
        flag = True

        for male in family:
            males = []
            # looping through the individual persons
            # in the family
            for ind_male in ind_males:
                if ind_male.sex is "M" and (family.uid in ind_males.famc or family.uid in ind_males.fams):
                    males.append[ind_maile]
                    for male in males[1:]:
                        if firstname(male) != firstsurname(males[0]):
                            # Flag out the false if the check if not true.
                            flag = False
                            return flag
        
            
            
                


    def prettyTablefunc(self):

        self.ptUsers.field_names = ["ID", "NAME", "GENDER", "BIRTH DATE", "AGE", "ALIVE", "DEATH", "CHILD", "SPOUSE"]

        for key in sorted(self.userdata.keys()):
            value = self.userdata[key]
            name = value["NAME"]
            gender = value["SEX"]
            birthdate = value["BIRTDATE"]
            age = value["AGE"]
            alive = value["ALIVE"]
            try:
                death = value["DEATDATE"]
            except KeyError:
                death = "NA"
            try:
                child = value["CHILD"]
            except KeyError:
                child = "NA"
            try:
                spouse = value["SPOUSE"]
            except KeyError:
                spouse = "NA"
            self.ptUsers.add_row([key, name, gender, birthdate, age, alive, death, child, spouse])

        print(self.ptUsers)

        self.ptFamily.field_names = ["ID", "MARRIAGE DATE", "DIVORCE DATE", "HUSBAND ID", "HUSBAND NAME", "WIFE ID", "WIFE NAME", "CHILDREN"]

        for key in sorted(self.familydata.keys()):

            value = self.familydata[key]
            husband_id = value["HUSB"]
            husband_name = self.userdata[husband_id]["NAME"]
            marriage = self.userdata[husband_id]["MARRDATE"]
            wife_id= value["WIFE"]
            wife_name = self.userdata[wife_id]["NAME"]
            try:
                divorce = self.userdata[husband_id]["DIVDATE"]
            except KeyError:
                divorce = "NA"
            try:
                child = value["CHIL"]
            except KeyError:
                child = "NA"
            self.ptFamily.add_row([key, marriage, divorce, husband_id, husband_name, wife_id, wife_name, child])

        print(self.ptFamily)

"""class TestCases(unittest.TestCase):
    def setUp(self):
        x = Gedcom("sampleged.ged")
        self.op = x.analyze()
    def test_equals(self):
        self.assertEqual(self.op, "--> 0 NOTE dates after now\n<-- 0|NOTE|Y|dates after now\n--> 1 SOUR Family Echo\n<-- 1|SOUR|N|Family Echo\n--> 2 WWW http://www.familyecho.com  (Links to an external site.)Links to an external site.\n<-- 2|WWW|N|http://www.familyecho.com  (Links to an external site.)Links to an external site.\n--> 0 bi00 INDI\n<-- 0|INDI|Y|bi00\n--> 1 NAME Jimmy /Conners/\n<-- 1|NAME|Y|Jimmy /Conners/\n")
"""
def main():

    file = input("Enter file name: \n")
    g = Gedcom(file)
    op, userdata, familydata = g.analyze()

    #print(op)
    #print(userdata)
    #print(familydata)

if __name__ == '__main__':
    #unittest.main(exit=False, verbosity=False)
main()
