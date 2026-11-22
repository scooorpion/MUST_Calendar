# MUST Calendar

[English](README_EN.md) | [简体中文](README.md)

Subscribe to your Macau University of Science and Technology student timetable on iOS, Android, HarmonyOS, macOS, or Windows.

The program signs in to MUST CAS, reads course names, rooms, teachers, and lesson times from the student timetable, and writes them to `output/[StudentID].ics`.

## Local setup

1. Clone the repository.
2. Create `.env` in the project directory:

    ```dotenv
    TERM_CODES=2609,2702
    USERNAME=Your student ID
    PASSWORD=Your WeMust password
    ALERT=30
    LOCALE=en_US
    CHROMEDRIVER_PATH=.venv/bin/chromedriver
    ```

3. Install a ChromeDriver whose major version matches Chrome: [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/#stable). Omit `CHROMEDRIVER_PATH` if ChromeDriver is already in `PATH`.
4. Create a virtual environment and run the exporter:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python ./main.py
    ```

`TERM_CODES` accepts comma-separated four-digit term codes.

## GitHub Actions deployment

1. Fork the repository and enable Actions.
2. Add these repository secrets under `Settings` → `Security` → `Secrets and variables` → `Actions`:
   - `USERNAME`: student ID
   - `PASSWORD`: WeMust password
3. Set `TERM_CODES`, `ALERT`, and `LOCALE` in [.github/workflows/python-app.yml](.github/workflows/python-app.yml).
4. Run `Update Calendar Everyday` once and verify that `output/[StudentID].ics` is created.

Subscription URL:

```text
https://raw.githubusercontent.com/yourGitHubAccount/MUST_Calendar/refs/heads/main/output/[StudentID].ics
```
## TODO

- [x] Multiple terms
- [x] Multiple languages
- [ ] Exam calendar

PRs and Issues are welcome!
