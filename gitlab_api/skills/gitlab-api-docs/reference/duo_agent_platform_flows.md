[Skip to main content](https://docs.gitlab.com/api/duo_agent_platform_flows/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/duo_agent_platform_flows/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/duo_agent_platform_flows/)
    * [18.8](https://docs.gitlab.com/18.8/api/duo_agent_platform_flows/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/duo_agent_platform_flows/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/duo_agent_platform_flows/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/duo_agent_platform_flows.html)
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
/
  1. [GitLab Docs](https://docs.gitlab.com/)


* * *
# Duo Agent Platform flows API
  * Tier: Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


Use this API to create and manage [flows](https://docs.gitlab.com/user/duo_agent_platform/flows/) in the [GitLab Duo Agent Platform](https://docs.gitlab.com/user/duo_agent_platform/). Flows are combinations of AI agents that work together to complete developer tasks, such as fixing bugs, writing code, or resolving vulnerabilities.
## Create a flow[](https://docs.gitlab.com/api/duo_agent_platform_flows/#create-a-flow "Permalink")
  * Status: Experiment


Creates and starts a new flow.
```
POST /ai/duo_workflows/workflows
```

Supported attributes:
Attribute | Type | Required | Description
---|---|---|---
`additional_context` | array of objects | No | Additional context for the flow. Each element must be an object with at minimum a `Category` (string) and `Content` (string, serialized JSON) key.
`agent_privileges` | integer array | No | Privilege IDs the agent is allowed to use. Defaults to all privileges. See [List all agent privileges](https://docs.gitlab.com/api/duo_agent_platform_flows/#list-all-agent-privileges).
`ai_catalog_item_consumer_id` | integer | No | ID of the AI Catalog item consumer that configures which catalog item to execute. Requires `project_id`. Cannot be used with `workflow_definition`; if both are provided, `ai_catalog_item_consumer_id` takes precedence. See [Look up the consumer ID](https://docs.gitlab.com/api/duo_agent_platform_flows/#look-up-the-consumer-id).
`ai_catalog_item_version_id` | integer | No | ID of the AI Catalog item version that sourced the flow configuration.
`allow_agent_to_request_user` | boolean | No | When `true` (default), the agent may pause to ask the user questions before proceeding. When `false`, the agent runs to completion without user input.
`environment` | string | No | Execution environment. One of: `ide`, `web`, `chat_partial`, `chat`, `ambient`.
`goal` | string | No | Description of the task for the agent to complete. Example: `Fix the failing pipeline`.
`image` | string | No | Container image to use when running the flow in a CI pipeline. Must meet the [custom image requirements](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/#custom-image-requirements). Example: `registry.gitlab.com/gitlab-org/duo-workflow/custom-image:latest`.
`issue_id` | integer | No | IID of the issue to associate the flow with. Requires `project_id`.
`merge_request_id` | integer | No | IID of the merge request to associate the flow with. Requires `project_id`.
`namespace_id` | string | No | ID or path of the namespace to associate the flow with.
`pre_approved_agent_privileges` | integer array | No | Privilege IDs the agent can use without asking for user approval. Must be a subset of `agent_privileges`.
`project_id` | string | No | ID or path of the project to associate the flow with.
`shallow_clone` | boolean | No | Whether to use a shallow clone of the repository during execution. Default: `true`.
`source_branch` | string | No | Source branch for the CI pipeline. Defaults to the project’s default branch.
`start_workflow` | boolean | No | When `true`, starts the flow immediately after creation.
`workflow_definition` | string | No | Flow type identifier. Example: `developer/v1`. Cannot be used with `ai_catalog_item_consumer_id`; if both are provided, `ai_catalog_item_consumer_id` takes precedence.
If successful, returns [`201 Created`](https://docs.gitlab.com/api/rest/troubleshooting/#status-codes) and the following response attributes:
Attribute | Type | Description
---|---|---
`agent_privileges` | integer array | Privilege IDs assigned to the agent.
`agent_privileges_names` | string array | Names corresponding to `agent_privileges`.
`ai_catalog_item_version_id` | integer | ID of the AI Catalog item version. `null` if not set.
`allow_agent_to_request_user` | boolean | When `true`, the agent may pause for user input.
`environment` | string | Execution environment. `null` if not set.
`gitlab_url` | string | Base URL of the GitLab instance.
`id` | integer | ID of the flow.
`image` | string | Container image for CI pipeline execution. `null` if not set.
`mcp_enabled` | boolean | Whether `MCP` (Model Context Protocol) tools are enabled for this flow.
`namespace_id` | integer | ID of the associated namespace. `null` if not set.
`pre_approved_agent_privileges` | integer array | Privilege IDs the agent can use without asking for approval.
`pre_approved_agent_privileges_names` | string array | Names corresponding to `pre_approved_agent_privileges`.
`project_id` | integer | ID of the associated project. `null` if not set.
`status` | string | Current flow status. One of `created`, `running`, `paused`, `finished`, `failed`, `stopped`, `input_required`, `plan_approval_required`, or `tool_call_approval_required`.
`workflow_definition` | string | Flow type identifier.
`workload` | object | Information about the workload.
`workload.id` | string | ID of the workload.
`workload.message` | string | Status message for the workload.
### Look up the consumer ID[](https://docs.gitlab.com/api/duo_agent_platform_flows/#look-up-the-consumer-id "Permalink")
Before you can use `ai_catalog_item_consumer_id`, you must use the GraphQL API to retrieve the ID from the [AI Catalog](https://docs.gitlab.com/user/duo_agent_platform/ai_catalog/). The item must already be enabled for the project.
graphql
```
query {
  aiCatalogConfiguredItems(projectId: "gid://gitlab/Project/<project_id>") {
    nodes {
      id
      item { name }
    }
  }
}
```

The `id` field is a Global ID in the format `gid://gitlab/AiCatalogItemConsumer/<numeric_id>`. Use the numeric suffix as the `ai_catalog_item_consumer_id` value.
Example request using a built-in flow type:
shell
```
curl --request POST \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --header "Content-Type: application/json" \
  --data '{
    "project_id": "5",
    "goal": "Fix the failing pipeline by correcting the syntax error in .gitlab-ci.yml",
    "workflow_definition": "developer/v1",
    "start_workflow": true
  }' \
  --url "https://gitlab.example.com/api/v4/ai/duo_workflows/workflows"
```

Example request using a catalog-configured flow:
shell
```
curl --request POST \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --header "Content-Type: application/json" \
  --data '{
    "project_id": "5",
    "goal": "Fix the failing pipeline by correcting the syntax error in .gitlab-ci.yml",
    "ai_catalog_item_consumer_id": 12,
    "start_workflow": true
  }' \
  --url "https://gitlab.example.com/api/v4/ai/duo_workflows/workflows"
```

Example response:
json
```
{
  "id": 1,
  "project_id": 5,
  "namespace_id": null,
  "agent_privileges": [1, 2, 3, 4, 5, 6],
  "agent_privileges_names": [
    "read_write_files",
    "read_only_gitlab",
    "read_write_gitlab",
    "run_commands",
    "use_git",
    "run_mcp_tools"
  ],
  "pre_approved_agent_privileges": [],
  "pre_approved_agent_privileges_names": [],
  "workflow_definition": "developer/v1",
  "status": "running",
  "allow_agent_to_request_user": true,
  "image": null,
  "environment": null,
  "ai_catalog_item_version_id": null,
  "workload": {
    "id": "abc-123",
    "message": "Workflow started"
  },
  "mcp_enabled": false,
  "gitlab_url": "https://gitlab.example.com"
}
```

## List all agent privileges[](https://docs.gitlab.com/api/duo_agent_platform_flows/#list-all-agent-privileges "Permalink")
Lists all available agent privileges with their IDs, names, descriptions, and whether each is enabled by default.
```
GET /ai/duo_workflows/workflows/agent_privileges
```

This endpoint has no supported attributes.
If successful, returns [`200 OK`](https://docs.gitlab.com/api/rest/troubleshooting/#status-codes) and the following response attributes:
Attribute | Type | Description
---|---|---
`all_privileges` | array of objects | All available agent privileges.
`all_privileges[].default_enabled` | boolean | Whether the privilege is enabled by default.
`all_privileges[].description` | string | Human-readable description of what the privilege permits.
`all_privileges[].id` | integer | Privilege ID.
`all_privileges[].name` | string | Machine-readable privilege name.
Example request:
shell
```
curl --header "PRIVATE-TOKEN: <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/ai/duo_workflows/workflows/agent_privileges"
```

Example response:
json
```
{
  "all_privileges": [
    {
      "id": 1,
      "name": "read_write_files",
      "description": "Allow local filesystem read/write access",
      "default_enabled": true
    },
    {
      "id": 2,
      "name": "read_only_gitlab",
      "description": "Allow read only access to GitLab APIs",
      "default_enabled": true
    },
    {
      "id": 3,
      "name": "read_write_gitlab",
      "description": "Allow write access to GitLab APIs",
      "default_enabled": true
    },
    {
      "id": 4,
      "name": "run_commands",
      "description": "Allow running any commands",
      "default_enabled": true
    },
    {
      "id": 5,
      "name": "use_git",
      "description": "Allow git commits, push and other git commands",
      "default_enabled": true
    },
    {
      "id": 6,
      "name": "run_mcp_tools",
      "description": "Allow running MCP tools",
      "default_enabled": true
    }
  ]
}
```

Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/duo_agent_platform_flows.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/duo_agent_platform_flows.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Create a flow](https://docs.gitlab.com/api/duo_agent_platform_flows/#create-a-flow)
  * [Look up the consumer ID](https://docs.gitlab.com/api/duo_agent_platform_flows/#look-up-the-consumer-id)
  * [List all agent privileges](https://docs.gitlab.com/api/duo_agent_platform_flows/#list-all-agent-privileges)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/duo_agent_platform_flows.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/duo_agent_platform_flows.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fduo_agent_platform_flows%2F&_biz_t=1772174256190&_biz_i=Duo%20Agent%20Platform%20flows%20API%20%7C%20GitLab%20Docs&_biz_n=38&rnd=32168&cdn_o=a&_biz_z=1772174256191)
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
