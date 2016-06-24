clear all; close all; clc;
addpath('jsonlab');
addpath('Occurrence/gmmFeat')
% datapath = '../../abstract_images/image_mat/';
% featpath = '../../abstract_images/image_feature_val/';
featpath_pairs = '../../abstract_images/image_features_pairs/';

datapath = '../../abstract_images/missing_mat_val/';
featpath = '../../abstract_images/missing_train/';


% get category and instance lists
f1 = load('Lists.mat');
catlist = f1.categorylist;
inslist = f1.instancelist;
insmat = f1.instancematrix;

% load the GMMs for Absolute and Relative Location Features
load('absGMM.mat');
load('relGMM.mat');

% get human data
fdata = fopen('paper_doll_data.txt');
tempread = textscan(fdata,'%s','delimiter','\n');
fclose(fdata);
humandata = zeros(20,3);
for i=1:1:length(tempread{1})
    t1 = textscan(tempread{1}{i},'%d');
    humandata(i,:) = t1{1};
end

% get features
errorCausingImages = [];
count = 1;
listing = dir(fullfile(datapath,'*.mat'));


for i=1:1:length(listing)

        
        path = fullfile(datapath,listing(i).name);
		
            tdata = load(path);
    
		scene = tdata;

        pri = scene.pri_obj;
        sec = scene.sec_obj;
        feat = ExtractFeaturesForEachImage(scene,pri,sec, catlist, inslist, insmat, humandata, GAbsPos, GRelPos);
		unique(feat)
        filename = listing(i).name;
		savefeat(fullfile(featpath,filename),feat);
		%other pairs
		if 0
		other_objects=zeros(0,2);
		count_other_obj=0;
		for j=1:1:length(scene.availableObject)
			inst = scene.availableObject{j}.instance;
			for k=1:1:length(inst)
				if inst{k}.present 
					count_other_obj=count_other_obj+1;
					other_objects(count_other_obj,:)=[j-1,k-1];
				end
			end
		end
		all_pairs=combvec(other_objects',other_objects')';
		feat_pairs=cell(size(all_pairs,1),1);
		for j=1:size(all_pairs,1)
			pri=[];
			pri.idx=all_pairs(j,1);
			pri.ins=all_pairs(j,2);
			sec=[];
			sec.idx=all_pairs(j,3);
			sec.ins=all_pairs(j,4);
			feat_pairs{j} = ExtractFeaturesForEachImage(scene,pri,sec, catlist, inslist, insmat, humandata, GAbsPos, GRelPos);
		end
		filename = listing(i).name;
		filename = filename(1:end-5);

		savefeat(fullfile(featpath_pairs,filename),feat_pairs);
		end
		
        disp(['Saved Feature for Image ' num2str(i) '/' num2str(length(listing))]);
end
if ~isempty(errorCausingImages)
    disp('****************************************');
    disp('The indices of error causing images are:');
    disp(errorCausingImages);
end