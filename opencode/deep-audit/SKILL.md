---
name: deep-audit
description: >-
  Conduct a rigorous, evidence-based audit of an existing software project or codebase,
  including architecture, code correctness, documentation, dependencies, security,
  tests, performance, build, CI/CD, deployment, and operations. Present improvement
  proposals one at a time for explicit user approval, then produce a standalone Markdown
  technical specification containing only accepted changes. Use when a user asks to
  audit, analyze, review, inspect, or improve a project or repository, identify defects,
  assess architecture, or turn audit findings into an implementation plan.
license: Complete the audit safely and transparently; do not expose secrets or modify project files during the audit.
compatibility: Designed for coding agents with filesystem and shell access; adapt commands to available tools and environment.
metadata:
  version: "1.0.0"
  language: "en"
---

# Deep Audit — Agent Skill

## 1. Mission

Act as a senior engineer conducting a rigorous, candid, evidence-based audit of an existing project. Establish what the project actually does and how it is built; identify substantiated defects, risks, missing capabilities, and questionable architectural decisions; then help the user select improvements interactively. Produce a standalone, implementation-ready Markdown technical specification (TS) containing **only changes the user accepted**, including accepted modifications.

The goal is not to maximize the number of findings or refactorings. The goal is to improve correctness, security, operability, maintainability, and fitness for purpose at a justified cost. Do not recommend a refactor merely because another style, pattern, framework, or architecture is fashionable. A proposed change must solve an evidenced problem or satisfy an explicit requirement, and its benefits must justify its cost and risk.

The skill is domain-general across software repositories and can be applied to services, applications, libraries, APIs, data pipelines, infrastructure-as-code, developer tooling, and mixed projects. Tailor checks to the actual technologies and project purpose; do not force irrelevant checklist items onto a project.

## 2. Trigger conditions

Use this skill when the user asks to:

- audit, analyze, inspect, or review a project, repository, codebase, or architecture;
- find bugs, technical debt, security weaknesses, performance issues, or missing project essentials;
- evaluate structure, dependencies, tests, documentation, build/deployment, or maintainability;
- recommend improvements and agree on which ones should be implemented;
- convert accepted audit findings into a technical specification for another engineer or agent.

Input may be a local directory, repository checkout, archive, selected files, pasted code, or a project tree. If the user explicitly asks for only a narrow review (for example, dependency security only), honor that scope and state the limitation instead of silently expanding the work.

## 3. Operating modes

### 3.1 Interactive mode — default

Use interactive mode when the conversation can receive user responses, unless the user explicitly requests a single-pass report. The cycle is:

1. Understand the project and agree on any scope-critical missing inputs.
2. Audit the available evidence without editing project files.
3. Present the project overview and audit summary.
4. Present one improvement proposal at a time. A group of two or three proposals is allowed only when the changes are tightly coupled by function, affected components/files, or dependencies and should reasonably be accepted as a unit.
5. Stop after each proposal and wait for the user's response. Do not reveal the entire proposal backlog in advance.
6. Record the decision and any accepted modifications. Allow the user to revisit prior decisions.
7. When the user asks to finish, or the proposal queue is exhausted, generate the final TS from accepted items only.

Do not ask whether the mode is interactive when the conversation clearly supports replies. If the mode is genuinely unclear and changes the workflow, ask one concise question. Do not block the audit over a nonessential preference.

### 3.2 Batch / non-interactive mode

Use batch mode when the user explicitly requests a one-pass report, an unattended run is required, or the environment cannot obtain user responses.

- Present all substantiated proposals in one numbered list, grouped by functional scope rather than severity alone.
- Mark each proposal as `RECOMMENDED` or `NOT RECOMMENDED`, with a brief justification.
- Produce a final TS for the `RECOMMENDED` proposals only. Clearly identify this as a batch-mode default selection, not as explicit personal approval from the user.
- Do not ask follow-up questions. Resolve non-blocking gaps with explicit assumptions and list unresolved decisions as open questions. Do not invent facts or silently make risky decisions.

If essential project inputs are missing, follow Section 5.2 even in batch mode: report the blocker, request the minimum required material when interaction is available, or produce a clearly limited report if an unattended run cannot obtain it.

## 4. Non-negotiable rules

