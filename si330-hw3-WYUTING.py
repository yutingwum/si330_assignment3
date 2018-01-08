import profile
import csv

# Here, we are reusing the document distance code

# Change 1, see bottom for comment
#from docdist1 import (get_words_from_string, count_frequency, vector_angle)
from docdist_dict import (get_words_from_string, count_frequency, vector_angle)

# As a convention, "constant" variable names are usually written in all-caps
OUTPUT_FILE = 'Sentence_Database_With_ID.csv'
MASTER_FILE = 'Sentences_Table_MasterList_sample.csv'
SENTENCE_DB_FILE = 'Sentence_Database_Without_ID_sample.csv'
#MASTER_FILE = 'Sentences_Table_MasterList.csv'
#SENTENCE_DB_FILE = 'Sentence_Database_Without_ID.csv'

def main():
    global MASTER_FILE, SENTENCE_DB_FILE

    # we will be collecting each row of the output file in this list
    output = []
    row_count = 0

    # Change 2, see bottom for comment
    master_file_data = get_csv_rows(MASTER_FILE)

    # looping through the SENTENCE_DB_FILE to process each row
    #with open(SENTENCE_DB_FILE, 'r', newline='') as input_file:
        #reader = csv.DictReader(input_file, delimiter=',', quotechar='"')

    for row in get_csv_rows(SENTENCE_DB_FILE):
        # Change 2, see bottom for comment
        #set_sentence_id(row)
        set_sentence_id(row, master_file_data)
        replace_target_with_blank(row)

        if row['SentID_GM'] != 'NA':
                #lookup_similar_id(row)
                #find_alternate_sentence(row)
            lookup_similar_id(row, master_file_data)
            find_alternate_sentence(row, master_file_data)
            find_unique_targets(row)

        output.append(row)
        row_count += 1
        print(row_count)

    write_output_file(output)

#def set_sentence_id(row):
# Change 2, see bottom for comment
def set_sentence_id(row, data):
    '''
        If you look at the SENTENCE_DB_FILE, each row has a Sentence with a missing SentID_GM
        SentID_GM can be found in the MASTER_FILE
        So, we use the MASTER_FILE data to find SentID_GM for each Sentence

        # -------------------------------------------------------------------------
        # Implement a better way to "lookup" SentID_GM,
        # without looping through each row again and again
        #
        # Ask yourself:
        # -------------
        #   - Is "list" the best data structure for "lookup / search"?
        #   - What is the 'type' of running time for the current implementation?
        #     Is it linear or quadratic?
        #
        # -------------------------------------------------------------------------

    '''
    #ORIGINAL FUNCTION EXPLANATION
    # This function finds the sentence ID from the master file and insert it in the legacy file; if no ID found in the master file, then insert NA

    # Data strcture:
    # record is a dictionary from the list of dictionaries returned from get_csv_rows, passing the MASTER_FILE
    # row is a dictionary from the list of dictionaries returned from get_csv_rows, passing the SENTENCE_DB_FILE
    # Input: a row (essentially a dictionary) from the DB file; Output: None
    # Input AFTER change 2: a row (essentially a dictionary) from the DB file, the list of dictionaries generated from master file data


    for record in data:
    #for record in get_csv_rows(MASTER_FILE):
        # use the get_csv_rows function to obtain a list of dictionaries generated from the MASTER_FILE
        # each record a dictionary, and is essentially a row in the MASTER_FILE
        # check if the sentence in the DB file is the same in the master file

        # Change 3, see bottom for detail
        #if record['Sentence_with_Target'].strip() == row['Sentence'].strip():
        # remove the strip() command to save time on producing unnecessary lists
        if record['Sentence_with_Target'] == row['Sentence']:
            # found a matching sentence!
            # insert the sentence ID from the master file into the DB file
            row['SentID_GM'] = record['SentID_GM']
            break
        else:
            # the default value
            # if not matched, set the dafault value to NA
            row['SentID_GM'] = 'NA'


