# nand2tetris Hack VM Translator

## Getting Started

```shell script
$ python setup.py clean install

...

Installed /Users/acto_mini/.pyenv/versions/3.7.3/lib/python3.7/site-packages/hvmt2-1.0.0-py3.7.egg
Processing dependencies for hvmt2==1.0.0
Finished processing dependencies for hvmt2==1.0.0
```

```shell script
$ hvmt ../StackArithmetic/SimpleAdd/SimpleAdd.vm --debug
  1: push constant 7      Command.PUSH         constant             7                   
  2: push constant 8      Command.PUSH         constant             8                   
  3: add                  Command.ARITHMETIC   None                 None    
```

