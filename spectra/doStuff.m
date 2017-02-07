%Just inout t


input=3;
catalogueName={'Potential_Sources'};        % Just change catalogue names!
[rows,cols]=size(catalogueName);
ROI=0.2;


for counter=1:cols
    clearvars -except input catalogueName rows counter ROI;
    mkdir data
    mkdir graphs
    mkdir (catalogueName{counter})

    makeCuts('lat_final_10GeV_alldata.txt',[catalogueName{counter} '.reg'],ROI);
    analyseCuts;
    movefile('data','data10')
    movefile('graphs','graphs10')
    movefile('data10',catalogueName{counter})
    movefile('graphs10',catalogueName{counter})

    clearvars -except input catalogueName rows counter ROI;

    mkdir data
    mkdir graphs
    makeCuts('lat_final_100GeV_alldata.txt',[catalogueName{counter} '.reg'],ROI);
    analyseCuts;
    movefile('data','data100')
    movefile('graphs','graphs100')
    movefile('data100',catalogueName{counter})
    movefile('graphs100',catalogueName{counter})
    
end