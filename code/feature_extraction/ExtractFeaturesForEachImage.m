function feat = ExtractFeaturesForEachImage(scene,pri,sec, catlist, inslist, ...
    insmat, humandata, GAbsPos, GRelPos)

    avobj = scene.availableObject;
    typemax = 10;

    %get zfactor
    sceneType = scene.sceneType;
    zfact = ones(1,5);
    if strcmp(sceneType(1:4),'Park')
        zt = 0.9;
    else
        zt = 0.95;
    end
    for i=2:1:5
        zfact(i) = zfact(i-1)*zt;
    end

    % get pri and sec indices
    for ii = 1:length(avobj)
%         if strcmp(avobj{ii}.instance{1}.name,scene.primaryName)
        if strcmp(avobj{ii}.instance{1}.name,scene.pri_name)
            priidx = ii;
        end
%         if strcmp(avobj{ii}.instance{1}.name, scene.secondaryName)
        if strcmp(avobj{ii}.instance{1}.name, scene.sec_name)
            secidx = ii;
        end
    end

    if scene.pri_name(1) == ' ' || scene.sec_name(1) == ' '
%     if isempty(pri) || isempty(sec)
        if scene.pri_name(1) == ' ' && scene.sec_name(1) ~= ' '
            prifeat = zeros(1,563);
            secins = sec.ins+1;
            secfeat = getobjectfeat(avobj{secidx}.instance{secins}, catlist,...
            inslist, insmat, typemax, humandata, zfact, GAbsPos);
        elseif scene.pri_name(1) ~= ' ' && scene.sec_name(1) == ' '
            priins = pri.ins+1;
            prifeat = getobjectfeat(avobj{priidx}.instance{priins}, catlist,...
            inslist, insmat, typemax, humandata, zfact, GAbsPos);
            secfeat = zeros(1,563);
        elseif scene.pri_name(1) == ' ' && scene.sec_name(1) == ' '
            prifeat = zeros(1,563);
            secfeat = zeros(1,563);
        end
        relLocFeat = zeros(1,48);
        
    else
        priins = pri.ins+1;
        secins = sec.ins+1;

        % get pri feat = 563
        prifeat = getobjectfeat(avobj{priidx}.instance{priins}, catlist,...
            inslist, insmat, typemax, humandata, zfact, GAbsPos);

        % get sec feat = 563
        secfeat = getobjectfeat(avobj{secidx}.instance{secins}, catlist,...
            inslist, insmat, typemax, humandata, zfact, GAbsPos);

        % get relative location features = 48
        priSecFeat = getRelLocationFeatures(avobj{priidx}.instance{priins}, avobj{secidx}.instance{secins}, GRelPos, zfact);
        secPriFeat = getRelLocationFeatures(avobj{secidx}.instance{secins}, avobj{priidx}.instance{priins}, GRelPos, zfact);
        relLocFeat = [priSecFeat, secPriFeat];
    end

    % get other features = 258
    othercatfeat = zeros(1,length(catlist));
    otherinsfeat = zeros(1,max(max(insmat)));
    for i=1:1:length(avobj)
        inst = avobj{i}.instance;
        for j=1:1:length(inst)
            if inst{j}.present
    %            if i~=priidx && j~=priins
    %                if i~=priidx && j~=priins
                        obj = avobj{i}.instance{j};
                        name = obj.name;
                        type = obj.type;
                        if strcmp(type,'human')
                            catid = find(strcmp(type,catlist));
                            insid = find(strcmp(name,inslist));
                        else
                            if strcmp(type,'animal')
                                catid = find(strcmp(type,catlist));
                                insid = find(strcmp(name,inslist));
                            else
                                catid = find(strcmp(type,catlist));
                                tempid = find(strcmp(name,inslist));
                                objtypeid = obj.typeID+1;
                                insid = insmat(tempid,objtypeid);
                            end                        
                        end
                        if othercatfeat(catid)~=1
                            othercatfeat(catid)=1;
                        end
                        if otherinsfeat(insid)~=1
                            otherinsfeat(insid)=1;
                        end
    %                end
    %            end
            end
        end
    end
    otherfeat = cat(2,othercatfeat,otherinsfeat);
    % get all features = 1150
%     feat_1 = cat(2,double(prifeat), double(secfeat));
    feat = cat(2,double(prifeat), double(secfeat), double(relLocFeat), double(otherfeat));
%     length(feat)
%     length(feat_1)
    assert(length(feat) == 1432)
end

