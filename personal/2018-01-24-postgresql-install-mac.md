---
author: Alex Strick van Linschoten
categories:
  - coding
  - useful-tools
  - python
  - sql
  - database
date: "2018-01-24"
description: "A straightforward guide to installing PostgreSQL on Mac using Postgres.app and setting up psycopg2 for Python integration."
layout: post
title: "Installing PostgreSQL on a Mac"
toc: true
aliases:
  - "/blog/postgresql-install-mac.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

PostgreSQL is a SQL-type database system. It has been around for a while, and is in the middle of [a sort of revival](https://www.infoworld.com/article/3240064/sql/why-old-school-postgresql-is-so-hip-again.html). Installing Postgres on your own system can be a little difficult. Last time I tried, I was helped through the process while doing the Udacity Intro to Programming Nanodegree.

Recently I had to reinstall Postgres, and there were some useful improvements to the process when guided through it in my [Dataquest](https://www.dataquest.io/m/129/project%3A-postgresql-installation/2/installing-postgre-sql) lessons.

[Postgres.app](http://postgresapp.com/) is an application you can install on your Mac which simplifies a lot of the legwork, particularly when setting up new databases, servers and so on.

When you want to install a commonly used Python library for interfacing with Postgres, `psycopg2` is a good option. You can do this easily with Anaconda:

```
conda install psycopg2
```
