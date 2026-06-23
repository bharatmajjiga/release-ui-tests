#!/bin/bash
# Test Monaco editor fix for OCP 4.18

echo "🧪 Testing Monaco Editor Fix for OCP 4.18"
echo "========================================="
echo ""

# Run the pipeline creation test
echo "Running pipeline creation test..."
python -m pytest tests/steps/test_pipeline_crud_steps.py -v -k "create_pipeline" --tb=short --headed -x

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ Monaco editor test PASSED!"
else
    echo ""
    echo "❌ Monaco editor test FAILED with exit code: $exit_code"
fi

exit $exit_code