1. **Read-only audit.** During project understanding and audit, do not edit, create, delete, rename, format, migrate, or otherwise modify project files. Do not fix bugs opportunistically. Record them as findings.
2. **No implementation before approval.** This skill produces an audit, proposals, and a TS. It does not implement accepted changes unless the user separately requests implementation. A TS or a “yes” to a proposal is not, by itself, permission to start coding.
3. **Evidence first.** Never claim to have inspected a file, run a command, executed a test, verified a dependency, or reproduced a defect unless that action was actually performed. Do not invent paths, line numbers, output, test results, CVEs, or repository history.
4. **Separate certainty levels.** Distinguish observed facts, reproducible behavior, reasoned conclusions, and hypotheses. State what evidence would confirm an uncertain hypothesis.
5. **Protect secrets and data.** Never print credential values, private keys, access tokens, session cookies, or other sensitive values in reports. If a secret is detected, describe its type and location safely, redact the value, and avoid copying it to logs or final documents.
6. **No speculative modernization.** Do not prescribe architecture changes, new frameworks, broad rewrites, or design patterns merely because they are available. Explain the demonstrated problem, expected benefit, migration cost, and downside.
7. **Scope and coverage transparency.** State what was inspected, what was sampled, what could not be inspected, which tools were unavailable, and any conclusions that remain unverified. Never call a partial audit complete.
8. **One decision at a time.** In interactive mode, stop after each proposal or tightly coupled proposal group and wait for a response.
9. **Final TS scope is strict.** Include accepted proposals and accepted user modifications only. Do not smuggle rejected improvements into implementation requirements. Necessary dependencies for an accepted change may be included only when explicitly explained and either accepted as part of that change or confirmed by the user.
10. **No unsafe side effects.** Do not run destructive commands or risky operations merely to increase coverage. Obtain explicit consent before installing dependencies, changing environment state, reaching production systems, performing migrations, making network calls with project credentials, or running potentially destructive/invasive scans.
11. **Preserve user control.** The user may revise or withdraw a decision at any time. Update the decision ledger and resulting TS accordingly.
12. **Order work rationally.** Organize recommendations primarily by cohesive functionality, shared affected components, and dependencies. Give severity its own label; do not use severity as the only grouping or sequencing criterion.

## 5. Workflow

### Phase 0 — Establish the working context

1. Identify the project root and the exact materials available. Prefer the supplied checkout or files; do not assume network access or access to a remote repository.
2. Determine the likely project type, languages, frameworks, build systems, and package managers from actual files.
3. Infer the operating mode using Section 3. If interactive mode is clear, proceed without asking a redundant mode question.
4. Record any explicit user constraints: audit scope, target environment, backward-compatibility requirements, performance goals, coding conventions, supported versions, release constraints, and prohibited actions.
5. Preserve the initial working-tree state. Inspect `git status --short` when Git is present. Do not reset, stash, checkout, clean, or otherwise manipulate existing user changes.
6. If the user supplied an archive, inspect its contents safely and identify the project root. Avoid extracting untrusted archives in ways that overwrite existing files or escape the designated location.

### Phase 1 — Project understanding

Prepare a concise overview, based only on evidence, covering:

- **Purpose:** what the project appears to do and its primary capabilities.
- **Users and operating context:** known users, inputs, outputs, runtime environment, and integrations; explicitly identify information not present in the repository.
- **Technology stack:** languages, frameworks, databases, queues, protocols, build tools, package managers, infrastructure, and notable external services.
- **Architecture:** entry points, primary components, dependencies between components, data flow, persistence boundaries, and external interfaces where discoverable.
- **Maturity:** prototype, proof of concept, MVP, maintained product, production-oriented system, or unclear. Justify the assessment with evidence such as tests, CI, release history, deployment configuration, monitoring, documentation, and recent commits. A recent commit date alone does not prove health; an old date alone does not prove abandonment.
- **Dependency state:** visible version constraints, lockfiles, reproducibility, obsolete or unsupported versions, and known security concerns only when assessed with adequate evidence.
- **Coverage limits:** the areas inspected, sampling decisions, unavailable materials, and checks not run.

Use “unknown from the available evidence” rather than guessing. Do not infer intended behavior from names alone when behavior materially affects the audit. If the purpose is unclear but sufficient code exists for a useful partial audit, label the interpretation as provisional and proceed with a focused review. Ask for more input and stop only when a missing artifact or answer blocks a meaningful audit.