def replace_target_with_blank(row):
    '''
        Each row in SENTENCE_DB_FILE has a "Target" word like "[education]".
        In this function, we replace the target word with "XXXXX", and
        store its value in "Sentence_With_Blank" column

        # -------------------------------------------------------------------------
        # Implement a better way to replace the Target word with XXXXX,
        # without looping through the words
        #
        # Ask yourself:
        # -------------
        #   - Is there an inbuilt python function,
        #     that can be used to substitute a word with another word?
        #
        # -------------------------------------------------------------------------

    '''

    new_words = []

    # Here, we split the sentence into words and loop through it till we find the target

    # This function finds the word from a sentence in the DB file and checks if it matches with the target word
    # if matched, insert XXXXX in the Sentence_With_Blank columns
    # if not, insert the original word back

    # Data structure:
    # row['Sentence'].split(): list; it is a list of words
    # word: string; word[0], word[1], etc: char
    # new_words: list; it is supposed to be a list of words
    # eventually, use the words in the new words list to form a new sentence
    # Input: a row (essentially a dictionary) from the DB file; Output: None

    # in the list of words generated from stripping the sentence
    # loop through the list and find the  word that starts and ends with "[" and "]" and check if matches with the target word
    for word in row['Sentence'].split():
        if word[0]=='[' and word[-1]==']' or word[-2:]=='].' and word[1:-1]==row['Targ']:
            # if matched, append "XXXXXX" to the new words list
            new_words.append('XXXXX')
        else:
            # if not mached, append the original word to the new word list
            new_words.append(word)

    # use the words in the new words list to form a new sentence
    # then put the new sentence in the row
    row['Sentence_With_Blank'] = ' '.join(new_words)

#def lookup_similar_id(row):
def lookup_similar_id(row, data):
    '''
        The MASTER_FILE also has a column 'SimilarTo_SentID_GM',
        which is the sentence ID of a similar sentence in the MASTER_FILE.

        In this function, we lookup the similar sentence for the given 'row',
        using the data in the MASTER_FILE

        # -------------------------------------------------------------------------
        # Implement a better way to find similar sentence,
        # without looping through the each row again and again
        #
        # Ask yourself:
        # -------------
        #   - Is "list" the best data structure for "lookup / search"?
        #   - What is the 'type' of running time for the current implementation?
        #     Is it linear or quadratic?
        #   - Can I reuse something from a previous step?
        #
        # -------------------------------------------------------------------------

    '''

    # This functions finds if the sentence id from DB file and master file matches, meaning that if the sentence is the same
    # if match, then check if record's SentID_GM is the same as record's SimilarTo_SentID_GM
    # if so, then row's SimilarTo_Sentence is record's sentence with target word, and row's SimilarTo_SentID_GM is record's SimilarTo_SentID_GM

    # Data structure:
    # similar_to: None or string (if the sentence matches)
    # record: a dictionary from the list of dictionaries returned from get_csv_rows, passing the MASTER_FILE
    # row: a dictionary from the list of dictionaries returned from get_csv_rows, passing the SENTENCE_DB_FILE
    # Input: a row (essentially a dictionary) from the DB file; Output: None
    # Input AFTER change 2: a row (essentially a dictionary) from the DB file, the list of dictionaries generated from master file data

    similar_to = None
    # Here we get SimilarTo_SentID_GM for this row's SentID_GM using the MASTER_FILE

    # loop through the MASTER_FILE
    #for record in get_csv_rows(MASTER_FILE):
    # Change 2, see bottom for details

    #for record in get_csv_rows(MASTER_FILE):
    for record in data:
        # if record's SentID_GM matches with the SentID_GM of the given row from the DB file
        if record['SentID_GM'] == row['SentID_GM']:
            # found a match
            # then similar_to becomes record's SimilarTo_SentID_GM
            similar_to = record['SimilarTo_SentID_GM']
            break

    # then we find the similar sentence from the MASTER_FILE
    # check if there is a similar ID found
    if similar_to is not None:
        # if found
        for record in get_csv_rows(MASTER_FILE):
        #for record in data:
            # record is a row in MASTER_FILE
            # if record's SentID_GM matches with its SimilarTo_SentID_GM
            if record['SentID_GM'] == similar_to:
                # then the given row's similar sentence is record's target sentence
                # and the given row's SimilarTo_SentID_GM is record's SimilarTo_SentID_GM
                row['SimilarTo_Sentence'] = record['Sentence_with_Target']
                row['SimilarTo_SentID_GM'] = similar_to
                break

