# ERI-38 synthetic implementation demonstration

This demonstration is content-free and does not authorize execution. It is
intended to exercise the selective planner, adaptive capacity seam, CE-gap
handling, and candidate review receipt shape before any real manuscript route
or human seal exists.

Run it from the repository with a private output root outside the repository:

```powershell
python scripts/run_eri38_demo.py `
  --output-root 'C:\Press\private-evidence\eri38-demo'
```

The generated `summary.json` reports two shapes:

| Shape | Requested stages | Candidate family nodes | Default demo admission |
|---|---:|---:|---:|
| Ten pieces | 1, 5, 6 | 10 RCI + 10 SEI + 10 CPR + 10 explicit CE gaps | 2 admitted, 38 waiting with two slots |
| One piece | 2 | 1 RCI prerequisite + 1 SGI | 2 admitted with three slots |

The demo writes only synthetic request, plan, and review receipts. It reports
zero model calls, zero network calls, no human dispatch, no publication effect,
and `execution_authorized: false`. `review` accepts the named
`university_press.synthetic_review_request.draft1` extension for this demo;
the live sealed-plan/human-authority path remains refused until its upstream
contract, route, and owner gates are adopted.
