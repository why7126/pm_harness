from pathlib import Path

required = [
    "MINIO_BUCKET",
    "MINIO_PREFIX_ORIGINAL",
    "MINIO_PREFIX_THUMBNAILS",
    "MINIO_PREFIX_VIDEO",
    "HOST_PORT_BACKEND",
    "HOST_PORT_WEB",
]

content = Path(".env.example").read_text(encoding="utf-8")
missing = [key for key in required if key not in content]

if missing:
    raise SystemExit(f"Missing env keys in .env.example: {', '.join(missing)}")

print(".env.example check passed")
