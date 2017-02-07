clear
filename='1FHL.txt';
fid = fopen(filename);
mydata = textscan(fid, '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %[^\n}]', 'delimiter', ',','CollectOutput',1);
data_temp=mydata{1};
data(:,1:2)=data_temp(:,19:20);
data(:,3)=data_temp(:,1);
fclose(fid);
data=strtrim(data);
%%%%%%%%%% Write to file %%%%%%%%%%%%%%
fid=fopen([filename(1:end-4) '.reg'],'wt');
fprintf(fid,'global color=yellow\n');
[rows,~]=size(data);


for i=1:rows
    fprintf(fid,'fk5;point(%s,%s)# point=cross text={%s}\n',data{i,1},data{i,2},data{i,3});
end
fclose(fid);
