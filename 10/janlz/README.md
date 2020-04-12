# nand2tetris Jack Code Analyzer

## Getting Started

### Tokenizer

#### Preconditions

${JackFIleBaseName}T.xml is the tokenized result.

And those files have been stored at the following directories.

```shell script
$ find ../projects/10/ -name "*T.xml" | grep -v "output"

../projects/10//ExpressionLessSquare/SquareT.xml
../projects/10//ExpressionLessSquare/SquareGameT.xml
../projects/10//ExpressionLessSquare/MainT.xml
../projects/10//ArrayTest/MainT.xml
../projects/10//Square/SquareT.xml
../projects/10//Square/SquareGameT.xml
../projects/10//Square/MainT.xml
```

#### Compile

```shell script
$ python setup.py clean install


Using /path/to/.pyenv/versions/3.7.3/lib/python3.7/site-packages/zipp-3.1.0-py3.7.egg
Finished processing dependencies for janlz==1.0.0
```

```shell script
$ janlz ../ArrayTest/Main.jack --debug
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
```


#### Compare with correct tokenized XML files

Successful examples.

```shell script
$ ./TextComparer.sh ../projects/10/ArrayTest/MainT.xml ../projects/10/ArrayTest/output/MainT.xml
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