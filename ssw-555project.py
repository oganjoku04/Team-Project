"""
Program by Sanjeev Rajasekaran
Use: Analyze gedcom files, takes a file as input
"""

import pathlib
import unittest

import sys
from collections import defaultdict

#define possible values as global constant
VALID_VALUES = {"0": ["INDI", "HEAD", "TRLR", "NOTE", "FAM"], "1": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE","CHIL","DIV"], "2": ["DATE"]}

class Gedcom:

    def __init__(self, file):
        self.file = file
        self.directory = pathlib.Path(__file__).parent
        self.output = ""
        self.userdata = defaultdict(list)
        self.familydata = defaultdict(list)
        self.tempdata = ""

    def analyze(self):
        """
        Function to check if file is valid
        """
        if self.file.endswith("ged"):
            read_lines = self.open_file()
            self.parse_file(read_lines)
            return self.output, self.userdata, self.familydata
        else:
            return "Can only analyze gedcom files. Enter a file ending with .ged"

    def open_file(self):
        """
        Function to try and open the file
        :return: Returns lines in the file if file is valid
        """
        try:
            with open(self.file, 'r') as ged:
                lines = ged.readlines()
        except FileNotFoundError:
            print("{} Not found in {}".format(self.file, self.directory))
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
                if len_split_words > 3: # if there is a big name or date, append it to a single value in list
                    split_words[2] += " " + " ".join(split_words[3:])
                try:
                    if split_words[0] == '0': # if it is defining INDI or FAM, change order
                        if split_words[2] == "INDI":
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[2] + "|" + "Y" + "|" + split_words[1] +  "\n"
                            self.userdata[split_words[1]] = []
                            curr_id = split_words[1]
                            continue
                        if split_words[2] == "FAM":
                            self.output += "<--" + " " + split_words[0] + "|" + split_words[2] + "|" + "Y" + "|" + split_words[1] +  "\n"
                            self.familydata[split_words[1]] = []
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
                            if split_words[1] in ["HUSB", "CHIL", "WIFE"]:
                                self.familydata[curr_id].append({split_words[1]: split_words[2]})
                            if split_words[0] == "2":
                                self.userdata[curr_id].append({self.tempdata + split_words[1]: split_words[2]})
                                continue
                            self.userdata[curr_id].append({split_words[1]: split_words[2]})
                except KeyError: # if invalid level value, throw eror
                    raise ValueError("Invalid line found on {}".format(offset + 1))

            else:
                return "Invalid line on {}".format(line)

        return self.output

    def age_less_150(individuals):
        """  US07 - Age should be less than 150 years for deceased and alive"""
        self.ind = individual
        # For each decesaded individual check age if age is over 150
        for self.ind in individuals:
            if individual.death and self.ind.birthdate:
                if self.ind.birthdate + timedelta(days=54750) < individual.death:
                    error_descrip = "Individual dies over 150 years of age"
                    error_location = [self.ind.uid]
                    report_error(error_type, error_descrip, error_location)
                    return_flag = False

                    

        # For each living individual, check age
        for self.ind in individuals:
            if individual.death is None and self.ind.birthdate:
                if self.ind.birthdate + timedelta(days= 366) < datetime.now(): # Use a normal calenard year to determine the living individual
                    error_descrip = "Living Individual over 150 years old"
                    error_location = [self.ind.uid]
                    report_error(error_type, error_descrip, error_location)
                    return_flag = False
            return "Individual is above 150 years old"  


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
    print(op)
    print(userdata)
    print(familydata)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=False)
