clear
totalModPhotons=3830;
totalPhotons=8305;

totalArea=360*180;

temp_areaMod=totalArea-10*360;  % Removed galactice plane

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%% Find TeV area %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%
% This value is the amount of the galactic plane that will be removed.
% Therefore photons that have l abs (removeFromPlane) <  removed

% Value is in degrees.
removeFromPlane=5;
%%%%%%%%%%%%

[sourceCoord,sources] = readCat('tevcat.reg',1);

[rows,~]=size(sourceCoord);
i=1;
for j=1:rows
    if abs(sourceCoord(i,2))<removeFromPlane
        sourceCoord(i,:)=[];
        sources(i,:)=[];
        i=i-1;
        rows=rows-1;
    end
    i=i+1;
end

%At this point we have a list of sources that are not in the galactic plane

[rows,~]=size(sourceCoord);

foo=zeros(rows,1);
for i=1:rows
    
    for j=1:rows
        if (distBetweenPoints(sourceCoord(i,:),sourceCoord(j,:)) < 0.5) && i~=j  
            foo(i)= foo(i)+1;
        end
    end
       
end

% Running the above shows that the TeVsources # 15 and 20 are close
% together. Therefore:

OverlappingArea=areaOfOverlappingCircles(0.25,0.25,sourceCoord(15,:),sourceCoord(20,:));
