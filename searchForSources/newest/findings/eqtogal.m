function [galcoord] = eqtogal(eqcoord)
% Convert sexagesimal to decimal.

%If input is a string, covert to number.(Note str2num is literal therefore '2'=> 2 and '5E+2'=>500)
if isnumeric(eqcoord)==0
    temp1=str2num(eqcoord{1});
    temp2=str2num(eqcoord{2});
    clearvars eqcoord;
    eqcoord(1)=temp1;
    eqcoord(2)=temp2;
end


% Convert Equatorial coordinates to Galactic Coordinates in the epch J2000.
% 
% To be consistent, all functions inputs and outputs are in RADIANS.
% Keywords arguments:
% ra  -- Right Ascension (in radians)
% dec -- Declination (in radians)
% 
% Return a vector (l, b):
% l -- Galactic longitude (in radians)
% b -- Galactic latitude (in radians)

%RA(radians),Dec(radians),distance(kpc) of Galactic center in J2000
Galactic_Center_Equatorial=[degtorad(266.40510), degtorad(-28.936175), 8.33333];

%RA(radians),Dec(radians) of Galactic Northpole in J2000
Galactic_Northpole_Equatorial=[degtorad(192.859508), degtorad(27.128336)];

ra = degtorad(eqcoord(1));
dec=degtorad(eqcoord(2));

alpha = Galactic_Northpole_Equatorial(1);
delta = Galactic_Northpole_Equatorial(2);
la = degtorad(33.0-0.0678);

b = asin(sin(dec) * sin(delta) + cos(dec) * cos(delta) * cos(ra - alpha));
l = atan2(sin(dec) * cos(delta) - cos(dec) * sin(delta) * cos(ra - alpha), cos(dec) * sin(ra - alpha)) + la;

if l >= 0 
else
    l= l + pi * 2.0;
end
l = mod(l,(2.0 * pi));
l=radtodeg(l);
b=radtodeg(b);

galcoord=[l,b];

end

