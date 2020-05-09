# nand2tetris Jack Code Compiler

## Getting Started

#### Preconditions

${JackFIleBaseName}T.xml is **tokenizer.py** result.

```shell script
```

#### Build

```shell script
$ python setup.py clean install
...

Using /Users/acto_mini/.pyenv/versions/3.7.3/lib/python3.7/site-packages/zipp-3.1.0-py3.7.egg
Finished processing dependencies for jac==1.0.0
```

#### Run

```shell script
$ jac ../ArrayTest/Main.jack --debug

```

#### Confirm the output file

```shell script
$ head ../ArrayTest/output/MainT.xml
```


#### Compare with correct tokenized XML files

Successful examples.

```shell script
$ ./TextComparer.sh ../projects/10/ArrayTest/MainT.xml ../projects/10/ArrayTest/output/MainT.xml
```

