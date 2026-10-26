# SRS v1.1 Revision Note

| Field | Value |
|---|---|
| Project | Online Exam Portal |
| Revises | SRS v1.0 (06-09-2026, author Bhumika Praveen Patil) |
| Prepared by | Vijay Suriya P (Product Owner / Business Analyst) |
| Date | 26-10-2026 |

## 1. Purpose

This note lists the corrections and scope clarifications found when SRS v1.0 was checked against the team contract
(Contract v1.0) and the testing documents. **No requirement text is added, removed or reworded.** The changes below
are to IDs, counts and scope statements only.

## 2. Revision history entry (to add to the SRS revision history table)

| Version | Date | Author | Change summary | Approval |
|---|---|---|---|---|
| 1.1 | 26-10-2026 | Vijay Suriya P | Corrected test case IDs in RTM (TC-RESULT to TC-RES); corrected functional requirement count (24, not 23) and sprint scope (22 of 24); clarified evaluation rule for OEP-F-021; aligned table of contents and section 7 heading | Pending |

## 3. Corrections

| # | SRS section | Issue found in v1.0 | Correction in v1.1 | Documents affected |
|---|---|---|---|---|
| C-01 | 8 (RTM) | The RTM lists the test cases for OEP-F-020 to OEP-F-024 as **TC-RESULT-01 to TC-RESULT-05**. Sections 4.6 and 6.2 and the team contract use **TC-RES-01 to TC-RES-05**. | Use **TC-RES-01 to TC-RES-05** everywhere. TC-RESULT is retired. | SRS RTM, RTM.xlsx, test_cases.xlsx, test method names (`test_TC_RES_01_...`) |
| C-02 | 4.6, 6.2, 8 | The SRS contains **OEP-F-024** (administrator views examination results, Medium, test TC-RES-05, suite OEP-TS-006). The contract (B1) says the SRS runs from OEP-F-001 to OEP-F-023 (23 requirements, 21 in scope). The SRS therefore has **24** functional requirements. | Functional requirements: **24**. Stretch/backlog stays at 2 (OEP-F-005, OEP-F-009). Sprint scope: **22**. | Contract B1, guide acceptance criteria ("21 in-scope requirements"), requirements_prioritisation.md, RTM.xlsx |
| C-03 | 4.6 | TC-RES-05 (OEP-F-024) has no owner in the test case ownership table (contract B9). | Proposed owner: Vijay (admin result list view `results:admin_result_list`). | test_cases.xlsx, contract B9 |
| C-04 | 4.6 (OEP-F-021) | The rule says "configured evaluation rules" without stating them. | For v1.0 the rule is: score = sum of marks of correctly answered questions; unanswered or blank answers score 0; **no negative marking**. Negative marking is change request CR-001, deferred to Sprint 2. | change_requests.md, test cases TC-RES-02 |
| C-05 | Table of contents, 7 | The table of contents calls section 7 "UML Use-Case Diagram". The body heading is "7. System models and diagrams" with sub-section 7.1. | Align the table of contents with the body heading. Insert the final use-case diagram under 7.1 (the text of the v1.0 file shows no diagram content there; check the file). | SRS document |
| C-06 | 8 (RTM) | The status column uses N/P/A for every row but the legend is not defined, and all rows show N. | Add a legend and update the statuses from the test execution log. The final statuses are set on Day 6. | RTM.xlsx |
| C-07 | 5.1.1, 8 | Security objectives SO-OEP-001 to 003 have no RTM rows. | Trace them through the existing security rows: SO-OEP-001 to OEP-SR-001 (TC-SEC-01), SO-OEP-002 to OEP-SR-003 (TC-SEC-03), SO-OEP-003 to OEP-SR-004 (TC-SEC-04). | RTM.xlsx |

## 4. Scope after v1.1

| Item | Contract / SRS v1.0 | v1.1 |
|---|---|---|
| Functional requirements in the SRS | 23 stated in contract; 24 present in SRS | **24** (OEP-F-001 to OEP-F-024) |
| Stretch / backlog | OEP-F-005, OEP-F-009 | Unchanged (tests TC-STU-02 and TC-EXAM-03 are also stretch) |
| In scope for the sprint | 21 | **22**: OEP-F-001 to 004, 006 to 008, 010 to 024 |
| Out of scope | Descriptive answers, online payment, live video proctoring (SRS 1.2, 2.5) | Unchanged. Negative marking is also out of scope (CR-001, Sprint 2). |

**Scope change:** the only change is that OEP-F-024 (admin result list) is now counted. It was already planned in the
contract (the `results:admin_result_list` view and Part A of the guide), so no new work is added.

**Open decision:** the non-functional requirements (OEP-NF-001 to 005) and security requirements (OEP-SR-001 to 005)
are not part of the 24 functional requirements. They stay in the RTM and are verified through TC-NFR and TC-SEC test
cases. Confirm with the team which NFRs are verified this sprint (for example, OEP-NF-004 availability can only be
checked on the deployed site).

## 5. Follow-up actions

| Action | Owner |
|---|---|
| Record the count change (23 to 24, scope 21 to 22) in `docs/contract_changes.md` after raising it at stand-up | Bhumika |
| Update the SRS file: revision history row, table of contents, section 7.1 diagram, RTM test IDs (C-01, C-05) | Bhumika (SRS author), with Vijay |
| Update RTM.xlsx, test_cases.xlsx, `docs/requirements_prioritisation.md` (21 to 22, add OEP-F-024, fill in the SRS IDs) | Vijay |
| Use TC-RES-xx in test names and test cases | All |
| Add the TC-RES-05 owner to the test ownership table (B9) | Vijay and Bhumika |

## 6. Definition of Done

- [ ] Reviewed pull request merged (merge commit, not squash)
- [ ] CI passing (docs-only change; no new tests or flake8 findings expected)
- [ ] Accepted by the Product Owner (Vijay Suriya P) in Jira
