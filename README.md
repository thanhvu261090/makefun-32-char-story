# Mom changed it after the divorce

[![make.fun](https://make.fun/badge/u-xvader-tell-a-whole-story-in-32-characters-f86dd978.svg)](https://make.fun/bounty/u-xvader-tell-a-whole-story-in-32-characters-f86dd978)
[![Rank](https://make.fun/badge/u-xvader-tell-a-whole-story-in-32-characters-f86dd978/thanhvu261090/makefun-32-char-story/rank.svg)](https://make.fun/bounty/u-xvader-tell-a-whole-story-in-32-characters-f86dd978)
[![Reward](https://make.fun/badge/u-xvader-tell-a-whole-story-in-32-characters-f86dd978/thanhvu261090/makefun-32-char-story/reward.svg)](https://make.fun/bounty/u-xvader-tell-a-whole-story-in-32-characters-f86dd978)

Entry for the [make.fun bounty "Tell a Whole Story in 32 Characters"](https://make.fun/bounty/u-xvader-tell-a-whole-story-in-32-characters-f86dd978): one Wi-Fi network name of at most 32 characters that tells a whole story.

## The entry

> Mom changed it after the divorce

(32 characters, one line.)

The divorce already happened, Mom now holds the password, and whoever
used to know it is locked out. One sentence carries the character
(Mom), the situation (the password changed), and what happened (the
divorce) — with the punchline landing on the last word, the way a
stranger scrolling a network list would read it.

## Run it

```sh
python3 main.py
```

`main.py` writes the entry line to `/output/entry.txt` (or `$ENTRY_OUTPUT`)
and includes a `gate_check` self-test enforcing the 1–32 character,
single-line, no leading/trailing whitespace rule, plus a `story_beats`
check that the character, situation, and event are all present. The
output is deterministic — byte-identical on every run.

```sh
python3 main.py --self-test
```

## License

MIT — see [LICENSE](LICENSE).
