#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail


# Precompress static files with brotli and gzip.
# The list of ignored file types was taken from https://github.com/evansd/whitenoise
find /etc/caddy/static -type f \
  ! -regex '^.+\.\(jpg\|jpeg\|png\|gif\|webp\|zip\|gz\|tgz\|bz2\|tbz\|xz\|br\|swf\|flv\|woff\|woff2\|3gp\|3gpp\|asf\|avi\|m4v\|mov\|mp4\|mpeg\|mpg\|webm\|wmv\)$' \
  -exec brotli --force --best {} \+ \
  -exec gzip --force --keep --best {} \+
