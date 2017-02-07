function [d] = distBetweenPoints( point1,point2 )

    x1=point1(1);
    y1=point1(2);

    x2=point2(1);
    y2=point2(2);
    
    
    d=sqrt((x2-x1)^2+(y2-y1)^2);

end

