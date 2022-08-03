#!/usr/bin/env python3

from pathlib import Path
import pickle
import sys

def index_files(doc_folder: Path, index_pkl: Path, doc_id_pkl: Path):
    index_table = {}
    doc_dict = {}
    doc_id = 1

    # Create a dict representation of index
    for file_path in doc_folder.iterdir():
        # print(file_path)
        if file_path.suffix in [".odt", ".pdf", ".db"] or file_path.is_dir(): #there is not support yet for files with these extensions
            continue
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

    # store the index table and docids somewhere
    with open(index_pkl, "wb") as pkl_file:
        pickle.dump(index_table, pkl_file)
    with open(doc_id_pkl, "wb") as pkl_file:
        pickle.dump(doc_dict, pkl_file)

def convert_dgap_to_docid(dgap_list):
    if len(dgap_list) > 1:
        for i in range(len(dgap_list)):
            if i>0:
                dgap_list[i] = dgap_list[i]+dgap_list[i-1]
        return dgap_list
        # return [dgap_list[i]+dgap_list[i-1] if i>0 else dgap_list[i] for i in range(len(dgap_list))]
    else:
        return dgap_list

def get_doc_ids_with_one_word(word: str, index_table, doc_dict):
    """Run this function if word contains only one word"""
    try:
        # print("get_doc_ids_with_one_word:", index_table[word])
        doc_id_list = convert_dgap_to_docid(index_table[word])
        return [doc_dict[i] for i in doc_id_list]
    except KeyError as e:
        print(e, "Query word not present in any document")
        return "Query word not present in any document"

def two_word_match(query: list, index_table, doc_dict):
    """This takes in a list of 2 words and checks if all these words are present.
    Currently implementing it only for 2 words, will extend later."""
    id_list_1 = convert_dgap_to_docid(index_table[query[0]])
    id_list_2 = convert_dgap_to_docid(index_table[query[1]])
    idx1, idx2 = (0,0)
    out = []
    # print(id_list_1, id_list_2)
    while idx1 < len(id_list_1) and idx2 < len(id_list_2):
        if id_list_1[idx1] < id_list_2[idx2]:
            idx1 += 1
        elif id_list_1[idx1] > id_list_2[idx2]:
            idx2 += 1
        else:
            out.append(doc_dict[id_list_1[idx1]])
            idx1 += 1
    return out

def process_query(query, index_pkl, doc_id_pkl):
    """Can process a query containing 1 or 2 words.
    TODO: Extend it to process multiple words"""
    with open(index_pkl, "rb") as pkl_file:
        index_table = pickle.load(pkl_file)
    with open(doc_id_pkl, "rb") as pkl_file:
        doc_dict = pickle.load(pkl_file)
    if len(query) == 1:
        out = get_doc_ids_with_one_word(query[0], index_table, doc_dict)
    elif len(query) == 2:
        out = two_word_match(query, index_table, doc_dict)
    else:
        out = "Cannot process a query consisting of more than 2 words!"
    return out

def main():
    # doc_folder = Path("documents_folder")
    # query = "the document"
    query = sys.argv[1].split(",")
    doc_folder = Path(sys.argv[2])
    index_pkl = Path("./index_table.pkl")
    doc_id_pkl = Path("./doc_ids.pkl")
    index_files(doc_folder, index_pkl, doc_id_pkl)

    # process query
    output = process_query(query, index_pkl, doc_id_pkl)
    # TODO: Separate indexing from query processing to prevent repeated indexing
    print(output)

if __name__ == '__main__':
    main()
