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


def test3():
    line = [
        "/**",
        " * Unpacks a 16-bit number into its binary representation:",
        " * Takes the 16-bit number stored in RAM[8000] and stores its individual ",
        " * bits in RAM[8001..8016] (each location will contain 0 or 1).",
        " * Before the conversion, RAM[8001]..RAM[8016] are initialized to -1.",
        " * ",
        " * The program should be tested as follows:",
        " * 1) Load the program into the supplied VM emulator",
        " * 2) Put some value in RAM[8000]",
        ' * 3) Switch to "no animation"',
        " * 4) Run the program (give it enough time to run)",
        " * 5) Stop the program",
        " * 6) Check that RAM[8001]..RAM[8016] contains the correct binary result, and",
        " *    that none of these memory locations contains -1.",
        " */"
    ]

    ## When
    result = _remove_comment(line)

    ## Then
    assert len(line) == len(result)
    for l in result:
        assert l == ""


def test4():
    line = [
        "    /** Converts the given decimal value to binary, and puts ",
        "     *  the resulting bits in RAM[8001]..RAM[8016]. */",
        "    /** Returns the next mask (the mask that should follow the given mask). */",
        "    /** Fills 'length' consecutive memory locations with 'value',",
        "      * starting at 'startAddress'. */"
    ]

    ## When
    result = _remove_comment(line)

    ## Then
    assert len(line) == len(result)
    for l in result:
        assert l.strip() == ""
