FROM alpine:3.15

RUN apk add --no-cache \
		python3 \
		borgbackup=1.1.17-r2

COPY docker-entrypoint.py /root/

ENV BORG_REPO="/repo"
ENV BORG_CONFIG_DIR="/etc/borg"

VOLUME ["/repo"]

ENTRYPOINT ["python3", "-u", "/root/docker-entrypoint.py"]
