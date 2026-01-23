#!/usr/bin/env python3
import re
from pathlib import Path

def check_mock_usage():
    """Check if Infrastructure tests are using proper mocking"""
    tests = Path('backend/tests/agent/infrastructure').rglob('test_*.py')
    violations = []

    print("🔍 Checking test mock usage...")

    for test in tests:
        content = test.read_text()

        # Check for test functions
        test_functions = re.findall(r'def test_\w+', content)
        if not test_functions:
            continue

        # Check if test has patch or fixture decorators
        has_mock = bool(re.search(r'@patch\(|@pytest\.fixture|unittest\.mock', content) or
                      re.search(r'with patch\(', content))

        # Look for direct external service calls (anti-pattern)
        direct_calls = bool(re.search(r'litellm\.completion\(|arxiv\.Search\(|requests\.(get|post)|httpx\.(get|post)', content) or
                        re.search(r'\.search\(|get_unpaywall_tool\(|zotero\.', content))

        if test_functions and not has_mock and direct_calls:
            violations.append(str(test))

    if violations:
        print('⚠️  以下测试可能缺少Mock:')
        for v in violations:
            print(f'  - {v}')
        return False
    else:
        print('✅ 所有Infrastructure测试都使用了Mock')
        return True

def check_factory_patterns():
    """Check Factory pattern usage"""
    infra_files = Path('backend/src/agent/infrastructure').rglob('*.py')

    print("🔍 Checking Factory pattern usage...")

    factory_functions = []
    for file in infra_files:
        content = file.read_text()
        matches = re.findall(r'def get_\w+\(\)\s*->', content)
        if matches:
            factory_functions.extend([f"{file}:{match}" for match in matches])

    if factory_functions:
        print('✅ Factory Pattern 实现情况:')
        for f in factory_functions:
            print(f'  - {f}')
        return True
    else:
        print('⚠️  未检测到Factory Pattern实现')
        return False

if __name__ == "__main__":
    import sys
    mock_ok = check_mock_usage()
    factory_ok = check_factory_patterns()

    success = mock_ok and factory_ok
    sys.exit(0 if success else 1)