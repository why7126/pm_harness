#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import zipfile

def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("用法: package_solution_baseline.py <方案基线目录> [输出ZIP]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    validator = Path(__file__).with_name("validate_solution_baseline.py")
    result = subprocess.run([sys.executable, str(validator), str(root)])
    if result.returncode:
        return result.returncode
    output = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else root.with_suffix(".zip")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                archive.write(path, Path(root.name) / path.relative_to(root))
    print(f"已生成: {output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
