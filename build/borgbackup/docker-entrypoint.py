import json
import os
import subprocess


class Entrypoint():
    """
    Provides functions for configuring the docker container.
    """

    def __init__(self):
        self.__crontab_file = "/etc/crontabs/borg"
        self.__cmd_output = ">/proc/1/fd/1 2>/proc/1/fd/2"
        self.__archive_format = "%Y-%m-%d_%H-%M-%S"

    def init_repo(self):
        """
        Initializes the repository.
        """
        proc = subprocess.run(["borg", "init", f"""--encryption={os.getenv("BORG_ENCRYPTION", "none")}"""], capture_output=True)
        if proc.returncode == 0:
            print(f"""Initialized new repository at {os.getenv("BORG_REPO")}.""")
        else:
            print(proc.stderr.decode("utf-8"))

        # Ignore the error generated when the repository already exists.
        return proc.returncode in [0, 2]

    def config_cron(self):
        """
        Configures the cron scheduler.
        """
        # Determine the log and compression options.
        log_level = f"""--{os.getenv("BORG_LOG_LEVEL", "INFO").lower()}"""
        compression = f"""--compression={os.getenv("BORG_COMPRESSION", "none")}"""

        # Create a new file for crontab.
        with open(self.__crontab_file, "w") as f:
            for item in json.loads(os.getenv("CRON_SCHED_ARCHIVE")):
                # Determine the exclusion options.
                if "exclude" not in item or not len(item["exclude"]):
                    exclude = ""
                else:
                    if not isinstance(item["exclude"], list):
                        item["exclude"] = [item["exclude"]]
                    exclude = " ".join(f"--exclude={x}" for x in item["exclude"])
                # Determine the paths to be archived.
                if not isinstance(item["path"], list):
                    item["path"] = [item["path"]]
                path = " ".join(x for x in item["path"])
                # Build the 'create' command and write it to the file.
                cmd = f"borg create --stats --show-rc {log_level} {compression} {exclude} ::`date +{self.__archive_format}` {path}"
                f.write(f"""{item["cron"]} {cmd}{self.__cmd_output}\n""")
            # Build the 'prune' command and write it to the file.
            cron = os.getenv("CRON_SCHED_PRUNE")
            if cron:
                cmd = f"borg prune --stats --show-rc {log_level}"
                for suffix in ["WITHIN", "LAST", "MINUTELY", "HOURLY", "DAILY", "MONTHLY", "YEARLY"]:
                    value = os.getenv(f"BORG_KEEP_{suffix}")
                    if value:
                        cmd += f" --keep-{suffix.lower()}={value}"
                f.write(f"{cron} {cmd}{self.__cmd_output}\n")

        # Replace crontab by the new file.
        subprocess.run(["crontab", self.__crontab_file])
        print("Configured cron schedule.")


if __name__ == "__main__":
    o = Entrypoint()
    if o.init_repo():
        o.config_cron()

    # Keep the cron scheduler in the foreground, so that the Docker image continues running.
    subprocess.run(["crond", "-f"])