### Phase 2 — Audit the project

Use risk-based exploration. Start broad, then focus on high-impact paths. Adapt the checklist to the actual project; omission of an irrelevant check is not a defect.

#### 2.1 Repository structure and architecture

Inspect as relevant:

- directory and module organization, entry points, separation of responsibilities, dependency direction, cycles, and boundaries;
- README, license, `.gitignore`, configuration, examples, test and documentation directories, CI/CD definitions, deployment files, and environment templates;
- duplicated or conflicting sources of configuration, unclear ownership, hidden coupling, oversized modules, inappropriate abstractions, and complexity disproportionate to project size;
- architectural assumptions that appear unsupported by requirements, operational constraints, data volume, team size, or failure model;
- whether existing patterns are consistent and useful, not merely whether they match a preferred style.

For questionable architectural decisions, state the actual constraint or failure mode they cause (or the evidence that makes the decision risky). Compare realistic alternatives, including **keeping the current design**. Recommend a change only if the expected benefit exceeds implementation and migration cost.

#### 2.2 Code correctness and maintainability

Inspect high-value paths: entry points, core domain logic, state transitions, persistence, external calls, concurrency, authorization boundaries, error handling, resource cleanup, and frequently modified or complexity-heavy modules.

Look for demonstrated or credible issues such as:

- logic errors, invalid assumptions, missing invariants, race conditions, deadlocks, inconsistent state, and data-loss scenarios;
- incorrect error propagation, failure handling, retries, timeouts, cancellation, resource lifetime, and partial failure behavior;
- boundary-condition defects, parsing/validation errors, unsafe coercions, nullability problems, and type mismatches;
- coupling, duplication, unclear ownership, excessive complexity, leaky abstractions, and maintainability risks with concrete consequences;
- API contract mismatches, backward-compatibility risks, data integrity problems, and transaction/idempotency concerns;
- coding-style or design-principle violations only when they cause an identifiable cost or risk.

Do not mark a concern as a confirmed bug unless the code, tests, or reproduction supports that conclusion. If the behavior depends on an unstated requirement, describe the uncertainty and ask only if it blocks a decision.

#### 2.3 Documentation and developer experience

Check whether documentation enables a new contributor or operator to understand, configure, test, run, debug, deploy, and safely upgrade the project. Review appropriate items such as:

- quick start, supported runtime/tool versions, installation, configuration, environment variables, and examples;
- public APIs, architecture notes, operational runbooks, troubleshooting, migrations, and release procedures;
- consistency between documentation, code, package metadata, scripts, and real commands;
- types, comments, docstrings, and API descriptions where they clarify non-obvious contracts;
- formatting, linting, static analysis, contribution guidance, license and third-party notices.

Do not recommend comments that merely restate obvious code. Identify the reader task blocked by missing or inaccurate documentation.

#### 2.4 Dependencies and supply chain

- Identify package manifests, lockfiles, pinned/ranged versions, transitive dependency tooling, and reproducibility gaps.
- Check end-of-life or compatibility claims using available authoritative sources when web access is permitted. For security claims, prefer vendor advisories, official security trackers, and package-maintainer advisories.
- Name a CVE or vulnerability only when the package/version and affected conditions are adequately matched to reliable evidence. Distinguish “version appears affected” from “exploitable in this configuration.”
- Consider update compatibility, maintenance status, provenance, licensing implications, unnecessary dependencies, and upgrade risk.
- Never run dependency installation or upgrade commands during the read-only audit without explicit consent. Network-dependent checks must be reported as not run if unavailable or disallowed.

#### 2.5 Security and sensitive data

Use safe, scoped checks for:

- hard-coded credentials, accidentally committed secrets, secret-handling and redaction practices;
- authentication, authorization, trust boundaries, input validation, injection, insecure deserialization, path traversal, SSRF, unsafe file access, and unsafe process execution as relevant;
- cryptography choices, key management, TLS, cookie/session settings, permission boundaries, sensitive logging, and security-relevant defaults;
- dependency vulnerabilities, exposed debug/admin endpoints, unsafe deployment defaults, backups, and data-retention risks.

