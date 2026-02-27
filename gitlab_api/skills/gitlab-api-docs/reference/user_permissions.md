[Skip to main content](https://docs.gitlab.com/user/permissions/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/user/permissions/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/user/permissions/)
    * [18.8](https://docs.gitlab.com/18.8/user/permissions/)
    * [18.7](https://archives.docs.gitlab.com/18.7/user/permissions/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/user/permissions/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/user/permissions.html)
  *     * [Archives](https://docs.gitlab.com/archives)


Select theme and layout
  * Light mode
  * Dark mode
  * Auto


  * Fixed width
  * Fluid width


[What's new?](https://about.gitlab.com/releases/whats-new/) [Get free trial](https://gitlab.com/-/trial_registrations/new?glm_source=docs.gitlab.com&amp;glm_content=navigation-cta-docs)
Toggle menu
  * [Use GitLab](https://docs.gitlab.com/user/)
  * [GitLab Duo](https://docs.gitlab.com/user/gitlab_duo/)
  * [Extend](https://docs.gitlab.com/api/)
  * [Install](https://docs.gitlab.com/install/)
  * [Administer](https://docs.gitlab.com/administration/)
  * [Subscribe](https://docs.gitlab.com/subscriptions/)
  * [Contribute](https://docs.gitlab.com/development/)
  * [Solutions](https://docs.gitlab.com/solutions/)


Select a topicUse GitLab GitLab Duo Extend Install Administer Subscribe Contribute Solutions
[Getting started](https://docs.gitlab.com/user/get_started/)
[Tutorials](https://docs.gitlab.com/tutorials/)
[Manage your organization](https://docs.gitlab.com/topics/set_up_organization/)
[Organize work with projects](https://docs.gitlab.com/user/project/organize_work_with_projects/)
[Plan and track work](https://docs.gitlab.com/topics/plan_and_track/)
[Manage authentication and authorization](https://docs.gitlab.com/auth/)
[User identity](https://docs.gitlab.com/administration/auth/)
[User authentication](https://docs.gitlab.com/auth/user_authentication/)
[User permissions](https://docs.gitlab.com/auth/user_permissions/)
[Auditor users](https://docs.gitlab.com/administration/auditor_users/)
[External users](https://docs.gitlab.com/administration/external_users/)
[Guest role](https://docs.gitlab.com/administration/guest_users/)
[Internal users](https://docs.gitlab.com/administration/internal_users/)
[Enterprise users](https://docs.gitlab.com/user/enterprise_user/)
[Participants](https://docs.gitlab.com/user/participants/)
[Service accounts](https://docs.gitlab.com/user/profile/service_accounts/)
[Roles and permissions](https://docs.gitlab.com/user/permissions/)
[Custom roles](https://docs.gitlab.com/user/custom_roles/)
[Custom permissions](https://docs.gitlab.com/user/custom_roles/abilities/)
[Auth best practices](https://docs.gitlab.com/auth/auth_practices/)
[Auth glossary](https://docs.gitlab.com/auth/auth_glossary/)
[Use Git](https://docs.gitlab.com/topics/git/)
[Manage your code](https://docs.gitlab.com/topics/manage_code/)
[Use CI/CD to build your application](https://docs.gitlab.com/topics/build_your_application/)
[Secure your application](https://docs.gitlab.com/user/application_security/secure_your_application/)
[Deploy and release your application](https://docs.gitlab.com/topics/release_your_application/)
[Manage your infrastructure](https://docs.gitlab.com/user/infrastructure/)
[Monitor your application](https://docs.gitlab.com/operations/)
[Analyze GitLab usage](https://docs.gitlab.com/user/analytics/)
[Feature support](https://docs.gitlab.com/policy/development_stages_support/)
[Find your GitLab version](https://docs.gitlab.com/user/version/)
/
  1. [GitLab Docs](https://docs.gitlab.com/)
  2. [Use GitLab](https://docs.gitlab.com/user/)
  3. [Manage authentication an…](https://docs.gitlab.com/auth/)
  4. [User permissions](https://docs.gitlab.com/auth/user_permissions/)
  5. [Roles and permissions](https://docs.gitlab.com/user/permissions/)


* * *
# Roles and permissions
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


Roles define a user’s permissions in a group or project.
Users with [administrator access](https://docs.gitlab.com/administration/) have all permissions and can perform any action.
## Roles[](https://docs.gitlab.com/user/permissions/#roles "Permalink")
History
  * Planner role [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/482733) in GitLab 17.7.


When you add a user to a group or project, you assign them a role. The role determines their permissions. Assign either a [default role](https://docs.gitlab.com/user/permissions/#default-roles) or a [custom role](https://docs.gitlab.com/user/custom_roles/).
A user can have different roles for each group and project. Users always retain the permissions for their highest role. For example, if a user has:
  * The Maintainer role for a parent group
  * The Developer role for a project in that group


The user inherits the permissions for their Maintainer role in the project.
To view assigned roles, go to the **Members** page for a [group](https://docs.gitlab.com/user/group/#view-group-members) or [project](https://docs.gitlab.com/user/project/members/#view-project-members).
### Default roles[](https://docs.gitlab.com/user/permissions/#default-roles "Permalink")
The following default roles are available:
Role | Description
---|---
Minimal Access | View limited group information without access to projects. For more information, see [Users with Minimal Access](https://docs.gitlab.com/user/permissions/#users-with-minimal-access).
Guest | View and comment on issues and epics. Cannot push code or access repository. This role applies to [private and internal projects](https://docs.gitlab.com/user/public_access/) only.
Planner | Create and manage issues, epics, milestones, and iterations. Focused on project planning and tracking with the ability to view and collaborate on code changes.
Reporter | View code, create issues, and generate reports. Cannot push code or manage protected branches.
Developer | Push code to non-protected branches, create merge requests, and run CI/CD pipelines. Cannot manage project settings.
Maintainer | Manage branches, merge requests, CI/CD settings, and project members. Cannot delete the project.
Owner | Full control over the project or group, including deletion and visibility settings.
By default, all users can create top-level groups and change their usernames. Users with [administrator access](https://docs.gitlab.com/administration/user_settings/) can change this behavior.
## Group permissions[](https://docs.gitlab.com/user/permissions/#group-permissions "Permalink")
Any user can remove themselves from a group, unless they are the only Owner of the group.
The following table lists group permissions available for each role:
### Groups[](https://docs.gitlab.com/user/permissions/#groups "Permalink")
Group permissions for [group features](https://docs.gitlab.com/user/group/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Browse group | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) projects in group | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View group [audit events](https://docs.gitlab.com/user/compliance/audit_events/) 1 |  |  |  | ✓ | ✓ | ✓
Create project in group 2 |  |  |  | ✓ | ✓ | ✓
Create subgroup 3 |  |  |  |  | ✓ | ✓
Change custom settings for [project integrations](https://docs.gitlab.com/user/project/integrations/) |  |  |  |  |  | ✓
Edit [epic](https://docs.gitlab.com/user/group/epics/) comments (posted by any user) |  |  |  |  | ✓ | ✓
Fork project into a group |  |  |  |  | ✓ | ✓
View [Billing](https://docs.gitlab.com/subscriptions/manage_subscription/#view-subscription) 4 |  |  |  |  |  | ✓
View group [Usage quotas](https://docs.gitlab.com/user/storage_usage_quotas/) page 4 |  |  |  |  |  | ✓
[Migrate group](https://docs.gitlab.com/user/group/import/) |  |  |  |  |  | ✓
Archive group |  |  |  |  |  | ✓
Delete group |  |  |  |  |  | ✓
Transfer group |  |  |  |  |  | ✓
Manage [subscriptions, storage, and compute minutes](https://docs.gitlab.com/subscriptions/manage_users_and_seats/#gitlabcom-billing-and-usage) |  |  |  |  |  | ✓
Manage [group access tokens](https://docs.gitlab.com/user/group/settings/group_access_tokens/) |  |  |  |  |  | ✓
Change group visibility level |  |  |  |  |  | ✓
Edit group settings |  |  |  |  |  | ✓
Configure project templates |  |  |  |  |  | ✓
Configure [SAML SSO](https://docs.gitlab.com/user/group/saml_sso/) 4 |  |  |  |  |  | ✓
Disable notification emails |  |  |  |  |  | ✓
Import [project](https://docs.gitlab.com/user/project/settings/import_export/) |  |  |  |  | ✓ | ✓
**Footnotes** :
  1. Developers and Maintainers can view events based on their individual actions only. For more information, see the [prerequisites](https://docs.gitlab.com/user/compliance/audit_events/#prerequisites).
  2. Developers, Maintainers and Owners: Only if the project creation role is set [for the instance](https://docs.gitlab.com/administration/settings/visibility_and_access_controls/#define-which-roles-can-create-projects) or [for the group](https://docs.gitlab.com/user/group/#specify-who-can-add-projects-to-a-group).
Developers: Developers can push commits to the default branch of a new project only if the [default branch protection](https://docs.gitlab.com/user/group/manage/#change-the-default-branch-protection-of-a-group) is set to “Partially protected” or “Not protected”.
  3. Maintainers: Only if users with the Maintainer role [can create subgroups](https://docs.gitlab.com/user/group/subgroups/#change-who-can-create-subgroups).
  4. Does not apply to subgroups.


### Group analytics[](https://docs.gitlab.com/user/permissions/#group-analytics "Permalink")
Group permission for [analytics](https://docs.gitlab.com/user/analytics/) features including value streams, product analytics, and insights:
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [GitLab Duo and SDLC trends](https://docs.gitlab.com/user/analytics/duo_and_sdlc_trends/) |  |  | ✓ | ✓ | ✓ | ✓
View [insights](https://docs.gitlab.com/user/project/insights/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [insights](https://docs.gitlab.com/user/project/insights/) charts | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [issue analytics](https://docs.gitlab.com/user/group/issues_analytics/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View contribution analytics | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View value stream analytics | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [productivity analytics](https://docs.gitlab.com/user/analytics/productivity_analytics/) |  |  | ✓ | ✓ | ✓ | ✓
View [group DevOps adoption](https://docs.gitlab.com/user/group/devops_adoption/) |  |  | ✓ | ✓ | ✓ | ✓
View metrics dashboard annotations |  |  | ✓ | ✓ | ✓ | ✓
Manage metrics dashboard annotations |  |  |  | ✓ | ✓ | ✓
### Group application security[](https://docs.gitlab.com/user/permissions/#group-application-security "Permalink")
Group permissions for [Application Security](https://docs.gitlab.com/user/application_security/secure_your_application/) features including dependency management, security analyzers, security policies, and vulnerability management.
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [dependency list](https://docs.gitlab.com/user/application_security/dependency_list/) |  |  |  | ✓ | ✓ | ✓
View [vulnerability report](https://docs.gitlab.com/user/application_security/vulnerability_report/) |  |  |  | ✓ | ✓ | ✓
View [security dashboard](https://docs.gitlab.com/user/application_security/security_dashboard/) |  |  |  | ✓ | ✓ | ✓
Create [security policy project](https://docs.gitlab.com/user/application_security/policies/) |  |  |  |  |  | ✓
Assign [security policy project](https://docs.gitlab.com/user/application_security/policies/) |  |  |  |  |  | ✓
### Group CI/CD[](https://docs.gitlab.com/user/permissions/#group-cicd "Permalink")
Group permissions for [CI/CD](https://docs.gitlab.com/ci/) features including runners, variables, and protected environments:
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View instance runner | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View group runners |  |  |  |  | ✓ | ✓
Manage group-level Kubernetes cluster |  |  |  |  | ✓ | ✓
Manage group runners |  |  |  |  |  | ✓
Manage group level CI/CD variables |  |  |  |  |  | ✓
Manage group protected environments |  |  |  |  |  | ✓
### Group compliance[](https://docs.gitlab.com/user/permissions/#group-compliance "Permalink")
Group permissions for [compliance](https://docs.gitlab.com/user/compliance/) features including compliance center, audit events, compliance frameworks, and licenses.
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [audit events](https://docs.gitlab.com/user/compliance/audit_events/) 1 |  |  |  | ✓ | ✓ | ✓
View licenses in [dependency list](https://docs.gitlab.com/user/application_security/dependency_list/) |  |  |  | ✓ | ✓ | ✓
View [compliance center](https://docs.gitlab.com/user/compliance/compliance_center/) |  |  |  |  |  | ✓
Manage [compliance frameworks](https://docs.gitlab.com/user/compliance/compliance_frameworks/) |  |  |  |  |  | ✓
Assign [compliance frameworks](https://docs.gitlab.com/user/compliance/compliance_frameworks/) to projects |  |  |  |  |  | ✓
Manage [audit streams](https://docs.gitlab.com/user/compliance/audit_event_streaming/) |  |  |  |  |  | ✓
**Footnotes** :
  1. Users can view events based on their individual actions only. For more details, see the [prerequisites](https://docs.gitlab.com/user/compliance/audit_events/#prerequisites).


### Group GitLab Duo[](https://docs.gitlab.com/user/permissions/#group-gitlab-duo "Permalink")
Group permissions for [GitLab Duo](https://docs.gitlab.com/user/gitlab_duo/):
Action | Non-member | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---|---
Use GitLab Duo features 1 |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Configure [GitLab Duo feature availability](https://docs.gitlab.com/user/gitlab_duo/turn_on_off/#for-a-group-or-subgroup) |  |  |  |  |  | ✓ | ✓
Configure [GitLab Duo Self Hosted](https://docs.gitlab.com/administration/gitlab_duo_self_hosted/configure_duo_features/) |  |  |  |  |  |  | ✓
Enable [beta and experimental features](https://docs.gitlab.com/user/gitlab_duo/turn_on_off/#turn-on-beta-and-experimental-features) |  |  |  |  |  |  | ✓
Purchase [GitLab Duo seats](https://docs.gitlab.com/subscriptions/subscription-add-ons/#purchase-additional-gitlab-duo-seats) |  |  |  |  |  |  | ✓
**Footnotes** :
  1. If the user has GitLab Duo Pro or Enterprise, the [user must be assigned a seat to gain access to that GitLab Duo add-on](https://docs.gitlab.com/subscriptions/subscription-add-ons/#assign-gitlab-duo-seats). If the user has GitLab Duo Core, there are no other requirements.


### Group packages and registries[](https://docs.gitlab.com/user/permissions/#group-packages-and-registries "Permalink")
Group permissions for the [package and container registry](https://docs.gitlab.com/user/packages/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Pull container registry images 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Pull container images with the dependency proxy | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Delete container registry images |  |  |  | ✓ | ✓ | ✓
Configure a virtual registry |  |  |  |  | ✓ | ✓
Pull an artifact from a virtual registry | ✓ |  | ✓ | ✓ | ✓ | ✓
**Footnotes** :
  1. Guests can only view events based on their individual actions.


Group permissions for [package registry](https://docs.gitlab.com/user/packages/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Pull packages |  |  | ✓ | ✓ | ✓ | ✓
Publish packages |  |  |  | ✓ | ✓ | ✓
Delete packages |  |  |  |  | ✓ | ✓
Manage package settings |  |  |  |  |  | ✓
Manage dependency proxy cleanup policies |  |  |  |  |  | ✓
Enable dependency proxy |  |  |  |  |  | ✓
Disable dependency proxy |  |  |  |  |  | ✓
Purge the group dependency proxy |  |  |  |  |  | ✓
Enable package request forwarding |  |  |  |  |  | ✓
Disable package request forwarding |  |  |  |  |  | ✓
### Group planning[](https://docs.gitlab.com/user/permissions/#group-planning "Permalink")
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View epic | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) epics 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add issues to an [epic](https://docs.gitlab.com/user/group/epics/) 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add [child epics](https://docs.gitlab.com/user/group/epics/manage_epics/#multi-level-child-epics) 3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add parent epic 4 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add internal notes |  | ✓ | ✓ | ✓ | ✓ | ✓
Create epics |  | ✓ | ✓ | ✓ | ✓ | ✓
Update epic details |  | ✓ | ✓ | ✓ | ✓ | ✓
Manage [epic boards](https://docs.gitlab.com/user/group/epics/epic_boards/) |  | ✓ | ✓ | ✓ | ✓ | ✓
Delete epics 5 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
**Footnotes** :
  1. You must have permission to [view the epic](https://docs.gitlab.com/user/group/epics/manage_epics/#who-can-view-an-epic).
  2. You must have permission to [view the epic](https://docs.gitlab.com/user/group/epics/manage_epics/#who-can-view-an-epic) and edit the issue.
  3. You must have permission to [view](https://docs.gitlab.com/user/group/epics/manage_epics/#who-can-view-an-epic) the parent and child epics.
  4. You must have permission to [view](https://docs.gitlab.com/user/group/epics/manage_epics/#who-can-view-an-epic) the parent epic.
  5. Users who don’t have the Planner or Owner role can only delete the epics they authored.


Group permissions for [wikis](https://docs.gitlab.com/user/project/wiki/group/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View group wiki 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) group wikis 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Create group wiki pages |  | ✓ |  | ✓ | ✓ | ✓
Edit group wiki pages |  | ✓ |  | ✓ | ✓ | ✓
Delete group wiki pages |  | ✓ |  | ✓ | ✓ | ✓
**Footnotes** :
  1. Guests: In addition, if your group is public or internal, all users who can see the group can also see group wiki pages.
  2. Guests: In addition, if your group is public or internal, all users who can see the group can also search group wiki pages.


### Group repositories[](https://docs.gitlab.com/user/permissions/#group-repositories "Permalink")
Group permissions for [repository](https://docs.gitlab.com/user/project/repository/) features including merge requests, push rules, and deploy tokens.
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Manage [deploy tokens](https://docs.gitlab.com/user/project/deploy_tokens/) |  |  |  |  |  | ✓
Manage [merge request settings](https://docs.gitlab.com/user/group/manage/#group-merge-request-approval-settings) |  |  |  |  |  | ✓
Manage [push rules](https://docs.gitlab.com/user/group/access_and_permissions/#group-push-rules) |  |  |  |  |  | ✓
### Group user management[](https://docs.gitlab.com/user/permissions/#group-user-management "Permalink")
Group permissions for user management:
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View 2FA status of members |  |  |  |  |  | ✓
Filter members by 2FA status |  |  |  |  |  | ✓
Manage group members |  |  |  |  |  | ✓
Manage group-level custom roles |  |  |  |  |  | ✓
Share (invite) groups to groups |  |  |  |  |  | ✓
### Group workspaces[](https://docs.gitlab.com/user/permissions/#group-workspaces "Permalink")
Groups permissions for workspaces:
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View workspace cluster agents mapped to a group |  |  |  |  | ✓ | ✓
Map or unmap workspace cluster agents to and from a group |  |  |  |  |  | ✓
## Project permissions[](https://docs.gitlab.com/user/permissions/#project-permissions "Permalink")
A user’s role determines what permissions they have on a project. The Owner role provides all permissions but is available only:
  * For group and project Owners.
  * For Administrators.


Personal [namespace](https://docs.gitlab.com/user/namespace/) owners:
  * Are displayed as having the Maintainer role on projects in the namespace, but have the same permissions as a user with the Owner role.
  * For new projects in the namespace, are displayed as having the Owner role.


When you configure [protected branch settings](https://docs.gitlab.com/user/project/repository/branches/protection_rules/), selecting a role grants access to users with that role and all higher roles. For example, if you select **Maintainers** in the protected branch settings, users with both the Maintainer and Owner roles can perform the action.
For more information about how to manage project members, see [members of a project](https://docs.gitlab.com/user/project/members/).
The following tables list the project permissions available for each role.
### Projects[](https://docs.gitlab.com/user/permissions/#projects "Permalink")
Project permissions for [project features](https://docs.gitlab.com/user/project/organize_work_with_projects/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Download project 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Leave comments | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Reposition comments on images (posted by any user) 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [insights](https://docs.gitlab.com/user/project/insights/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [requirements](https://docs.gitlab.com/user/project/requirements/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [time tracking](https://docs.gitlab.com/user/project/time_tracking/) reports 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [snippets](https://docs.gitlab.com/user/snippets/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) [snippets](https://docs.gitlab.com/user/snippets/) and comments | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [project traffic statistics](https://docs.gitlab.com/api/project_statistics/) |  |  | ✓ | ✓ | ✓ | ✓
Create [snippets](https://docs.gitlab.com/user/snippets/) |  |  | ✓ | ✓ | ✓ | ✓
View [releases](https://docs.gitlab.com/user/project/releases/) 3 |  | ✓ | ✓ | ✓ | ✓ | ✓
Manage [releases](https://docs.gitlab.com/user/project/releases/) 4 |  |  |  |  | ✓ | ✓
Configure [webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/) |  |  |  |  | ✓ | ✓
Manage [project access tokens](https://docs.gitlab.com/user/project/settings/project_access_tokens/) 5 |  |  |  |  | ✓ | ✓
[Export project](https://docs.gitlab.com/user/project/settings/import_export/) |  |  |  |  | ✓ | ✓
Rename project |  |  |  |  | ✓ | ✓
Edit project badges |  |  |  |  | ✓ | ✓
Edit project settings |  |  |  |  | ✓ | ✓
Change [project features visibility](https://docs.gitlab.com/user/public_access/) level 6 |  |  |  |  | ✓ | ✓
Change custom settings for [project integrations](https://docs.gitlab.com/user/project/integrations/) |  |  |  |  | ✓ | ✓
Edit comments posted by other users |  |  |  |  | ✓ | ✓
Add [deploy keys](https://docs.gitlab.com/user/project/deploy_keys/) |  |  |  |  | ✓ | ✓
Manage [project operations](https://docs.gitlab.com/operations/) |  |  |  |  | ✓ | ✓
View [Usage quotas](https://docs.gitlab.com/user/storage_usage_quotas/) page |  |  |  |  | ✓ | ✓
Globally delete [snippets](https://docs.gitlab.com/user/snippets/) |  |  |  |  | ✓ | ✓
Globally edit [snippets](https://docs.gitlab.com/user/snippets/) |  |  |  |  | ✓ | ✓
Archive project |  |  |  |  |  | ✓
Change project visibility level |  |  |  |  |  | ✓
Delete project |  |  |  |  |  | ✓
Disable notification emails |  |  |  |  |  | ✓
Transfer project |  |  |  |  |  | ✓
**Footnotes** :
  1. On GitLab Self-Managed, users with the Guest role are able to perform this action only on public and internal projects (not on private projects). [External users](https://docs.gitlab.com/administration/external_users/) must be given explicit access (at least the **Reporter** role) even if the project is internal. Users with the Guest role on GitLab.com are only able to perform this action on public projects because internal visibility is not available.
  2. Applies only to comments on [Design Management](https://docs.gitlab.com/user/project/issues/design_management/) designs.
  3. Guest users can access GitLab [**Releases**](https://docs.gitlab.com/user/project/releases/) for downloading assets but are not allowed to download the source code nor see [repository information like commits and release evidence](https://docs.gitlab.com/user/project/releases/#view-a-release-and-download-assets).
  4. If the [tag is protected](https://docs.gitlab.com/user/project/protected_tags/), this depends on the access given to Developers and Maintainers.
  5. For GitLab Self-Managed, project access tokens are available in all tiers. For GitLab.com, project access tokens are supported in the Premium and Ultimate tier (excluding [trial licenses](https://about.gitlab.com/free-trial/)).
  6. A Maintainer or Owner can’t change project features visibility level if [project visibility](https://docs.gitlab.com/user/public_access/) is set to private.


Project permissions for [GitLab Pages](https://docs.gitlab.com/user/project/pages/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View GitLab Pages protected by [access control](https://docs.gitlab.com/user/project/pages/pages_access_control/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Manage GitLab Pages |  |  |  |  | ✓ | ✓
Manage GitLab Pages domain and certificates |  |  |  |  | ✓ | ✓
Remove GitLab Pages |  |  |  |  | ✓ | ✓
### Project analytics[](https://docs.gitlab.com/user/permissions/#project-analytics "Permalink")
Project permissions for [analytics](https://docs.gitlab.com/user/analytics/) features including value streams, usage trends, product analytics, and insights.
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [issue analytics](https://docs.gitlab.com/user/group/issues_analytics/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [value stream analytics](https://docs.gitlab.com/user/group/value_stream_analytics/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [CI/CD analytics](https://docs.gitlab.com/user/analytics/ci_cd_analytics/) |  |  | ✓ | ✓ | ✓ | ✓
View [code review analytics](https://docs.gitlab.com/user/analytics/code_review_analytics/) |  |  | ✓ | ✓ | ✓ | ✓
View [DORA metrics](https://docs.gitlab.com/user/analytics/ci_cd_analytics/) |  |  | ✓ | ✓ | ✓ | ✓
View [merge request analytics](https://docs.gitlab.com/user/analytics/merge_request_analytics/) |  |  | ✓ | ✓ | ✓ | ✓
View [repository analytics](https://docs.gitlab.com/user/analytics/repository_analytics/) |  |  | ✓ | ✓ | ✓ | ✓
View [Value Streams Dashboard](https://docs.gitlab.com/user/analytics/value_streams_dashboard/) |  |  | ✓ | ✓ | ✓ | ✓
View [GitLab Duo and SDLC trends](https://docs.gitlab.com/user/analytics/duo_and_sdlc_trends/) |  |  | ✓ | ✓ | ✓ | ✓
### Project application security[](https://docs.gitlab.com/user/permissions/#project-application-security "Permalink")
Project permissions for [application security](https://docs.gitlab.com/user/application_security/secure_your_application/) features including dependency management, security analyzers, security policies, and vulnerability management.
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [dependency list](https://docs.gitlab.com/user/application_security/dependency_list/) |  |  |  | ✓ | ✓ | ✓
View licenses in [dependency list](https://docs.gitlab.com/user/application_security/dependency_list/) |  |  |  | ✓ | ✓ | ✓
View [security dashboard](https://docs.gitlab.com/user/application_security/security_dashboard/) |  |  |  | ✓ | ✓ | ✓
View [vulnerability report](https://docs.gitlab.com/user/application_security/vulnerability_report/) |  |  |  | ✓ | ✓ | ✓
Create [vulnerability manually](https://docs.gitlab.com/user/application_security/vulnerability_report/#manually-add-a-vulnerability) |  |  |  |  | ✓ | ✓
Create [issue](https://docs.gitlab.com/user/application_security/vulnerabilities/#create-a-gitlab-issue-for-a-vulnerability) from vulnerability finding |  |  |  | ✓ | ✓ | ✓
Create [on-demand DAST scans](https://docs.gitlab.com/user/application_security/dast/on-demand_scan/) |  |  |  | ✓ | ✓ | ✓
Run [on-demand DAST scans](https://docs.gitlab.com/user/application_security/dast/on-demand_scan/) |  |  |  | ✓ | ✓ | ✓
Create [individual security policies](https://docs.gitlab.com/user/application_security/policies/) |  |  |  | ✓ | ✓ | ✓
Change [individual security policies](https://docs.gitlab.com/user/application_security/policies/) |  |  |  | ✓ | ✓ | ✓
Delete [individual security policies](https://docs.gitlab.com/user/application_security/policies/) |  |  |  | ✓ | ✓ | ✓
Create [CVE ID request](https://docs.gitlab.com/user/application_security/cve_id_request/) |  |  |  |  | ✓ | ✓
Change vulnerability status 1 |  |  |  |  | ✓ | ✓
Create [security policy project](https://docs.gitlab.com/user/application_security/policies/) |  |  |  |  |  | ✓
Assign [security policy project](https://docs.gitlab.com/user/application_security/policies/) |  |  |  |  |  | ✓
Manage [security configurations](https://docs.gitlab.com/user/application_security/detect/security_configuration/) |  |  |  |  | ✓ | ✓
**Footnotes** :
  1. The `admin_vulnerability` permission was [removed](https://gitlab.com/gitlab-org/gitlab/-/issues/412693) from the Developer role in GitLab 17.0.


### Project CI/CD[](https://docs.gitlab.com/user/permissions/#project-cicd "Permalink")
[GitLab CI/CD](https://docs.gitlab.com/ci/) permissions for some roles can be modified by these settings:
  * [Project-based pipeline visibility](https://docs.gitlab.com/ci/pipelines/settings/#change-which-users-can-view-your-pipelines): When set to public, gives access to certain CI/CD features to Guest project members.
  * [Pipeline visibility](https://docs.gitlab.com/ci/pipelines/settings/#change-pipeline-visibility-for-non-project-members-in-public-projects): When set to **Everyone with Access** , gives access to certain CI/CD “view” features to non-project members.


Project Owners can perform any listed action, and can delete pipelines:
Action | Non-member | Guest | Planner | Reporter | Developer | Maintainer
---|---|---|---|---|---|---
View instance runner | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View existing artifacts 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View list of jobs 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View artifacts 3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Download artifacts 3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [environments](https://docs.gitlab.com/ci/environments/) 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View job logs and job details page 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View pipelines and pipeline details pages 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View pipelines tab in MR 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [vulnerabilities in a pipeline](https://docs.gitlab.com/user/application_security/detect/security_scanning_results/) 4 |  | ✓ | ✓ | ✓ | ✓ | ✓
Run deployment job for a protected environment 5 |  |  |  | ✓ | ✓ | ✓
View [agents for Kubernetes](https://docs.gitlab.com/user/clusters/agent/) |  |  |  |  | ✓ | ✓
View project [Secure Files](https://docs.gitlab.com/api/secure_files/) |  |  |  |  | ✓ | ✓
Download project [Secure Files](https://docs.gitlab.com/api/secure_files/) |  |  |  |  | ✓ | ✓
View a job with [debug logging](https://docs.gitlab.com/ci/variables/variables_troubleshooting/#enable-debug-logging) |  |  |  |  | ✓ | ✓
Create [environments](https://docs.gitlab.com/ci/environments/) |  |  |  |  | ✓ | ✓
Delete [environments](https://docs.gitlab.com/ci/environments/) |  |  |  |  | ✓ | ✓
Stop [environments](https://docs.gitlab.com/ci/environments/) |  |  |  |  | ✓ | ✓
Run, rerun, or retry CI/CD pipeline or job |  |  |  |  | ✓ | ✓
Run, rerun, or retry CI/CD pipeline or job for a protected branch 6 |  |  |  |  | ✓ | ✓
Delete job logs or job artifacts 7 |  |  |  |  | ✓ | ✓
Enable [review apps](https://docs.gitlab.com/ci/review_apps/) |  |  |  |  | ✓ | ✓
Cancel jobs 8 |  |  |  |  | ✓ | ✓
Read [Terraform](https://docs.gitlab.com/user/infrastructure/) state |  |  |  |  | ✓ | ✓
Run [interactive web terminals](https://docs.gitlab.com/ci/interactive_web_terminal/) |  |  |  |  | ✓ | ✓
Use pipeline editor |  |  |  |  | ✓ | ✓
View project runners 9 |  |  |  |  |  | ✓
Manage project runners 9 |  |  |  |  |  | ✓
Delete project runners 10 |  |  |  |  |  | ✓
Manage [agents for Kubernetes](https://docs.gitlab.com/user/clusters/agent/) |  |  |  |  |  | ✓
Manage CI/CD settings |  |  |  |  |  | ✓
Manage job triggers |  |  |  |  |  | ✓
Manage project CI/CD variables |  |  |  |  |  | ✓
Manage project protected environments |  |  |  |  |  | ✓
Manage project [Secure Files](https://docs.gitlab.com/api/secure_files/) |  |  |  |  |  | ✓
Manage [Terraform](https://docs.gitlab.com/user/infrastructure/) state |  |  |  |  |  | ✓
Add project runners to project 11 |  |  |  |  |  | ✓
Clear runner caches manually |  |  |  |  |  | ✓
Enable instance runners in project |  |  |  |  |  | ✓
Create pipeline schedules 12 |  |  |  |  | ✓ | ✓
Edit own pipeline schedules 12 |  |  |  |  | ✓ | ✓
Delete own pipeline schedules |  |  |  |  | ✓ | ✓
Run pipeline schedules manually 13 |  |  |  |  | ✓ | ✓
Take ownership of pipeline schedules |  |  |  |  |  | ✓
Delete others’ pipeline schedules |  |  |  |  |  | ✓
**Footnotes** :
  1. Non-members and guests: Only if the project is public.
  2. Non-members: Only if the project is public and **Project-based pipeline visibility** is enabled.
Guests: Only if **Project-based pipeline visibility** is enabled.
  3. Non-members: Only if the project is public, **Project-based pipeline visibility** is enabled, and [`artifacts:public: false`](https://docs.gitlab.com/ci/yaml/#artifactspublic) is not set on the job.
Guests: Only if **Project-based pipeline visibility** is enabled and `artifacts:public: false` is not set on the job.
Reporters: Only if `artifacts:public: false` is not set on the job.
The `artifacts:public` setting only affects GitLab UI and API access. CI/CD job tokens can still access artifacts with the runner API.
  4. Guests: Only if **Project-based pipeline visibility** is enabled.
  5. Reporters: Only if the user is [part of a group with access to the protected environment](https://docs.gitlab.com/ci/environments/protected_environments/#deployment-only-access-to-protected-environments).
Developers and maintainers: Only if the user is [allowed to deploy to the protected environment](https://docs.gitlab.com/ci/environments/protected_environments/#protecting-environments).
  6. Developers and maintainers: Only if the user is [allowed to merge or push to the protected branch](https://docs.gitlab.com/ci/pipelines/#pipeline-security-on-protected-branches).
  7. Developers: Only if the job was triggered by the user and runs for a non-protected branch.
  8. Cancellation permissions can be [restricted in the pipeline settings](https://docs.gitlab.com/ci/pipelines/settings/#restrict-roles-that-can-cancel-pipelines-or-jobs).
  9. Maintainers: Must have the Maintainer role for a project associated with the runner.
  10. Maintainers: Must have the Maintainer role for [the owner project](https://docs.gitlab.com/ci/runners/runners_scope/#project-runner-ownership) (first project associated with runner).
  11. Maintainers: Must have the Maintainer role for the project being added and for a project already associated with the runner.
  12. Developers: Only for branches where the user has merge permissions. For protected branches, must have merge permissions for the target branch. For protected tags, the user must be allowed to create protected tags. These permission requirements apply when creating or editing schedules, and are checked dynamically as branch protection rules may change over time.
  13. When running manually, the pipeline executes with the triggering user’s permissions instead of the schedule owner’s permissions.


This table shows granted privileges for jobs triggered by specific roles.
Project Owners can do any listed action, but no users can push source and LFS together. Guest users and members with the Reporter role cannot do any of these actions.
Action | Developer | Maintainer
---|---|---
Clone source and LFS from current project | ✓ | ✓
Clone source and LFS from public projects | ✓ | ✓
Clone source and LFS from internal projects 1 | ✓ | ✓
Clone source and LFS from private projects 2 | ✓ | ✓
Pull container images from current project | ✓ | ✓
Pull container images from public projects | ✓ | ✓
Pull container images from internal projects 1 | ✓ | ✓
Pull container images from private projects 2 | ✓ | ✓
Push container images to current project 3 | ✓ | ✓
**Footnotes** :
  1. Developers and Maintainers: Only if the triggering user is not an external user.
  2. Only if the triggering user is a member of the project. See also [Usage of private Docker images with `if-not-present` pull policy](https://docs.gitlab.com/runner/security/#usage-of-private-docker-images-with-if-not-present-pull-policy).
  3. You cannot push container images to other projects.


### Project compliance[](https://docs.gitlab.com/user/permissions/#project-compliance "Permalink")
Project permissions for [compliance](https://docs.gitlab.com/user/compliance/) features including compliance center, audit events, compliance frameworks, and licenses.
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [allowed and denied licenses in MR](https://docs.gitlab.com/user/compliance/license_scanning_of_cyclonedx_files/) 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [audit events](https://docs.gitlab.com/user/compliance/audit_events/) 2 |  |  |  | ✓ | ✓ | ✓
View licenses in [dependency list](https://docs.gitlab.com/user/application_security/dependency_list/) |  |  |  | ✓ | ✓ | ✓
Manage [audit streams](https://docs.gitlab.com/user/compliance/audit_event_streaming/) |  |  |  |  |  | ✓
**Footnotes** :
  1. On GitLab Self-Managed, users with the Guest role are able to perform this action only on public and internal projects (not on private projects). [External users](https://docs.gitlab.com/administration/external_users/) must have the Reporter, Developer, Maintainer, or Owner role, even if the project is internal. Users with the Guest role on GitLab.com are able to perform this action only on public projects because internal visibility is not available.
  2. Users can only view events based on their individual actions. For more details, see the [prerequisites](https://docs.gitlab.com/user/compliance/audit_events/#prerequisites).


### Project GitLab Duo[](https://docs.gitlab.com/user/permissions/#project-gitlab-duo "Permalink")
Project permissions for [GitLab Duo](https://docs.gitlab.com/user/gitlab_duo/):
Action | Non-member | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---|---
Use GitLab Duo features 1 |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Configure [GitLab Duo feature availability](https://docs.gitlab.com/user/gitlab_duo/turn_on_off/#for-a-project) |  |  |  |  |  | ✓ | ✓
**Footnotes** :
  1. Code Suggestions requires a [user being assigned a seat to gain access to a GitLab Duo add-on](https://docs.gitlab.com/subscriptions/subscription-add-ons/#assign-gitlab-duo-seats).


### Project merge requests[](https://docs.gitlab.com/user/permissions/#project-merge-requests "Permalink")
Project permissions for [merge requests](https://docs.gitlab.com/user/project/merge_requests/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
[View](https://docs.gitlab.com/user/project/merge_requests/#view-merge-requests) a merge request 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) merge requests and comments 12 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Approve](https://docs.gitlab.com/user/project/merge_requests/approvals/) merge requests 3 |  | ✓ | ✓ | ✓ | ✓ | ✓
Add internal note |  | ✓ | ✓ | ✓ | ✓ | ✓
Comment and add suggestions |  | ✓ | ✓ | ✓ | ✓ | ✓
Create [snippets](https://docs.gitlab.com/user/snippets/) |  |  | ✓ | ✓ | ✓ | ✓
Create [merge request](https://docs.gitlab.com/user/project/merge_requests/creating_merge_requests/) 4 |  |  |  | ✓ | ✓ | ✓
Update merge request details 5 |  |  |  | ✓ | ✓ | ✓
Manage [merge request settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/) |  |  |  |  | ✓ | ✓
Manage [merge request approval rules](https://docs.gitlab.com/user/project/merge_requests/approvals/rules/) |  |  |  |  | ✓ | ✓
Delete merge request |  |  |  |  |  | ✓
**Footnotes** :
  1. On GitLab Self-Managed, users with the Guest role are able to perform this action only on public and internal projects (not on private projects). [External users](https://docs.gitlab.com/administration/external_users/) must be given explicit access (at least the **Reporter** role) even if the project is internal. Users with the Guest role on GitLab.com are only able to perform this action on public projects because internal visibility is not available.
  2. Users with the Planner role can not use advanced search for merge requests and comments on merge requests. For more information, see [epic &17674](https://gitlab.com/groups/gitlab-org/-/work_items/17674).
  3. Approval from Planner and Reporter roles is available only if [enabled for the project](https://docs.gitlab.com/user/project/merge_requests/approvals/rules/#enable-approval-permissions-for-additional-users).
  4. In projects that accept contributions from external members, users can create, edit, and close their own merge requests. For **private** projects, this excludes the Guest role as those users [cannot clone private projects](https://docs.gitlab.com/user/public_access/#private-projects-and-groups). For **internal** projects, includes users with read-only access to the project, as [they can clone internal projects](https://docs.gitlab.com/user/public_access/#internal-projects-and-groups).
  5. In projects that accept contributions from external members, users can create, edit, and close their own merge requests. They cannot edit some fields, like assignees, reviewers, labels, and milestones.


### Project model registry and experiments[](https://docs.gitlab.com/user/permissions/#project-model-registry-and-experiments "Permalink")
Project permissions for [model registry](https://docs.gitlab.com/user/project/ml/model_registry/) and [model experiments](https://docs.gitlab.com/user/project/ml/experiment_tracking/).
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View [models and versions](https://docs.gitlab.com/user/project/ml/model_registry/) 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [model experiments](https://docs.gitlab.com/user/project/ml/experiment_tracking/) 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Create models, versions, and artifacts 3 |  |  |  | ✓ | ✓ | ✓
Edit models, versions, and artifacts |  |  |  | ✓ | ✓ | ✓
Delete models, versions, and artifacts |  |  |  | ✓ | ✓ | ✓
Create experiments and candidates |  |  |  | ✓ | ✓ | ✓
Edit experiments and candidates |  |  |  | ✓ | ✓ | ✓
Delete experiments and candidates |  |  |  | ✓ | ✓ | ✓
**Footnotes** :
  1. Non-members can only view models and versions in public projects with the **Everyone with access** visibility level. Non-members can’t view internal projects, even if they’re logged in.
  2. Non-members can only view model experiments in public projects with the **Everyone with access** visibility level. Non-members can’t view internal projects, even if they’re logged in.
  3. You can also upload and download artifacts with the package registry API, which uses a different set of permissions.


### Project monitoring[](https://docs.gitlab.com/user/permissions/#project-monitoring "Permalink")
Project permissions for monitoring including [error tracking](https://docs.gitlab.com/operations/error_tracking/) and [incident management](https://docs.gitlab.com/operations/incident_management/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View an [incident](https://docs.gitlab.com/operations/incident_management/incidents/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Assign an [incident management](https://docs.gitlab.com/operations/incident_management/) alert | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Participate in on-call rotation for [Incident Management](https://docs.gitlab.com/operations/incident_management/) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [alerts](https://docs.gitlab.com/operations/incident_management/alerts/) |  |  | ✓ | ✓ | ✓ | ✓
View [error tracking](https://docs.gitlab.com/operations/error_tracking/) list |  |  | ✓ | ✓ | ✓ | ✓
View [escalation policies](https://docs.gitlab.com/operations/incident_management/escalation_policies/) |  |  | ✓ | ✓ | ✓ | ✓
View [on-call schedules](https://docs.gitlab.com/operations/incident_management/oncall_schedules/) |  |  | ✓ | ✓ | ✓ | ✓
Create [incident](https://docs.gitlab.com/operations/incident_management/incidents/) |  |  | ✓ | ✓ | ✓ | ✓
Change [alert status](https://docs.gitlab.com/operations/incident_management/alerts/#change-an-alerts-status) |  |  | ✓ | ✓ | ✓ | ✓
Change [incident severity](https://docs.gitlab.com/operations/incident_management/manage_incidents/#change-severity) |  |  | ✓ | ✓ | ✓ | ✓
Change [incident escalation status](https://docs.gitlab.com/operations/incident_management/manage_incidents/#change-status) |  |  |  | ✓ | ✓ | ✓
Change [incident escalation policy](https://docs.gitlab.com/operations/incident_management/manage_incidents/#change-escalation-policy) |  |  |  | ✓ | ✓ | ✓
Manage [error tracking](https://docs.gitlab.com/operations/error_tracking/) |  |  |  |  | ✓ | ✓
Manage [escalation policies](https://docs.gitlab.com/operations/incident_management/escalation_policies/) |  |  |  |  | ✓ | ✓
Manage [on-call schedules](https://docs.gitlab.com/operations/incident_management/oncall_schedules/) |  |  |  |  | ✓ | ✓
### Project packages and registries[](https://docs.gitlab.com/user/permissions/#project-packages-and-registries "Permalink")
Project permissions for [container registry](https://docs.gitlab.com/user/packages/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Pull container registry images 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Push container registry images |  |  |  | ✓ | ✓ | ✓
Delete container registry images |  |  |  | ✓ | ✓ | ✓
Manage cleanup policies |  |  |  |  | ✓ | ✓
Create [tag protection](https://docs.gitlab.com/user/packages/container_registry/protected_container_tags/) rules |  |  |  |  | ✓ | ✓
Create [immutable tag protection](https://docs.gitlab.com/user/packages/container_registry/immutable_container_tags/) rules |  |  |  |  |  | ✓
**Footnotes** :
  1. Viewing the container registry and pulling images is controlled by [container registry visibility permissions](https://docs.gitlab.com/user/packages/container_registry/#container-registry-visibility-permissions). The Guest role does not have viewing or pulling permissions in private projects.


Project permissions for [package registry](https://docs.gitlab.com/user/packages/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
Pull packages 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Publish packages |  |  |  | ✓ | ✓ | ✓
Delete packages |  |  |  |  | ✓ | ✓
Delete files associated with a package |  |  |  |  | ✓ | ✓
**Footnotes** :
  1. On GitLab Self-Managed, users with the Guest role are able to perform this action only on public and internal projects (not on private projects). [External users](https://docs.gitlab.com/administration/external_users/) must be given explicit access (at least the **Reporter** role) even if the project is internal. Users with the Guest role on GitLab.com are only able to perform this action on public projects because internal visibility is not available.


### Project planning[](https://docs.gitlab.com/user/permissions/#project-planning "Permalink")
Project permissions for [issues](https://docs.gitlab.com/user/project/issues/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View issues | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) issues and comments | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Create issues | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View [confidential issues](https://docs.gitlab.com/user/project/issues/confidential_issues/) |  | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) confidential issues and comments 6 |  | ✓ | ✓ | ✓ | ✓ | ✓
Edit issues, including metadata, item locking, and resolving threads 1 |  | ✓ | ✓ | ✓ | ✓ | ✓
Add internal notes |  | ✓ | ✓ | ✓ | ✓ | ✓
Close and reopen issues 2 |  | ✓ | ✓ | ✓ | ✓ | ✓
Manage [design management](https://docs.gitlab.com/user/project/issues/design_management/) files |  | ✓ | ✓ | ✓ | ✓ | ✓
Manage [issue boards](https://docs.gitlab.com/user/project/issue_board/) |  | ✓ | ✓ | ✓ | ✓ | ✓
Manage [milestones](https://docs.gitlab.com/user/project/milestones/) |  | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) milestones 6 |  | ✓ | ✓ | ✓ | ✓ | ✓
Archive or reopen [requirements](https://docs.gitlab.com/user/project/requirements/) 3 |  | ✓ | ✓ | ✓ | ✓ | ✓
Create or edit [requirements](https://docs.gitlab.com/user/project/requirements/) 4 |  | ✓ | ✓ | ✓ | ✓ | ✓
Import or export [requirements](https://docs.gitlab.com/user/project/requirements/) |  | ✓ | ✓ | ✓ | ✓ | ✓
Archive [test cases](https://docs.gitlab.com/ci/test_cases/) |  | ✓ | ✓ | ✓ | ✓ | ✓
Create [test cases](https://docs.gitlab.com/ci/test_cases/) |  | ✓ | ✓ | ✓ | ✓ | ✓
Move [test cases](https://docs.gitlab.com/ci/test_cases/) |  | ✓ | ✓ | ✓ | ✓ | ✓
Reopen [test cases](https://docs.gitlab.com/ci/test_cases/) |  | ✓ | ✓ | ✓ | ✓ | ✓
[Import](https://docs.gitlab.com/user/project/issues/csv_import/) issues from a CSV file |  | ✓ |  | ✓ | ✓ | ✓
[Export](https://docs.gitlab.com/user/project/issues/csv_export/) issues to a CSV file | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Delete issues 5 |  | ✓ | ✓ | ✓ | ✓ | ✓
Manage [Feature flags](https://docs.gitlab.com/operations/feature_flags/) |  |  |  | ✓ | ✓ | ✓
**Footnotes** :
  1. Metadata includes labels, assignees, milestones, epics, weight, confidentiality, time tracking, and more. Guest users can only set metadata when creating an issue. They cannot change the metadata on existing issues. Guest users can modify the title and description of issues that they authored or are assigned to.
  2. Guest users can close and reopen issues that they authored or are assigned to.
  3. Guest users can archive and reopen issues that they authored or are assigned to.
  4. Guest users can modify the title and description that they authored or are assigned to.
  5. Users who don’t have the Planner or Owner role can only delete the issues they authored.
  6. Users with the Planner role can not use advanced search for milestones or comments on confidential issues. For more information, see [epic 17674](https://gitlab.com/groups/gitlab-org/-/work_items/17674).


Project permissions for [tasks](https://docs.gitlab.com/user/tasks/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View tasks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) tasks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Create tasks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Edit tasks, including metadata, item locking, and resolving threads 1 |  | ✓ | ✓ | ✓ | ✓ | ✓
Add a linked item | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Convert to another item type |  | ✓ | ✓ | ✓ | ✓ | ✓
Remove from issue | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add internal note |  | ✓ | ✓ | ✓ | ✓ | ✓
Delete tasks 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
**Footnotes** :
  1. Guest users can modify the title and description that they authored or are assigned to.
  2. Users who don’t have the Planner or Owner role can only delete the tasks they authored.


Project permissions for [OKRs](https://docs.gitlab.com/user/okrs/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View OKRs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) OKRs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Create OKRs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Edit OKRs, including metadata, item locking, and resolving threads | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add a child OKR | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Add a linked item | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Convert to another item type | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Edit OKRs |  | ✓ | ✓ | ✓ | ✓ | ✓
Change confidentiality in OKR |  | ✓ | ✓ | ✓ | ✓ | ✓
Add internal note |  | ✓ | ✓ | ✓ | ✓ | ✓
Project permissions for [wikis](https://docs.gitlab.com/user/project/wiki/):
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View wiki | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) wikis | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Create wiki pages |  | ✓ |  | ✓ | ✓ | ✓
Edit wiki pages |  | ✓ |  | ✓ | ✓ | ✓
Delete wiki pages |  | ✓ |  | ✓ | ✓ | ✓
### Project repositories[](https://docs.gitlab.com/user/permissions/#project-repositories "Permalink")
Project permissions for [repository](https://docs.gitlab.com/user/project/repository/) features including source code, branches, push rules, and more:
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View project code 1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) project code 1 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
[Search](https://docs.gitlab.com/user/search/) commits and comments 1 2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
Pull project code 3 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓
View commit status |  |  | ✓ | ✓ | ✓ | ✓
Create commit status 4 |  |  |  | ✓ | ✓ | ✓
Update commit status 4 |  |  |  | ✓ | ✓ | ✓
Create [Git tags](https://docs.gitlab.com/user/project/repository/tags/) |  |  |  | ✓ | ✓ | ✓
Delete [Git tags](https://docs.gitlab.com/user/project/repository/tags/) |  |  |  | ✓ | ✓ | ✓
Create new [branches](https://docs.gitlab.com/user/project/repository/branches/) |  |  |  | ✓ | ✓ | ✓
Push to non-protected branches |  |  |  | ✓ | ✓ | ✓
Force push to non-protected branches |  |  |  | ✓ | ✓ | ✓
Delete non-protected branches |  |  |  | ✓ | ✓ | ✓
Manage [protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/) |  |  |  |  | ✓ | ✓
Push to protected branches 4 |  |  |  |  | ✓ | ✓
Delete protected branches |  |  |  |  | ✓ | ✓
Manage [protected tags](https://docs.gitlab.com/user/project/protected_tags/) |  |  |  |  | ✓ | ✓
Manage [push rules](https://docs.gitlab.com/user/project/repository/push_rules/) |  |  |  |  | ✓ | ✓
Remove fork relationship |  |  |  |  |  | ✓
Force push to protected branches 5 |  |  |  |  |  |
**Footnotes** :
  1. On GitLab Self-Managed, users with the Guest role are able to perform this action only on public and internal projects (not on private projects). [External users](https://docs.gitlab.com/administration/external_users/) must be given explicit access (at least the **Planner** role) even if the project is internal. Users with the Guest role on GitLab.com are only able to perform this action on public projects because internal visibility is not available. In GitLab 15.9 and later, users with the Guest role and an Ultimate license can view private repository content if an administrator (on GitLab Self-Managed or GitLab Dedicated) or group owner (on GitLab.com) gives those users permission. The administrator or group owner can create a [custom role](https://docs.gitlab.com/user/custom_roles/) through the API or UI and assign that role to the users. In GitLab 18.7 and later, users with the Planner role can view private repository content.
  2. Users with the Planner role can not use exact code search or advanced search for code, commits, and comments on commits in private projects. For more information, see [epic &17674](https://gitlab.com/groups/gitlab-org/-/work_items/17674).
  3. If the [branch is protected](https://docs.gitlab.com/user/project/repository/branches/protected/), this depends on the access given to Developers and Maintainers.
  4. On GitLab Self-Managed, users with the Guest role are able to perform this action only on public and internal projects (not on private projects). [External users](https://docs.gitlab.com/administration/external_users/) must be given explicit access (at least the **Reporter** role) even if the project is internal. Users with the Guest role on GitLab.com are only able to perform this action on public projects because internal visibility is not available. In GitLab 15.9 and later, users with the Guest role and an Ultimate license can view private repository content if an administrator (on GitLab Self-Managed or GitLab Dedicated) or group owner (on GitLab.com) gives those users permission. The administrator or group owner can create a [custom role](https://docs.gitlab.com/user/custom_roles/) through the API or UI and assign that role to the users.
  5. Not allowed for Guest, Reporter, Developer, Maintainer, or Owner. See [protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/#allow-force-push).


### Project user management[](https://docs.gitlab.com/user/permissions/#project-user-management "Permalink")
Project permissions for [user management](https://docs.gitlab.com/user/project/members/).
Action | Guest | Planner | Reporter | Developer | Maintainer | Owner
---|---|---|---|---|---|---
View 2FA status of members |  |  |  |  | ✓ | ✓
Manage [project members](https://docs.gitlab.com/user/project/members/) 1 |  |  |  |  | ✓ | ✓
Share (invite) projects with groups 2 |  |  |  |  |  | ✓
**Footnotes** :
  1. Maintainers cannot create, demote, or remove Owners, and they cannot promote users to the Owner role. They also cannot approve Owner role access requests.
  2. When [Share Group Lock](https://docs.gitlab.com/user/project/members/sharing_projects_groups/#prevent-a-project-from-being-shared-with-groups) is enabled the project can’t be shared with other groups. It does not affect group with group sharing.


## Subgroup permissions[](https://docs.gitlab.com/user/permissions/#subgroup-permissions "Permalink")
When you add a member to a subgroup, they inherit the membership and permission level from the parent groups. This model allows access to nested groups if you have membership in one of its parents.
For more information, see [subgroup memberships](https://docs.gitlab.com/user/group/subgroups/#subgroup-membership).
## Users with Minimal Access[](https://docs.gitlab.com/user/permissions/#users-with-minimal-access "Permalink")
  * Tier: Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


History
  * Support for inviting users with Minimal Access role [introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/106438) in GitLab 15.9.
  * Minimal Access users [changed](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/216727) to non-billable in GitLab 18.9.


Users with the Minimal Access role do not:
  * Automatically have access to projects and subgroups in that top-level group. Owners must explicitly add these users to the specific subgroups and projects.
  * Count as licensed seats, provided the user has no other role anywhere on the instance or in the GitLab.com namespace.


If a user with the Minimal Access role is granted a [billable role](https://docs.gitlab.com/subscriptions/manage_users_and_seats/#billable-users) in any project or subgroup, they consume a license seat based on their highest role.
You can use the Minimal Access role with [SAML SSO for GitLab.com groups](https://docs.gitlab.com/user/group/saml_sso/) to control access to groups and projects in the group hierarchy. You can set the default role to Minimal Access for members automatically added to the top-level group through SSO.
  1. On the top bar, select **Search or go to** and find your group.
  2. Select **Settings** > **SAML SSO**.
  3. From the **Default membership role** dropdown list, select **Minimal Access**.
  4. Select **Save changes**.


### Minimal access users receive 404 errors[](https://docs.gitlab.com/user/permissions/#minimal-access-users-receive-404-errors "Permalink")
Because of an [outstanding issue](https://gitlab.com/gitlab-org/gitlab/-/issues/267996), when a user with the Minimal Access role:
  * Signs in with standard web authentication, they receive a `404` error when accessing the parent group.
  * Signs in with Group SSO, they receive a `404` error immediately because they are redirected to the parent group page.


To work around the issue, give these users the Guest, Planner, Reporter, Developer, Maintainer, or Owner role to any project or subgroup in the parent group. Guest users consume a license seat in the Premium tier but do not in the Ultimate tier.
## Related topics[](https://docs.gitlab.com/user/permissions/#related-topics "Permalink")
  * [Protect your repository](https://docs.gitlab.com/user/project/repository/protect/)
  * [Custom roles](https://docs.gitlab.com/user/custom_roles/)
  * [Members](https://docs.gitlab.com/user/project/members/)
  * Customize permissions on [protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/)
  * [LDAP user permissions](https://docs.gitlab.com/user/group/access_and_permissions/#manage-group-memberships-with-ldap)
  * [Value stream analytics permissions](https://docs.gitlab.com/user/group/value_stream_analytics/#access-permissions)
  * [Project aliases](https://docs.gitlab.com/user/project/working_with_projects/#project-aliases)
  * [Auditor users](https://docs.gitlab.com/administration/auditor_users/)
  * [Confidential issues](https://docs.gitlab.com/user/project/issues/confidential_issues/)
  * [Container registry permissions](https://docs.gitlab.com/user/packages/container_registry/#container-registry-visibility-permissions)
  * [Release permissions](https://docs.gitlab.com/user/project/releases/#release-permissions)
  * [Read-only namespaces](https://docs.gitlab.com/user/read_only_namespaces/)


Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/user/permissions.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/permissions.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Roles](https://docs.gitlab.com/user/permissions/#roles)
  * [Default roles](https://docs.gitlab.com/user/permissions/#default-roles)
  * [Group permissions](https://docs.gitlab.com/user/permissions/#group-permissions)
  * [Groups](https://docs.gitlab.com/user/permissions/#groups)
  * [Group analytics](https://docs.gitlab.com/user/permissions/#group-analytics)
  * [Group application security](https://docs.gitlab.com/user/permissions/#group-application-security)
  * [Group CI/CD](https://docs.gitlab.com/user/permissions/#group-cicd)
  * [Group compliance](https://docs.gitlab.com/user/permissions/#group-compliance)
  * [Group GitLab Duo](https://docs.gitlab.com/user/permissions/#group-gitlab-duo)
  * [Group packages and registries](https://docs.gitlab.com/user/permissions/#group-packages-and-registries)
  * [Group planning](https://docs.gitlab.com/user/permissions/#group-planning)
  * [Group repositories](https://docs.gitlab.com/user/permissions/#group-repositories)
  * [Group user management](https://docs.gitlab.com/user/permissions/#group-user-management)
  * [Group workspaces](https://docs.gitlab.com/user/permissions/#group-workspaces)
  * [Project permissions](https://docs.gitlab.com/user/permissions/#project-permissions)
  * [Projects](https://docs.gitlab.com/user/permissions/#projects)
  * [Project analytics](https://docs.gitlab.com/user/permissions/#project-analytics)
  * [Project application security](https://docs.gitlab.com/user/permissions/#project-application-security)
  * [Project CI/CD](https://docs.gitlab.com/user/permissions/#project-cicd)
  * [Project compliance](https://docs.gitlab.com/user/permissions/#project-compliance)
  * [Project GitLab Duo](https://docs.gitlab.com/user/permissions/#project-gitlab-duo)
  * [Project merge requests](https://docs.gitlab.com/user/permissions/#project-merge-requests)
  * [Project model registry and experiments](https://docs.gitlab.com/user/permissions/#project-model-registry-and-experiments)
  * [Project monitoring](https://docs.gitlab.com/user/permissions/#project-monitoring)
  * [Project packages and registries](https://docs.gitlab.com/user/permissions/#project-packages-and-registries)
  * [Project planning](https://docs.gitlab.com/user/permissions/#project-planning)
  * [Project repositories](https://docs.gitlab.com/user/permissions/#project-repositories)
  * [Project user management](https://docs.gitlab.com/user/permissions/#project-user-management)
  * [Subgroup permissions](https://docs.gitlab.com/user/permissions/#subgroup-permissions)
  * [Users with Minimal Access](https://docs.gitlab.com/user/permissions/#users-with-minimal-access)
  * [Minimal access users receive 404 errors](https://docs.gitlab.com/user/permissions/#minimal-access-users-receive-404-errors)
  * [Related topics](https://docs.gitlab.com/user/permissions/#related-topics)


[![GitLab Docs logo](https://docs.gitlab.com/gitlab-logo-footer.svg)](https://docs.gitlab.com/)
  * [Facebook](https://www.facebook.com/gitlab)
  * [LinkedIn](https://www.linkedin.com/company/gitlab-com)
  * [Twitter](https://twitter.com/gitlab)
  * [YouTube](https://www.youtube.com/channel/UCnMGQ8QHMAnVIsI3xJrihhg)

[![Creative Commons License](https://docs.gitlab.com/by-sa.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
Company
  * [About GitLab](https://about.gitlab.com/company/)
  * [View pricing](https://about.gitlab.com/pricing/)
  * [Try GitLab for free](https://about.gitlab.com/free-trial/)


Feedback
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/permissions.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/user/permissions.md)
  * [Contribute to GitLab](https://about.gitlab.com/community/contribute/)
  * [Suggest updates](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


Help & Community
  * [Get certified](https://university.gitlab.com/pages/certifications)
  * [Get support](https://about.gitlab.com/support/)
  * [Post on the GitLab forum](https://forum.gitlab.com/new-topic?title=topic%20title&body=topic%20body&tags=docs-feedback)


Resources
  * [Terms](https://about.gitlab.com/terms/)
  * [Privacy statement](https://about.gitlab.com/privacy/)
  * [Use of generative AI](https://docs.gitlab.com/legal/use_generative_ai/)
  * [Acceptable use of user licenses](https://docs.gitlab.com/legal/licensing_policy/)
  * Cookie Preferences


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fuser%2Fpermissions%2F&_biz_t=1772174517059&_biz_i=Roles%20and%20permissions%20%7C%20GitLab%20Docs&_biz_n=208&rnd=731477&cdn_o=a&_biz_z=1772174517060)
![Company Logo](https://cdn.cookielaw.org/logos/aa14a5c8-79e3-442a-8177-464ad850b19d/e46c1d0d-1f66-481f-bc06-5427671431da/253e6fee-c4c0-4b60-bc35-79cdae5dda32/gitlab-logo-100.png)
## Privacy Preference Center
## Privacy Preference Center
  * ### Your Privacy
  * ### Strictly Necessary Cookies
  * ### Functionality Cookies
  * ### Performance and Analytics Cookies
  * ### Targeting and Advertising Cookies
  * ### Ad User Data
  * ### Ad Personalization


#### Your Privacy
When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. This information might be about you, your preferences or your device and is mostly used to make the site work as you expect it to. The information does not usually directly identify you, but it can give you a more personalized web experience. Because we respect your right to privacy, you can choose not to allow some types of cookies. Click on the different category headings to find out more and change our default settings. However, blocking some types of cookies may impact your experience of the site and the services we are able to offer.
[Cookie Policy](https://about.gitlab.com/privacy/cookies/)
**User ID:** 42fad8d5-ed56-4786-8d74-3c72635252d2
_This User ID will be used as a unique identifier while storing and accessing your preferences for future._
**Timestamp:** --
#### Strictly Necessary Cookies
Always Active
These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, enabling you to securely log into the site, filling in forms, or using the customer checkout. GitLab processes any personal data collected through these cookies on the basis of our legitimate interest.
Cookies Details
#### Functionality Cookies
Functionality Cookies
These cookies enable helpful but non-essential website functions that improve your website experience. By recognizing you when you return to our website, they may, for example, allow us to personalize our content for you or remember your preferences. If you do not allow these cookies then some or all of these services may not function properly. GitLab processes any personal data collected through these cookies on the basis of your consent
Cookies Details
#### Performance and Analytics Cookies
Performance and Analytics Cookies
These cookies allow us and our third-party service providers to recognize and count the number of visitors on our websites and to see how visitors move around our websites when they are using it. This helps us improve our products and ensures that users can easily find what they need on our websites. These cookies usually generate aggregate statistics that are not associated with an individual. To the extent any personal data is collected through these cookies, GitLab processes that data on the basis of your consent.
Cookies Details
#### Targeting and Advertising Cookies
Targeting and Advertising Cookies
These cookies enable different advertising related functions. They may allow us to record information about your visit to our websites, such as pages visited, links followed, and videos viewed so we can make our websites and the advertising displayed on it more relevant to your interests. They may be set through our website by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant advertisements on other websites. GitLab processes any personal data collected through these cookies on the basis of your consent.
Cookies Details
#### Ad User Data
Ad User Data
Sets consent for sending user data to Google for advertising purposes.
Cookies Details
#### Ad Personalization
Ad Personalization
Sets consent for personalized advertising.
Cookies Details
Back Button
### Cookie List
Filter Button
Consent Leg.Interest
checkbox label label
checkbox label label
checkbox label label
Clear
  * checkbox label label


Apply Cancel
Confirm My Choices
Allow All
[![Powered by Onetrust](https://cdn.cookielaw.org/logos/static/powered_by_logo.svg)](https://www.onetrust.com/products/cookie-consent/)
