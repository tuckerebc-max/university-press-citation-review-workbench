# Project history and scope

This repository was split from the first University Press workbench after the intended users were clarified.

The LunaRoute edition remains a separate, owner-operated repository. This edition removes that dependency and routes each review through the editor's own authenticated Codex CLI installation. The split keeps credentials, provider assumptions, setup instructions, and receipts unambiguous.

The decisions carried into both editions are unchanged:

- University Press owns the editorial constitution and every acceptance or publication decision.
- Reference and Citation Integrity runs before Scholarly and Editorial Integrity.
- Both skill packages are pinned and checked by tree hash.
- Source chapters remain untouched; author copies contain proposals and queries.
- Every run starts from a manifest, records its execution plan, and closes with receipts.
- Restricted manuscripts are blocked until a separately reviewed handling policy exists.

The Codex edition adds user-controlled model selection and user-controlled output location. Model access and billing follow the account authenticated with `codex login`.
