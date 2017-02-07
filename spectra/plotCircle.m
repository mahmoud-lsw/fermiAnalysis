function [ xunit,yunit ] = plotCircle(x,y,r)
th = 0:pi/50:2*pi;

xunit = r * cos(th) + x;

yunit = r * sin(th) + y;

h = plot(xunit, yunit,'m');

end

