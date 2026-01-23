#!/usr/bin/env python3
import ast
import sys
from pathlib import Path

def check_domain_purity():
    violations = []
    domain_files = Path('backend/src/agent/domain').rglob('*.py')
    forbidden = ['requests', 'httpx', 'sqlalchemy', 'psycopg2']

    print("🔍 Checking domain layer purity...")

    for file in domain_files:
        try:
            tree = ast.parse(file.read_text())
        except Exception as e:
            print(f"⚠️  Could not parse {file}: {e}")
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(f in alias.name for f in forbidden):
                        violations.append(f'{file}: {alias.name}')
            elif isinstance(node, ast.ImportFrom):
                if node.module and any(f in node.module for f in forbidden):
                    violations.append(f'{file}: {node.module}')

    if violations:
        print('❌ Domain层违规依赖:')
        for v in violations:
            print(f'  - {v}')
        return False
    else:
        print('✅ Domain层纯净性检查通过')
        return True

if __name__ == "__main__":
    success = check_domain_purity()
    sys.exit(0 if success else 1)