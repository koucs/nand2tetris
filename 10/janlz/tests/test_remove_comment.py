from janlz.tokenizer import _remove_comment


def test_add():
    ## Given
    line = [
        "// ",
        "/** */",
        "/**",
        " *   TTTTTTTTTT",
        " *   TTTTTTTTTT",
        " *   TTTTTTTTTT",
        " *   TTTTTTTTTT",
        " */",
    ]

    ## When
    result = _remove_comment(line)

    ## Then
    assert len(line) == len(result)
    for l in result:
        assert l == ""


def test2():
    line = [
        "/**",
        " * Computes the value of 1 + (2 * 3) and prints the result",
        " * at the top-left of the screen.  ",
        " */"
    ]

    ## When
    result = _remove_comment(line)

    ## Then
    assert len(line) == len(result)
    for l in result:
        assert l == ""
