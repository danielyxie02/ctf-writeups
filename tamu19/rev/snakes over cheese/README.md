# Snakes over Cheese

Given a .pyc file, we can decompile it with uncompyle6 (https://pypi.org/project/uncompyle6/).

This is what's inside:

```
from datetime import datetime
Fqaa = [102, 108, 97, 103, 123, 100, 101, 99, 111, 109, 112, 105, 108, 101, 125]
XidT = [83, 117, 112, 101, 114, 83, 101, 99, 114, 101, 116, 75, 101, 121]

def main():
    print 'Clock.exe'
    input = raw_input('>: ').strip()
    kUIl = ''
    for i in XidT:
        kUIl += chr(i)

    if input == kUIl:
        alYe = ''               
        for i in Fqaa:          
            alYe += chr(i)      

        print alYe              
    else:
        print datetime.now()


if __name__ == '__main__':
    main()
```
kUIl is a string from XidT, input is our input, and alYe is the flag (string from Fqaa).

We can just copy/paste the code into a file and modify it to build and print alYe immediately, giving us the flag.
