#/usr/bin/env bash
source /run/agenix/discord
cd /home/stefan/kirkbot/
/run/current-system/sw/bin/poetry install
/run/current-system/sw/bin/poetry run python kirkbot/cli.py
