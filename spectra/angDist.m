function [ ang_dist] = angDist(coord1,coord2)

ra1=degtorad(coord1(1));
d1=degtorad(coord1(2));

ra2=degtorad(coord2(1));
d2=degtorad(coord2(2));

ang_dist = radtodeg(acos(sin(d1)*sin(d2) + cos(d1)*cos(d2)*cos(ra1-ra2)));

%ang_dist = radtodeg(sqrt((ra1-ra2)^2+(d1-d2)^2)); % Doesn't work

end

