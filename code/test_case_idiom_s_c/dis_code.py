def chained_assignment():
    a,b=b,a
    x = y = a
    a, b, c = d, a
import dis
if __name__ == '__main__':
    dis.dis(chained_assignment)