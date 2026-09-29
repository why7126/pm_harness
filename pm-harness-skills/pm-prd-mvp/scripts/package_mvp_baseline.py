#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, zipfile

def main():
    if len(sys.argv) not in (2,3):
        raise SystemExit("用法: package_mvp_baseline.py <基线目录> [输出ZIP]")
    root = Path(sys.argv[1]).resolve()
    validator = Path(__file__).with_name("validate_mvp_baseline.py")
    subprocess.run([sys.executable, str(validator), str(root)], check=True)
    out = Path(sys.argv[2]).resolve() if len(sys.argv)==3 else root.with_suffix(".zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file(): z.write(p, Path(root.name) / p.relative_to(root))
    print(f"已生成: {out}")
if __name__ == "__main__": main()
