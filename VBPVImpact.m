%  A function that returns the GWP100 impact from the solar panel setup based
%  on total number of sections.

function [VBPVI, PVI , misc ] = VBPVImpact(n_sections)
 
% Input:
% n_shelters: Number of seperate shelters
% n_sections: Total number sections of length 2.192 m
% anchor:     Length of anchoring into ground. 1/6 of length over ground can
%             be used as default
% Output:
% VBPVI:      Full impact of VBPV GWP100 impact [kg CO2 eq]
% PVI:        Panel GWP100 impact [kg CO2 eq]
% misc:       Not yet discovered output
%
% Default setup:
% [VBPVI, PVI ,~] = VBPVImpact(32)

% The area of active PV for every section is given by
sec_area = 4 * (2.1*1.046); % [m^2]

% Total area depends on the number of sections 
tot_area = sec_area * n_sections; % [m^2]


% Impact per area of panel is used to determine the total impact of the panel 
% This is divided into the different phases in order to allow checking if
% the results changes when aqcuiring data from different sources
% Some uncertainty is related to the fact that support systems (BOS) doesn't
% scale linearly

% EPD impact based on 60MW Jolywood plant 
[UI , CI , DI] = JolywoodImpact(1);

% Production:
% Sourced from: 
UpstreamI = UI;      % [kg CO2 eq]/[m^2]

% Use phase:
% Sourced from: 
CoreI = CI;      % [kg CO2 eq]/[m^2]

% EOL:
% Sourced from: 
DownstreamI = DI;      % [kg CO2 eq]/[m^2]

% Total for panel:
% Summed over all phases 
PVI = (UI + CI + DI) * tot_area ;      % kg CO2 eq

% In order to take into account the contribution from the extra steel
% structure a function is called to estimate the impact from the steel
% this only consideres the impact of the steel to gate meaning that
% transport to location is not considered. Likewise EOL is not considered.

% The anchoring is defined here but could be difined externally for
% sensitivity analysis
anchoring = (4.3/6);  %
[StI , ~ ] = SteelImpact(1,n_sections,anchoring);

VBPVI = PVI + StI;

misc= StI;
end