#def find_alternate_sentence(row):
def find_alternate_sentence(row, data):
    '''
        Just like SimilarTo_Sentence and SimilarTo_SentID_GM, we will determine
        Alternate_SimilarTo_Sentence and Alternate_SimilarTo_SentID_GM
        by calculating the cosine distance between two sentences
        using the **document distance** code that we discussed in the previous class

        # -------------------------------------------------------------------------
        # Your aim in this function is to speed up the code using a simple trick
        # and a modification
        #
        # Biggest hint: look at the other files in the folder
        #
        # Ask yourself:
        # -------------
        #   - Why are the functions called here, so slow?
        #   - Is there something you learned in the class about "document distance" problem,
        #     that can be used here?
        #   - Is there a step which can be taken out of the 'for' loop?
        #
        # -----
        # Bonus:
        # ------
        # This code calculates the cosine distance between the given row's Sentence
        # and the Sentence_with_Target all the rows in MASTER_FILE.
        # This is repeated for each 'row' in SENTENCE_DB_FILE.
        # In first iteration, you already calculate the cosine distance of
        # "I go to school because I want to get a good [education]."
        # and all the rows in the MASTER_FILE
        # and that includes "I go to school because I want to get a good [education]."
        # This is repeated in 2nd iteration for "I go to school because I want to get a good [education].".
        #
        # Can you cache (store) these calculations for future iterations?
        # What would be the best data structure for caching?
        # Try to further optimize the code using a cache
        # -------------------------------------------------------------------------

    '''

    # This function creates a frequency mapping for the sentence from DB file and for the sentence in the master file
    # then check the distance between of the frequency mapping of the two sentences
    # if cosine distance is within 0 and 0.75 (non inclusive),
    # then insert the distance, record's Sentence_with_Target, and record' SentID_GM into similar_sentence as values to the corresponding keys
    # then use similar_sentence's SentID_GM and Sentence_with_Target into row's Alternate_SimilarTo_SentID_GM and Alternate_SimilarTo_Sentence

    # Data structure:
    # similar_sentence: None or dictionary (if the sentence matches);
    # similar_sentence is a dictionary where keys are distance, Sentence_with_Target, and SentID_GM and the values of the keys come from record
    # record: a dictionary from the list of dictionaries returned from get_csv_rows, passing the MASTER_FILE
    # row: a dictionary from the list of dictionaries returned from get_csv_rows, passing the SENTENCE_DB_FILE
    # Input: a row (essentially a dictionary) from the DB file; Output: None


    # find alternate similar sentence using document distance
    similar_sentence = None
    #for record in get_csv_rows(MASTER_FILE):
    # Change 2, see bottom for details

    #for record in get_csv_rows(MASTER_FILE):
    for record in data:
        if record['SentID_GM'] == row['SentID_GM']:
            # ignore the same sentence
            continue

        # get frequency mapping for row['Sentence']
        row_word_list = get_words_from_string(row['Sentence'])
        row_freq_mapping = count_frequency(row_word_list)

        # get frequency mapping for record['Sentence_with_Target']
        record_word_list = get_words_from_string(record['Sentence_with_Target'])
        record_freq_mapping = count_frequency(record_word_list)

        distance = vector_angle(row_freq_mapping, record_freq_mapping)
        # if the cosine distance is between 0 and 0.75 (non-inclusive)
        if 0 < distance < 0.75:
            if (not similar_sentence) or (distance < similar_sentence['distance']):
                # then make similar_sentence into a dictionary where keys are distance, Sentence_with_Target, and SentID_GM
                # and the values of the keys come from record
                similar_sentence = {
                    'distance': distance,
                    'Sentence_with_Target': record['Sentence_with_Target'],
                    'SentID_GM': record['SentID_GM']
                }

    # if similar sentence is not none and similar_sentence['SentID_GM'] is not the row's SimilarTo_SentID_GM
    if similar_sentence and similar_sentence['SentID_GM'] != row.get('SimilarTo_SentID_GM'):
        # then the row's Alternate_SimilarTo_SentID_GM equals to similar_sentence's Sentece ID
        # and the row's Alternate_SimilarTo_Sentence equals to similar_sentence's Sentence with Target
        row['Alternate_SimilarTo_SentID_GM']  = similar_sentence['SentID_GM']
        row['Alternate_SimilarTo_Sentence']  = similar_sentence['Sentence_with_Target']


