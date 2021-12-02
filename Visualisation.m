
%% Visualisation of impacts


% VBPV windshelter
[VBPVI, PVI , StI] = VBPVImpact(32);

% Conventional windshelter
[TotI , FUI , PI , WI , EI] = WSImpact(70,1.515e+06);


CI  = {'GWP','AP','EP','POFP','PM','ADPE','ADPF','WSF'};
Cat = categorical({'GWP','AP','EP','POFP','PM','ADPE','ADPF','WSF'}');
Cat = reordercats(Cat,{'GWP','AP','EP','POFP','PM','ADPE','ADPF','WSF'});

U    = {'[kg CO2 eq]','[kg SO2 eq]','[kg PO4 eq]','[kg diNMVOC eq]','[kg PM2.5 eq]','[kg Sb eq]','[MJ net calorific]','[m3 H2O eq]'};
unit = categorical({'[kg CO2 eq]','[kg SO2 eq]','[kg PO4 eq]','[kg diNMVOC eq]','[kg PM2.5 eq]','[kg Sb eq]','[MJ net calorific]','[m3 H2O eq]'}');
unit = reordercats(unit,{'[kg CO2 eq]','[kg SO2 eq]','[kg PO4 eq]','[kg diNMVOC eq]','[kg PM2.5 eq]','[kg Sb eq]','[MJ net calorific]','[m3 H2O eq]'});

T = table(Cat,unit,VBPVI,TotI)

% Plotting totals and Conventional
figure(1)
clf
subplot(2,1,1)
hold on
plot(TotI)
plot(VBPVI)
hold off
title('Totals');
xlabel('categories'); ylabel('impact');
legend("Conventional","Photovoltaic");grid;
subplot(2,1,2)
hold on
plot(PI)
plot(WI)
plot(EI)
hold off
xlabel('categories'); ylabel('impact');
legend("Post","Web","Gridmix");grid;

% Plotting totals and Conventional
figure(2)
clf
subplot(3,1,1)
hold on
bar(Cat,[TotI,VBPVI])
hold off
title('Totals, Conventional, Photovoltaic');
xlabel('Categories'); ylabel('Impact');
legend("Conventional","Photovoltaic",'location','best');grid;
subplot(3,1,2)
hold on
bar(Cat,[PI,WI,EI])
hold off
xlabel('Categories'); ylabel('Impact');
legend("Post","Web","Gridmix",'location','best');grid;
subplot(3,1,3)
hold on
bar(Cat,[PVI,VBPVI])
hold off
xlabel('Categories'); ylabel('Impact');
legend("Panel","Total",'location','best');grid;

% Plotting totals and Conventional
figure(3)
clf
subplot(3,1,1)
hold on
bar(Cat,[TotI./TotI*100,VBPVI./TotI*100])
set(gca, 'YScale', 'log')
hold off
title('Totals(1), Conventional(2), Photovoltaic(3)');
xlabel('Normalized based on conventional total'); ylabel({'Normalized';'Impact (logaritmic)'});
legend("Conventional","Photovoltaic",'location','eastoutside');grid;
subplot(3,1,2)
hold on
bar(Cat,[PI./TotI*100,WI./TotI*100,EI./TotI*100])
%set(gca, 'YScale', 'log')
hold off
xlabel('Normalized based on conventional total'); ylabel({'Normalized';'Impact'});
legend("Posts","Wind netting","Electric mix",'location','eastoutside');grid;
subplot(3,1,3)
hold on
bar(Cat,[PVI./VBPVI*100,StI./VBPVI*100])
%set(gca, 'YScale', 'log')
hold off
xlabel('Normalized based on photovoltaic total'); ylabel({'Normalized';'Impact'});
legend("Panel","Steel structure",'location','eastoutside');grid;

%       ['GWP'  ;   % GWP
%        'AP'   ;   % AP
%        'EP'   ;   % EP
%        'POFP' ;   % POFP
%        'PM'   ;   % Particulate matter
%        'ADPE' ;   % ADPE
%        'ADPF' ;   % ADPF
%        'WSF'  ];  % Water Scar. Foot.];

% Plotting totals and Conventional
figure(4)
clf
hold on
bar(Cat,[TotI,VBPVI])
hold off
title('Totals');
xlabel('Categories'); ylabel('Impact');
legend("Conventional","Photovoltaic",'location','best');grid;



%% Plotting totals and Conventional
H = categorical({'Conventional','Photovoltaic'});
H = reordercats(H,{'Conventional','Photovoltaic'});
for i=[1:8]
    figure(4+i)
clf
hold on
C = categorical({CI{i}});
bar(H,[TotI(i),VBPVI(i)],0.4)
x0=100;
y0=100;
width=250;
height=400;
set(gcf,'position',[x0,y0,width,height])
hold off
title(CI{i});
xlabel('Scenario'); ylabel(['Impact ' U{i}]);
grid;
end
H = categorical({'Conventional','Gridmix','Post','Web','Photovoltaic'});
H = reordercats(H,{'Conventional','Gridmix','Post','Web','Photovoltaic'});

% % Plotting totals and Conventional
% for i=[1:8]
%     figure(4+i)
% clf
% hold on
% C = categorical({CI{i}});
% bar(H,[TotI(i),EI(i),PI(i),WI(i),VBPVI(i)],0.4)
% hold off
% title(CI{i});
% xlabel('Category'); ylabel('Impact');
% grid;
% end

% % Plotting totals and Conventional
% for i=[1:8]
%     figure(4+i)
% clf
% hold on
% C = categorical({CI{i}});
% bar(C,[TotI(i),EI(i),PI(i),WI(i),VBPVI(i)],0.4)
% hold off
% title(CI{i});
% xlabel('Category'); ylabel('Impact');
% legend("Conventional","Gridmix","Post","Web","Photovoltaic",'location','best');grid;
% end

%TF = (Cat == CI{i});