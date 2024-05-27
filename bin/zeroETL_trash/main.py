

def testFunc(*args):
    print(f"para1: {para1}")
    print(f"para2: {para2}")
    print(f"para3: {para3}")
    print(args)

def main():
    para1 = "val1"
    para2 = "val2"
    para3 = "val3"
    testFunc(para1 , para2 , para3)


main()