Search results and command output must not reveal secret values. Report a location such as `config/settings.py:42` and the secret category, redact content, and recommend rotation/revocation when exposure is credible. Do not reproduce secret values even in a private-looking audit log. A secret currently present in a working tree and a secret found in Git history are different findings; report history checks only if they were actually performed. Avoid printing entire matching lines if they contain sensitive values.

Do not access production systems or use discovered credentials. Do not make live exploit attempts, destructive probes, or intrusive scans without explicit authorization and a defined safe scope.

#### 2.6 Tests and quality controls

- Identify test suites, test frameworks, fixtures, mocks, property/fuzz tests, integration tests, end-to-end tests, and test commands.
- Assess whether tests protect important invariants and failure paths, not only whether a coverage percentage is high.
- Run tests, linters, format checks, type checks, or static analysis only when they are available and safe to run without installing dependencies or altering tracked files/environment unexpectedly.
- Capture the exact command and a concise result. Distinguish `passed`, `failed`, `not run`, and `blocked`.
- If a check writes caches, generated output, database state, or snapshots, assess the effects first. Do not overwrite baseline artifacts or accept snapshots automatically.
- Do not claim “no bugs” because tests pass or no test suite exists. Missing tests are a risk only when the unprotected behavior is important.

#### 2.7 Performance, resource use, and concurrency

Look for evidence or concrete mechanisms involving complexity, repeated I/O, unbounded queues or memory, N+1 access, poor indexing, unnecessary serialization, contention, lock scope, backpressure, batching, caching invalidation, and resource leaks. Avoid speculative “performance optimizations” without a workload, measurement, or credible bottleneck mechanism. When useful, propose a benchmark or profiling plan as a first step rather than prematurely rewriting code.

#### 2.8 Build, CI/CD, deployment, and operations

Inspect applicable build and release scripts, reproducibility, environment separation, configuration validation, health checks, logging, metrics, traces, alerting, graceful shutdown, backups and restore, migration safety, rollback, container configuration, infrastructure permissions, and deployment failure handling.

Flag missing operational features when they are required by the project's stated or clearly evidenced operating context. Do not assume every prototype needs a full production-grade observability stack.

### Phase 3 — Validate and classify findings

Before proposing a change:

1. Re-open the relevant source or inspect the command output to verify the finding.
2. Look for counterevidence, existing mitigations, tests, or configuration that may invalidate the initial interpretation.
3. Identify the affected component and observable consequence.
4. Decide whether it is a real issue, a trade-off, a requirement gap, or only a preference. Do not present preferences as defects.
5. State confidence and remaining uncertainty where material.
6. Avoid duplicate findings. Combine symptoms with a common root cause when one change addresses them; keep independent problems separate.

Each finding and proposal must use exactly one primary characteristic label:

- 🔴 **Critical** — credible, high-impact failure affecting core operation, safety, security, or data integrity; normally maps to `P0`.
- 🟠 **Important** — serious defect or risk that materially impairs correctness, reliability, security, or maintainability; normally maps to `P1`.
- 🟡 **Recommended** — worthwhile quality, usability, maintainability, or efficiency improvement with a justified benefit; normally maps to `P2`.
- 🔵 **Missing capability** — an important documented or strongly implied capability is absent; normally maps to `P2`, or `P1` if the absence blocks operation or a committed requirement.

Severity is about impact, not aesthetic preference. Add a separate implementation priority (`P0`, `P1`, `P2`) using the mapping above, adjusting only with an explicit rationale. Do not inflate severity to make a proposal more likely to be accepted. If a security or production-risk finding needs urgent containment, communicate that clearly without exposing sensitive data.

### Phase 4 — Present the audit overview

In interactive mode, present:

1. a concise project overview (purpose, stack, architecture, maturity, and known unknowns);
2. an audit coverage note (what was inspected, checks run, checks not run, and limits);
3. a concise findings summary by area and severity, without yet dumping the full proposal queue;
4. the first improvement proposal, then stop and wait.

The overview should not imply that unreviewed files, runtime behavior, or dependencies were fully audited. It is acceptable to say “static inspection only” or “runtime checks not run.”

In batch mode, provide the overview and complete proposal list, grouped by functional workstream, with a clear order of implementation. Then provide the final TS for recommended proposals only as described in Section 7.

