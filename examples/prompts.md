# Prompt library

Copy, tweak, and paste. Each prompt assumes the Lynqu MCP server is connected
and the relevant skill is installed. Plain language works — these are just
good starting points.

## Getting oriented

> "Use Lynqu to tell me who I am and give me an org summary."

> "What can you help me do with Lynqu?" *(triggers the `how-can-you-help-me` tool)*

## Lead research → `lynqu-lead-research`

> "Build a list of 10 mid-market SaaS companies in DACH attending SaaStr Europe,
> find a VP Sales or RevOps lead at each, score them for Lynqu, and create leads
> for anything scoring 7+."

> "Here are 5 companies we're curious about [list]. Research each, find the best
> decision-maker, and tell me which are worth pursuing before you create
> anything."

## Lead capture → `lynqu-lead-capture`

> "Here are 25 people from yesterday's booth [paste]. Dedupe against our
> contacts, add the new ones to the Events pipeline at 'New', tag them
> `SaaStr-2026`, set temperature warm, and attach them to the SaaStr campaign."

> "Import this prospect list [paste]. Skip anyone we already have, and tell me
> who you skipped and why."

## Lead management → `lynqu-lead-management`

> "Groom the Inbound pipeline: list unassigned leads, round-robin them across
> active SDRs, flag deals stuck in Qualified 14+ days, and bulk-set cold for
> anything untouched in 30 days. Confirm with me before bulk changes."

> "Move all my Demo-stage leads tagged `webinar` into the Won stage — wait, show
> me the list first."

## Sales follow-up → `lynqu-sales-followup`

> "Draft post-event follow-ups for everyone tagged `SaaStr-2026` in the Warm
> stage using the 'Event recap' template, personalize from each lead's notes,
> show me the drafts, then send and log after I approve."

> "Write a re-engagement note for this stalled lead [name] based on their
> timeline, and once I'm happy, send it and bump the stage."

## Event blitz → `lynqu-event-blitz`

> "We have a booth at SaaStr next week. Set up the campaign and event in Lynqu,
> point them at the Events pipeline, and prep the 'Event recap' template. I'll
> paste scans each evening for you to process and attribute."

> "The conference is over — give me the event's results against goal and
> recommend who to follow up with first."

## Pipeline report → `lynqu-pipeline-report`

> "Weekly pipeline report for the Inbound environment: what moved, what's
> stalled 14+ days, how the Q2 campaign tracks to goal, and the top 5 things I
> should do Monday."

> "How are our cards performing this month, and is event-sourced pipeline
> converting better than inbound?"

## Card studio → `lynqu-card-studio`

> "Create a digital business card for me as 'Head of Partnerships at Acme' with
> my work email and LinkedIn, add 'Partnership programs' as a service, use a
> clean dark template with a purple palette, then show me this month's stats for
> my existing card."

> "Update my card's website link and swap the template to something more
> minimal."

## Deal desk → `lynqu-deal-desk`

> "Acme wants 25 Business seats plus the onboarding package, 10% off
> onboarding. Put that on their deal and tell me the new total."

> "What's actually in the Northwind quote — line by line — and what's it worth?"

> "Draft a quote on the Contoso deal, valid 30 days, with our standard terms.
> I'll send it myself."

> "Add 'Premium Support' to the price book at €99/month, then show me
> everything we sell in euros."

Note the assistant will draft a quote but never send, accept or decline one —
those stay with you, and it will hand off rather than pretend otherwise.

## Chaining skills

> "Research 10 fintech targets in London, create leads for the good ones, set
> them up in the Outbound pipeline, then draft intro emails for me to approve."

This naturally walks `lynqu-lead-research` → `lynqu-lead-management` →
`lynqu-sales-followup`.

> "Pull everything we captured at the summit, qualify the ones with 5+ seats,
> price the two that asked for a proposal, and draft their quotes."

`lynqu-event-blitz` → `lynqu-lead-management` → `lynqu-deal-desk`.
