---
name: postgres
description: Start, stop, or restart the Postgres + pgAdmin pod for the my-fapi project via Podman. Use this skill whenever the user says "start postgres", "stop postgres", "restart postgres", "start the db pod", "bring up the database", "start pgadmin", "spin up postgres", "kill the postgres pod", or any variation of wanting to run or manage the local Postgres/pgAdmin pod. Always reports the connection URL and credentials for both Postgres and pgAdmin after a start or restart.
argument-hint: [start|stop|restart]
allowed-tools: [Bash, Read]
version: 1.0.0
author: Nikhil Pagote
tags: [postgres, pgadmin, podman, pod, database, my-fapi]
---

# Postgres + pgAdmin Pod Management

Manage the Podman pod running Postgres and pgAdmin for the `my-fapi` project.

**Manifest:** `/home/nikhil/Documents/python/my-fapi/db-pod.yaml`
**Pod name:** `my-fapi-db`

## Arguments

`$ARGUMENTS` may contain an action: `start`, `stop`, or `restart`.
If no action is given, infer from the user's message (e.g. "bring up" → start, "kill" → stop).

---

## Start

Check whether the pod already exists:

```bash
podman pod exists my-fapi-db && echo EXISTS || echo MISSING
```

- If `MISSING`: create and start it from the manifest.
  ```bash
  cd /home/nikhil/Documents/python/my-fapi
  podman kube play db-pod.yaml
  ```
- If `EXISTS`: just start it (this preserves the Postgres data volume, no need to recreate).
  ```bash
  podman pod start my-fapi-db
  ```
- If it's already running, say so instead of restarting anything.

Then always run the **Report** step below.

---

## Stop

```bash
podman pod stop my-fapi-db
```

If no pod is found, say so — don't show it as an error.

---

## Restart

```bash
podman pod exists my-fapi-db && podman pod restart my-fapi-db || (cd /home/nikhil/Documents/python/my-fapi && podman kube play db-pod.yaml)
```

Then always run the **Report** step below.

---

## Report (after start or restart only)

The manifest is the single source of truth for credentials — always read it fresh rather than assuming the values below haven't changed:

```bash
cat /home/nikhil/Documents/python/my-fapi/db-pod.yaml
```

From it, extract for the `postgres` container: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and the postgres `hostPort`. Extract for the `pgadmin` container: `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD`, and the pgadmin `hostPort`.

Report in this exact format:

```
Postgres:  postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:<postgres hostPort>/<POSTGRES_DB>
pgAdmin:   http://localhost:<pgadmin hostPort>  (login: <PGADMIN_DEFAULT_EMAIL> / <PGADMIN_DEFAULT_PASSWORD>)
```

## Stop report

On stop, just confirm: `my-fapi-db pod stopped` (no credentials needed).
