clear
filename='davesPhotons.txt';

fid = fopen(filename,'r');
mydata = textscan(fid, '%f %f %f', 'delimiter', ',','CollectOutput',1);
data=mydata{1};
fclose(fid);

fid=fopen('Daves_Sources.reg','wt');
fprintf(fid,'global color=yellow\n');
[rows,~]=size(data);

for i=1:rows
    fprintf(fid,'fk5;point(%f,%f)# point=cross text={%s}\n',data(i,1),data(i,2),['DS' num2str(i) ' - ' num2str(data(i,3)) 'GeV']);
end

fclose(fid);