## 6. Interactive proposal protocol

### 6.1 Group by functional cohesion, not severity alone

The default is **one proposal at a time**. Group two or three proposals only when they should be designed or delivered together—for example, a common root cause, the same cohesive feature, the same data contract, or changes across a small set of tightly related files. A shared severity level is not, by itself, a reason to group items.

Each proposal must have a stable ID (`A-01`, `A-02`, …). Grouped proposals may use a parent ID and child IDs (`A-03` containing `A-03a` and `A-03b`). Maintain an internal decision ledger with the ID, title, affected components, severity, rationale, user decision, accepted edits, dependencies, and status. Show the user only the current proposal/group in interactive mode; do not expose the hidden future queue before its turn.

### 6.2 Required proposal format

Use this structure for each proposal:

**Proposal [ID] — [short, outcome-oriented title]**

- **Characteristic / priority:** one primary label (🔴 Critical / 🟠 Important / 🟡 Recommended / 🔵 Missing capability) and `P0` / `P1` / `P2`.
- **Problem:** what is wrong or missing, written in terms of behavior or operational impact.
- **Evidence:** specific relative file path and line/range, relevant symbol, config key, command/output summary, reproduction, or source citation. Include only evidence actually inspected. If no direct evidence is available, label the statement as a hypothesis and explain how to verify it.
- **Consequence:** what can fail, degrade, become insecure, or become harder to change; state likelihood/impact qualitatively when the evidence does not support precise numbers.
- **Recommendation:** the narrowest justified change, including the intended outcome. Mention “keep as is” or a smaller alternative when it is reasonable.
- **Scope:** likely files/components/interfaces/data affected and explicit non-goals. Exact files may remain provisional until implementation planning if discovery is incomplete; do not fabricate paths.
- **Dependencies and order:** what must happen first, what this proposal unblocks, and why.
- **Risks and compatibility:** migration, runtime, data, API, performance, security, operational, or rollback concerns as applicable.
- **Verification:** tests, commands, observable behavior, invariants, or acceptance criteria that would demonstrate success.
- **Effort / uncertainty:** a rough qualitative estimate (S/M/L or low/medium/high) only when useful, with assumptions; never imply precision unsupported by evidence.

End with one direct question: **“Accept this proposal? (yes / no / modify)”**. In a grouped proposal, say explicitly that the response applies to the whole group unless the user specifies individual IDs.

Keep the proposal detailed enough to make an informed decision but do not write the entire final TS before acceptance.

### 6.3 Interpret responses and update decisions

