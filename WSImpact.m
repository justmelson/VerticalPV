% Wind shelter Impact
% A function that returns the impact from a traditional windshelter based
% on the length of the wind shelter

function [TotI , FUI , PI , WI , EI] = WSImpact(length,ElecPot)
 
% Input:
% Length:   Length of a 4 meter high windshelter [m] 
% ElecPot:  The power output of 
%
% Output:
% TotI:    Total impact of in relevant categories
%
% Default setup:
% [TotI , FUI , PI , WI , EI] = WSImpact(70,3.6055e+06) 
%
% Somewhat arbitrary number based on the E_rsl from the EPD 

% Total area of windshelter
tot_area = 4*length; % [m^2]

%% Beam Impact calculation
% Total number of wooden beams is based on an estimation of the distance
% between beams
l_sec    = 4; %[m]
n_beams  = ceil(length/l_sec);

% It's estimated that each beam has a length of 5 meters and a diameter of 0.16 m
% The total volume of wood required is then

tot_vol  = n_beams*5*0.16*pi;

% rho      = 60;           %[kg]/[m3]
% tot_mass = tot_vol*rho;

% The

Fs = 1/42.9*0.028*1000;   %[m3]
% functional unit was initially in poles this is converted to m^3
% simultatiniously imperical units are converted to SI
ImpactPerVol= [162*0.45359237*Fs;   % [kg CO2 eq]/(1000[kg])
                0;                 % N/A AP
                0;                 % N/A EP
                0;                 % N/A (PFOP) 
                0;                 % N/A (Particulate matter)
                0;                 % N/A ADPE
                4.1*1055*Fs;          % ADPF
                46*0.00378541178*Fs]; % Water scarsity

PI = tot_vol*ImpactPerVol;  % Impact from poles               
%% Wind net impact calculation

% The mass of plastic netting used is roughly estimated based on the 
% density of an available web for windbreaking

rho_web = 0.25;   %[kg]/[m^2]

web_mass = tot_area*rho_web;

% Pvc using Gabi

ImpactPerMass2 =[3.6;      % [kg CO2 eq] (incineration not consideret)
                0.0146;    % AP
                0.00119;   % EP
                0.00342;   % PFOP 
                0.00714;   % Particulate matter
                1.77E-5;   % ADPE
                55.7;      % ADPF
                2.67];     % Water scarsity

WI = web_mass*ImpactPerMass2; %impact from web

%% Energy grid impact calculation

ImpactPerKWH = [0.31;      % GWP [kg CO2 eq]
                4.75E-4;   % AP
                7.38E-5;   % EP
                3.72E-4;   % POFP 
                9.1E-5;    % Particulate matter
                1.45E-7;   % ADPE
                3.07;      % ADPF
                0.0207];   % Water scarsity


EI = ElecPot*ImpactPerKWH; % Impact from alternative energy source

% Total for windshelter:
% Expanded to Energy alternive


TotI = PI + WI + EI;  % Impact of entire windshelter and energy alternative

FUI  = TotI/tot_area; % Impact in terms of functional unit

end