def find_unique_targets(row):
    '''
        This steps finds [target] word in "SimilarTo_Sentence" and "Alternate_SimilarTo_Sentence",
        selects only unique target word(s), and saves it in `row['SimilarTo_Targets']`

        # -------------------------------------------------------------------------
        # Implement a better way to find unique target words,
        # without looping through the words
        #
        # Ask yourself:
        # -------------
        #   - Can you use regular expressions to do this?
        #   - What is the data structure that stores only unique values?
        #     Can it be used here instead of checking "if target not in targets:"?
        #     Try searching the web for "python get unique values from a list".
        #
        # -------------------------------------------------------------------------

    '''

    # This function looks into the similar sentence and alternative similar sentence, finds the target word in both and adds the target words in the list
    # then puts the unique target word(s) and saves it in row['SimilarTo_Targets']

    # Data structure:
    # targets: a list; a list target words
    # key: a string in the tuple created by row's similar sentence and alternate similar sentence
    # word: a list of words from the key (which is a sentence)
    # target: string (a word)
    # row: a dictionary from the list of dictionaries returned from get_csv_rows, passing the SENTENCE_DB_FILE

    # find unique targets from similar sentences
    targets = []
    # create a tuple using row's similar sentence and alternate similar sentence
    for key in ('SimilarTo_Sentence', 'Alternate_SimilarTo_Sentence'):
        # split the sentence into a list of words
        for word in row.get(key, '').split():
            # find the target word
            if word.startswith('[') and word.endswith(']'):
                target = word[1:-1]
                if target not in targets:
                    # add it in the target word lists
                    targets += [target]

            elif word.startswith('[') and word.endswith('].'):
                target = word[1:-2]
                if target not in targets:
                    targets += [target]

    row['SimilarTo_Targets'] = ','.join(targets)


def get_csv_rows(filename):
    '''Read the CSV file using DictReader and then append all rows in a list'''
    with open(filename, 'r', newline='') as input_file:
        reader = csv.DictReader(input_file, delimiter=',', quotechar='"')

        data = []
        for row in reader:
            data.append(row)

        return data


def write_output_file(output):
    '''Write output into a new CSV file. Uses the OUTPUT_FILE variable to determine the filename.'''
    global OUTPUT_FILE
    with open(OUTPUT_FILE, 'w', newline='') as output_file_obj:
        sentence_db_writer = csv.DictWriter(output_file_obj,
                                fieldnames=["SentID_GM", "Sentence", "Targ", "Sentence_With_Blank",
                                        "SimilarTo_Sentence", "SimilarTo_SentID_GM",
                                        "Alternate_SimilarTo_Sentence", "Alternate_SimilarTo_SentID_GM",
                                        "SimilarTo_Targets"],
                                extrasaction="ignore", delimiter=",", quotechar='"')

        sentence_db_writer.writeheader()

        for row in output:
            sentence_db_writer.writerow(row)


if __name__ == '__main__':
    profile.run('main()')
    # main()





# Original code information:
# The orginal code runs 192.134 sec without code modification
# optimize_this.py, docdist_dict.py, docdist1.py are in the HWK3 folder
# find_alternate_sentence takes the most time, which a total time of 4.261 sec and 0.048 sec per call
# The list of the total time of all the functions (before code improvement):
# look_up_similar_id: 0.133 sec
# main: 0.008 sec
# find_alternate_sentence: 4.261 sec
# find_unique_targets: 0.002 sec
# get_csv_rows: 2.710 sec
# write_output_file: 0.033 sec
# set_sentence_id: 0.282 sec
# replace_target_with_blank: 0.05 sec


# After code improvement:
# The execution time for the complete file is 372.354 sec, compared to 14.343 sec of the sample file
# The sample file runtime was reduced from 192.134 sec to 14.343 sec
# The things I learned: 1. avoid unnecessary for loops, 2. use dictionary instead of lists when appropraite 3. regex does not necessarily always mean faster


# Change 1:
# Line: 8
# Change the import file from docdist1.py to docdist_dict.py
# Reason: docdist1 is a list and docdist_dict is a dictionary, it is faster to find things in a dictionary instead of from a list
# reduced time: from 192.134 sec to 37.684 sec

# Change 2:
# Line: multiple lines
# Call get_csv_rows ONLY ONCE in the main function and save it to a variable (the data type will be a list of dictionaries)
# then add it as an extra argument in the other functions such as set_sentence_id, lookup_similar_id, find_alternate_sentence to cut time
# Reason: all the 3 functions use the list of dictionaries generated from the master file. There is no need to call get_csv_rows and loop through the file a few more times
# reduced from 37.684 sec to 19.593 sec

# Change 3:
# Line: 86
# in set_sentence_id function, remove .strip() command
# Reason: .strip() command creates a list of words, which is unnecessary in this case. Creating and checking the lists takes extra time.
# reduced from 19.593 sec to 17.635 sec

# Change 4:
# Line: starts at line 48
# get the write_output_file out of the for loop, there is no need to write the file every single time. Just need to write it once when we have all the output data
# Reason: this is no need to create a new list to store the DB file data, just loop through the dictRead object is enough
# reduced from 15.629 sec to 13.918 sec, main reduced from 0.006 sec to 0.004 sec





