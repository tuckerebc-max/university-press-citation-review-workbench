# University Press Workbench Security Review Boundary

## Posture

The workbench handles untrusted manuscript files and sends approved manuscript text through the editor's signed-in Codex account. It fails closed around archive structure, path identity, route approval, source drift, model output shape, browser origin, and release language.

No review can prove an application secure. The controls below describe the reviewed code path for this release.

## Trust boundaries

- Manuscripts, filenames, DOCX contents, citation strings, and model output are untrusted.
- The local editor controls the source folder, output parent, Codex login, model request, and per-run approval.
- Codex authentication and remote model processing are outside this repository. The workbench invokes the installed CLI but does not read or store its credentials.
- Crossref is an optional, separate metadata route limited to DOI candidate lookup.
- Author packets are proposals for human review; they are not publication-ready decisions.

## Implemented controls

- Binds the browser service to `127.0.0.1` and rejects non-loopback Host headers.
- Requires a random per-process request token and a same-origin header for each state-changing browser request.
- Sends restrictive CSP, frame, MIME-sniffing, cache, and referrer headers.
- Resolves a fixed `codex` executable and invokes it with a subprocess argument array, `shell=False`, and a bounded model identifier.
- Sends manuscript data through standard input, not the command line.
- Runs each Codex call ephemerally in a new temporary directory with a read-only sandbox, ignored user configuration and project rules, shell disabled, web search disabled, and a strict JSON output schema.
- Does not read, log, copy, or store Codex access tokens, API keys, authorization headers, or Codex credential files.
- Allows application-managed HTTP requests only to `api.crossref.org` when Crossref lookup is selected. Redirects and non-public DNS results are rejected.
- Never fetches a URL supplied by a manuscript or model.
- Rejects symlinks and Windows reparse points, enforces canonical source and output roots, and derives output names from internal chapter IDs.
- Checks the complete generated Windows path budget before model work and uses short atomic-write names, preventing a late packet failure caused by Word or Explorer path limits.
- Inspects DOCX member paths, duplicates, counts, expanded sizes, compression ratios, XML declarations, active content, embedded objects, and external relationships before parsing.
- Caps chapter count, individual and total bytes, request bodies, model input characters, subprocess output, workers, execution time, and model calls.
- Binds route approval to the exact source manifest hash and re-hashes each chapter before both model stages and packet assembly.
- Reads each approved chapter into a hash-checked byte snapshot and performs extraction from that snapshot, so later path changes cannot alter the content sent for review.
- Marks manuscript text as inert data in both review prompts and rejects schema-invalid output without coercion.
- Applies source-availability and neutral-language rules after model output.
- HTML-escapes author-facing values and produces script-free review HTML.
- Writes every model suggestion as a comment or query. Acceptance and publication are not reachable application actions.

Bandit records reviewed suppressions for B404/B603 at the four local-Codex subprocess sites. Those calls are the application's intended provider boundary: the executable is resolved to a regular file, arguments are passed as an array with `shell=False`, the model identifier is syntax-bounded, and manuscript content is passed through standard input. The gate also skips B606 for the guarded `os.startfile` call behind **Open output folder**. Its target comes from a validated, workbench-owned run record and is not interpreted by a shell.

## Credential handling

Run `codex login` outside the workbench. Codex owns its authentication store and token refresh. Do not copy `auth.json`, an API key, or an access token into this repository or a chapter folder. If a credential is exposed, preserve the evidence and ask the credential owner or workspace administrator to revoke or rotate it through the proper account controls.

## Residual risk

Remaining risks include Codex CLI or service behavior changes, a malicious executable earlier on the user's PATH, operating-system compromise, model prompt-following errors, schema-valid but inaccurate findings, parser gaps in unusual Word files, provider data-handling choices, and the draft status of both integrity skill packages. Disabling model tools limits prompt-injection impact but does not guarantee correct analysis.

## Release disposition

The September 11, 2026 local review disposition is **Ready with conditions**: the full release gate and a live end-to-end Codex run passed. GitHub Actions must also pass for the exact tagged tree before the release link is shared. Operation remains supervised. A press editor must review every packet and all blocked or high-risk findings.

Report suspected vulnerabilities privately to the repository owner. Do not include credentials or confidential chapter text in a public GitHub issue.
