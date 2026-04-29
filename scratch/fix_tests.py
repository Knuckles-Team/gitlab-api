import re

path = (
    "/home/apps/workspace/agent-packages/agents/gitlab-api/tests/test_gitlab_models.py"
)
with open(path) as f:
    content = f.read()

# Find all test functions and their expected base_type
# Pattern: response = Response(data=example_data, ...)\n    assert response.data[0].base_type == "ModelName"
# We want to change Response(...) to Response[ModelName](...)


def replace_response(match):
    full_match = match.group(0)
    model_name = match.group(2)
    # Replace Response( with Response[ModelName](
    new_match = full_match.replace("Response(", f"Response[{model_name}](")
    return new_match


# Regex to match the pattern
pattern = r'(response = Response\(data=example_data,.*?\))\n\s+assert response\.data\[0\]\.base_type == "(\w+)"'
new_content = re.sub(pattern, replace_response, content, flags=re.DOTALL)

# Also ensure all models are imported
models = set(re.findall(r'assert response\.data\[0\]\.base_type == "(\w+)"', content))
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
