# nand2tetris Jack Code Analyzer

## Getting Started

#### Preconditions

${JackFIleBaseName}T.xml is **tokenizer.py** result.

```shell script
../projects/10//ExpressionLessSquare/SquareT.xml
../projects/10//ExpressionLessSquare/SquareGameT.xml
../projects/10//ExpressionLessSquare/MainT.xml
../projects/10//ArrayTest/MainT.xml
../projects/10//Square/SquareT.xml
../projects/10//Square/SquareGameT.xml
../projects/10//Square/MainT.xml
```

${JackFIleBaseName}.xml is **compilation_engine.py** result.

```shell script
../projects/10//ExpressionLessSquare/Main.xml
../projects/10//ExpressionLessSquare/SquareGame.xml
../projects/10//ExpressionLessSquare/Square.xml
../projects/10//ArrayTest/Main.xml
../projects/10//Square/Main.xml
../projects/10//Square/SquareGame.xml
../projects/10//Square/Square.xml
```

#### Build

```shell script
$ python setup.py clean install
...

Using /path/to/.pyenv/versions/3.7.3/lib/python3.7/site-packages/zipp-3.1.0-py3.7.egg
Finished processing dependencies for janlz==1.0.0
```

#### Run

```shell script
$ janlz ../ArrayTest/Main.jack --debug
in    : /path/to/nand2tetris/projects/10/ArrayTest/Main.jack
out(T): /path/to/nand2tetris/projects/10/ArrayTest/output/MainT.xml
out   : /path/to/nand2tetris/projects/10/ArrayTest/output/Main.xml

  1:                                None                 None                 None       None                 None       None
  2:                                None                 None                 None       None                 None       None
  3:                                None                 None                 None       None                 None       None
  4:                                None                 None                 None       None                 None       None
  5:                                None                 None                 None       None                 None       None
  6:                                None                 None                 None       None                 None       None
  7:                                None                 None                 None       None                 None       None
  8: class Main                     None                 None                 None       None                 None       None
  8:  Main {                        Token.KEYWORD        class                None       None                 None       None
  8: Main {                         None                 None                 None       None                 None       None
  8:  {                             Token.IDENTIFIER     None                 None       Main                 None       None
  8: {                              None                 None                 None       None                 None       None
```

#### Confirm the output file

```shell script
$ head ../ArrayTest/output/MainT.xml
<tokens>
<keyword> class </keyword>
<identifier> Main </identifier>
<symbol> { </symbol>
<keyword> function </keyword>
<keyword> void </keyword>
<identifier> main </identifier>
<symbol> ( </symbol>
<symbol> ) </symbol>
<symbol> { </symbol>

$ head ../ArrayTest/output/MainT.xml
<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList>
```


#### Compare with correct tokenized XML files

Successful examples.

```shell script
$ ./TextComparer.sh ../projects/10/ArrayTest/MainT.xml ../projects/10/ArrayTest/output/MainT.xml
Comparison ended successfully

$ ./TextComparer.sh ../projects/10/ArrayTest/Main.xml ../projects/10/ArrayTest/output/Main.xml
Comparison ended successfully
```

Failed example.

```shell script
$ ./TextComparer.sh ../projects/10/Square/SquareGameT.xml ../projects/10/Square/output/SquareGameT.xml
Comparison failure in line 0:
<tokens_failed>
<tokens>
```

#### Appendix

This project uses [tox](https://tox.readthedocs.io/en/latest/#).

```shell script
$ tox

...

============================================================= test session starts =============================================================
platform darwin -- Python 3.7.3, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
cachedir: .tox/py37/.pytest_cache
rootdir: /path/to/nand2tetris/projects/10/janlz, inifile: setup.cfg, testpaths: tests
collected 1 item

tests/test_remove_comment.py .                                                                                                          [100%]

============================================================== 1 passed in 0.03s ==============================================================
...

TOTAL                                                                      16361   8972    45%
coverage-report run-test: commands[2] | coverage html
___________________________________________________________________ summary ___________________________________________________________________
  py37: commands succeeded
  coverage-report: commands succeeded
  congratulations :)

```