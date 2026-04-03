# NutriCore Mission Control Rules

> **Get Shit Done**: A spec-driven, context-engineered development methodology.
> 
> These rules enforce disciplined, high-quality autonomous development.

## Canonical Rules

1. **Plan Before You Build** — No code without specification (see `SPEC.md`).
2. **State Is Sacred** — Every significant action updates `STATE.md`.
3. **Context Is Limited** — Use search-first for research and targeted reads.
4. **Verify Empirically** — No "trust me, it works". Run tests and capture proof.
5. **Clean Workspace** — Do not leave test artifacts (`pytest_error*.txt`, etc.) in the repository.

## Workflow Integration

- **Execution**: Every task must be tracked in `task.md`.
- **Verification**: Changes must be validated using automated tests (backend `pytest`, frontend `npm run dev/lint`).
- **Audit**: Periodic audits for security and performance are mandatory.
