#!/bin/bash
if [ -d "dist" ]; then
    rm -r dist/
fi && \
./venv/bin/python -m build
