#!/bin/bash

PACKAGE_NAME="automation_test_wt"
PY_VERSION="3.12"
SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
VENV_DIR_NAME=.env
EXPECTED_VENV_DIR=${EXPECTED_VENV_DIR:="$SCRIPT_DIR/$VENV_DIR_NAME"}
PYTHON_TEST_CASE_SCOPE="test\_\*.py"

# Set the test scope as provided by user input, otherwise test for all test cases
if [ -n "$1" ]; then
    SANITIZED_TEST_FILE_NAME=$(echo "$1" | sed 's:[&/\]$::' | sed 's/[&/\]/\\&/g')
    if [[ $SANITIZED_TEST_FILE_NAME == *".py"* ]]; then
        if ! [ -f "$1" ]; then
            echo "Invalid file path: $1"
            exit 1
        else
            # Set specified .py file as main python_files to test
            sed -i '' "s/python_files = .*/python_files = \"$SANITIZED_TEST_FILE_NAME\"/" pyproject.toml
        fi
    else
        # Set specified test suite folder as main python_files to test
        sed -i '' "s/python_files = .*/python_files = \"$SANITIZED_TEST_FILE_NAME\/$PYTHON_TEST_CASE_SCOPE\"/" pyproject.toml
    fi
else
    sed -i '' "s/python_files = .*/python_files = \"test_*.py\"/" pyproject.toml
fi



if [ -n "$VIRTUAL_ENV" ] && [ "$VIRTUAL_ENV" != "$EXPECTED_VENV_DIR" ]
then
    >&2 echo -e "WARNING: The \"$EXPECTED_VENV_DIR\" virtual environment will \
be used instead of \"$VIRTUAL_ENV\" which is currently active. If you want to \
use a different environment, modify the EXPECTED_VENV_DIR variable in this \
script, or pass it as the environment variable:\n\n\
  EXPECTED_VENV_DIR=$VIRTUAL_ENV ./run.sh\n"
fi

# Remove all previous test case results to avoid conflicting results from previous and new test case run
rm -rf allure-results/

if [ ! -d $EXPECTED_VENV_DIR ]
then
    echo "Creating a virtual environment..."

    for x in "python$PY_VERSION" python3 python
    do
        if command -v $x &> /dev/null && $x --version &> /dev/null
        then
            PY_CMD=$x
            break
        fi
    done

    if [ -e "$PY_CMD" ]
    then
        >&2 echo "ERROR: failed to find Python. Please, make sure Python \
$PY_VERSION or greater is available and try again"
        exit 1
    fi

    REQUESTED_MINOR_VERSION=`echo $PY_VERSION | cut -d "." -f 2`
    INSTALLED_MINOR_VERSION=`$PY_CMD --version | cut -d "." -f 2`

    if [ $INSTALLED_MINOR_VERSION -lt $REQUESTED_MINOR_VERSION ]
    then
        >&2 echo "WARNING: the project was generated for Python $PY_VERSION, \
but this version can't be found. The version 3.$INSTALLED_MINOR_VERSION will \
be used instead, but you need to update the 'requires-python' property in \
pyproject.toml in order to run the project. If a compatibility issue occurs, \
install a newer version, or set it as the one behind python3/python commands. \
Then, delete the $VENV_DIR_NAME folder and run the script again"
    fi

    $PY_CMD -m venv "$EXPECTED_VENV_DIR" || exit 1
    NEW_VENV="true"
fi

if [ "$VIRTUAL_ENV" != "$EXPECTED_VENV_DIR" ]
then
    . "$EXPECTED_VENV_DIR/bin/activate" || exit 1
fi

if [ -n "$NEW_VENV" ]
then
    python -m pip --require-virtualenv install --upgrade pip setuptools wheel || exit 1
fi

if ! pip show "$PACKAGE_NAME" &> /dev/null
then
    pip --require-virtualenv install --requirement "$SCRIPT_DIR/requirements.txt" || exit 1
    pip --require-virtualenv install --no-deps --editable "$SCRIPT_DIR[dev]" || exit 1
fi

pytest --alluredir "$SCRIPT_DIR/allure-results" $@
