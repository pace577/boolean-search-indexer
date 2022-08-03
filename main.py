#!/usr/bin/env python3

from pathlib import Path
import pickle

def index_files(doc_folder, index_pkl, doc_id_pkl):
    index_table = {}
    doc_dict = {}
    doc_id = 1

    # Create a dict representation of index
    for file_path in doc_folder.iterdir():
        doc_dict[doc_id] = file_path
        strings = sorted(set(file_path.read_text().split()))
        for word in strings:
            if word in index_table.keys():
                index_table[word].append(doc_id)
            else:
                index_table[word] = [doc_id]
        doc_id += 1

    # Convert to doc_ids into dgaps
    for key in index_table.keys():
        if len(index_table[key]) > 1:
            l = index_table[key]
            l = [l[i]-l[i-1] if i>0 else l[i] for i in range(len(l))]
            index_table[key] = l

    # store it somewhere
    with open(index_pkl, "wb") as pkl_file:
        pickle.dump(index_table, pkl_file)
    with open(doc_id_pkl, "wb") as pkl_file:
        pickle.dump(doc_dict, pkl_file)

    # return the docids

def single_word_match(query: str, index_table):
    """Run this function if query contains only one word"""
    try:
        # print("single_word_match:", index_table[query])
        return index_table[query]
    except KeyError as e:
        print(e, "Query word not present in any document")
        return "Query word not present in any document"

def two_word_match(query: list, index_table):
    """This takes in a list of words and checks if all these words are present.
    Currently implementing it only for 2 words, will extend later."""

def get_doc_names_from_ids(doc_id_list, doc_id_pkl):
    with open(doc_id_pkl, "rb") as pkl_file:
        doc_dict = pickle.load(pkl_file)
    # print("get_doc_names_from_ids:", doc_id_list)
    return [doc_dict[i] for i in doc_id_list]

def convert_dgap_to_docid(dgap_list):
    if len(dgap_list) > 1:
        for i in range(len(dgap_list)):
            if i>0:
                dgap_list[i] = dgap_list[i]+dgap_list[i-1]
        return dgap_list
        # return [dgap_list[i]+dgap_list[i-1] if i>0 else dgap_list[i] for i in range(len(dgap_list))]
    else:
        return dgap_list

def process_query(query, index_pkl, doc_id_pkl):
    """Can process a query containing 1 or 2 words.
    TODO: Extend it to process multiple words"""
    with open(index_pkl, "rb") as pkl_file:
        index_table = pickle.load(pkl_file)
    query = query.split()
    if len(query) == 1:
        out = get_doc_names_from_ids(convert_dgap_to_docid(single_word_match(query[0], index_table)), doc_id_pkl)
    elif len(query) == 2:
        out = get_doc_names_from_ids(convert_dgap_to_docid(two_word_match(query, index_table)), doc_id_pkl)
    else:
        out = "Cannot process a query consisting of more than 2 words!"
    print(out)

def main():
    doc_folder = Path("./documents_folder")
    index_pkl = Path("./index_table.pkl")
    doc_id_pkl = Path("./doc_ids.pkl")
    index_files(doc_folder, index_pkl, doc_id_pkl)

    # process query
    query = "This"
    process_query(query, index_pkl, doc_id_pkl)

if __name__ == '__main__':
    main()
