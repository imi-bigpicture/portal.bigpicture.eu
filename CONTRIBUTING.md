# Contributing

Thanks for improving the BigPicture Sweden website. This file covers the
conventions used when writing pages for the **submission manual** under
`datasets/submission/`. For how to build and preview the site, see
[README.md](README.md).

## Submission manual page conventions

Every page in the manual is **fill-in-the-blanks**. Two conventions make that
possible — the **OS tabset** and the **verify step**.

### 1. The OS tabset

Where a command or instruction differs by operating system, wrap it in a
`panel-tabset` with **Windows / macOS / Linux** tabs, **in that order**. The
reader picks their tab once and ignores the rest.

````markdown
::: {.panel-tabset}
## Windows
Open **PowerShell** and run:
```powershell
winget install --id Git.Git -e
```
## macOS
In **Terminal**, run:
```bash
brew install git
```
## Linux
```bash
sudo apt-get install -y git
```
:::
````

**Rules**

- Always include all three tabs, in the order Windows, macOS, Linux — even if a
  command is identical, so the reader's chosen tab is always present.
- Keep commands copy-pasteable: one tool per code block, no shell prompts
  (`$`, `>`) inside the block.
- **Linux is the reference path.** Write and validate the Linux tab first; the
  others mirror its shape.

### 2. The verify step

After an install or a state-changing command, give the reader a way to confirm
it worked before moving on. Use a **`callout-tip` titled "Verify"** with the
*paste-this / expect-this* pattern.

````markdown
::: {.callout-tip}
## Verify

Paste this:

```bash
git --version
```

Expected output (your version may differ):

```
git version 2.40.0
```
:::
````

**Rules**

- Show the **exact command** to paste and a representative **expected output**.
- If the output varies (versions, paths, dates), say so — "your version may
  differ" — so the reader knows what to ignore.
- One verify step per meaningful action; don't make the reader run five things
  before they can check anything.

### 3. Page skeleton

Start every operator page from this shape:

```markdown
---
title: <Short imperative title>
---

One or two sentences: what this step accomplishes and why.

## Do it

<OS tabset with the commands>

::: {.callout-tip}
## Verify
<paste-this / expect-this>
:::

## If something goes wrong

<the one or two most common failures and their fixes>
```

The **« Prev / Next »** navigation is automatic — it comes from the sidebar order
in `_quarto.yml`, so you never hand-write next-step links.

## Contact addresses

Email addresses are defined once in `_variables.yml` and referenced as Quarto
variables, never typed inline. Two exist, and they mean different things:

| Variable | Address | Use it for |
|---|---|---|
| `email.bpops` | `bp-ops@nbis.se` | Server, inbox, and data-archive operations (the WP2 team) |
| `email.helpdesk` | `servicedesk@bigpicture.eu` | General and technical support, and access requests |

Write them as `[bp-ops](mailto:{{< var email.bpops >}})`, and make the link text
match the variable's meaning — a link labelled "helpdesk" pointing at
`email.bpops` is how these get mixed up. Do **not** put personal or institutional
individual addresses on a rendered page.

## Testing the pipeline itself

Testing the `bp-submission-pipeline` software (its `make test-unit` and
`make smoke` targets) is documented with that software, in the
[imi-bigpicture/bp-submission-pipeline](https://github.com/imi-bigpicture/bp-submission-pipeline)
repository — not here.
