#!/bin/bash
set -e

echo "DEBUG: Environment = $(env)"
echo "$@"
exec "$@"
