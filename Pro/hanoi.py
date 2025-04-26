def towerofHanoi(n, source, dest, aux):
    if (n == 1):
        print("move disk 1 from " + source + " to " + dest)
    else:
        towerofHanoi(n-1, source, aux, dest)
        print("move disk " + str(n) + " from " + source + " to " + dest)
        towerofHanoi(n-1, aux, dest, source)


towerofHanoi(3, "A", "B", "C")
