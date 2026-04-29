import re

path = (
    "/home/apps/workspace/agent-packages/agents/gitlab-api/tests/test_gitlab_models.py"
)
with open(path) as f:
    content = f.read()

# Pattern 1: response.data[0]
pattern1 = r'(response = Response\(data=example_data,.*?\))\n\s+assert response\.data\[0\]\.base_type == "(\w+)"'


def replace1(match):
    return f'response = Response[{match.group(2)}](data=example_data, status_code=200, json_output=example_data)\n    assert response.data[0].base_type == "{match.group(2)}"'


# Pattern 2: response.data (single object)
pattern2 = r'(response = Response\(data=example_data,.*?\))\n\s+assert response\.data\.base_type == "(\w+)"'


def replace2(match):
    return f'response = Response[{match.group(2)}](data=example_data, status_code=200, json_output=example_data)\n    assert response.data.base_type == "{match.group(2)}"'


# Reset Response[...] back to Response(...) before re-applying to fix my previous mistakes
content = re.sub(r"Response\[\w+\]\(", "Response(", content)

new_content = re.sub(pattern1, replace1, content, flags=re.DOTALL)
new_content = re.sub(pattern2, replace2, new_content, flags=re.DOTALL)

# Find all models used in asserts
models = set(
    re.findall(r'assert response\.data(?:\[0\])?\.base_type == "(\w+)"', new_content)
)
models.add("Response")
sorted_models = sorted(list(models))
print(f"Found models: {sorted_models}")

# Update imports
import_block = "    from gitlab_api.gitlab_response_models import (\n"
for m in sorted_models:
    import_block += f"        {m},\n"
import_block += "    )"

import_pattern = r"    from gitlab_api\.gitlab_response_models import \(.*?\)"
new_content = re.sub(import_pattern, import_block, new_content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(new_content)
