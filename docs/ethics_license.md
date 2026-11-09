# Ethics, Privacy, Open-Source Licensing, and Patents

## Purpose and scope

The Online Exam Portal is a student project for creating multiple-choice exams,
recording attempts, evaluating answers, and displaying results. This note
documents the ethical and licensing considerations for the project. It is not
legal advice.

## Ethical use of AI

AI tools may assist with drafting, code suggestions, test ideas, and
documentation. Team members remain responsible for reviewing, understanding,
testing, and correcting AI-generated material before accepting it. AI output
must not be treated as authoritative or submitted without verification. Team
members should record meaningful AI assistance and corrections in their
individual AI reflections.

Do not enter passwords, secret keys, or identifiable real student information
into AI tools. Use synthetic data for development and testing. Automated
evaluation should apply the published answer key and marking rules consistently;
students should be able to see their own result, while access to other students'
results must be restricted.

## Student data and privacy

The portal can process account details, exam responses, scores, and pass/fail
results. This information should be treated as confidential educational data.
The team should:

- collect and retain only information needed to operate and test the portal;
- use synthetic or anonymised records in screenshots, demonstrations, and test
  reports;
- restrict result access to the relevant student and authorised staff;
- avoid committing production data, credentials, or database files to source
  control;
- use HTTPS and appropriate access controls when deploying the application;
- remove or securely dispose of test data when it is no longer needed.

The development database and test accounts are for demonstration only. Any real
deployment should follow the institution's applicable privacy and data-retention
policies and should provide students with clear information about the use of
their data.

## Project and third-party licences

The project intends to use the **MIT License** for its own original code and
documentation. The MIT License permits reuse, modification, and distribution,
including commercial use, provided the copyright and permission notice are
preserved. A copy of the MIT License should be included as the repository's
`LICENSE` file before distribution. The repository root inspected for this note
did not contain a `LICENSE` file, so the licence selection still needs to be
made effective in the distributed repository.

Third-party components have their own licence terms and those terms remain in
force. Django is distributed under the BSD 3-Clause License. Bootstrap is
distributed under the MIT License when used. The team should verify the exact
versions and licences of dependencies actually included or loaded (including
CDN assets), retain required notices, and review the dependency inventory/SBOM
before release. A dependency's licence is not replaced by the project's MIT
licence.

## Software patents

This project implements conventional web-application functions—exam authoring,
multiple-choice answer submission, and score calculation—using established
frameworks and standard programming techniques. No novel patentable invention
is claimed by this student project, and software is not automatically patented
merely because it is written as code. Patent rules vary by jurisdiction, so this
statement is a project-scope observation rather than a legal conclusion. The
team has not conducted a formal patent search and makes no claim that no patent
could apply to any third-party technology.

## Review before release

- Confirm that the repository includes the chosen MIT `LICENSE` file.
- Check dependency and CDN notices against the versions actually used.
- Keep real student data and secrets out of source control and test evidence.
- Recheck access controls and privacy handling before any deployment with real
  users.
