#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf '用法: %s <目录路径>\n' "${0##*/}" >&2
  printf '示例: %s CloudNativePGDeployement\n' "${0##*/}" >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

directory=${1%/}
if [[ -z "$directory" ]]; then
  directory=/
fi

if [[ ! -d "$directory" ]]; then
  printf '错误: 目录不存在: %s\n' "$1" >&2
  exit 1
fi

directory=$(cd -- "$directory" && pwd -P)
directory_name=${directory##*/}
if [[ -z "$directory_name" ]]; then
  directory_name=root
fi

archive="${directory_name}.tar"
temporary_archive=$(mktemp "${TMPDIR:-/tmp}/${directory_name}.tar.XXXXXX")
trap 'rm -f -- "$temporary_archive"' EXIT

tar -cf "$temporary_archive" -C "$directory" .

mv -f -- "$temporary_archive" "$archive"
printf '已创建: %s\n' "$archive"
