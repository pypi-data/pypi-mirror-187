FROM ubuntu:22.04 as compress

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt clean \
    && apt-get update -y

RUN apt-get install --no-install-recommends -y brotli gzip

WORKDIR /etc/caddy

COPY ./docker/caddy/compress.sh /etc/caddy/compress.sh

COPY ./docker/caddy/static /etc/caddy/static

RUN chmod +x ./compress.sh

RUN ./compress.sh

FROM caddy:2.6.2-alpine as caddy

WORKDIR /etc/caddy

COPY ./docker/caddy/Caddyfile /etc/caddy/

COPY --from=compress /etc/caddy/static /etc/caddy/static

HEALTHCHECK --interval=30s --timeout=30s --retries=3 --start-period=20s CMD wget -O /dev/null http://localhost:2019/metrics || exit 1

ENTRYPOINT ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
