echo "Running test suite with coverage..."

# Run tests with coverage; adjust "--source=src" if your source folder is different.
coverage run --source=src -m pytest
TEST_STATUS=$?

if [ $TEST_STATUS -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit $TEST_STATUS
fi

echo "Checking coverage threshold (70%)..."

# This command will exit with a non-zero status if coverage is below 70%
coverage report --fail-under=70
COVERAGE_STATUS=$?

if [ $COVERAGE_STATUS -ne 0 ]; then
    echo "❌ Test coverage is below 70%. Commit aborted."
    exit $COVERAGE_STATUS
fi

echo "✅ All tests pass and coverage is at or above 70%. Commit allowed."
exit 0