% n100 = zeros(10,3);
% for j=4:4
%     for i=1:10
%         n100(i,j-1) = findSources(['lat_MOD_final_100_1deg_plane' num2str(i) '.txt'],j);
%         '-'
%     end
%     j
% end

tic
n100 = zeros(11,4);

for i=5:10
    n100(i+1,2) = numSources(['lat_MOD_final_100_tevcat_1deg_plane' num2str(i) '.txt'],2);
    toc
end

for j=3:4
    for i=0:10
        n100(i+1,j) = numSources(['lat_MOD_final_100_tevcat_1deg_plane' num2str(i) '.txt'],j);
        toc
    end
    j
end