load('allData');
[rows,cols]=size(sourceCoord);
[rowsData,colsData]=size(data);
angleAroundSource=1;
% 1: Normal Aitoff Projection
% 2: Aitoff Projection of Photon Cuts
% 3: Spectrums
numberOfBins=10;

%%  READ
    %This analyse hist had a really weird binning problem, I made my own
    %weigted histogram
    %
%%
set(gcf,'Visible', 'off');
if input==1
    figure
    hold on
    
    aitoff_coord=zeros(rowsData,2);
    for i=1:rowsData
        aitoff_coord(i,:) = aitoff(data(i,4:5)); 
 
    end
    plot(aitoff_coord(:,1),aitoff_coord(:,2),'b.') ; 

    aitoff_sourceCoord=zeros(rows,2);
    for i=1:rows
       aitoff_sourceCoord(i,:)=aitoff(sourceCoord(i,1:2)); 
    end
    
    plot(aitoff_sourceCoord(:,1),aitoff_sourceCoord(:,2),'r.') ; 

    set(gca,'FontSize',16);                
    saveas(gca,'graphs/Aitoff Projection','epsc2');
    hold off
    
end
if input==2
    figure
    hold on
    
    for i=1:rows
        loc=['/home/james/fermidata/spectra/data/',sources{i},'.mat'];
        load(loc);
        [rows_p,~]=size(photonsAroundSource);

        temp1=aitoff(sourceCoordinates);
        for j=1:rows_p
            temp2(j,:)=aitoff(photonsAroundSource(j,4:5));    
        end    
        plot(temp2(:,1),temp2(:,2),'.');
        plot(temp1(1),temp1(2),'r.');
    end
    set(gca,'FontSize',16);                
    saveas(gca,'graphs/Cut Aitoff Projection','epsc2');
    hold off
end

if input==3
    warning off;
    delete '/home/james/fermidata/spectra/graphs/emptySources.txt';
    fid = fopen('/home/james/fermidata/spectra/graphs/emptySources.txt','a+');
    
   
    for i=1:rows
        
        loc=['/home/james/fermidata/spectra/data/',sources{i},'.mat'];
        load(loc);
        
        [rows_p,~]=size(photonsAroundSource);
        energy=zeros(rows_p,1);
        angularDistance=zeros(rows_p,1);
        
        for j=1:rows_p
            energy(j,1) = photonsAroundSource(j,1);
            angularDistance(j,1) = angDist(photonsAroundSource(j,4:5),sourceCoordinates);     
            
        end
              
        binIntervals=angleAroundSource/numberOfBins;
        binCenters=0:binIntervals:angleAroundSource-binIntervals;         % Shift over by half a bin to avoid binning in negative (since 0 is now middle)
                                                            % a.k.a instead makeing 0 the center, make it an inner radius
        sizeOfHalfBin=binIntervals/2;
        binCenters=binCenters+sizeOfHalfBin;
        
        [photonsInBin]=hist(angularDistance,binCenters);
 
        outerRadii=binCenters+sizeOfHalfBin;
        innerRadii=binCenters-sizeOfHalfBin;

        area=pi.*(outerRadii.^2-innerRadii.^2);
        [rows_ang,~]=size(angularDistance);
                                %Start first one here because it makes catting the matrixes easier
        clearvars weights;
        weights = zeros(1,photonsInBin(1)) + 1./area(1);
        
        for z=2:numberOfBins
            weights = [weights (zeros(1,photonsInBin(z)))+1./area(z)];
        end
        
        if photonsAroundSource(1,1)==0
            fprintf(fid, '%s\n', sourceName); 
        else
            [histw, intervals] = histwc(angularDistance, weights, numberOfBins);
            bar(intervals, histw,'hist');
            
            set(gca,'FontSize',16);            
            xlabel(' Angular Distance','FontSize',16);
            ylabel('Weigthed Number of Photons','FontSize',16);
            xlim([0 angleAroundSource]);
            title(sources{i});
            saveas(gca,['graphs/',sources{i},'_WEIGTHEDHISTOGRAM'],'epsc2');
        end
       
        if photonsAroundSource(1,1)==0
            continue;
        elseif rows_p<3
            plot(angularDistance,energy./1000,'o');
            set(gca,'FontSize',16);
            xlabel('Angular Distance ({\circ})','FontSize',16);
            ylabel('Energy (GeV)','FontSize',16);
            xlim([0 angleAroundSource]);
            title(sources{i});
            saveas(gca,['graphs/',sources{i},'_energyvsDistance_plot'],'epsc2');
        elseif rows_p<10
            
            plot(angularDistance,energy./1000,'o');
            set(gca,'FontSize',16);
            xlabel('Angular Distance ({\circ})','FontSize',16);
            ylabel('Energy (GeV)','FontSize',16);
            xlim([0 angleAroundSource]);
            title(sources{i});
            saveas(gca,['graphs/',sources{i},'_energyvsDistance_plot'],'epsc2');
            
            ndhist([angularDistance],[energy./1000],'themax'); 
            colorbar('YTick',[0:10000])
            set(gca,'FontSize',16);
            xlabel('Angular Distance ({\circ})','FontSize',16);
            ylabel('Energy (GeV)','FontSize',16);
            title(sources{i});
            saveas(gca,['graphs/',sources{i},'_energyvsDistance_Colormap'],'epsc2');
            
            
        else
            ndhist([angularDistance],[energy./1000],'themax'); 
                             
            colorbar('YTick',[0:10000])
            set(gca,'FontSize',16);
            xlabel('Angular Distance ({\circ})','FontSize',16);
            ylabel('Energy (GeV)','FontSize',16);
            title(sources{i});
            saveas(gca,['graphs/',sources{i},'_energyvsDistance_Colormap'],'epsc2');
        end
    end
    fclose(fid);
    warning on;
end
set(gcf,'Visible', 'on');


%     set(gca,'FontSize',16);                
%     xlabel('','FontSize',16);
%     ylabel('Number of Photons','FontSize',16);
%     saveas(gca,,'eps');

