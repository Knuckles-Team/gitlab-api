# GitLab API

![PyPI - Version](https://img.shields.io/pypi/v/gitlab-api)
![PyPI - Downloads](https://img.shields.io/pypi/dd/gitlab-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/gitlab-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/gitlab-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/gitlab-api)
![PyPI - License](https://img.shields.io/pypi/l/gitlab-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/gitlab-api)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/gitlab-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/gitlab-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/gitlab-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/gitlab-api)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/gitlab-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/gitlab-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/gitlab-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/gitlab-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/gitlab-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/gitlab-api)

*Version: 0.15.0*

GitLab API Python Wrapper

Includes a large portion of useful API calls to GitLab

This repository is actively maintained - Contributions are welcome!

AI Skill Ready (**PEP8** Documented) - Assimilate the following package into your agent and begin using it! 


### API Calls:
- Branches
- Commits
- Deploy Tokens
- Groups
- Jobs
- Members
- Merge Request
- Merge Request Rules
- Packages
- Pipeline
- Projects
- Protected Branches
- Releases
- Runners
- Users
- Wiki

<details>
  <summary><b>Usage:</b></summary>

```python
#!/usr/bin/python
# coding: utf-8
import gitlab_api

token = "<GITLAB_TOKEN/PERSONAL_TOKEN>"
gitlab_url = "<GITLAB_URL>"
client = gitlab_api.Api(url=gitlab_url, token=token)

users = client.get_users()
print(users)

created_merge_request = client.create_merge_request(project_id=123, source_branch="development", 
                                                    target_branch="production",title="Merge Request Title")
print(created_merge_request)

print(f"Users: {client.get_users()}")

print(f"Projects: {client.get_projects()}")

response = client.get_runners(runner_type='instance_type', all_runners=True)
print(f"Runners: {response}")
```

</details>

<details>
  <summary><b>Installation Instructions:</b></summary>

Install Python Package

```bash
python -m pip install gitlab-api
```

</details>

<details>
  <summary><b>Repository Owners:</b></summary>


<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)
</details>
