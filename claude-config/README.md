# Claude Code configuration

My setup for running reproducible quantitative analysis with Claude Code:
a backup hook, two skills, and a project scaffold.

## Layout

| Path | What |
|---|---|
| `CLAUDE.md` | How I want answers written |
| `settings.json` | Theme, update channel, hooks |
| `hooks/` | Scripts the harness runs automatically |
| `skills/` | Know-how loaded when a task calls for it |
| `templates/` | Starting points to copy into a project |

Global config is about *how I work*. Per-project config — the data, the
variables, the decisions already settled — goes in `<project>/.claude/CLAUDE.md`,
started from `templates/project-CLAUDE.md`.

## Hooks are not skills

A **skill** is instructions the model reads and follows. It applies judgment,
and it can be missed: if the description does not match the request, the skill
never loads.

A **hook** is a command the harness runs on an event, whether or not the model
thinks of it. No judgment, no forgetting.

So anything that must happen *every single time* is a hook, and anything needing
judgment about how to do the work is a skill. "Back up before editing" is a hook
for exactly that reason — a rule the model has to remember is a rule that
eventually gets skipped, and the cost of skipping it is a lost file.

## What is here

**Hook** — `PreToolUse` on `Write|Edit` runs `hooks/backup-file.py`, copying the
file to `backups/YYYY-MM-DD/HHMMSS_name.ext` before it changes. Silent on
failure, so a backup problem never blocks an edit. Uses Python rather than an
inline shell command because `jq` is not installed everywhere.

**`stata-analysis`** — sets up the project folder, writes every analysis to a
numbered do-file that runs top to bottom from raw data, and keeps the code free
of macros so each line reads on its own.

**`text-breakdown`** — works through a dense reading paragraph by paragraph,
with a running thread so the argument accumulates instead of fragmenting into
flashcards.

## Limits worth knowing

The backup hook covers the Edit and Write tools. It does **not** cover files
changed by shell commands, since a shell command does not announce which file it
is about to touch. It also does not cover Stata overwriting its own data — which
is why `stata-analysis` requires saving under a new filename.

Backups accumulate and nothing prunes them. Delete old dated folders when they
get large.

## Install

Copy into `~/.claude/`. The hook expects `python` on PATH.