function feat = getobjectfeat(pstruct,catlist,inslist,insmat, ...
    typemax,humandata,zfact, GAbsPos)
    %{
        Total Feat = 457
    Common feat = 203
    catID = 4
    InsID = 184
    Flip = 1
    Absolute Location = 9 (x,y) + 5 (z)

    humanfeat = 244
    TypeID = 10
    Age = 5
    Gender = 2
    Skin Color = 3
    Pose = 224

    Animalfeat = 10
        TypeID = 10
    
    Otherfeat = 0

    %}
    name = pstruct.name;
    type = pstruct.type;
    z = pstruct.z;
    % get the location of primary object
    z_coord = pstruct.z;
    x_coord = pstruct.x;
    y_coord = pstruct.y;

    % change to matlab indexing, pick a component based on depth
    useGAbsPos = GAbsPos(z_coord+1);
    absPosFeat = gmmEncodeF(double([x_coord, y_coord]), useGAbsPos);
    assert(size(absPosFeat, 2)==1)
    % concatenate the depth feature
    absDepthFeat = zeros(1, length(GAbsPos));
    absDepthFeat(z_coord+1) = 1;
    % final position/location feature
    absPosFeat = [absDepthFeat kron(absDepthFeat,absPosFeat')];


    catid = find(strcmp(type,catlist));
    insid = find(strcmp(name,inslist));
    totalins = max(max(insmat));

    % get common features
    cf1 = calcbinfeat(catid,length(catlist));
    %cf2 = calcbinfeat(insid,length(inslist));
    cf3 = pstruct.flip;
    cf4 = absPosFeat;

    if strcmp(type,'human')
        humanid = str2num(name(end-1:end));
        cf2 = calcbinfeat(insid,totalins);
        % calculate human feat
        hf1 = calcbinfeat(pstruct.expressionID + 1,typemax);
        hf2 = calcbinfeat(humandata(humanid,1),5);
        hf3 = calcbinfeat(humandata(humanid,2),2);
        hf4 = calcbinfeat(humandata(humanid,3),3);
        hf5 = getposefeat(pstruct.deformableX,pstruct.deformableY,...
            pstruct.globalScale, zfact(z+1),cf3);
        humanfeat = cat(2,hf1,hf2,hf3,hf4,hf5);
        animalfeat = zeros(1,10);
    else
        if strcmp(type,'animal')
            % calculate animal feat
            cf2 = calcbinfeat(insid,totalins);
            typeid = pstruct.poseID + 1;
            humanfeat = zeros(1,244);
            af1 = calcbinfeat(typeid,typemax);
            animalfeat = af1;
        else
            % calculate other feat
            typeid = pstruct.typeID + 1;
            cf2 = calcbinfeat(insmat(insid,typeid),totalins);
            humanfeat = zeros(1,244);
            animalfeat = zeros(1,10);
        end    
    end
    commonfeat = cat(2, cf1, cf2, cf3, cf4);
    feat = cat(2,commonfeat,humanfeat,animalfeat);
end

function out = getposefeat(X,Y,scale,z,flip)

	%GRRR: baby interpolations
	if length(X)==8
		dX=X(1)*1.25-X(2)*0.25;
		dY=Y(1)*1.25-Y(2)*0.25;
		X=[X(1) (X(1)+X(2))/2 X(2) dX (dX+X(3))/2 X(3) dX (dX+X(4))/2 X(4) X(5) (X(5)+X(6))/2 X(6) X(7) (X(7)+X(8))/2 X(8)];
		Y=[Y(1) (Y(1)+Y(2))/2 Y(2) dY (dY+Y(3))/2 Y(3) dY (dY+Y(4))/2 Y(4) Y(5) (Y(5)+Y(6))/2 Y(6) Y(7) (Y(7)+Y(8))/2 Y(8)];
	end


    defxy(:,1) = X;
    defxy(:,2) = Y;
    defxy = defxy*(scale*z);
    adefxy = defxy(2:end,:);
    if flip==0
        new = [2 1 12 13 14 9 10 11 3 4 5 6 7 8];
    else
        new = [2 1 9 10 11 12 13 14 6 7 8 3 4 5];
    end
    newdefxy = adefxy(new(1:end),:);
    partXY = cell(1,1);
    xy.x = newdefxy(:,1);
    xy.y = newdefxy(:,2);
    partXY{1} = xy;
    out = ComputeFeatures(partXY);
end

function binfeat = calcbinfeat(num,max)
    binfeat = zeros(1,max);
    binfeat(num) = 1;
end

function relfeat = getRelLocationFeatures(pstruct, sstruct, GRelPos, zfact)
    x1 = pstruct.x;
    x2 = sstruct.x;
    y1 = pstruct.y;
    y2 = sstruct.y;
    z1 = pstruct.z;
    flip = pstruct.flip;

    % change flip 1 to -1 and 0 to 1
    flip(flip==1) = -1;
    flip(flip==0) = 1;
    del_x = ((x1-x2)*flip)/zfact(z1+1);
    del_y = (y1-y2)/zfact(z1+1);

    relfeat = gmmEncodeF(double([del_x, del_y]), GRelPos);
    assert(size(relfeat,2)==1 && size(relfeat,1) == 24);
    relfeat = relfeat';
end
