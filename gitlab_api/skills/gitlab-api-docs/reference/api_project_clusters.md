[Skip to main content](https://docs.gitlab.com/api/project_clusters/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/project_clusters/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/project_clusters/)
    * [18.8](https://docs.gitlab.com/18.8/api/project_clusters/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/project_clusters/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/project_clusters/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/project_clusters.html)
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
# Project clusters API (certificate-based) (deprecated)
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


This feature was [deprecated](https://gitlab.com/groups/gitlab-org/configure/-/epics/8) in GitLab 14.5.
Users need the Maintainer or Owner role to use these endpoints.
## List project clusters[](https://docs.gitlab.com/api/project_clusters/#list-project-clusters "Permalink")
Returns a list of project clusters.
```
GET /projects/:id/clusters
```

Parameters:
Attribute | Type | Required | Description
---|---|---|---
`id` | integer or string | yes | The ID or [URL-encoded path of the project](https://docs.gitlab.com/api/rest/#namespaced-paths)
Example request:
shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/projects/26/clusters"
```

Example response:
json
```
[
  {
    "id":18,
    "name":"cluster-1",
    "domain":"example.com",
    "created_at":"2019-01-02T20:18:12.563Z",
    "managed": true,
    "enabled": true,
    "provider_type":"user",
    "platform_type":"kubernetes",
    "environment_scope":"*",
    "cluster_type":"project_type",
    "user":
    {
      "id":1,
      "name":"Administrator",
      "username":"root",
      "state":"active",
      "avatar_url":"https://www.gravatar.com/avatar/4249f4df72b..",
      "web_url":"https://gitlab.example.com/root"
    },
    "platform_kubernetes":
    {
      "api_url":"https://104.197.68.152",
      "namespace":"cluster-1-namespace",
      "authorization_type":"rbac",
      "ca_cert":"-----BEGIN CERTIFICATE-----\r\nhFiK1L61owwDQYJKoZIhvcNAQELBQAw\r\nLzEtMCsGA1UEAxMkZDA1YzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM4ZDBj\r\nMB4XDTE4MTIyNzIwMDM1MVoXDTIzMTIyNjIxMDM1MVowLzEtMCsGA1UEAxMkZDA1\r\nYzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM.......-----END CERTIFICATE-----"
    },
    "management_project":
    {
      "id":2,
      "description":null,
      "name":"project2",
      "name_with_namespace":"John Doe8 / project2",
      "path":"project2",
      "path_with_namespace":"namespace2/project2",
      "created_at":"2019-10-11T02:55:54.138Z"
    }
  },
  {
    "id":19,
    "name":"cluster-2",
    ...
  }
]
```

## Get a single project cluster[](https://docs.gitlab.com/api/project_clusters/#get-a-single-project-cluster "Permalink")
Gets a single project cluster.
```
GET /projects/:id/clusters/:cluster_id
```

Parameters:
Attribute | Type | Required | Description
---|---|---|---
`id` | integer or string | yes | The ID or [URL-encoded path of the project](https://docs.gitlab.com/api/rest/#namespaced-paths)
`cluster_id` | integer | yes | The ID of the cluster
Example request:
shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/projects/26/clusters/18"
```

Example response:
json
```
{
  "id":18,
  "name":"cluster-1",
  "domain":"example.com",
  "created_at":"2019-01-02T20:18:12.563Z",
  "managed": true,
  "enabled": true,
  "provider_type":"user",
  "platform_type":"kubernetes",
  "environment_scope":"*",
  "cluster_type":"project_type",
  "user":
  {
    "id":1,
    "name":"Administrator",
    "username":"root",
    "state":"active",
    "avatar_url":"https://www.gravatar.com/avatar/4249f4df72b..",
    "web_url":"https://gitlab.example.com/root"
  },
  "platform_kubernetes":
  {
    "api_url":"https://104.197.68.152",
    "namespace":"cluster-1-namespace",
    "authorization_type":"rbac",
    "ca_cert":"-----BEGIN CERTIFICATE-----\r\nhFiK1L61owwDQYJKoZIhvcNAQELBQAw\r\nLzEtMCsGA1UEAxMkZDA1YzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM4ZDBj\r\nMB4XDTE4MTIyNzIwMDM1MVoXDTIzMTIyNjIxMDM1MVowLzEtMCsGA1UEAxMkZDA1\r\nYzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM.......-----END CERTIFICATE-----"
  },
  "management_project":
  {
    "id":2,
    "description":null,
    "name":"project2",
    "name_with_namespace":"John Doe8 / project2",
    "path":"project2",
    "path_with_namespace":"namespace2/project2",
    "created_at":"2019-10-11T02:55:54.138Z"
  },
  "project":
  {
    "id":26,
    "description":"",
    "name":"project-with-clusters-api",
    "name_with_namespace":"Administrator / project-with-clusters-api",
    "path":"project-with-clusters-api",
    "path_with_namespace":"root/project-with-clusters-api",
    "created_at":"2019-01-02T20:13:32.600Z",
    "default_branch":null,
    "tag_list":[], //deprecated, use `topics` instead
    "topics":[],
    "ssh_url_to_repo":"ssh://gitlab.example.com/root/project-with-clusters-api.git",
    "http_url_to_repo":"https://gitlab.example.com/root/project-with-clusters-api.git",
    "web_url":"https://gitlab.example.com/root/project-with-clusters-api",
    "readme_url":null,
    "avatar_url":null,
    "star_count":0,
    "forks_count":0,
    "last_activity_at":"2019-01-02T20:13:32.600Z",
    "namespace":
    {
      "id":1,
      "name":"root",
      "path":"root",
      "kind":"user",
      "full_path":"root",
      "parent_id":null
    }
  }
}
```

## Add existing cluster to project[](https://docs.gitlab.com/api/project_clusters/#add-existing-cluster-to-project "Permalink")
Adds an existing Kubernetes cluster to the project.
```
POST /projects/:id/clusters/user
```

Parameters:
Attribute | Type | Required | Description
---|---|---|---
`id` | integer or string | yes | The ID or [URL-encoded path of the project](https://docs.gitlab.com/api/rest/#namespaced-paths)
`name` | string | yes | The name of the cluster
`domain` | string | no | The [base domain](https://docs.gitlab.com/user/project/clusters/gitlab_managed_clusters/#base-domain) of the cluster
`management_project_id` | integer | no | The ID of the [management project](https://docs.gitlab.com/user/clusters/management_project/) for the cluster
`enabled` | boolean | no | Determines if cluster is active or not, defaults to `true`
`managed` | boolean | no | Determines if GitLab manages namespaces and service accounts for this cluster. Defaults to `true`
`platform_kubernetes_attributes[api_url]` | string | yes | The URL to access the Kubernetes API
`platform_kubernetes_attributes[token]` | string | yes | The token to authenticate against Kubernetes
`platform_kubernetes_attributes[ca_cert]` | string | no | TLS certificate. Required if API is using a self-signed TLS certificate.
`platform_kubernetes_attributes[namespace]` | string | no | The unique namespace related to the project
`platform_kubernetes_attributes[authorization_type]` | string | no | The cluster authorization type: `rbac`, `abac` or `unknown_authorization`. Defaults to `rbac`.
`environment_scope` | string | no | The associated environment to the cluster. Defaults to `*`. Premium and Ultimate only.
Example request:
shell
```
curl --request POST \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --header "Accept: application/json" \
  --header "Content-Type:application/json" \
  --data '{"name":"cluster-5", "platform_kubernetes_attributes":{"api_url":"https://35.111.51.20","token":"12345","namespace":"cluster-5-namespace","ca_cert":"-----BEGIN CERTIFICATE-----\r\nhFiK1L61owwDQYJKoZIhvcNAQELBQAw\r\nLzEtMCsGA1UEAxMkZDA1YzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM4ZDBj\r\nMB4XDTE4MTIyNzIwMDM1MVoXDTIzMTIyNjIxMDM1MVowLzEtMCsGA1UEAxMkZDA1\r\nYzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM.......-----END CERTIFICATE-----"}}' \
  --url "https://gitlab.example.com/api/v4/projects/26/clusters/user"
```

Example response:
json
```
{
  "id":24,
  "name":"cluster-5",
  "created_at":"2019-01-03T21:53:40.610Z",
  "managed": true,
  "enabled": true,
  "provider_type":"user",
  "platform_type":"kubernetes",
  "environment_scope":"*",
  "cluster_type":"project_type",
  "user":
  {
    "id":1,
    "name":"Administrator",
    "username":"root",
    "state":"active",
    "avatar_url":"https://www.gravatar.com/avatar/4249f4df72b..",
    "web_url":"https://gitlab.example.com/root"
  },
  "platform_kubernetes":
  {
    "api_url":"https://35.111.51.20",
    "namespace":"cluster-5-namespace",
    "authorization_type":"rbac",
    "ca_cert":"-----BEGIN CERTIFICATE-----\r\nhFiK1L61owwDQYJKoZIhvcNAQELBQAw\r\nLzEtMCsGA1UEAxMkZDA1YzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM4ZDBj\r\nMB4XDTE4MTIyNzIwMDM1MVoXDTIzMTIyNjIxMDM1MVowLzEtMCsGA1UEAxMkZDA1\r\nYzQ1YjctNzdiMS00NDY0LThjNmEtMTQ0ZDJkZjM.......-----END CERTIFICATE-----"
  },
  "management_project":null,
  "project":
  {
    "id":26,
    "description":"",
    "name":"project-with-clusters-api",
    "name_with_namespace":"Administrator / project-with-clusters-api",
    "path":"project-with-clusters-api",
    "path_with_namespace":"root/project-with-clusters-api",
    "created_at":"2019-01-02T20:13:32.600Z",
    "default_branch":null,
    "tag_list":[], //deprecated, use `topics` instead
    "topics":[],
    "ssh_url_to_repo":"ssh:://gitlab.example.com/root/project-with-clusters-api.git",
    "http_url_to_repo":"https://gitlab.example.com/root/project-with-clusters-api.git",
    "web_url":"https://gitlab.example.com/root/project-with-clusters-api",
    "readme_url":null,
    "avatar_url":null,
    "star_count":0,
    "forks_count":0,
    "last_activity_at":"2019-01-02T20:13:32.600Z",
    "namespace":
    {
      "id":1,
      "name":"root",
      "path":"root",
      "kind":"user",
      "full_path":"root",
      "parent_id":null
    }
  }
}
```

## Edit project cluster[](https://docs.gitlab.com/api/project_clusters/#edit-project-cluster "Permalink")
Updates an existing project cluster.
```
PUT /projects/:id/clusters/:cluster_id
```

Parameters:
Attribute | Type | Required | Description
---|---|---|---
`id` | integer or string | yes | The ID or [URL-encoded path of the project](https://docs.gitlab.com/api/rest/#namespaced-paths)
`cluster_id` | integer | yes | The ID of the cluster
`name` | string | no | The name of the cluster
`domain` | string | no | The [base domain](https://docs.gitlab.com/user/project/clusters/gitlab_managed_clusters/#base-domain) of the cluster
`management_project_id` | integer | no | The ID of the [management project](https://docs.gitlab.com/user/clusters/management_project/) for the cluster
`enabled` | boolean | no | Determines if cluster is active or not
`managed` | boolean | no | Determines if GitLab manages namespaces and service accounts for this cluster
`platform_kubernetes_attributes[api_url]` | string | no | The URL to access the Kubernetes API
`platform_kubernetes_attributes[token]` | string | no | The token to authenticate against Kubernetes
`platform_kubernetes_attributes[ca_cert]` | string | no | TLS certificate. Required if API is using a self-signed TLS certificate.
`platform_kubernetes_attributes[namespace]` | string | no | The unique namespace related to the project
`environment_scope` | string | no | The associated environment to the cluster
`name`, `api_url`, `ca_cert` and `token` can only be updated if the cluster was added through the [“Add existing Kubernetes cluster”](https://docs.gitlab.com/user/project/clusters/add_existing_cluster/) option or through the [“Add existing cluster to project”](https://docs.gitlab.com/api/project_clusters/#add-existing-cluster-to-project) endpoint.
Example request:
shell
```
curl --request PUT \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --header "Content-Type:application/json" \
  --data '{"name":"new-cluster-name","domain":"new-domain.com","api_url":"https://new-api-url.com"}' \
  --url "https://gitlab.example.com/api/v4/projects/26/clusters/24"
```

Example response:
json
```
{
  "id":24,
  "name":"new-cluster-name",
  "domain":"new-domain.com",
  "created_at":"2019-01-03T21:53:40.610Z",
  "managed": true,
  "enabled": true,
  "provider_type":"user",
  "platform_type":"kubernetes",
  "environment_scope":"*",
  "cluster_type":"project_type",
  "user":
  {
    "id":1,
    "name":"Administrator",
    "username":"root",
    "state":"active",
    "avatar_url":"https://www.gravatar.com/avatar/4249f4df72b..",
    "web_url":"https://gitlab.example.com/root"
  },
  "platform_kubernetes":
  {
    "api_url":"https://new-api-url.com",
    "namespace":"cluster-5-namespace",
    "authorization_type":"rbac",
    "ca_cert":null
  },
  "management_project":
  {
    "id":2,
    "description":null,
    "name":"project2",
    "name_with_namespace":"John Doe8 / project2",
    "path":"project2",
    "path_with_namespace":"namespace2/project2",
    "created_at":"2019-10-11T02:55:54.138Z"
  },
  "project":
  {
    "id":26,
    "description":"",
    "name":"project-with-clusters-api",
    "name_with_namespace":"Administrator / project-with-clusters-api",
    "path":"project-with-clusters-api",
    "path_with_namespace":"root/project-with-clusters-api",
    "created_at":"2019-01-02T20:13:32.600Z",
    "default_branch":null,
    "tag_list":[], //deprecated, use `topics` instead
    "topics":[],
    "ssh_url_to_repo":"ssh:://gitlab.example.com/root/project-with-clusters-api.git",
    "http_url_to_repo":"https://gitlab.example.com/root/project-with-clusters-api.git",
    "web_url":"https://gitlab.example.com/root/project-with-clusters-api",
    "readme_url":null,
    "avatar_url":null,
    "star_count":0,
    "forks_count":0,
    "last_activity_at":"2019-01-02T20:13:32.600Z",
    "namespace":
    {
      "id":1,
      "name":"root",
      "path":"root",
      "kind":"user",
      "full_path":"root",
      "parent_id":null
    }
  }
}
```

## Delete project cluster[](https://docs.gitlab.com/api/project_clusters/#delete-project-cluster "Permalink")
Deletes an existing project cluster. Does not remove existing resources within the connected Kubernetes cluster.
```
DELETE /projects/:id/clusters/:cluster_id
```

Parameters:
Attribute | Type | Required | Description
---|---|---|---
`id` | integer or string | yes | The ID or [URL-encoded path of the project](https://docs.gitlab.com/api/rest/#namespaced-paths)
`cluster_id` | integer | yes | The ID of the cluster
Example request:
shell
```
curl --request DELETE \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/projects/26/clusters/23"
```

Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/project_clusters.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/project_clusters.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [List project clusters](https://docs.gitlab.com/api/project_clusters/#list-project-clusters)
  * [Get a single project cluster](https://docs.gitlab.com/api/project_clusters/#get-a-single-project-cluster)
  * [Add existing cluster to project](https://docs.gitlab.com/api/project_clusters/#add-existing-cluster-to-project)
  * [Edit project cluster](https://docs.gitlab.com/api/project_clusters/#edit-project-cluster)
  * [Delete project cluster](https://docs.gitlab.com/api/project_clusters/#delete-project-cluster)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/project_clusters.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/project_clusters.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fproject_clusters%2F&_biz_t=1771981656785&_biz_i=Project%20clusters%20API%20\(certificate-based\)%20\(deprecated\)%20%7C%20GitLab%20Docs&_biz_n=136&rnd=969772&cdn_o=a&_biz_z=1771981656786)
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
**User ID:** d8a8ce5a-8fe2-4380-9852-3ffbac7eb562
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
