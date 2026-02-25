[Skip to main content](https://docs.gitlab.com/api/graphql/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/graphql/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/graphql/)
    * [18.8](https://docs.gitlab.com/18.8/api/graphql/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/graphql/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/graphql/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/graphql/index.html)
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
[GraphQL API](https://docs.gitlab.com/api/graphql/)
[Queries and mutations](https://docs.gitlab.com/api/graphql/getting_started/)
[Resources](https://docs.gitlab.com/api/graphql/reference/)
[Examples](https://docs.gitlab.com/api/graphql/examples/)
[Removed items](https://docs.gitlab.com/api/graphql/removed_items/)
[OAuth 2.0 identity provider API](https://docs.gitlab.com/api/oauth2/)
[GitLab Duo CLI (duo)](https://docs.gitlab.com/user/gitlab_duo_cli/)
[GitLab CLI (glab)](https://docs.gitlab.com/cli/)
[Editor and IDE extensions](https://docs.gitlab.com/editor_extensions/)
/
  1. [GitLab Docs](https://docs.gitlab.com/)
  2. [Extend](https://docs.gitlab.com/api/)
  3. [GraphQL API](https://docs.gitlab.com/api/graphql/)


* * *
# GraphQL API
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


[GraphQL](https://graphql.org/) is a query language for APIs. You can use it to request the exact data you need, and therefore limit the number of requests you need.
GraphQL data is arranged in types, so your client can use [client-side GraphQL libraries](https://graphql.org/community/tools-and-libraries/) to consume the API and avoid manual parsing.
The GraphQL API is [versionless](https://graphql.org/learn/schema-design/#versioning).
## Getting started[](https://docs.gitlab.com/api/graphql/#getting-started "Permalink")
If you’re new to the GitLab GraphQL API, see [Get started with GitLab GraphQL API](https://docs.gitlab.com/api/graphql/getting_started/).
You can view the available resources in the [GraphQL API reference](https://docs.gitlab.com/api/graphql/reference/).
The GitLab GraphQL API endpoint is located at `/api/graphql`.
### Interactive GraphQL explorer[](https://docs.gitlab.com/api/graphql/#interactive-graphql-explorer "Permalink")
Explore the GraphQL API using the interactive GraphQL explorer, either:
  * [On GitLab.com](https://gitlab.com/-/graphql-explorer).
  * On GitLab Self-Managed on `https://<your-gitlab-site.com>/-/graphql-explorer`.


For more information, see [GraphiQL](https://docs.gitlab.com/api/graphql/getting_started/#graphiql).
### View GraphQL examples[](https://docs.gitlab.com/api/graphql/#view-graphql-examples "Permalink")
You can work with sample queries that pull data from public projects on GitLab.com:
  * [Create an audit report](https://docs.gitlab.com/api/graphql/audit_report/)
  * [Identify issue boards](https://docs.gitlab.com/api/graphql/sample_issue_boards/)
  * [Query users](https://docs.gitlab.com/api/graphql/users_example/)
  * [Use custom emoji](https://docs.gitlab.com/api/graphql/custom_emoji/)


The [get started](https://docs.gitlab.com/api/graphql/getting_started/) page includes different methods to customize GraphQL queries.
### Authentication[](https://docs.gitlab.com/api/graphql/#authentication "Permalink")
You can access some queries without authentication, but others require authentication. Mutations always require authentication.
You can authenticate by using either a:
  * [Token](https://docs.gitlab.com/api/graphql/#token-authentication)
  * [Session cookie](https://docs.gitlab.com/api/graphql/#session-cookie-authentication)


If the authentication information is not valid, GitLab returns an error message with a status code of `401`:
json
```
{"errors":[{"message":"Invalid token"}]}
```

#### Token authentication[](https://docs.gitlab.com/api/graphql/#token-authentication "Permalink")
Use any of the following tokens to authenticate with the GraphQL API:
  * [OAuth 2.0 tokens](https://docs.gitlab.com/api/oauth2/)
  * [Personal access tokens](https://docs.gitlab.com/user/profile/personal_access_tokens/)
  * [Project access tokens](https://docs.gitlab.com/user/project/settings/project_access_tokens/)
  * [Group access tokens](https://docs.gitlab.com/user/group/settings/group_access_tokens/)


Authenticate with a token by passing it through in a [request header](https://docs.gitlab.com/api/graphql/#header-authentication) or as a [parameter](https://docs.gitlab.com/api/graphql/#parameter-authentication).
Tokens require the correct [scope](https://docs.gitlab.com/api/graphql/#token-scopes).
##### Header authentication[](https://docs.gitlab.com/api/graphql/#header-authentication "Permalink")
Example of token authentication using an `Authorization: Bearer <token>` request header:
shell
```
curl --request POST \
  --url "https://gitlab.com/api/graphql" \
  --header "Authorization: Bearer <token>" \
  --header "Content-Type: application/json" \
  --data "{\"query\": \"query {currentUser {name}}\"}"
```

##### Parameter authentication[](https://docs.gitlab.com/api/graphql/#parameter-authentication "Permalink")
Example of using an OAuth 2.0 token in the `access_token` parameter:
shell
```
curl --request POST \
  --url "https://gitlab.com/api/graphql?access_token=<oauth_token>" \
  --header "Content-Type: application/json" \
  --data "{\"query\": \"query {currentUser {name}}\"}"
```

You can pass in personal, project, or group access tokens using the `private_token` parameter:
shell
```
curl --request POST \
  --url "https://gitlab.com/api/graphql?private_token=<access_token>" \
  --header "Content-Type: application/json" \
  --data "{\"query\": \"query {currentUser {name}}\"}"
```

##### Token scopes[](https://docs.gitlab.com/api/graphql/#token-scopes "Permalink")
Tokens must have the correct scope to access the GraphQL API, either:
Scope | Access
---|---
`read_api` | Grants read access to the API. Sufficient for queries.
`api` | Grants read and write access to the API. Required by mutations.
#### Session cookie authentication[](https://docs.gitlab.com/api/graphql/#session-cookie-authentication "Permalink")
Signing in to the main GitLab application sets a `_gitlab_session` session cookie.
The [interactive GraphQL explorer](https://docs.gitlab.com/api/graphql/#interactive-graphql-explorer) and the web frontend of GitLab itself use this method of authentication.
## Object identifiers[](https://docs.gitlab.com/api/graphql/#object-identifiers "Permalink")
The GitLab GraphQL API uses a mix of identifiers.
[Global IDs](https://docs.gitlab.com/api/graphql/#global-ids), full paths, and internal IDs (IIDs) are all used as arguments in the GitLab GraphQL API, but often a particular part of schema does not accept all of these at the same time.
Although the GitLab GraphQL API has historically not been consistent on this, in general you can expect:
  * If the object is a project, group, or namespace, you use the object’s full path.
  * If an object has an IID, you use a combination of full path and IID.
  * For other objects, you use a [Global ID](https://docs.gitlab.com/api/graphql/#global-ids).


For example, finding a project by its full path `"gitlab-org/gitlab"`:
graphql
```
{
  project(fullPath: "gitlab-org/gitlab") {
    id
    fullPath
  }
}
```

Another example, locking an issue by its project’s full path `"gitlab-org/gitlab"` and the issue’s IID `"1"`:
graphql
```
mutation {
  issueSetLocked(input: { projectPath: "gitlab-org/gitlab", iid: "1", locked: true }) {
    issue {
      id
      iid
    }
  }
}
```

An example of finding a CI runner by its Global ID:
graphql
```
{
  runner(id: "gid://gitlab/Ci::Runner/1") {
    id
  }
}
```

Historically, the GitLab GraphQL API has been inconsistent with typing of full path and IID fields and arguments, but generally:
  * Full path fields and arguments are a GraphQL `ID` type.
  * IID fields and arguments are a GraphQL `String` type.


### Global IDs[](https://docs.gitlab.com/api/graphql/#global-ids "Permalink")
In the GitLab GraphQL API, a field or argument named `id` is nearly always a [Global ID](https://graphql.org/learn/global-object-identification/) and never a database primary key ID. A Global ID in the GitLab GraphQL API begins with `"gid://gitlab/"`. For example, `"gid://gitlab/Issue/123"`.
Global IDs are a convention used for caching and fetching in some client-side libraries.
GitLab Global IDs are subject to change. If changed, the use of the old Global ID as an argument is deprecated and supported according to the [deprecation and breaking change](https://docs.gitlab.com/api/graphql/#breaking-changes) process. You should not expect that a cached Global ID will be valid beyond the time of a GitLab GraphQL deprecation cycle.
## Available top-level queries[](https://docs.gitlab.com/api/graphql/#available-top-level-queries "Permalink")
The top-level entry points for all queries are defined in the [`Query` type](https://docs.gitlab.com/api/graphql/reference/#query-type) in the GraphQL reference.
### Multiplex queries[](https://docs.gitlab.com/api/graphql/#multiplex-queries "Permalink")
GitLab supports batching queries into a single request. For more information, see [Multiplex](https://graphql-ruby.org/queries/multiplex.html).
## Breaking changes[](https://docs.gitlab.com/api/graphql/#breaking-changes "Permalink")
The GitLab GraphQL API is [versionless](https://graphql.org/learn/best-practices/#versioning) and changes to the API are primarily backward-compatible.
However, GitLab sometimes changes the GraphQL API in a way that is not backward-compatible. These changes are considered breaking changes, and can include removing or renaming fields, arguments, or other parts of the schema. When creating a breaking change, GitLab follows a [deprecation and removal process](https://docs.gitlab.com/api/graphql/#deprecation-and-removal-process).
To avoid having a breaking change affect your integrations, you should:
  * Familiarize yourself with the [deprecation and removal process](https://docs.gitlab.com/api/graphql/#deprecation-and-removal-process).
  * Frequently [verify your API calls against the future breaking-change schema](https://docs.gitlab.com/api/graphql/#verify-against-the-future-breaking-change-schema).


For GitLab Self-Managed, [reverting](https://docs.gitlab.com/update/convert_to_ee/revert/) from an EE instance to CE causes breaking changes.
### Breaking change exemptions[](https://docs.gitlab.com/api/graphql/#breaking-change-exemptions "Permalink")
Schema items labeled as experiments in the [GraphQL API reference](https://docs.gitlab.com/api/graphql/reference/) are exempt from the deprecation process. These items can be removed or changed at any time without notice.
Fields behind a feature flag and disabled by default do not follow the deprecation and removal process. These fields can be removed at any time without notice.
GitLab makes all attempts to follow the [deprecation and removal process](https://docs.gitlab.com/api/graphql/#deprecation-and-removal-process). GitLab might make immediate breaking changes to the GraphQL API to patch critical security or performance concerns if the deprecation process would pose significant risk.
### Verify against the future breaking-change schema[](https://docs.gitlab.com/api/graphql/#verify-against-the-future-breaking-change-schema "Permalink")
History
  * [Introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/353642) in GitLab 15.6.


You can make calls against the GraphQL API as if all deprecated items were already removed. This way, you can verify API calls ahead of a [breaking-change release](https://docs.gitlab.com/api/graphql/#deprecation-and-removal-process) before the items are actually removed from the schema.
To make these calls, add a `remove_deprecated=true` query parameter to the GraphQL API endpoint. For example, `https://gitlab.com/api/graphql?remove_deprecated=true` for GraphQL on GitLab.com.
### Deprecation and removal process[](https://docs.gitlab.com/api/graphql/#deprecation-and-removal-process "Permalink")
Parts of the schema marked for removal from the GitLab GraphQL API are first deprecated but still available for at least six releases. They are then removed entirely during the next `XX.0` major release.
Items are marked as deprecated in:
  * The [schema](https://spec.graphql.org/October2021/#sec--deprecated).
  * The [GraphQL API reference](https://docs.gitlab.com/api/graphql/reference/).
  * The [deprecation feature removal schedule](https://docs.gitlab.com/update/deprecations/), which is linked from release posts.
  * Introspection queries of the GraphQL API.


The deprecation message provides an alternative for the deprecated schema item, if applicable.
To avoid experiencing breaking changes, you should remove the deprecated schema from your GraphQL API calls as soon as possible. You should [verify your API calls against the schema without the deprecated schema items](https://docs.gitlab.com/api/graphql/#verify-against-the-future-breaking-change-schema).
#### Deprecation example[](https://docs.gitlab.com/api/graphql/#deprecation-example "Permalink")
The following fields are deprecated in different minor releases, but both removed in GitLab 17.0:
Field deprecated in | Reason
---|---
15.7 | GitLab traditionally has 12 minor releases per major release. To ensure the field is available for 6 more releases, it is removed in the 17.0 major release (and not 16.0).
16.6 | The removal in 17.0 allows for 6 months of availability.
### List of removed items[](https://docs.gitlab.com/api/graphql/#list-of-removed-items "Permalink")
View the [list of items removed](https://docs.gitlab.com/api/graphql/removed_items/) in previous releases.
## Limits[](https://docs.gitlab.com/api/graphql/#limits "Permalink")
The following limits apply to the GitLab GraphQL API.
Limit | Default
---|---
Maximum page size | 100 records (nodes) per page. Applies to most connections in the API. Particular connections may have different max page size limits that are higher or lower.
[Maximum query complexity](https://docs.gitlab.com/api/graphql/#maximum-query-complexity) | 200 for unauthenticated requests and 250 for authenticated requests.
Maximum query size | 10,000 characters per query or mutation. If this limit is reached, use [variables](https://graphql.org/learn/queries/#variables) and [fragments](https://graphql.org/learn/queries/#fragments) to reduce the query or mutation size. Remove white spaces as last resort.
Rate limits | For GitLab.com, see [GitLab.com-specific rate limits](https://docs.gitlab.com/user/gitlab_com/#rate-limits-on-gitlabcom).
[Data limits](https://docs.gitlab.com/api/graphql/#data-limits) | Blob requests are limited to 20 MB when more than one blob path is specified.
Request timeout | 30 seconds.
### Maximum query complexity[](https://docs.gitlab.com/api/graphql/#maximum-query-complexity "Permalink")
The GitLab GraphQL API scores the complexity of a query. Generally, larger queries have a higher complexity score. This limit is designed to protecting the API from performing queries that could negatively impact its overall performance.
You can [query](https://docs.gitlab.com/api/graphql/getting_started/#query-complexity) the complexity score of a query and the limit for the request.
If a query exceeds the complexity limit, an error message response is returned.
In general, each field in a query adds `1` to the complexity score, although this can be higher or lower for particular fields. Sometimes, adding certain arguments may also increase the complexity of a query.
### Data limits[](https://docs.gitlab.com/api/graphql/#data-limits "Permalink")
Blob requests are limited to:
  * A single blob of any size.
  * Multiple blobs with a total size of 20 MB or less.


Blobs larger than 20 MB must be requested individually. This limit applies only when you request fields that contain blob data.
You might need to limit the number of paths in your requests to stay within the data limit. Make a request for the `size` field while excluding the data fields:
gql
```
{
  project(fullPath: "gitlab-org/gitlab") {
    repository {
      blobs(paths: ["big_file.rb", "small_file.rb", "huge_file.rb", ..., etc.], ref: "master") {
        nodes {
          path
          size
        }
      }
    }
  }
}
```

Use the response to calculate the total size and ensure subsequent requests do not exceed the 20 MB data limit.
## Resolve mutations detected as spam[](https://docs.gitlab.com/api/graphql/#resolve-mutations-detected-as-spam "Permalink")
GraphQL mutations can be detected as spam. If a mutation is detected as spam and:
  * A CAPTCHA service is not configured, a [GraphQL top-level error](https://spec.graphql.org/June2018/#sec-Errors) is raised. For example:
json
```
{
  "errors": [
    {
      "message": "Request denied. Spam detected",
      "locations": [ { "line": 6, "column": 7 } ],
      "path": [ "updateSnippet" ],
      "extensions": {
        "spam": true
      }
    }
  ],
  "data": {
    "updateSnippet": {
      "snippet": null
    }
  }
}
```

  * A CAPTCHA service is configured, you receive a response with:
    * `needsCaptchaResponse` set to `true`.
    * The `spamLogId` and `captchaSiteKey` fields set.
For example:
json
```
{
  "errors": [
    {
      "message": "Request denied. Solve CAPTCHA challenge and retry",
      "locations": [ { "line": 6, "column": 7 } ],
      "path": [ "updateSnippet" ],
      "extensions": {
        "needsCaptchaResponse": true,
        "captchaSiteKey": "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
        "spamLogId": 67
      }
    }
  ],
  "data": {
    "updateSnippet": {
      "snippet": null,
    }
  }
}
```

  * Use the `captchaSiteKey` to obtain a CAPTCHA response value using the appropriate CAPTCHA API. Only [Google reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display) is supported.
  * Resubmit the request with the `X-GitLab-Captcha-Response` and `X-GitLab-Spam-Log-Id` headers set.


The GitLab GraphiQL implementation doesn’t permit passing of headers, so the request must be a cURL query. `--data-binary` is used to properly handle escaped double quotes in the JSON-embedded query.
shell
```
export CAPTCHA_RESPONSE="<CAPTCHA response obtained from CAPTCHA service>"
export SPAM_LOG_ID="<spam_log_id obtained from initial REST response>"
curl --request POST \
  --header "Authorization: Bearer $PRIVATE_TOKEN" \
  --header "Content-Type: application/json" \
  --header "X-GitLab-Captcha-Response: $CAPTCHA_RESPONSE" \
  --header "X-GitLab-Spam-Log-Id: $SPAM_LOG_ID" \
  --data-binary '{"query": "mutation {createSnippet(input: {title: \"Title\" visibilityLevel: public blobActions: [ { action: create filePath: \"BlobPath\" content: \"BlobContent\" } ] }) { snippet { id title } errors }}"}' "https://gitlab.example.com/api/graphql"
```

Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/graphql/_index.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/graphql/_index.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Getting started](https://docs.gitlab.com/api/graphql/#getting-started)
  * [Interactive GraphQL explorer](https://docs.gitlab.com/api/graphql/#interactive-graphql-explorer)
  * [View GraphQL examples](https://docs.gitlab.com/api/graphql/#view-graphql-examples)
  * [Authentication](https://docs.gitlab.com/api/graphql/#authentication)
  * [Token authentication](https://docs.gitlab.com/api/graphql/#token-authentication)
  * [Session cookie authentication](https://docs.gitlab.com/api/graphql/#session-cookie-authentication)
  * [Object identifiers](https://docs.gitlab.com/api/graphql/#object-identifiers)
  * [Global IDs](https://docs.gitlab.com/api/graphql/#global-ids)
  * [Available top-level queries](https://docs.gitlab.com/api/graphql/#available-top-level-queries)
  * [Multiplex queries](https://docs.gitlab.com/api/graphql/#multiplex-queries)
  * [Breaking changes](https://docs.gitlab.com/api/graphql/#breaking-changes)
  * [Breaking change exemptions](https://docs.gitlab.com/api/graphql/#breaking-change-exemptions)
  * [Verify against the future breaking-change schema](https://docs.gitlab.com/api/graphql/#verify-against-the-future-breaking-change-schema)
  * [Deprecation and removal process](https://docs.gitlab.com/api/graphql/#deprecation-and-removal-process)
  * [Deprecation example](https://docs.gitlab.com/api/graphql/#deprecation-example)
  * [List of removed items](https://docs.gitlab.com/api/graphql/#list-of-removed-items)
  * [Limits](https://docs.gitlab.com/api/graphql/#limits)
  * [Maximum query complexity](https://docs.gitlab.com/api/graphql/#maximum-query-complexity)
  * [Data limits](https://docs.gitlab.com/api/graphql/#data-limits)
  * [Resolve mutations detected as spam](https://docs.gitlab.com/api/graphql/#resolve-mutations-detected-as-spam)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/graphql/_index.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/graphql/_index.md)
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
