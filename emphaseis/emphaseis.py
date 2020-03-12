"""
Copyright 2020 Aine O'Toole (aine.otoole@ed.ac.uk)

This module contains the main script for emPHASEis. It is executed when a user runs `emphaseis`
(after installation) or `emphaseis-runner.py` (directly from the source directory).


"""

import argparse
import os
import sys
from collections import defaultdict
from collections import Counter

from Bio import SeqIO


from .version import __version__


def parse_args():
    parser = argparse.ArgumentParser(description='Putting the emPHASEis on the right sylLABle.')

    parser.add_argument("--reads", action="store", type=str, dest="reads")
    parser.add_argument("--mapping", action="store", type=str, dest="mapping")

    parser.add_argument("--error-threshold", action="store", type=str, dest="error_threshold")
    parser.add_argument("--min-depth", action="store", type=str, dest="min_depth")

    parser.add_argument("--out-file", action="store", type=str, dest="out_file")

    return parser.parse_args()

def do_nothing(number):
    return 0
    
def add_len(number):
    return len(number)
    
def increment(number):
    return 1

def add_number(number):
    return int(number)
    
def get_position(position, last_symbol, number):
    symbol_key = {"=":add_len,
                  ":":add_number,
                  "*":increment,
                  "+":do_nothing,
                  "-":add_len
                 }
        
    position += symbol_key[last_symbol](number)
    return position

def parse_cigar_for_mismatches(cigar):
    mismatches = []
    position = 0
    cigar = cigar[5:] # removes the cs:Z: from the beginning of the cigar
    
    symbol = ''
    last_symbol = None
    number = ''
    
    for i in cigar:
        if i in symbol_key:
            symbol = i
            
            if last_symbol:

                position = get_position(position, last_symbol, number)
                if last_symbol == '*':
                    
                    mismatches.append((position, number))
                last_symbol = symbol
                number = ''
            else:
                last_symbol = symbol
        else:
            number += i

    position = get_position(position, last_symbol, number)
    if last_symbol == '*':
        
        mismatches.append((position, number))
    return mismatches

def create_haplotype(cs, min_depth, mismatch_counter):
    mismatches = parse_cigar_for_mismatches(cs)
    haplotype_string = ''
    for mismatch in mismatches:
        if mismatch_counter[mismatch] >= min_depth:
            haplotype_string += f"{mismatch[0]}{mismatch[1]}"
    return haplotype_string

def process_file(mapping_file, hap_file, min_read_depth, error_cutoff):
    c=0
    mismatch_counter = Counter()
    with open(mapping_file, "r") as f:
        for l in f:
            c+=1
            l = l.rstrip("\n")
            cs = l.split()[-1]
            mismatches = parse_cigar_for_mismatches(cs)
            for mismatch in mismatches:
                mismatch_counter[mismatch] +=1

    haplotypes = defaultdict(list)
    with open(mapping_file, "r") as f:
        for l in f:
            l = l.rstrip("\n")
            read_name = l.split()[0]
            cs = l.split()[-1]            
            hap = create_haplotype(cs, 4, mismatch_counter)
            haplotypes[hap].append(read_name)

    with open(hap_file, "w") as f:
        for haplotype in haplotypes:

            reads = haplotypes[haplotype]
            if len(reads)>= min_read_depth:
                print("Haplotype found:")
                print(f"Haplotype:\t{haplotype}\tNumber of reads:\t{len(reads)}")
                # fw.write("{haplotype},{}")
                return len(haplotypes)

if __name__ == '__main__':

    args = parse_args()

    process_file(args.mapping_file, args.out_file, args.min_depth, args.error_cutoff)

