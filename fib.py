def power(x,y):
    if y==1:
        return x
    else:
        return x*power(x,y-1)
power(3,2)