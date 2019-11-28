# calc (150 pts)
> Have you ever use Microsoft calculator?
>
> nc chall.pwnable.tw 10100

## Analysis
An infinite loop in ```calc()``` runs as long as the user is using the calculator. In each pass, the program 
1. Zeroes out a buffer that stores the user-supplied expression as well as well as a buffer that stores the result
2. Gets the expression by calling ```get_expr()```
3. Evaluates the expression by calling ```parse_expr()```
4. Prints the result

1, 2, and 4 are pretty self-explanatory and secure, so there's no need to look deeper into them. 

### The ```parse_expr()``` function
There's a small region in memory responsible for storing information related to the expression, let's call it ```pool```. Normally:
- ```pool[0]``` stores the number of operands (hopefully, it's 2)
- ```pool[1]``` stores the left operand AND (later) the result of the operation
- ```pool[2]``` stores the right operand

Let's run through an example expression ```2*5+1```.
Initially: 
```
pool[0] = 1
pool[1] = 0
pool[2] = 0
```
The program loops through every character of the expression. When it hits an operation, it'll stop and do a calculation. In this case, the first operation is multiplication, and the state of the pool changes as follows: 
```
//storing the operands
pool[0] = 2
pool[1] = 2 //left operand
pool[2] = 5 //right operand
```
```
//after an eval():
pool[0] = 2
pool[1] = 10
pool[2] = 5
```
The next operation is addition:
```
//storing the operands (pool[1] remains unchanged)
pool[0] = 2
pool[1] = 10
pool[2] = 1
```
```
//after an eval():
pool[0] = 2
pool[1] = 11 <-- the final result
pool[2] = 1
```
Next, let's take a look at what's actually happening when we evaluate an expression, and how we can exploit it. 
#### The ```eval()``` function

This function takes two arguments:
1. A pointer to the pool 
2. The operation it needs to perform

Here's what the function does: 

```pool[pool[0]-1] = pool[pool[0]-1] {operation} pool[pool[0]]```

where the operation is +, -, \*, or /.

This is based on the assumption that ```pool[0] = 2``` since there are 2 operands, so when evaluating an expression ```pool[1]``` is the left operand, ```pool[2]``` is the right operand, and the result is stored in ```pool[1]```. This is where the vulnerability is. By entering an expression with no left operand, like```+10000```, ```pool[0]``` has a value of 1, not 2, since there's only 1 operand. This is because ```pool[0]``` is actually initialized to 1, and the program adds 1 to it when it sees a left operand to get the normal value of 2. As a result, this operation is performed:

```pool[0] = pool[0] {operation} pool[1]```

The program mistakenly sees ```pool[0]``` as the left operand and ```pool[1]``` as the right operand, and the result is stored in ```pool[0]```. The implication of this is an arbitrary write, since we've demonstrated that we have control over ```pool[0]```, and the ```eval()``` function writes to a (stack) destination that is referenced by ```pool[0]```. So, if we wanted to write something 40 bytes above ```pool```, we would send an expression like ```+9+1```

This is the expression ```+9+1``` in action: 
Initially,
```
pool[0] = 1 
pool[1] = 0 
pool[2] = 0
```
The program encounters the first addition operation, and ```eval()```s accordingly:
```
//storing the operands
pool[0] = 1 //left operand - oops!
pool[1] = 9 //right operand
pool[2] = 0
```
After addtion: 
```
//after addition
pool[0] = 10
pool[1] = 9 
pool[2] = 0
```
The program now hits the second addtion operation. Here, there are actually two operands, so it's "normal," but ```pool[0]``` is unchanged from the previous hack:
```
//storing the operands
pool[0] = 10 
pool[1] = 1 
pool[2] = 0
```
Now, the program executes the addtion operation, but the result is stored in ```pool[9]```! 
## Crafting the exploit
We have write and read control over anything on the stack above ```pool```, and since ```pool``` is initialized in ```calc()```, we should have control over the return address of ```calc()```, opening up a ROP exploit. Using ROPgadget, we can find the addresses we need to load on the stack for a ROP chain that gives us a shell. 

However, we don't have "complete" write control; we can only modify values that are already on the stack (i.e. through addition or subtraction operations). So, we have to first leak the value that we want to write to, then add or subtract accordingly. 


