#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters.

Writes one Wi-Fi network name of at most 32 characters -- a whole
domestic drama in a single line -- to /output/entry.txt.

The entry: "Mom changed it after the divorce"

One sentence, 32 characters. The divorce already happened, Mom now
holds the password, and whoever used to know it is locked out. A
stranger reading it in a network list gets the situation, the
character, and what happened, with the punchline landing on the last
word.

Deterministic: the entry is a fixed string; every run writes
byte-identical output.
"""

import os
import sys

ENTRY = "Mom changed it after the divorce"

MAX_CHARS = 32


def validate_is_string(text) -> None:
    """Entry must be a string."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")


def validate_length(text: str) -> None:
    """Entry must be 1-32 characters."""
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")


def validate_single_line(text: str) -> None:
    """Entry must be a single line (no newline or carriage return)."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def validate_no_surrounding_whitespace(text: str) -> None:
    """Entry must not have leading/trailing whitespace and must not be
    only whitespace."""
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def validate_utf8(text: str) -> None:
    """Entry must encode as valid UTF-8."""
    text.encode("utf-8")


def story_beats(text: str) -> dict:
    """Name the story beats the entry carries, for the self-test.

    A whole-story Wi-Fi name needs a character, a situation, and
    something that happened. This entry's beats: Mom (the character),
    the password change (the situation), and the divorce (what
    happened, landing on the last word).
    """
    words = text.split()
    return {
        "character": words[0] if words else "",
        "situation": "password changed",
        "event": words[-1] if words else "",
        "word_count": len(words),
    }


def gate_check(text: str) -> None:
    """Enforce the competition gate: 1-32 chars, single line, no
    leading/trailing whitespace, non-blank, valid UTF-8."""
    validate_is_string(text)
    validate_length(text)
    validate_single_line(text)
    validate_no_surrounding_whitespace(text)
    validate_utf8(text)


def resolve_output_path() -> str:
    """Output path comes from ENTRY_OUTPUT, defaulting to /output/entry.txt."""
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def write_entry(text: str, out_path: str) -> None:
    """Write exactly the line, no trailing newline, so the gated file is
    byte-identical to the entry."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def run_self_test() -> int:
    """Expanded self-test: verify the entry and each gate rule.

    Covers: the exact 32-char entry, byte-identical repeat writes,
    and rejection of a 33-char string, a multi-line string, a string
    with a carriage return, leading/trailing whitespace, an empty
    string, a whitespace-only string, and a non-string value.
    Returns 0 on success, 1 on any failure.
    """
    failures = []

    def expect_reject(label: str, value) -> None:
        try:
            gate_check(value)
        except ValueError:
            return
        failures.append(f"{label}: gate_check accepted it")

    def expect_accept(label: str, value) -> None:
        try:
            gate_check(value)
        except ValueError as exc:
            failures.append(f"{label}: gate_check rejected it ({exc})")

    # The entry itself: exact text and exact length.
    expected = "Mom changed it after the divorce"
    if ENTRY != expected:
        failures.append("ENTRY does not match the expected 32-char line")
    if len(ENTRY) != 32:
        failures.append(f"ENTRY is {len(ENTRY)} chars, expected 32")
    expect_accept("entry", ENTRY)

    # The story beats: a character, a situation, and an event, with
    # the punchline ("divorce") as the last word.
    beats = story_beats(ENTRY)
    if beats["character"] != "Mom":
        failures.append(f"story character is {beats['character']!r}, expected 'Mom'")
    if beats["event"] != "divorce":
        failures.append(f"story event is {beats['event']!r}, expected 'divorce'")
    if beats["word_count"] != 6:
        failures.append(f"entry has {beats['word_count']} words, expected 6")

    # Repeat writes must be byte-identical.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.txt")
        p2 = os.path.join(tmp, "b.txt")
        write_entry(ENTRY, p1)
        write_entry(ENTRY, p2)
        with open(p1, "rb") as f:
            first = f.read()
        with open(p2, "rb") as f:
            second = f.read()
        if first != second:
            failures.append("repeat writes are not byte-identical")
        if first != ENTRY.encode("utf-8"):
            failures.append("written bytes do not match ENTRY")

    # Boundary lengths: exactly 32 passes, 33 fails, 1 char passes.
    expect_accept("32-char string", "x" * 32)
    expect_reject("33-char string", "x" * 33)
    expect_accept("1-char string", "x")

    # Line and whitespace rules.
    expect_reject("multi-line string", "first line\nsecond line")
    expect_reject("carriage-return string", "first line\rsecond line")
    expect_reject("leading whitespace", "  padded")
    expect_reject("trailing whitespace", "padded  ")
    expect_reject("empty string", "")
    expect_reject("whitespace-only string", "   ")

    # Type rule.
    expect_reject("non-string value", 12345)

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAIL: {failure}", file=sys.stderr)
        return 1
    print("SELF-TEST PASS: entry 32 chars, gate rules verified")
    return 0


def main() -> int:
    gate_check(ENTRY)
    out_path = resolve_output_path()
    write_entry(ENTRY, out_path)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(run_self_test())
    sys.exit(main())
