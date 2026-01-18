---
author: Alex Strick van Linschoten
categories:
  - git
  - softwareengineering
  - versioncontrol
date: "2023-04-28"
description: "Instructions how to remove a commit from your git logs."
layout: post
title: How to remove a commit (or two) from your git branch
toc: false
image: images/tree-picking.png
include-before-body:
  '<script defer data-domain="mlops.systems"
  src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
aliases:
  - "/posts/2023-04-28-removing-git-commits.html"
---

I ran into a problem where a tool I was using auto-updated my git branch,
forcing dozens of changes. The changes were relatively innocuous, but they were
irrelevant to the work I was doing which would make reviewing the Pull Request
pretty hard going.

This is what I did to remove the traces of that commit from my git branch logs:

First, make sure you are on the branch where the commit you want to remove
exists. If not, switch to that branch using:

```shell
git checkout <branch_name>
```

Use `git log` to find the commit hash (the unique identifier) of the commit you
want to remove. The commit hash will be a long string of characters and numbers,
e.g., `ab12cd34ef56gh78ij90kl12mn34op56qr78st90`.

Use `git rebase -i` (interactive rebase) to remove the commit. This command will
open an editor where you can manipulate the commit history. Use the commit hash
that's one before the one you want to remove:

```shell
git rebase -i <parent_commit_hash>
```

In the editor that opens, you will see a list of commits starting from the
parent commit hash you provided. Find the line with the commit you want to
remove. Change the word pick at the beginning of that line to drop or simply
delete the entire line. Save and close the editor. (Alternatively, if you're
using VS Code, a sort of UI interface will open which will allow you to select
from drop-down pickers which options you want for each of the downstream
commits. There is a button at the bottom to switch to the pure text interface if
you prefer.)

Git will perform the rebase, removing the specified commit from the commit tree.

If you're satisfied with the changes, push your branch to the remote repository:

```shell
git push -f origin <branch_name>
```

**Important Note:** Using `git push -f` (force push) can be dangerous, as it
overwrites the remote branch with your local one. Make sure you are confident
about your changes before using this command. If you're working on a shared
branch with others it's important to communicate with your team to ensure that
no one else is working on the same branch to avoid losing any work.

The commits I'd made after the one I wanted to remove didn't overlap or relate
to each other, so I didn't face any conflicts during the rebase process.
However, if you do encounter conflicts, you'll need to resolve them manually and
continue with the rebase using `git rebase --continue`.

Remember that rebasing and force pushing can rewrite the commit history, so
always be cautious when performing these operations.
