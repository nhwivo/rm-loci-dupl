#!/usr/bin/env python

"""
This program takes in a MSA (.fasta) file and remove the duplicates within each loci. 
ex: 2 sequences with the same name in loci L388 will result in only 1 after running the program 

example command: rm_loci_dupl.py fname.fas
The command above will result in a cleaned file named 'duplicates_removed_fname.fas'
To specify name of output file: rm_loci_dupl.py fname.fas --out desired_name.fas

Nhi Vo 01 Aug 2022
"""

import argparse
import os

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
# required parameters/inputs:
parser.add_argument("file", help="path to fasta file containing the multiple sequence alignment to be cleaned.")
# optional parameters/inputs:
parser.add_argument("--out", help="path/name of file output. False = output would be in current directory.") 
args = parser.parse_args()

class Sequence:
    def __init__(self, filename=''):
        """
        Initializes the object
        
        param mode: string, path of file to be edited
        """
        self.filename = filename  # name of file to be read 
        self.seqdict = {}  # dictionary of sequence information ('seqname':genomic_sequence)
        self.total_dup = 0  # number of duplicates removed 
        self.total_seq = 0  # number of sequences total 
        
        if filename:
            self.open_file('r')
            
    def open_file(self, mode):
        """
        Opens file contained in self.filename and sets the filehandle as self.file 
        If the file can't be opened, exit status will equal 1

        param mode: string, mode for opening file, usually 'r' or 'w'
        return: filehandle of opened file
        """
        try:
            self.file = open(self.filename, mode)
        except OSError:
            print('Error opening file named' + self.filename)
            # exit with status = 1
            exit(1)
            
    def next_line(self):
        """
        Returns the next line from a file
        
        return: logical, True if line is read, False when end of file 
        """
        line = self.file.readline().strip() 
        if not line: 
            # no more line, file is finished
            return False 
        
        self.line = line 
        return True  #return True when there is still line to be read 
    
    def read_file(self): 
        """
        description
        """
        prev_loci_num = -100
        seqnamelist = []  # list of seqnames (to find duplciates)
                
        while self.next_line():  # iterate through every lines in the file
            if self.line.startswith('>'):  # line containing seqname 
                self.total_seq += 1  # increase count of total number of sequences being processed 
                loci_num, seqname = self.line.split('|', 1)  # split to get loci number and seqname 
                if loci_num != prev_loci_num:  # new loci 
                    seqnamelist = []  # reset the list 
                prev_loci_num = loci_num
                if seqname in seqnamelist:  # duplicate
                    self.total_dup += 1
                if seqname not in seqnamelist:  # seqname is new (not a duplicate)
                    seqnamelist.append(seqname)  # add seqname to list of seqnames 
                    self.seqdict[self.line] = ''  # record the seqname into dictionary containing all sequences 
            else:  # actual sequence of that loci  
                last_key = list(self.seqdict.keys())[-1]  # access the last key created in dictionary 
                self.seqdict[last_key] += self.line  # add line (sequence) as value of key 
                
    def save_output(self, output_name):
        """
        Save the cleaned output 
        
        param mode: logical, False if user did not specify name for output
        """
        if not output_name:  # user did not specify name for output 
            basename = os.path.basename(self.filename)
            output_name = 'duplicates_removed_'+basename  # name for output file 
        
        print(str(self.total_seq) + ' sequences processed, ' + str(self.total_dup) + ' duplicates were removed.')
        print("Saving results...")
        with open(output_name, 'w') as f:
            print(self.seqdict)
            for key, value in self.seqdict.items():
                f.write(key)
                f.write('\n')
                f.write(value)
                f.write('\n')
        
        print("Resulting file named '" + output_name + "' saved - program is finished.")
        
if __name__ == '__main__':
    MSA_path = args.file  # path to the file 
    MSA = Sequence(MSA_path)  # create Sequence object and open file
    MSA.read_file()  # process the file     
    # SAVE FILE: 
    output_name = False  # no user specified name
    if args.out:  # user specified output file name 
        output_name=args.out
    MSA.save_output(output_name)