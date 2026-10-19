#!/usr/bin/env bash
TARGET=${1:-"my_custom_skill"}
python3 validator/skills_ref_validate.py "$TARGET"