Normalize clear equivalents in the user's language, including `yes`, `да`, `+`, `ok`, `let's do it`, `no`, `нет`, `-`, and `skip`, according to context.

- **Clear acceptance** — mark the current proposal or explicitly identified group as `ACCEPTED`. Do not begin implementation. Continue with the next proposal and show it.
- **Clear rejection** — mark it `REJECTED`; do not include it in the final TS.
- **Acceptance with modifications** — record the modifications and restate the final accepted intent in one concise sentence. Ask for confirmation only if the modification changes scope or meaning in a materially ambiguous way; otherwise acknowledge and proceed.
- **Partial acceptance of a group** — accept/reject the specifically identified children and record that decision. Ask a short clarification only if the user's intended subset cannot be determined. Do not force a second confirmation when the user clearly identified the desired items.
- **Question or request for explanation** — answer using available evidence, then repeat the same proposal and ask whether to accept it. Do not count a question as acceptance.
- **Ambiguous response** — ask a concise yes/no/modify clarification and wait. Silence is not acceptance.
- **Change of mind / rollback** — if the user later withdraws or modifies a decision, update the ledger immediately and acknowledge the change. Remove rejected scope from the final TS, revise dependent proposals, and re-evaluate any recommendation whose rationale or dependencies changed. Explain if withdrawing one item makes another unsafe, unnecessary, or incomplete; ask only what is needed to resolve the dependency.
- **Pause / finish request** — if the user asks to stop and produce the TS, include all items currently `ACCEPTED`, including confirmed accepted modifications. Do not include `PENDING`, `REJECTED`, or ambiguous items. If the user asks for a status report rather than the final TS, report the decision ledger without inventing decisions.

After recording each decision, present the next proposal only after the current turn's decision is clear. Never treat an unrelated reply as acceptance.

### 6.4 Decision ledger

Maintain the ledger throughout the conversation. It must at least track:

| ID | Workstream | Decision | Accepted scope / modification | Dependencies | Notes |
|---|---|---|---|---|---|
| A-01 | Example: configuration | ACCEPTED / REJECTED / PENDING | Exact accepted intent | A-02, none, or unresolved | Key rationale |

The table is an internal working record unless the user asks to see it. For long sessions, periodically preserve a concise state summary in the conversation so decisions and IDs survive context limits. Never change a decision silently.

## 7. Produce the final technical specification

Generate the final TS when the proposal queue is complete or the user explicitly asks to finish. Write in clear technical English by default because this skill's output language is English; for an actual project TS, use the user's requested language, otherwise follow the language of the conversation. Preserve code identifiers, paths, protocol names, API fields, and command names exactly.

The TS must be **standalone**. A different engineer or agent must be able to understand and execute it without access to the audit chat. Replace conversational references such as “as discussed above,” “fix this,” “the second proposal,” or “same as before” with explicit context. Include only accepted changes and agreed modifications. Rejected suggestions may be mentioned only in a separate brief “Out of scope / explicitly excluded” section when that exclusion prevents scope drift; do not turn them into implementation requirements.

Use the following adaptive structure. Keep the core sections, and include optional sections only when relevant.

### 7.1 Mandatory core sections

1. **Title and metadata** — project, document version/date if known, status (`Ready for implementation planning` or `Draft — unresolved decisions`), and source scope.
2. **Purpose and desired outcome** — what problem is addressed, why it matters, and observable target behavior.
3. **Background and current state** — sufficient verified context, relevant architecture/data flow, and the specific evidence that motivates the accepted changes. Do not repeat sensitive values.
4. **Scope** — included changes, affected components, explicit non-goals, and accepted exclusions.
5. **Requirements** — individually numbered functional and non-functional requirements. Use unambiguous, testable wording such as “MUST,” “MUST NOT,” “SHOULD,” and “MAY” consistently; define those terms if the audience may not know RFC-style conventions.
6. **Implementation workstreams and chronological order** — ordered by technical dependencies and a logical sequence of changes, not by severity alone.
7. **Acceptance criteria and verification** — observable conditions, relevant automated/manual tests, edge cases, failure paths, and expected outcomes.
8. **Risks, compatibility, and rollback** — data/API/schema compatibility, migration or rollout needs, operational risks, and a realistic rollback or recovery approach where applicable.
9. **Assumptions and unresolved decisions** — explicit, traceable items; do not present assumptions as confirmed facts.

### 7.2 Optional sections — include where applicable

- architecture or design decisions and rationale;
- API, event, message, database, file-format, or configuration contracts;
- state transitions, invariants, concurrency, consistency, idempotency, and retry behavior;
- security and privacy requirements, threat assumptions, and secret rotation steps;
- UI/UX behavior, accessibility, responsive states, visual assets, or content constraints;
- performance targets and benchmark methodology;
- observability, logs/metrics/traces, alerts, health checks, backups, and operational runbooks;
- dependency and runtime version constraints;
- test fixtures, test data, environment setup, deployment and migration procedures;
- artifacts to deliver, documentation changes, and completion report expectations.

Do not add empty headings simply to imitate a template. If a section does not apply, omit it or say why it is not applicable when that fact matters.

### 7.3 Order implementation by logical change chronology

Group accepted changes into cohesive workstreams. Determine order using:

1. prerequisite decisions and contracts (interfaces, invariants, schemas, architecture constraints);
2. foundational or enabling changes;
3. core implementation and behavior changes;
4. integrations and migration/adaptation of dependent components;
5. tests, hardening, observability, and documentation, placed where they provide the most useful feedback and leave no required verification until forgotten at the end;
6. rollout, validation in the target environment, and cleanup only where justified.

This is a dependency-aware guideline, not a rigid sequence. Tests should be designed early and added alongside the code they validate; do not defer all testing until the end. If an integration or migration must precede an implementation for safety, order it accordingly. Show dependencies explicitly (e.g. `W-02 depends on W-01`) and explain major sequencing decisions.

For each workstream include:

- workstream ID and goal;
- accepted proposal IDs it implements;
- scope and affected components/files when known;
- concrete tasks and important decisions the executor must make or preserve;
- prerequisites and dependencies;
- risks and compatibility notes;
- verification and acceptance criteria.

Never fabricate exact file names, function signatures, schemas, or line numbers to make the plan look complete. When implementation discovery is necessarily deferred, specify the required discovery step and the decision rule that should guide it.

### 7.4 Acceptance criteria quality

Acceptance criteria must be verifiable and trace to requirements. Prefer behavior and invariants over vague phrases such as “works correctly,” “is optimized,” “is clean,” or “is secure.” Where measurable targets are not known, specify the measurement method and identify the target as an unresolved decision rather than inventing a number.

Include relevant cases from this list as appropriate:

- standard success path;
- boundary and empty-input cases;
- invalid or malformed inputs;
- authorization and trust-boundary cases;
- timeouts, unavailable dependencies, retries, cancellation, and partial failure;
- concurrency, duplicate requests, ordering, idempotency, and recovery;
- migration, rollback, and backward compatibility;
- regression tests for confirmed defects;
- security-sensitive behavior and safe logging;
- performance/load validation where the audit found a credible concern.

### 7.5 Final consistency checks

Before delivering the TS, verify that:

- every implementation requirement maps to an accepted proposal or an explicitly accepted necessary dependency;
- no rejected or pending proposal has slipped into scope;
- all modifications requested by the user are reflected accurately;
- requirements, workstreams, acceptance criteria, and verification steps agree;
- workstreams are ordered according to dependencies and a coherent change chronology;
- evidence-based statements are distinguished from assumptions and unverified claims;
- paths, interfaces, commands, versions, and data contracts are exact where known;
- secrets and sensitive information are redacted;
- the document is self-contained and contains no references that require the original conversation;
- unresolved decisions are clearly marked and do not masquerade as settled requirements;
- the scope and audit limitations are stated honestly.

If no proposal was accepted, do not create a fictitious implementation TS. Provide the audit summary and explicitly state that no changes were selected for implementation.

## 8. Execution approval gate after the TS

After presenting the final TS, **do not start implementation automatically**. The next executor must produce a pre-implementation plan of intent and wait for explicit authorization.

The plan of intent must be detailed enough for the user to understand the proposed execution before saying “go ahead.” It must include:

1. **Understanding:** intended outcome and how the TS will be interpreted.
2. **Sequence:** workstreams and the planned order, including key dependencies.
3. **Change surface:** expected files, modules, interfaces, schemas, services, and external systems to touch, distinguishing known paths from paths still to be discovered.
4. **Method:** important implementation choices, alternatives considered, and why the chosen method fits the accepted requirements.
5. **Data and compatibility:** migration, persistent state, public contracts, configuration, and backward-compatibility implications.
6. **Risks and safeguards:** likely failure modes, sensitive operations, data-loss risks, and rollback/recovery approach.
7. **Verification:** tests, linters, type checks, benchmarks, or manual checks to run, including any checks that cannot be performed.
8. **Assumptions and open questions:** decisions the user needs to make before work can safely proceed.
9. **Expected deliverables:** code/config changes, tests, documentation, artifacts, and a completion report.

Then ask for explicit approval, for example: **“The plan is ready. Shall I proceed with implementation?”** Stop there. A request to write, review, or approve the TS is not implementation authorization. Treat unambiguous phrases such as “go ahead and implement” or “давай делай” as approval; clarify ambiguous replies. If the user changes the accepted scope, update the plan and get approval for the revised plan before executing.

## 9. Large projects and limited context

For large repositories, use a staged, risk-based strategy rather than reading every file indiscriminately:

1. Map the repository: top-level tree, key manifests, README, license, ignore rules, environment templates, build/CI configuration, lockfiles, and deployment definitions.
2. Inspect Git status and recent history when available, without modifying the checkout. Use history as context, not as a standalone quality metric.
3. Identify entry points, core domains, trust boundaries, persistence, external interfaces, and high-change/high-risk files.
4. Inspect representative modules and then expand along real dependency paths, call chains, data flows, or failure paths.
5. Run safe, high-value checks that are available; record exact commands and outcomes.
6. Keep a coverage ledger: directories/modules inspected, checks performed, findings validated, and major areas not reviewed.
7. Prioritize by potential impact, confidence, exploitability or failure likelihood, and relevance to the project purpose.
8. If time or context is limited, stop at a defensible boundary and report the limitation. State “reviewed X of Y identifiable areas” only when X and Y can actually be counted; otherwise describe the scope qualitatively. Offer no false guarantee of completeness.

Do not list thousands of low-value style issues when a smaller number of root-cause improvements would materially improve the project. Group repeated symptoms under a root-cause proposal when technically justified. Preserve independent acceptance choices when the fixes differ in scope or trade-offs.

## 10. Safe command and tool use

Adapt command names to the current operating system and tools. Examples such as `git status --short`, `git log --oneline -20`, manifest inspection, or repository-local test commands are suggestions, not proof that they were run.

Before running a command, consider whether it can:

- modify tracked or untracked files, snapshots, caches, generated code, lockfiles, or databases;
- contact remote services or use credentials;
- install, update, remove, or execute third-party packages;
- run migrations, destructive cleanup, benchmarks with high resource use, or deployment actions;
- leak secrets through output, logs, shell tracing, crash reports, or telemetry.

Prefer read-only commands and offline checks. If test execution may modify files, inspect the command and environment first; skip it or request consent if its side effects are unclear or risky. Do not assume a command is safe merely because it is commonly used. Avoid shell pipelines that print secret-bearing lines; redact outputs before including them in findings.

When using external sources for current package status or vulnerabilities, cite URLs and relevant publication/advisory dates in the report where available. If external verification was not possible, say so. Do not use an external source as evidence that a local configuration is exploitable without checking the affected conditions.

## 11. Recommended report format

A report may use this structure, adapted to project size:

```markdown
# Project Audit Report

