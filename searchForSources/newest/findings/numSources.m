function [numberOfPotentialSources] = numSources(modified_fits,minPhotons)

% See if any photon has three photons around it (make sure to exclude doubles). 
% If it put it into a .reg file with name PS##-NP##,
% where PS = potential source, NP=number of photons.
% ++PS if their is a calatogue source next to the photon

% NB THIS PROGRAM USES A FITS FILE THAT HAS ROW NUMBERS IN THE FIRST COLUMN

%%%%%%%%%%%%%% Constant Variables  %%%%%%%%%%%%%%%
cutoffAngle=0.2;
cutoffAngle_cat=0.5;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fid = fopen(modified_fits);
mydata = textscan(fid, '%f %f %f %f %f %f %*[^\n]', 'delimiter', ',','CollectOutput',1);
data=mydata{1};
fclose(fid);

[sourceCoord1,~] = readCat('1FGL.reg',1);
[sourceCoord2,~] = readCat('2FGL.reg',1);
% For each photon, go through the fits file and see if there are two others
% beside it. If yes, save the photon, delete the other two.
% If the photon has a source next to it, make it a ++

[rows_data,~] = size(data);
[rows_cat1,~]=size(sourceCoord1);
[rows_cat2,~]=size(sourceCoord2);
listOfPotentialSources=cell(1,1);
l=1;
if (minPhotons==1)
    [numberOfPotentialSources,~] = size(data);
    return
end

for i=1:rows_data
    current_photon = data(i,:);
    potentialSource=current_photon;
    k=2;
    for j=1:rows_data
        if i==j
            continue;           % Don't choose the same photon
        end
        
        if current_photon(1)<0
            break;                % Ignore deleted photons (temporary fix)
        end
        
        isClose=data(j,:);
        
        if angDist(current_photon(5:6),isClose(5:6))<cutoffAngle
            potentialSource(k,:)=isClose;
            k=k+1;
            data(j,:)=zeros(1,6)+-9999;       % Remove to avoid double counting
        end                                   % -9999 is a temporary fix to avoid having to change rows_data
                                              % this may take more time to
                                              % run but f that   
        
    end
    
    % Were there at least 3 sources. If so, save it!
    if k>minPhotons
        alreadyHasPlus=0;
        
        listOfPotentialSources{l,1}= current_photon(3);     % Put RA of photon
        listOfPotentialSources{l,2}= current_photon(4);     % Put DEC of photon
        
        listOfPotentialSources(l,3)={ ['PS' num2str(l) '-NP' num2str(k-1)]};       % Make the name (k-1 because k was added at end of loop!)
        
        % If there is a catalogue source next to it, make it a ++
        for z=1:rows_cat1       
            if angDist(sourceCoord1(z,1:2),current_photon(5:6))<cutoffAngle_cat && alreadyHasPlus~=1
                alreadyHasPlus=1;
                listOfPotentialSources(l,3)={['++' listOfPotentialSources{l,3}]};
                break;
            end
        
        end
        
        % If there is a catalogue source next to it, make it a ++
        for z=1:rows_cat2        
            if angDist(sourceCoord2(z,1:2),current_photon(5:6))<cutoffAngle_cat && alreadyHasPlus~=1
                listOfPotentialSources(l,3)={['++' listOfPotentialSources{l,3}]};
                break;
            end
        
        end
        
        l=l+1;
    end
    
end


%%%%%%%%%%% Put everything into a file  %%%%%%%%%%%%%%%%%%%%

% fid=fopen('Potential_Sources.reg','wt');
% fprintf(fid,'global color=white\n');
% for i=1:l-1
%     fprintf(fid,'fk5;point(%f,%f)# point=cross text={%s}\n',listOfPotentialSources{i,1},listOfPotentialSources{i,2},listOfPotentialSources{i,3});
% end
% fclose(fid);

[numberOfPotentialSources,~] = size(listOfPotentialSources);

end

