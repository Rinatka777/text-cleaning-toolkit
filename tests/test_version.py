from app import VERSION

def test_version_semver_like() -> None:
  parts = VERSION.split(".")
  assert len(parts) == 3
  assert all(p.isdigit() for p in parts)