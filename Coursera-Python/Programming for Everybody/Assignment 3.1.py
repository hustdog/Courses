hrs = input('Enter Hours: ')
rate = input('Enter rate: ')
try:
    h = float(hrs)
    r = float(rate)
    if h <= 40:
       p = h*r
    else:
       p = h*r + (h-40)*r*0.5
    print(p)

except:
    print('error')
    quit()