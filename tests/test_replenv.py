import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from REPLenv import ReplManager


def test_extract_code_with_python_fence():
    repl = ReplManager()
    response = """
    Here is the code:
    ```python
    value = 2 + 2
    print(value)
    ```
    """

    code = repl.extract_code(response)

    assert code == "value = 2 + 2\nprint(value)"


def test_extract_code_from_py_fence_alias():
    repl = ReplManager()
    response = """
    ```py
    result = 7 * 6
    print(result)
    ```
    """

    code = repl.extract_code(response)

    assert code == "result = 7 * 6\nprint(result)"


def test_execute_returns_error_message_for_invalid_code():
    repl = ReplManager()
    result = repl.execute("not valid python")

    assert "[REPL] Error during execution" in result
