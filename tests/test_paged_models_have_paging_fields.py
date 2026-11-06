"""Every input model fed to the paged fetch carries the paging fields it reads."""

import re
from pathlib import Path

from gitlab_api import gitlab_input_models as models

API_DIR = Path(__file__).parent.parent / "gitlab_api" / "api"
PAGED = re.compile(
    r"(\w+) = (\w+Model)\(\*\*kwargs\)\s*\n\s*try:\s*\n\s*response, data = "
    r"self\._fetch_all_pages\(\s*endpoint=[^\n]*\n\s*model=\1"
)


def test_paged_models_have_max_pages():
    missing = set()
    for path in API_DIR.glob("*.py"):
        for _var, name in PAGED.findall(path.read_text()):
            if "max_pages" not in getattr(models, name).model_fields:
                missing.add(name)
    assert not missing, sorted(missing)
