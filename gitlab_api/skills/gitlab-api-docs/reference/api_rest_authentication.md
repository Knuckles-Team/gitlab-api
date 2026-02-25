[Skip to main content](https://docs.gitlab.com/api/rest/authentication/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/rest/authentication/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/rest/authentication/)
    * [18.8](https://docs.gitlab.com/18.8/api/rest/authentication/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/rest/authentication/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/rest/authentication/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/rest/authentication.html)
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
[Getting started](https://docs.gitlab.com/api/get_started/get_started_extending/)
[Tutorials](https://docs.gitlab.com/tutorials/develop/)
[Integrations](https://docs.gitlab.com/integration/)
[Webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/)
[REST API](https://docs.gitlab.com/api/rest/)
[Resources](https://docs.gitlab.com/api/api_resources/)
[Authentication](https://docs.gitlab.com/api/rest/authentication/)
[Third-party clients](https://docs.gitlab.com/api/rest/third_party_clients/)
[Deprecations and removals](https://docs.gitlab.com/api/rest/deprecations/)
[OpenAPI](https://docs.gitlab.com/api/openapi/openapi_interactive/)
[Automate storage management](https://docs.gitlab.com/user/storage_management_automation/)
[Troubleshooting](https://docs.gitlab.com/api/rest/troubleshooting/)
[GraphQL API](https://docs.gitlab.com/api/graphql/)
[OAuth 2.0 identity provider API](https://docs.gitlab.com/api/oauth2/)
[GitLab Duo CLI (duo)](https://docs.gitlab.com/user/gitlab_duo_cli/)
[GitLab CLI (glab)](https://docs.gitlab.com/cli/)
[Editor and IDE extensions](https://docs.gitlab.com/editor_extensions/)
/
  1. [GitLab Docs](https://docs.gitlab.com/)
  2. [Extend](https://docs.gitlab.com/api/)
  3. [REST API](https://docs.gitlab.com/api/rest/)
  4. [Authentication](https://docs.gitlab.com/api/rest/authentication/)


* * *
# REST API authentication
Most API requests require authentication, or return only public data when authentication isn’t provided. When authentication is not required, the documentation for each endpoint specifies this. For example, the [`/projects/:id` endpoint](https://docs.gitlab.com/api/projects/#retrieve-a-project) does not require authentication.
You can authenticate with the GitLab REST API in several ways:
  * [OAuth 2.0 tokens](https://docs.gitlab.com/api/rest/authentication/#oauth-20-tokens)
  * [Personal access tokens](https://docs.gitlab.com/user/profile/personal_access_tokens/)
  * [Project access tokens](https://docs.gitlab.com/user/project/settings/project_access_tokens/)
  * [Group access tokens](https://docs.gitlab.com/user/group/settings/group_access_tokens/)
  * [Session cookie](https://docs.gitlab.com/api/rest/authentication/#session-cookie)
  * [CI/CD job tokens](https://docs.gitlab.com/api/rest/authentication/#job-tokens) (specific endpoints only)


Project access tokens are supported by:
  * GitLab Self-Managed: Free, Premium, and Ultimate.
  * GitLab.com: Premium and Ultimate.


If you are an administrator, you or your application can authenticate as a specific user, using either:
  * [Impersonation tokens](https://docs.gitlab.com/api/rest/authentication/#impersonation-tokens)
  * [Sudo](https://docs.gitlab.com/api/rest/authentication/#sudo)


If authentication information is not valid or is missing, GitLab returns an error message with a status code of `401`:
json
```
{
  "message": "401 Unauthorized"
}
```

Deploy tokens can’t be used with the GitLab public API. For details, see [Deploy Tokens](https://docs.gitlab.com/user/project/deploy_tokens/).
## OAuth 2.0 tokens[](https://docs.gitlab.com/api/rest/authentication/#oauth-20-tokens "Permalink")
You can use an [OAuth 2.0 token](https://docs.gitlab.com/api/oauth2/) to authenticate with the API by passing it in either the `access_token` parameter or the `Authorization` header.
Example of using the OAuth 2.0 token in a parameter:
shell
```
curl --request GET \
  --url "https://gitlab.example.com/api/v4/projects?access_token=OAUTH-TOKEN"
```

Example of using the OAuth 2.0 token in a header:
shell
```
curl --request GET \
  --header "Authorization: Bearer OAUTH-TOKEN" \
  --url "https://gitlab.example.com/api/v4/projects"
```

Read more about [GitLab as an OAuth 2.0 provider](https://docs.gitlab.com/api/oauth2/).
All OAuth access tokens are valid for two hours after they are created. You can use the `refresh_token` parameter to refresh tokens. See [OAuth 2.0 token](https://docs.gitlab.com/api/oauth2/) documentation for how to request a new access token using a refresh token.
## Personal, project, and group access tokens[](https://docs.gitlab.com/api/rest/authentication/#personal-project-and-group-access-tokens "Permalink")
You can use access tokens to authenticate with the API. Pass the token using the `PRIVATE-TOKEN` header (recommended) or other methods.
For example, using the recommended header method:
shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/projects"
```

You can also use personal, project, or group access tokens with OAuth-compliant headers. For example:
shell
```
curl --request GET \
  --header "Authorization: Bearer <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/projects"
```

## Job tokens[](https://docs.gitlab.com/api/rest/authentication/#job-tokens "Permalink")
You can use job tokens to authenticate with [specific API endpoints](https://docs.gitlab.com/ci/jobs/ci_job_token/#job-token-access). In GitLab CI/CD jobs, the token is available as the `CI_JOB_TOKEN` variable.
Pass the token using the `JOB-TOKEN` header (recommended) or other methods. For all authentication methods, see [CI/CD job token authentication](https://docs.gitlab.com/ci/jobs/ci_job_token/#rest-api-authentication).
For example, using the header method:
shell
```
curl --request GET \
  --header "JOB-TOKEN: $CI_JOB_TOKEN" \
  --url "https://gitlab.example.com/api/v4/projects/1/releases"
```

## Session cookie[](https://docs.gitlab.com/api/rest/authentication/#session-cookie "Permalink")
Signing in to the main GitLab application sets a `_gitlab_session` cookie. The API uses this cookie for authentication if it’s present. Using the API to generate a new session cookie isn’t supported.
The primary user of this authentication method is the web frontend of GitLab itself. The web frontend can use the API as the authenticated user to get a list of projects without explicitly passing an access token.
## Impersonation tokens[](https://docs.gitlab.com/api/rest/authentication/#impersonation-tokens "Permalink")
Impersonation tokens are a type of [personal access token](https://docs.gitlab.com/user/profile/personal_access_tokens/). They can be created only by an administrator, and are used to authenticate with the API as a specific user.
Use impersonation tokens as an alternative to:
  * The user’s password or one of their personal access tokens.
  * The [Sudo](https://docs.gitlab.com/api/rest/authentication/#sudo) feature. The user’s or administrator’s password or token may not be known, or may change over time.


For more details, see the [User tokens API](https://docs.gitlab.com/api/user_tokens/#create-an-impersonation-token) documentation.
Impersonation tokens are used exactly like regular personal access tokens, and can be passed in either the `private_token` parameter or the `PRIVATE-TOKEN` header.
### Disable impersonation[](https://docs.gitlab.com/api/rest/authentication/#disable-impersonation "Permalink")
By default, impersonation is enabled. To disable impersonation:
  * [Linux package (Omnibus)](https://docs.gitlab.com/api/rest/authentication/)
  * [Self-compiled (source)](https://docs.gitlab.com/api/rest/authentication/)


  1. Edit the `/etc/gitlab/gitlab.rb` file:
ruby
```
gitlab_rails['impersonation_enabled'] = false
```

  2. Save the file, and then [reconfigure](https://docs.gitlab.com/administration/restart_gitlab/#reconfigure-a-linux-package-installation) GitLab for the changes to take effect.


  1. Edit the `config/gitlab.yml` file:
yaml
```
gitlab:
  impersonation_enabled: false
```

  2. Save the file, and then [restart](https://docs.gitlab.com/administration/restart_gitlab/#self-compiled-installations) GitLab for the changes to take effect.


To re-enable impersonation, remove this configuration and reconfigure GitLab (Linux package installations) or restart GitLab (self-compiled installations).
## Sudo[](https://docs.gitlab.com/api/rest/authentication/#sudo "Permalink")
All API requests support performing an API request as if you were another user, provided you’re authenticated as an administrator with an OAuth or personal access token that has the `sudo` scope. The API requests are executed with the permissions of the impersonated user.
As an [administrator](https://docs.gitlab.com/user/permissions/), pass the `sudo` parameter either by using query string or a header with an ID or username (case-insensitive) of the user you want to perform the operation as. If passed as a header, the header name must be `Sudo`.
If a non administrative access token is provided, GitLab returns an error message with a status code of `403`:
json
```
{
  "message": "403 Forbidden - Must be admin to use sudo"
}
```

If an access token without the `sudo` scope is provided, an error message is returned with a status code of `403`:
json
```
{
  "error": "insufficient_scope",
  "error_description": "The request requires higher privileges than provided by the access token.",
  "scope": "sudo"
}
```

If the sudo user ID or username cannot be found, an error message is returned with a status code of `404`:
json
```
{
  "message": "404 User with ID or username '123' Not Found"
}
```

Example of a valid API request and a request using cURL with sudo request, providing a username:
```
GET /projects?private_token=<your_access_token>&sudo=username
```

shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --header "Sudo: username" \
  --url "https://gitlab.example.com/api/v4/projects"
```

Example of a valid API request and a request using cURL with sudo request, providing an ID:
```
GET /projects?private_token=<your_access_token>&sudo=23
```

shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: <your_access_token>" \
  --header "Sudo: 23" \
  --url "https://gitlab.example.com/api/v4/projects"
```

Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/authentication.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/authentication.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [OAuth 2.0 tokens](https://docs.gitlab.com/api/rest/authentication/#oauth-20-tokens)
  * [Personal, project, and group access tokens](https://docs.gitlab.com/api/rest/authentication/#personal-project-and-group-access-tokens)
  * [Job tokens](https://docs.gitlab.com/api/rest/authentication/#job-tokens)
  * [Session cookie](https://docs.gitlab.com/api/rest/authentication/#session-cookie)
  * [Impersonation tokens](https://docs.gitlab.com/api/rest/authentication/#impersonation-tokens)
  * [Disable impersonation](https://docs.gitlab.com/api/rest/authentication/#disable-impersonation)
  * [Sudo](https://docs.gitlab.com/api/rest/authentication/#sudo)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/authentication.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/authentication.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Frest%2F&_biz_t=1771981684435&_biz_i=REST%20API%20%7C%20GitLab%20Docs&_biz_n=150&rnd=862039&cdn_o=a&_biz_z=1771981684602)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Frest%2Fdeprecations%2F&_biz_t=1771981684506&_biz_i=REST%20API%20deprecations%20%7C%20GitLab%20Docs&_biz_n=151&rnd=977028&cdn_o=a&_biz_z=1771981684603)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Frest%2Fauthentication%2F&_biz_t=1771981684602&_biz_i=REST%20API%20authentication%20%7C%20GitLab%20Docs&_biz_n=152&rnd=174098&cdn_o=a&_biz_z=1771981684603)
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
