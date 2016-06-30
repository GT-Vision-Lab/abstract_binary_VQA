# Unbalanced and Balanced Abstract Binary VQA Datasets

Unbalanced and Balanced datasets from the paper- 

Yin and Yang: Balancing and Answering Binary Visual Questions.
Peng Zhang\*, Yash Goyal\*, Douglas Summers-Stay, Dhruv Batra, Devi Parikh.
Computer Vision and Pattern Recognition (CVPR), 2016.

The datasets can be downloaded from [here](https://computing.ece.vt.edu/~ygoyal/binaryVQA_dataset/binaryVQA_dataset.zip)

The zip file contains 6 folders-- {unbalanced, balanced}_{train, val, test}_data
The subfolders inside each of the above folder are explained below (with the example of 'balanced_test_data'):

balanced_test_data/ 
	vqa/ contains OpenEnded and MultipleChoice questions, and annotation files
	scene_data/ contains the scenes information
		ills/ contains png image files
		json/ contains scene information in json format (More details about the structure of the json here: https://github.com/VT-vision-lab/abstract_scenes_v002#scene-json-format)
			balanced_abstract_v002_test.json contains the scene information for all scenes in one big file
			balanced_abstract_v002_test_indv/ contains individual scene information files
	attention_features/ contains attention features (A-IMG) used by our approach (Q+Tuple+A-IMG) for all scenes (one row for each scene)
	holistic_features/ contains holistic features (H-IMG) used by baseline (Q+Tuple+H-IMG) for all scenes (one row for each scene)
	scenes_id/ contains the mapping between rows of features and the question ids. Index i in the scenes_id file contains the question id of the data point (image, question) to which the image features at row i in the features file refer to. For example, the image features for a datapoint with question id x can be accessed using `features[scenes_id.index(x)]` (loosely using python syntax)


Note:

1. Since test annotations for VQA dataset (Antol et al.) are not public, it is not possible to filter binary questions and balance that dataset. Therefore, we use their val set as our unbalanced test set. Our unbalanced train and val sets are subsets of their train set. Our balanced train, val and test sets are balanced versions of our unbalanced train, val and test sets respectively.

2. The features (both attention and holistic) and scenes id files for train and val sets are combined (named with "trainval"). So, both train and val features and scenes_id folders contain the same files for both balanced and unbalanced cases.



References:
S. Antol, A. Agrawal, J. Lu, M. Mitchell, D. Batra, C. L. Zitnick, and D. Parikh. VQA: Visual Question Answering. In ICCV, 2015
