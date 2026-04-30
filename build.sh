#!/usr/bin/env bash
# Render build script for native Python runtime
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
