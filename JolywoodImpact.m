%  A function that returns the GWP100 impact from the pv panels based
%  on number of seperate shelters and total number of sections.

function [UI , CI , DI] = JolywoodImpact(frame)
 
% Input:
% n_sections: Total number sections of 2.192 m
%             
% Output:
% UI:         Upstream PV GWP100 impact [kg CO2 eq]
% CI:         Core PV GWP100 impact [kg CO2 eq]
% DI:         Downstream PV GWP100 impact [kg CO2 eq]
%
% Default setup:
% [UI , CI , DI] = JolywoodImpact(1)

% The impact per active area of photovoltaic panel is found using an EPD 
% from the pv- manufacturer Jolywood:
% {Link}
% The unit declared is 1 kWh of net electricity. This has to be converted
% to an impact per active area.
% It is only on GWP100 for test reasons it is one of  the main impacts given in the EPD

EPD_C   =  60000;          % [kW]  Peak power of farm   
EPD_CpP =  0.415;          % [kW]  Peak power per panel 
EPD_Pn  =  EPD_C/EPD_CpP;  % [1]   Number of panels      
EPD_PA  =  0.72*1.5875;    % [m^2] Panel area           
EPD_AA  =  EPD_Pn*EPD_PA;  % [m^2] Total active are     
EPD_E   =  2127954734;     % [kWh] Total lifetime electricity production 
EpAA    =  EPD_E/EPD_AA;   % [kWh/m^2] Lifetime production per area

if frame == 1
    ImpactPerKWH = [0.0108    0.00654  0.000165;   % GWP
                    8.14E-5   1.15E-4  1.01E-6    ;   % AP
                    9.37E-6   2.08E-5  1.81E-8 ;   % EP
                    4.43e-5   3.91E-5  6.85e-7 ;   % POFP
                    7.16E-6   1.17E-5  7.22E-8 ;   % Particulate matter
                    1.11E-6   4.42E-7  1.66E-10;   % ADPE
                    0.119     0.0706   1.93E-3  ;   % ADPF
                    0.0829    1.08     1.30E-5 ];  % Water Scar. Foot.
elseif frame == 0
    ImpactPerKWH = [0.0103    0.00654  0.000163;   % GWP
                    7.76E-5   1.15E-4  1E-6    ;   % AP
                    9.07E-6   2.08E-5  1.80E-8 ;   % EP
                    4.18e-5   3.91E-5  6.75e-7 ;   % POFP
                    6.83E-6   1.17E-5  7.12E-8 ;   % Particulate matter
                    9.12E-7   4.42E-7  1.62E-10;   % ADPE
                    0.113     0.0706   1.9E-3  ;   % ADPF
                    0.0827    1.08     1.28E-5 ];  % Water Scar. Foot.];
else
    ImpactPerKWH = 0;
    Error("Frame configuration unknown only frame(1) or frameless(0)")
end

ImpactPerArea = ImpactPerKWH*EpAA ;      % [kg CO2 eq]/[m^2]

% The resulting impact meassured only on GWP100 
UI = ImpactPerArea(:,1);
CI = ImpactPerArea(:,2);
DI = ImpactPerArea(:,3);
end
