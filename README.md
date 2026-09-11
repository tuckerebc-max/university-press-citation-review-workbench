# University Press Citation Review Workbench

This is the shareable Codex edition of the University Press workbench. It turns a folder of chapter manuscripts into author review packets while keeping the original chapters untouched. It runs the pinned Reference and Citation Integrity package first, then the pinned Scholarly and Editorial Integrity package.

Each editor uses their own Codex login and model capacity. There is no LunaRoute dependency and no workbench API key.

## What it produces

Every run creates a new folder in the output location you choose. For each chapter, the workbench produces a review copy with Word comments, an author query sheet, a browser-readable review, the two formal review records, a citation inventory, and a receipt tied to the source chapter's SHA-256 hash.

The workbench proposes edits and questions. It does not accept changes, overwrite manuscripts, decide that misconduct occurred, or authorize publication.

## Before the first run

The supported desktop path is Windows 10 or 11 with PowerShell, Python 3.11 or newer, and the Codex CLI.

1. Clone this repository with GitHub Desktop.
2. Open PowerShell in the repository folder.
3. Confirm that Codex is installed: `codex --version`.
4. Sign in with the Codex account whose capacity you want to use: `codex login`.
5. Run `./Setup-Workbench.ps1` once. It installs the single runtime dependency and checks the two vendored skill packages.
6. Run `./Start-Workbench.ps1` whenever you want to open the workbench.

If dependencies are already installed, `./Check-Setup.ps1` performs a read-only readiness check.

Codex supports either a ChatGPT sign-in or an OpenAI API-key sign-in. Authentication belongs to Codex itself; this repository does not read, copy, or store the credential. See the [official Codex authentication documentation](https://learn.chatgpt.com/docs/auth).

## Run a chapter batch

The browser interface opens at `http://127.0.0.1:8765/`.

1. Enter the folder containing the chapters.
2. Enter a separate output parent folder. The workbench will create a new, timestamped run folder there.
3. Scan the source set and name the editor or case owner.
4. Confirm that the signed-in Codex account is an approved processing route for that exact chapter manifest.
5. Leave the model field as `default`, or enter a model identifier available to the signed-in account.
6. Start the run and keep the PowerShell window open.
7. When the run finishes, choose **Open output folder** and start with `00_OPEN_RUN_SUMMARY.html`.

The model is not hard-wired. `default` asks Codex to use its current product default; an explicit model identifier overrides that choice for the run. If the account cannot use the requested model, the affected chapter stops with a visible error.

Supported chapter formats are `.docx`, `.md`, and UTF-8 `.txt`. Temporary Word owner files, symlinks, reparse points, empty files, and unsupported formats are skipped. A chapter may be at most 20 MB. A batch may contain at most 250 chapters or 500 MB.

## What “local” means

The workbench application, source scanning, document extraction, output assembly, state database, and author packets run on the editor's computer. Model inference is not offline: approved manuscript text is sent through the editor's signed-in Codex account. The account's workspace rules, retention terms, and model availability apply.

Every model call uses `codex exec` with an ephemeral session, a read-only temporary working directory, user configuration and project rules ignored, shell tools disabled, web search disabled, and a strict output schema. The source text goes through standard input rather than a command-line argument. [OpenAI's non-interactive Codex documentation](https://learn.chatgpt.com/docs/non-interactive-mode) describes the underlying command and schema controls.

Crossref DOI candidate lookup is a separate, optional network step and is off by default. Turn it on only for a manuscript set approved for that lookup.

## Choose a model and output folder from PowerShell

```powershell
./Run-Batch.ps1 `
  -InputFolder 'C:\Press\Volume 1\Chapters' `
  -OutputFolder 'C:\Press\Volume 1\Reviews' `
  -CaseOwner 'Volume editor' `
  -Model 'default' `
  -ApproveCodex
```

Replace `default` with a model identifier available to the signed-in Codex account. Add `-Crossref` to enable the optional Crossref step. One chapter runs at a time by default; `-Concurrency 2` or `3` is available for accounts with enough capacity.

## Output structure

```text
UP-Review-<timestamp>-<id>/
  00_SOURCE_MANIFEST.json
  00_IMMUTABLE_PLAN.json
  00_COMPANY_CONSTITUTION.json
  00_WORKBENCH_CONFIGURATION.json
  00_RUN_RECEIPT.json
  00_OPEN_RUN_SUMMARY.html
  events.jsonl
  learning-observations.jsonl
  chapters/
    CH001-<chapter-name>/
      author-review/
        <chapter>__AUTHOR_REVIEW.docx
        <chapter>__AUTHOR_QUERIES.md
        OPEN_REVIEW.html
      editorial-record/
        citation-inventory.json
        rci-run-result.json
        rci-workbench-record.json
        sei-run-result.json
        sei-workbench-record.json
        chapter-receipt.json
```

## Release and operating limits

- Treat this as supervised editorial review software. A press editor must check every proposed change and query.
- The two skill packages are pinned by commit and tree hash. Updating either package requires a new review and release.
- The deterministic citation parser is conservative. Unusual reference styles can receive partial coverage and a human-review condition.
- Encrypted Word files, active content, embedded objects, unsafe external relationships, symlinks, and reparse points are blocked.
- Do not commit chapter manuscripts, author packets, the `data/` directory, Codex credentials, or run output.

Run `./scripts/Run-ReleaseGate.ps1` before tagging a changed version. `SECURITY.md` records the security boundary and residual risks; `VERIFICATION.md` records the evidence for the reviewed release.
