
featpath = '../../abstract_images/image_feature_val/';
listing = dir(fullfile(featpath,'*.mat'));

feat_file = [];
for i = 1:length(listing)
    path = fullfile(featpath,listing(i).name);
	tdata = load(path);
    
    feat_file(i,:) = tdata.feat;
end