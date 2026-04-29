import re

path = (
    "/home/apps/workspace/agent-packages/agents/gitlab-api/tests/test_gitlab_models.py"
)
with open(path) as f:
    lines = f.readlines()

new_lines = []
models_used = set()
i = 0
while i < len(lines):
    line = lines[i]
    if "response = Response(" in line:
        # Find end of call
        end_idx = i
        while ")" not in lines[end_idx] and end_idx < len(lines) - 1:
            end_idx += 1

        # Look for model name
        model_name = None
        for j in range(end_idx + 1, min(end_idx + 10, len(lines))):
            next_line = lines[j].strip()
            if not next_line:
                continue
            match = re.search(
                r'assert response\.data(?:\[0\])?\.base_type == "(\w+)"', next_line
            )
            if match:
                model_name = match.group(1)
                break

        if model_name:
            new_lines.append(line.replace("Response(", f"Response[{model_name}]("))
            models_used.add(model_name)
            for k in range(i + 1, end_idx + 1):
                new_lines.append(lines[k])
            i = end_idx + 1
            continue

    new_lines.append(line)
    i += 1

# Update imports
import_block_start = -1
import_block_end = -1
for i, line in enumerate(new_lines):
    if "from gitlab_api.gitlab_response_models import (" in line:
        import_block_start = i
    if import_block_start != -1 and ")" in line:
        import_block_end = i
        break

if import_block_start != -1 and import_block_end != -1:
    models_used.add("Response")
    sorted_models = sorted(list(models_used))
    new_import_lines = ["    from gitlab_api.gitlab_response_models import (\n"]
    for m in sorted_models:
        new_import_lines.append(f"        {m},\n")
    new_import_lines.append("    )\n")
    new_lines[import_block_start : import_block_end + 1] = new_import_lines

with open(path, "w") as f:
    f.writelines(new_lines)

print(f"Fixed {len(models_used)} models: {sorted_models}")
