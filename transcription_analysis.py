# This script contains two ways of evaluating how close one string is to another (here, used to evaluate German participants' attempts at transcribing Nigerian English). 
# It takes as input a .csv file with the columns recording ID, correct transcription, transcription attempt, and participant ID, and returns a .csv file with the columns recording ID, transcription attempt, correct transcription, evaluation between 0 (completely incorrect or not attempted) and 1 (the attempt perfectly matches the correct transcription), and participant ID.
 
import os
import string
import re
import csv
import Levenshtein as lev

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def clean_text(text):
    '''This function turns text in a string format into a cleaned-up word list (lowercase, without punctuation) first, then transfers this list back into a space-separated text.'''
    wordList = re.split('\'|\s',text)
    cleanWordList = [x.lower().strip(string.punctuation) for x in wordList]
    return " ".join(cleanWordList)

t = open(os.path.join(__location__, 'output.csv'), "w") # open output file
t.write("quest_id;text;transcription;package;CASE\n") # header of output file

with open(os.path.join(__location__, 'input.csv')) as csv_file: # open input file
    csv_reader = csv.reader(csv_file, delimiter=',') # file needs to be comma-separated
    line_count = 0
    dunno_list = ["weiß nicht", "wei nicht", "weiss nicht", "ich weiß nicht", "ich wei nicht", "ich weiss nicht", 
    "keine ahnung", "nicht verstanden", "nichts verstanden",
    "don't know", "i don't know", "dont know", "i dont know", "no idea"]

    for row in csv_reader:
        if line_count == 0:
            line_count += 1 # skip header
        else:
            if row[2].lower() in dunno_list: # assign 0 if participants indicated they didn't understand the recording at all
                pack = 0
            else:
                pack = lev.ratio(clean_text(row[1]), clean_text(row[2])) # compare transcription and attempt, having stripped off punctuation and converted to lower case
            t.write(str(row[0]) + ';' + str(row[1]) + ';' + str(row[2]) + ';' + str(pack) + ';' + str(row[3]) + '\n') # write to output file
            line_count += 1

t.close()