#!/bin/bash

# This script automates the creation of a new module following the DTDD workflow.

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <backend|frontend> <ModuleName>"
  exit 1
fi

TARGET_DIR=$1
MODULE_NAME=$2

if [ "$TARGET_DIR" == "frontend" ]; then
  # Frontend scaffolding (TypeScript/React)
  BASE_PATH="frontend/src/components/${MODULE_NAME}"
  mkdir -p $BASE_PATH
  touch "${BASE_PATH}/I${MODULE_NAME}.ts"
  touch "${BASE_PATH}/${MODULE_NAME}.tsx"
  touch "${BASE_PATH}/${MODULE_NAME}.spec.ts"
  echo "Frontend module '${MODULE_NAME}' created in '${BASE_PATH}'"

elif [ "$TARGET_DIR" == "backend" ]; then
  # Backend scaffolding (Python)
  BASE_PATH="backend/src/agent/${MODULE_NAME}"
  mkdir -p $BASE_PATH
  touch "${BASE_PATH}/__init__.py"
  touch "${BASE_PATH}/${MODULE_NAME}_protocol.py"
  touch "${BASE_PATH}/${MODULE_NAME}_service.py"
  touch "${BASE_PATH}/test_${MODULE_NAME}.py"
  echo "Backend module '${MODULE_NAME}' created in '${BASE_PATH}'"

else
  echo "Invalid target specified. Use 'frontend' or 'backend'."
  exit 1
fi

echo "Module structure for '${MODULE_NAME}' created successfully."
