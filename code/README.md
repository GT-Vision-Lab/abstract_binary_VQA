# Binary-VQA

This is the code for extracting attention-based image features used in the paper: 

Yin and Yang: Balancing and Answering Binary Visual Questions
Peng Zhang*, Yash Goyal*, Douglas Summers-Stay, Dhruv Batra, Devi Parikh
Computer Vision and Pattern Recognition (CVPR), 2016

There are three folders: tuple extraction, mutual information and feature extraction.

1: 3 python files to extract tuple consisting of primary object, relation and secondary object from a question. `pars_sentence.py' first parses the results from a parser, then `extract_tuple.py' extracts summary of the question, and finally, `tuple_chunk.py' creates the tuple.

To run this, one should first have Stanford parser ready. The parsed output should be saved in a text file. At the end of this text file, add an empty line followed by "(ROOT". An example is given in the folder. 

2. To align the words and clipart objects, one needs to run the code in `mutual_information' folder. Run `mapping.py' followed by other two matlab files.

3. To extract features, the code in `feature_extraction' should be focused. The main file is `ExtractFeatures.m'. 

