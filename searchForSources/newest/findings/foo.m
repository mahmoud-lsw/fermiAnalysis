for i=1:4
   bar([0:10],n100(:,i),'hist')
    set(gca,'FontSize',16);
    xlabel('b cut (\circ)','FontSize',16);
    ylabel('Number of Cluster','FontSize',16);
    if i==4
        set(gca,'ytick',[0;1;2;3])
        set(gca,'yticklabel',['0'; '1';'2';'3'])
    end
    title(['100 GeV Cuts - ' num2str(i) ' clusters']);
    saveas(gca,['photonsPerCut_100GeV_' num2str(i) 'clusters.eps'],'epsc2');
end
