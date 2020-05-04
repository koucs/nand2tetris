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
