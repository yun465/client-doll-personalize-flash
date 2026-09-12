# Contributing

Thanks for helping improve this privacy-first workflow.

## Before opening a change

1. Use an Issue to describe the hardware profile, workflow gap, or reproducible failure.
2. Remove customer names, chat text, recordings, credentials, device backups, private paths, MAC addresses, and customer firmware artifacts.
3. Keep project-specific hardware constants in a clearly labeled reference profile; do not turn one project's paths or recovery behavior into a universal Skill rule.
4. Preserve the independent approval gates for persona analysis, audio, build, board identification, flashing, credential writes, and real cloud calls.

## Pull requests

- Keep `SKILL.md` concise and route detailed project procedures to `references/`.
- Update both `README.md` and `README.zh-CN.md` when public behavior changes.
- Add or update a sanitized example when it materially clarifies the workflow.
- Run:

  ```text
  python scripts/validate_skill.py
  ```

- Summarize what was tested and which operations were deliberately not performed.

Never attach real customer data to an Issue or Pull Request, even if the repository is later made private.
