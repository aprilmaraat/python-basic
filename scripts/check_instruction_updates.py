import hashlib
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_FILES = [
    REPO_ROOT / '.github' / 'application-setup.yml',
    REPO_ROOT / '.cursor' / 'rules' / 'application-setup.mdc',
]
CODE_DIRS = ['app', 'main.py']

GUARD_BEGIN = 'INSTRUCTION-GUARD-BEGIN'
GUARD_END = 'INSTRUCTION-GUARD-END'


def extract_guard_content(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    if GUARD_BEGIN not in text or GUARD_END not in text:
        return ''
    start = text.index(GUARD_BEGIN)
    end = text.index(GUARD_END)
    return text[start:end]


def hash_guard_blocks() -> str:
    h = hashlib.sha256()
    for f in INSTRUCTION_FILES:
        if f.exists():
            h.update(extract_guard_content(f).encode('utf-8'))
    return h.hexdigest()


def detect_code_changes() -> bool:
    # Simple heuristic: if any tracked files under app/ or main.py changed compared to HEAD.
    # For CI usage where git is available.
    import subprocess
    try:
        result = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print('Warning: git diff failed, assuming no changes.', e)
        return False
    changed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    for c in changed:
        if c.startswith('app/') or c == 'main.py':
            return True
    return False


def instructions_modified(changed_files: list[str]) -> bool:
    # Normalize changed file paths to posix-style relative
    normalized = {p.replace('\\', '/') for p in changed_files}
    for f in INSTRUCTION_FILES:
        rel = f.relative_to(REPO_ROOT).as_posix()
        if rel in normalized:
            return True
    return False


def main():
    import subprocess
    # Collect staged changes for pre-commit; fallback to diff HEAD for CI.
    try:
        staged = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, check=True)
        changed_files = [line.strip() for line in staged.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        changed_files = []

    code_changed = any(f.startswith('app/') or f == 'main.py' for f in changed_files) or detect_code_changes()

    if not code_changed:
        print('Instruction Guard: No relevant code changes detected.')
        sys.exit(0)

    if instructions_modified(changed_files):
        print('Instruction Guard: Instruction files updated alongside code changes. OK.')
        sys.exit(0)

    print('\nERROR: Code changes detected under app/ or main.py without updating instruction files:')
    for f in changed_files:
        print(f' - {f}')
    print('\nPlease edit .github/application-setup.yml and/or .cursor/rules/application-setup.mdc to reflect changes (increment guard_version if substantive).')
    sys.exit(1)


if __name__ == '__main__':
    main()
