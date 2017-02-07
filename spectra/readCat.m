function [catalogueCoord,sourceNames] = readCat(filename,convertToGalactic)
fid = fopen(filename);

if strcmp(filename(end-3:end),'.reg')
    mydata = textscan(fid, '%*s %s %s %*s %[^\n}]', 'delimiter', '(,){}','CollectOutput',1);
    data =mydata{1};
    data(1,:)=[];           % Remove first line
elseif strcmp(filename(end-3:end),'.txt') %assuming its a .fits that has been converted to .txt      
   fid = fopen('1FGL.txt');
    mydata = textscan(fid, '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %[^\n}]', 'delimiter', ',','CollectOutput',1);
    data_temp=mydata{1};
    data(:,1:2)=data_temp(:,19:20);
    data(:,3)=data_temp(:,1);
end
fclose(fid);

sourceNames=data(:,3);
sourceNames =strtrim(sourceNames);

[rows,~]=size(data);
catalogueCoord = zeros(rows,2);

if data{1}(3)==':'
    for i=1:rows
         temp1=strread(data{i,1},'%f', 'delimiter', ':').';
         temp2=strread(data{i,2},'%f', 'delimiter', ':').';


         catalogueCoord(i,1)=15*(abs(temp1(1))+(temp1(2)/60)+(temp1(3)/3600));

         %Dec is already in degrees
         catalogueCoord(i,2)=abs(temp2(1))+(temp2(2)/60)+(temp2(3)/3600);

         %Check for possible negative
        if data{i,1}(1)=='-'
            catalogueCoord(i,1)=-1*catalogueCoord(i,1);
        end
        if data{i,2}(1)=='-'
            catalogueCoord(i,2)=-1*catalogueCoord(i,2);
        end

    end
else   
    for i=1:rows
        catalogueCoord(i,1) = str2double(data{i,1});
        catalogueCoord(i,2) = str2double(data{i,2});
    end
end

if convertToGalactic==1
   for i=1:rows
       catalogueCoord(i,:)=eqtogal(catalogueCoord(i,:));
   end
   
end

end

