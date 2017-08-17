#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

celery -A djangoprogramy.taskapp worker -l INFO
