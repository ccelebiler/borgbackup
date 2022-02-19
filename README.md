# README #

## What is this repository for? ##

This repository contains a dockerized [BorgBackup](https://borgbackup.readthedocs.io/en/stable/) package.

The package is meant to support the [WordPress package](https://github.com/ccelebiler/wordpress), though it should be generic enough for other use cases.

### Features

   * Configurable cron schedules
   * Optional compression (LZ4, zlib, LZMA, zstd)
   * Optional encryption (SHA-256, BLAKE2b)
   * Configurable archive retention
   * Configurable log level

### Archive names

The archive names have the following format:
```
<year>-<month>-<day>_<hour>-<minute>-<second>
```

## Get started

### Configure environment variables

Create a new `.env` file in the root folder with the following content:
```
BORG_PASSPHRASE=
```

<b>Note:</b> The variable is required only for encryption.

Restrict access to the file:
```
chmod 600 .env
```

### Customize configuration

The following environment variables are supported:
   * `CRON_SCHED_ARCHIVE` - list of JSON objects with the following properties:
      * `cron` - supports [Linux crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) syntax
      * `path` - path(s) to archive
      * `exclude` - optional, pattern(s) for excluding matching paths
   * `CRON_SCHED_PRUNE`
   * `BORG_COMPRESSION` - see the [official documentation](https://borgbackup.readthedocs.io/en/stable/quickstart.html#backup-compression)
   * `BORG_ENCRYPTION` - see the [official documentation](https://borgbackup.readthedocs.io/en/stable/quickstart.html#repository-encryption)
   * `BORG_KEEP_WITHIN` - keep all archives within this time interval, see the [official documentation](https://borgbackup.readthedocs.io/en/stable/usage/prune.html)
   * `BORG_KEEP_LAST` - number of archives to keep
   * `BORG_KEEP_MINUTELY` - number of minutely archives to keep
   * `BORG_KEEP_HOURLY` - number of hourly archives to keep
   * `BORG_KEEP_DAILY` - number of daily archives to keep
   * `BORG_KEEP_WEEKLY` - number of weekly archives to keep
   * `BORG_KEEP_MONTHLY` - number of monthly archives to keep
   * `BORG_KEEP_YEARLY` - number of yearly archives to keep
   * `BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK` - automatic answerer for unencrypted repository warning
   * `BORG_LOG_LEVEL` - supported values are DEBUG, INFO, WARNING, ERROR, CRITICAL

### Run package

Run the following command from the root folder:
```
docker-compose up -d
```

## Restore

To restore an existing archive, run the following commands:
```
docker exec -it borgbackup /bin/sh
borg extract ::<archive>
```

See the [official documentation](https://borgbackup.readthedocs.io/en/stable/quickstart.html#restoring-a-backup) for further details.
