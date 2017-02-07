function [ait_coord] = aitoff(gal_coord)
% Make Aitoff map projection.
% 
% Take traditional longitude and latitude in radians and return a
% tuple (x, y).
% 
% Notice that traditionally longitude is in [-pi:pi] from the meridian,
% and latitude is in [-pi/2:pi/2] from the equator. So, for example, if
% you would like to make a galactic map projection centered on the galactic
% center, before passing galactic longitude l to the function you should
% first do:
% l = l if l <= math.pi else l - 2 * math.pi
% 
% Keyword arguments:
% lon -- Traditional longitude in radians, in range [-pi:pi]
% lat -- Traditional latitude in radians, in range [-pi/2:pi/2]

% ASSUMES INPUT IS IN GALACTIC COORDINATES AND IN DEGREES

% First convert to radians
l=gal_coord(:,1);
b=gal_coord(:,2);

l = degtorad(l);
b = degtorad(b);

% Then to log and lat
if l<=pi
    lon=l;
else
    lon=l-2*pi;
end
lat = b;


% check if the input values are in the range
if lon > pi || lon < -pi || lat > pi/ 2 || lat < -pi /2
    throw(MException('AcctError:Incomplete','Aitoff: Input longitude and latitude out of range.\n lon: [-pi,pi]; lat: [-pi/2,pi/2].\n'));
end
% take care of the sigularity at (0, 0), otherwise division by zero may happen
if lon == 0 && lat ==0
    x=0;
    y=0;
else
    
    alpha = acos(cos(lat) * cos(lon./2.0));

% the sinc function used here is the unnormalized sinc function
    x = 2.0.*cos(lat).*sin(lon./2.0)/sinc(alpha./pi);

    y = sin(lat)./sinc(alpha./pi);
end

x=radtodeg(x);
y=radtodeg(y);
ait_coord=[x,y];
end

