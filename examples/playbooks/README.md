# Worked example — a playbook doc set

`lynqu-sales-playbook` reads a folder like this one and provisions it into
Lynqu: leads, buying committees, dated tasks, the playbook attached to each
lead, and stage rules that deliver the prep at the right moment.

Everything here is **fictional**. Northwind Brokerage, its people and its
numbers do not exist. The point is the *shape* — swap in your own account and
the skill works the same way.

| File | What the skill takes from it |
| --- | --- |
| [`DECISION-MAKERS.md`](DECISION-MAKERS.md) | The people, their role in the deal, and which track they belong to |
| [`OUTREACH-SEQUENCE.md`](OUTREACH-SEQUENCE.md) | The touches: channel, day offset, purpose |
| [`MEETING-PREP.md`](MEETING-PREP.md) | The briefing that gets attached to the "Discovery booked" stage |

## Running it

```
/lynqu playbook examples/playbooks
```

The skill shows you the plan — how many leads, which pipeline, which stages get
rules — and waits for a yes before it writes anything.

## What you should end up with

- **2 leads.** The three corporate people collapse onto ONE deal with three
  participants (they all have to say yes to the same purchase); the regional
  manager is her own lead on a separate track.
- **Dated tasks** from the sequence, counted from the day you run it.
- **This playbook attached** to each lead, rendered inline in the browser — the
  lead's Engagement tab shows the Documents panel, and Markdown opens as
  formatted text rather than a download.
- **Two stage rules**, which are the part that keeps working after this run:
  every lead that ever reaches "Discovery booked" gets the meeting-prep note
  and an agenda task, not just these two.

Stage rules need the Workflow Automation add-on. Without it everything else
still provisions, and the skill tells you which stages have no rule.
