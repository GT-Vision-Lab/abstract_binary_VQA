# Binary-VQA
These are the code for the paper: 

Yin and Yang: Balancing and Answering Binary Visual Questions

There are three folders: tuple extraction, mutual information and feature extraction.

1: Tuple extraction: 3 python files try to extraction primary object, relation and secondary object from a question. The code first parses the results from a parser(pars_sentence.py), then extracts summary and tuples(extract_tuple.py), and finally, separate the tuple(tuple_chunk.py).

To run this, one should first have Stanford parser ready. Then save the output into a txt file. At the end of the file, add an empty line, then followed (ROOT. An example is given in the folder. 

2. To have the word and clipart object aligned, one needs to run the code in mutual_information folder. mapping.py function prepares everything. And by following the other two matlab files, one can get it.

3. To extract feature, the code in feature_extraction should be focused. The main file is ExtractFeatures.m. 

