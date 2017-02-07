
x=[100:500];
x1=[10:500];

Po=1.38134903838;
Io=1.7388;
So=6183.669922;

P=0.3710788542;
I=1.328206986;
S=6183.669377;

y=P*10.^-14*(x./S).^-(I);
yo=Po*10.^-14*(x./So).^-(Io);

plot(x,y)
hold on
plot(x,yo,'r')
legend('10-500 GeV Model','100-500 GeV Model')
set(gca,'FontSize',16);
xlabel('Energy (GeV)','FontSize',16);
ylabel('Flux','FontSize',16);
saveas(gca,'OldAndNewFlux','epsc2');

flux = @(e) P*10.^-14*(e./S).^-(I);
fluxo=@(e) Po*10.^-14*(e./So).^-(Io);

