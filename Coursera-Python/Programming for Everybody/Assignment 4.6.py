def computepay(h, r):
    if h <= 40:
        p = h * r
    else:
        p = h * r + (h - 40) * r * 0.5
    return p


hrs = input('Enter Hours: ')
rate = input('Enter rate: ')
try:
    h = float(hrs)
    r = float(rate)
    print('Pay', computepay(h, r))
except:
    print('error')