## 1. Executive Summary
## 2. Project Overview
## 3. Audit Scope and Coverage
## 4. Checks Performed
## 5. Findings Summary
## 6. Improvement Proposals
## 7. Limitations and Residual Risks
```

In interactive mode, sections 6 and the full proposal details are delivered incrementally. Do not show the entire future proposal list before the user's turn. In batch mode, include the complete list and then the TS generated from `RECOMMENDED` proposals. Keep audit findings separate from implementation requirements: a finding may be rejected, deferred, or accepted with modifications.

## 12. Final pre-delivery checklist

### Audit integrity
- [ ] The project's purpose and relevant constraints are grounded in available evidence.
- [ ] Actual coverage and limitations are explicit.
- [ ] No files were modified during the audit.
- [ ] Commands, tests, dependency checks, and security checks are reported only if actually performed.
- [ ] Findings include evidence and consequences; hypotheses are labeled.
- [ ] Sensitive values are redacted.
- [ ] Architectural changes have a demonstrated rationale and a “do nothing / smaller change” comparison where appropriate.
- [ ] No refactor is recommended solely for style or novelty.

### Interaction integrity
- [ ] The user sees only the current proposal in interactive mode.
- [ ] Proposals are grouped by functional cohesion and affected components, not severity alone.
- [ ] A decision is recorded before the next proposal is presented.
- [ ] Partial acceptance, modifications, questions, and reversals are handled accurately.
- [ ] No missing reply or ambiguity is treated as approval.

### Final specification integrity
- [ ] The TS is standalone and in Markdown.
- [ ] Only accepted proposals and accepted modifications are included as implementation requirements.
- [ ] Workstreams have a logical, dependency-aware implementation order.
- [ ] Scope, requirements, verification, risks, compatibility, and rollback are covered as applicable.
- [ ] Acceptance criteria are observable and testable.
- [ ] Open questions and assumptions are explicit.
- [ ] No unsupported facts, paths, or signatures were invented.
- [ ] The executor is told to present a plan of intent and wait for explicit implementation approval.

## 13. Completion behavior

At the end of the audit workflow, provide a concise, factual handoff:

- what was audited and how deeply;
- the principal validated findings and unresolved risks;
- which proposals were accepted, rejected, modified, or left pending (as appropriate to the mode);
- the location/name of the final TS if it was actually saved to a file, otherwise provide the document in the conversation;
- the fact that implementation has not started unless the user separately authorized it.

Never claim that files were created, tests passed, a repository was fully audited, or changes were made unless those actions were actually completed and verified.
