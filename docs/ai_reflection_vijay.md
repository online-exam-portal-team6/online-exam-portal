# AI-use reflection — Vijay

## How I used AI assistance

I used an AI coding assistant (Claude Code) mainly for grunt work: repetitive,
time-consuming tasks where the thinking was already done and what remained was
mechanical effort. The decisions about what to test, what counts as a pass, and
what the evidence has to show stayed with me.

My main area was test execution and recording results in `docs/test_cases.xlsx`.
The assistant helped with the tedious parts of that work:

- Writing throwaway Django test-client scripts that follow each test case's
  steps exactly, such as logging in through the real form, posting data and
  reloading pages.
- Running the full test suite repeatedly and matching test names to TC IDs.
- Filling in the Actual result, Status, Execution date and Evidence columns in a
  consistent format for each row.
- Searching routes, views and branches to confirm whether a feature existed at
  all before I marked a case.

## Example from this project

TC-STU-02 (student profile view/update) was first recorded as **Not executed**
because no profile route or view existed at the time. The assistant ran the URL
probes and branch search that showed this. I decided that the result was
"Not executed" and not "Fail", since you cannot fail a feature that has not been
built.

After the profile feature (OEP-05) was merged, I asked the assistant to re-run
the case. It wrote the scripted steps: log in, open the profile from the
dashboard, change name and email, try to inject `username`/`is_staff`, reload,
and check duplicate-email and role access. It then updated the spreadsheet row.
I checked that the assertions matched the case's expected result before
accepting the **Pass**.

## My responsibility

The assistant saved me typing time but did not make my decisions. I chose the
pass/fail criteria, confirmed that each scripted check matched the written test
steps, used only synthetic users on a throwaway in-memory database, and made
sure the notes stated what was and was not verified. For example, the
server-rendered timer was checked but the JavaScript countdown in a real browser
was not. No credentials or real student data were given to the tool.

## Benefits

- Much faster execution and write-up of more than 20 test cases.
- Consistent, traceable evidence notes linking each row to a named test.
- More time left for judgement calls, such as how to classify a blocked case.

## Limitations

AI can produce a test that passes without checking the right thing, or it can
assume routes and fields that do not exist. A green run therefore means nothing
until someone reads the assertions. I treated every result as a draft until I
had reviewed it.

## What I learned

AI is most useful for removing the repetitive work around testing and
documentation. The judgement about what "correct" means, and the accountability
for the recorded result, belong to the tester.
