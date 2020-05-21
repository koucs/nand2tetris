# nand2tetris Jack Code Compiler

## Getting Started

#### Build

```shell script
$ python setup.py clean install
...

Using /Users/acto_mini/.pyenv/versions/3.7.3/lib/python3.7/site-packages/zipp-3.1.0-py3.7.egg
Finished processing dependencies for jac==1.0.0
```

#### Run

```shell script
$ jac ../ComplexArrays --debug
input                    : /path/to/nand2tetris/projects/11/ComplexArrays/Main.jack
output (tokenized)       : /path/to/nand2tetris/projects/11/ComplexArrays/output/MainT.xml
output (parsed)          : /path/to/nand2tetris/projects/11/ComplexArrays/output/Main.xml
output (vm)              : /path/to/nand2tetris/projects/11/ComplexArrays/output/Main.vm
```

#### Confirm the VM file

```shell script
$ head /path/to/nand2tetris/projects/11/ComplexArrays/Main.jack

function Main.main 3
push constant 10
call Array.new 1
pop local 0
push constant 5
call Array.new 1
pop local 1
push constant 1
call Array.new 1
pop local 2

```