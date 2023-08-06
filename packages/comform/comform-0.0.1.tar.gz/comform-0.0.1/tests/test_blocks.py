from comform.codeline import CodeLines
from comform.kernel import fix_blocks

TEST_KEY = "blocks"


def test_blocks() -> None:

    with open(Rf".\tests\examples\{TEST_KEY}_good.py") as fh:
        correct_text = fh.read()

    code_lines = CodeLines(Rf".\tests\examples\{TEST_KEY}_bad.py")
    fix_blocks(code_lines, col_max=88)
    result = "".join(line.text for line in code_lines)

    # with open("temp.py", "w") as fh:
    #     fh.write(result)
    assert correct_text == result
