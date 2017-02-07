totalModPhotons=3830;
totalPhotons=8305;

totalArea=360*180;

temp_areaMod=totalArea-10*360;  % Removed galactice plane

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%% Find TeV area %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

teVArea_temp=61*0.25^2*pi;  % 61 sources




areaOfOverlappingCircles=0.2471;

teVArea=teVArea_temp+areaOfOverlappingCircles;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
areaMod=temp_areaMod-teVArea;


numberOfBinsMod=(areaMod)/(pi*0.2^2);

averageMod=totalModPhotons/numberOfBinsMod;
average=totalPhotons/numberOfBinsMod;

X=[0:1:5];

YMod=poisspdf(X,averageMod);
Y=poisspdf(X,average);

YModBins=round(YMod*numberOfBinsMod);
YBins=round(Y*numberOfBinsMod);

%%%%%%%%%%%%%%%%%


%semilogy(X,YModBins)


bar(X,YModBins,'hist');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Matlab cannot plot a histogram with a log scale. Here is a work around
% Get histogram patches
ph = get(gca,'children');
% Determine number of histogram patches
N_patches = length(ph);
for i = 1:N_patches
      % Get patch vertices
      vn = get(ph(i),'Vertices');
      % Adjust y location
      vn(:,2) = vn(:,2) + 1;
      % Reset data
      set(ph(i),'Vertices',vn)
end
% Change scale
set(gca,'yscale','log')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

set(gca,'FontSize',16);
xlabel('Number of Photons','FontSize',16);
ylabel('Number Of Bins','FontSize',16);
xlim(gca,[min(X) max(X)])
saveas(gca,'MOD_PoissonDistribution','epsc2');

%%%%%%%%%%%%%%%%%%%%%%%%%%%

bar(X,YBins,'hist');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Matlab cannot plot a histogram with a log scale. Here is a work around
% Get histogram patches
ph = get(gca,'children');
% Determine number of histogram patches
N_patches = length(ph);
for i = 1:N_patches
      % Get patch vertices
      vn = get(ph(i),'Vertices');
      % Adjust y location
      vn(:,2) = vn(:,2) + 1;
      % Reset data
      set(ph(i),'Vertices',vn)
end
% Change scale
set(gca,'yscale','log')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

set(gca,'FontSize',16);
xlabel('Number of Photons','FontSize',16);
ylabel('Number Of Bins','FontSize',16);
xlim(gca,[min(X) max(X)])
saveas(gca,'PoissonDistribution','epsc2');

