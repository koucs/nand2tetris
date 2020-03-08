# nand2tetris Hack VM Translator

## Getting Started

```shell script
$ python setup.py clean install

...

Installed /Users/ksugihara/.pyenv/versions/3.6.5/lib/python3.6/site-packages/hvmt-1.0.0-py3.6.egg
Processing dependencies for hvmt==1.0.0
Finished processing dependencies for hvmt==1.0.0
```

```shell script
$ hvmt ../StackArithmetic/SimpleAdd/SimpleAdd.vm --debug
  1: push constant 7      Command.PUSH         constant             7                   
  2: push constant 8      Command.PUSH         constant             8                   
  3: add                  Command.ARITHMETIC   None                 None    
```

```shell script
$ cat ../StackArithmetic/SimpleAdd/SimpleAdd.asm

// DEBUG == Command.PUSH constant 7 ==
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == Command.PUSH constant 8 ==
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// DEBUG == add ==
@SP
AM=M-1
D=M
A=A-1
M=D+M

```