function [sourcePhotonRows] = findSourceAndGPPhotons(filename,catalogueName,degreesAwayFromCenter,planeRemoval)
fid = fopen(filename);
mydata = textscan(fid, '%f %f %f %f %f %*[^\n]', 'delimiter', ',','CollectOutput',1);
data=mydata{1};
fclose(fid);

%%%%%%%%%%%%
% This value is the amount of the galactic plane that will be removed.
% Therefore photons that have l abs (removeFromPlane) <  removed

% Value is in degrees.
boxSizeB=7;
boxSizel=40;
%%%%%%%%%%%%

[sourceCoord,sources] = readCat(catalogueName,1);

% [rows,~]=size(sourceCoord);
% i=1;
% 
% %Remove box around galactic center
% for j=1:rows
%     if abs(sourceCoord(i,2))<removeFromPlane
%         sourceCoord(i,:)=[];
%         sources(i,:)=[];
%         i=i-1;
%         rows=rows-1;
%     end
%     i=i+1;
% end

%At this point we have a list of sources that are not in the galactic plane

[rows,~]=size(sourceCoord);
[rowsData,~]=size(data);

%Now find all photons in galactic plane!

spr=1;
sourcePhotonRows1=zeros(1,1);

for i=1:rowsData 
    if (abs(data(i,5))<=boxSizeB && abs(data(i,6))<=boxSizeL) || (abs(data(i,5))<=planeRemoval
        sourcePhotonRows1(spr,1)=i;
        spr=spr+1;
    end
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Now create the cuts!
% For each source, go through all the photons
sourcePhotonRows2=zeros(1,1);
spr=1;     % SourcePhotonsRows
for i=1:rows                %PARSE THE TEV SOURCES
 
   for j=1:rowsData         %PARSE THE PHOTONS
       
       % Find distance between each photon and the source center
       % Use cos(A) = sin(Decl.1)sin(Decl.2) + cos(Decl.1)cos(Decl.2)cos(RA.1 - RA.2) and thus, A = arccos(A)
       % Only use (l,b) instead of (RA,DEC)
       
       angularDistance_temp = angDist(data(j,4:5),sourceCoord(i,1:2));      
       
       if(angularDistance_temp<=degreesAwayFromCenter)
            % Keep track of which rows in the fits file this was (will be used to modify to fits file later on.)
            sourcePhotonRows2(spr,1)=j;
            spr=spr+1;
            
        end
   end
   
end
sourcePhotonRows=[sourcePhotonRows1; sourcePhotonRows2];
sourcePhotonRows=unique(sourcePhotonRows);
sourcePhotonRows=sort(sourcePhotonRows,'descend');

photonDeleteFile=['photonRowsToDelete_', catalogueName(1:end-4),'_' ,int2str(degreesAwayFromCenter),'deg_plane' , int2str(planeRemoval),'.txt'];
fid = fopen(photonDeleteFile, 'wt' );
fprintf(fid,'%i\n',sourcePhotonRows);
fclose(fid);
%Problems:
% Rough cut isnt working, its letting in too many photons
% Also, data is only 5 columns. Its coded this way at the begining of this
% file. Not a big deal to fix.



% ^^
% Fixed it.
% Problem was that the values were not in Aitoff projection.
% However, new caviate is that my Aitoff goes from -180 to 180 deg, whereas ds9 Aitoff is from 180 to 360 then 0 to 180.





end

