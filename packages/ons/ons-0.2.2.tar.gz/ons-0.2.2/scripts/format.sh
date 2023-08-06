#!/bin/bash
SOURCES="ons tests"

echo "Running isort..."
isort $SOURCES
echo "-----"

echo "Running black..."
black --skip-string-normalization $SOURCES
