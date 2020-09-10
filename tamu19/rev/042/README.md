# 042
This seems pretty important (line 142):
```
L_.str.2:                               ## @.str.2
	.asciz	"gigem{%s}\n"
```
If the program ever does printf(L_.str.2, somestring) that's probably the flag.

Conveniently, it does (line 114):
```
leaq	L_.str.2(%rip), %rdi
leaq	-16(%rbp), %rsi
movl	%eax, -72(%rbp)         ## 4-byte Spill
movb	$0, %al
callq	_printf
 ```
Looks like %s is retrieved from whatever is in [rbp-16]. Scanning the program for modifications to addresses around [rbp-16], we see (line 71):
 
```
movb	$65, -16(%rbp)
movb	$53, -15(%rbp)
movb	$53, -14(%rbp)
movb	$51, -13(%rbp)
movb	$77, -12(%rbp)
movb	$98, -11(%rbp)
movb	$49, -10(%rbp)
movb	$89, -9(%rbp)
```
Convert each number to a character, and get we the flag.
 
