try:
    score = input("Enter Score: ")
    fs = float(score)
    if fs > 1.0 or fs < 0.0:
        print('enter a number between 0.0 and 1.0')
    elif fs >= 0.9:
        print('A')
    elif fs >= 0.8:
        print('B')
    elif fs >= 0.7:
        print('C')
    elif fs >= 0.6:
        print('D')
    else:
        print('F')
except:
    print('please enter a number')
    quit()