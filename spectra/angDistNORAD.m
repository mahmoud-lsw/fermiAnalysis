function [ ang_dist] = angDistNORAD(coord1,coord2)

ra1=(coord1(1));
d1=(coord1(2));

ra2=(coord2(1));
d2=(coord2(2));

ang_dist = (acos(sin(d1)*sin(d2) + cos(d1)*cos(d2)*cos(ra1-ra2)));

%ang_dist = (sqrt((ra1-ra2)^2+(d1-d2)^2)); % Doesn't work

end

