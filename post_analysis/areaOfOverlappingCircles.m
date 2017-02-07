function [area] = areaOfOverlappingCircles(r1,r2,point1,point2)
    x1=point1(1);
    y1=point1(2);

    x2=point2(1);
    y2=point2(2);
    
    
    d=sqrt((x2-x1)^2+(y2-y1)^2);
    
    if d==0
        area=pi*max(r1,r2)^2;
        return
    else
        areaOfOverlap=r1^2*acos((d^2+r1^2-r2^2)/(2*d*r1)) + r2^2*acos((d^2+r2^2-r1^2)/(2*d*r2))- 0.5 *sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2));
        areaOfOverlap=real(areaOfOverlap);
        
        area=pi*r1^2 + pi*r2^2 -areaOfOverlap;
    end
end


