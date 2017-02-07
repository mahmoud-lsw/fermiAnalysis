plot(vvmax,TSValues,'ko')

set(gca,'FontSize',16);
xlabel('V/Vmax','FontSize',16);
ylabel('TS Values','FontSize',16);

saveas(gca,['VVMAX'],'epsc2')

plot(vvmax,1,'ko')

set(gca,'FontSize',16);
xlabel('V/Vmax','FontSize',16);

saveas(gca,['VVMAX1'],'epsc2')