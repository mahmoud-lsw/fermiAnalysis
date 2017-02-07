[rows_sim,~]=size(data);

% 
% pNum=0;
% for i=1:rows_sim
% 
%     if strcmp(data{i,1}(1),'c')
%         pNum=pNum+1;
%         sourceCoord=zeros(1,1);
%         simbadData=zeros(1,1);
%         simbadName=cell(1,1);
%         j=1;
%         i=i+1;
%         while true
%             i
%             simbadData(j,1:2)=strread(data{i,1},'%f', 'delimiter', ' ').';     %Get coordiantes
%             simbadData(j,3)=str2double(data{i,2});          % get anglular distance
%             simbadName{j,1}=data{i,3};
%             i=i+1;
%             if strcmp(data{i,1}(1),'c')
%                 break;
%             end
% 
%         end
%         
%        loc = strcat('data/', ['PS' num2str(pNum)],'.mat');
%        save(loc,'simbadData','simbadName');
%        %clearvars simbadData simbadName;
%         
%         
%     end
%     
%     
% end


% 
%  for i=1:rows_sim
%            simbadData(i,1:2)=strread(data{i,1},'%f', 'delimiter', ' ').';     %Get coordiantes
%            simbadData(i,3)=str2num(data{i,2});     %Get coordiantes
%  end


fid=fopen('Simbad_Sources.reg','wt');
fprintf(fid,'global color=yellow\n');



for i=1:rows_sim
    fprintf(fid,'fk5;point(%s)# point=cross text={%s}\n',data{i,1},data{i,2});
end

fclose(fid);

