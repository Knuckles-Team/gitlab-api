[Skip to main content](https://docs.gitlab.com/api/rest/deprecations/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/rest/deprecations/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/rest/deprecations/)
    * [18.8](https://docs.gitlab.com/18.8/api/rest/deprecations/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/rest/deprecations/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/rest/deprecations/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/rest/deprecations.html)
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
  4. [Deprecations and removals](https://docs.gitlab.com/api/rest/deprecations/)


* * *
# REST API deprecations
You should regularly review the following deprecations and make the recommended changes. These deprecations often signal improved API features and recommend using new fields or endpoints for features.
Though some deprecations mention a v5 REST API, no v5 REST API development is active. GitLab will not make these changes within REST API v4, and [follows semantic versioning for the REST API](https://docs.gitlab.com/api/rest/#versioning-and-deprecations).
##  `geo_nodes` API endpoints[](https://docs.gitlab.com/api/rest/deprecations/#geo_nodes-api-endpoints "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/369140).
The [`geo_nodes` API endpoints](https://docs.gitlab.com/api/geo_nodes/) are deprecated and are replaced by [`geo_sites`](https://docs.gitlab.com/api/geo_sites/). It is a part of the global change on [how to refer to Geo deployments](https://docs.gitlab.com/administration/geo/glossary/). Nodes are renamed to sites across the application. The functionality of both endpoints remains the same.
##  `merged_by` API field[](https://docs.gitlab.com/api/rest/deprecations/#merged_by-api-field "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/350534).
The `merged_by` field in the [merge request API](https://docs.gitlab.com/api/merge_requests/#list-merge-requests) has been deprecated in favor of the `merge_user` field which more correctly identifies who merged a merge request when performing actions (set to auto-merge, add to merge train) other than a simple merge.
API users are encouraged to use the new `merge_user` field instead. The `merged_by` field will be removed in v5 of the GitLab REST API.
##  `merge_status` API field[](https://docs.gitlab.com/api/rest/deprecations/#merge_status-api-field "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/382032).
The `merge_status` field in the [merge request API](https://docs.gitlab.com/api/merge_requests/#merge-status) has been deprecated in favor of the `detailed_merge_status` field which more correctly identifies all of the potential statuses that a merge request can be in. API users are encouraged to use the new `detailed_merge_status` field instead. The `merge_status` field will be removed in v5 of the GitLab REST API.
### Null value for `private_profile` attribute in User API[](https://docs.gitlab.com/api/rest/deprecations/#null-value-for-private_profile-attribute-in-user-api "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/387005).
When creating and updating users through the API, `null` was a valid value for the `private_profile` attribute, which would internally be converted to the default value. In v5 of the GitLab REST API, `null` will no longer be a valid value for this parameter, and the response will be a 400 if used. After this change, the only valid values will be `true` and `false`.
## Single merge request changes API endpoint[](https://docs.gitlab.com/api/rest/deprecations/#single-merge-request-changes-api-endpoint "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/322117).
The endpoint to get [changes from a single merge request](https://docs.gitlab.com/api/merge_requests/#retrieve-merge-request-changes) has been deprecated in favor the [list merge request diffs](https://docs.gitlab.com/api/merge_requests/#list-merge-request-diffs) endpoint. API users are encouraged to switch to the new diffs endpoint instead.
The `changes from a single merge request` endpoint will be removed in v5 of the GitLab REST API.
## Managed Licenses API endpoint[](https://docs.gitlab.com/api/rest/deprecations/#managed-licenses-api-endpoint "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/397067).
The endpoint to get all managed licenses for a given project has been deprecated in favor the [License Approval policy](https://docs.gitlab.com/user/compliance/license_approval_policies/) feature.
Users who wish to continue to enforce approvals based on detected licenses are encouraged to create a new [License Approval policy](https://docs.gitlab.com/user/compliance/license_approval_policies/) instead.
The `managed licenses` endpoint will be removed in v5 of the GitLab REST API.
## Approvers and Approver Group fields in Merge Request Approval API[](https://docs.gitlab.com/api/rest/deprecations/#approvers-and-approver-group-fields-in-merge-request-approval-api "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/353097).
The endpoint to get the configuration of approvals for a project returns empty arrays for `approvers` and `approval_groups`. These fields were deprecated in favor of the endpoint to [list all approval rules](https://docs.gitlab.com/api/merge_request_approvals/#list-all-approval-rules-for-a-merge-request) for a merge request. API users are encouraged to switch to this endpoint instead.
These fields will be removed from the `get configuration` endpoint in v5 of the GitLab REST API.
## Runner usage of `active` replaced by `paused`[](https://docs.gitlab.com/api/rest/deprecations/#runner-usage-of-active-replaced-by-paused "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/351109).
Occurrences of the `active` identifier in the GitLab Runner GraphQL API endpoints will be renamed to `paused` in GitLab 16.0.
  * In v4 of the REST API, you can use the `paused` property in place of `active`
  * In v5 of the REST API, this change will affect endpoints taking or returning `active` property, such as:
    * `GET /runners`
    * `GET /runners/all`
    * `GET /runners/:id` / `PUT /runners/:id`
    * `PUT --form "active=false" /runners/:runner_id`
    * `GET /projects/:id/runners` / `POST /projects/:id/runners`
    * `GET /groups/:id/runners`


The 16.0 release of GitLab Runner will start using the `paused` property when registering runners.
## Runner status will not return `paused`[](https://docs.gitlab.com/api/rest/deprecations/#runner-status-will-not-return-paused "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/344648).
In a future v5 of the REST API, the endpoints for GitLab Runner will not return `paused` or `active`.
A runner’s status will only relate to runner contact status, such as: `online`, `offline`, or `not_connected`. Status `paused` or `active` will no longer appear.
When checking if a runner is `paused`, API users are advised to check the boolean attribute `paused` to be `true` instead. When checking if a runner is `active`, check if `paused` is `false`.
## Runner will not return `ip_address`[](https://docs.gitlab.com/api/rest/deprecations/#runner-will-not-return-ip_address "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/415159).
In GitLab 17.0, the [Runners API](https://docs.gitlab.com/api/runners/) will return `""` in place of `ip_address` for runners. In v5 of the REST API, the field will be removed.
##  `default_branch_protection` API field[](https://docs.gitlab.com/api/rest/deprecations/#default_branch_protection-api-field "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/408315).
The `default_branch_protection` field is deprecated in GitLab 17.0 for the following APIs:
  * [New group API](https://docs.gitlab.com/api/groups/#create-a-group).
  * [Update group API](https://docs.gitlab.com/api/groups/#update-group-attributes).
  * [Application Settings API](https://docs.gitlab.com/api/settings/#update-application-settings)


You should use the `default_branch_protection_defaults` field instead, which provides more finer grained control over the default branch protections.
The `default_branch_protection` field will be removed in v5 of the GitLab REST API.
##  `require_password_to_approve` API field[](https://docs.gitlab.com/api/rest/deprecations/#require_password_to_approve-api-field "Permalink")
The `require_password_to_approve` was deprecated in GitLab 16.9. Use the `require_reauthentication_to_approve` field instead. If you supply values to both fields, the `require_reauthentication_to_approve` field takes precedence.
The `require_password_to_approve` field will be removed in v5 of the GitLab REST API.
## Pull mirroring configuration with the projects API endpoint[](https://docs.gitlab.com/api/rest/deprecations/#pull-mirroring-configuration-with-the-projects-api-endpoint "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/494294).
In GitLab 17.6, the [pull mirroring configuration with the Projects API](https://docs.gitlab.com/api/project_pull_mirroring/#update-pull-mirroring-for-a-project-deprecated) is deprecated. It is replaced by a new configuration and endpoint, [`projects/:id/mirror/pull`](https://docs.gitlab.com/api/project_pull_mirroring/#update-project-pull-mirroring-settings).
The previous configuration using the Projects API will be removed in v5 of the GitLab REST API.
##  `restrict_user_defined_variables` parameter with the projects API endpoint[](https://docs.gitlab.com/api/rest/deprecations/#restrict_user_defined_variables-parameter-with-the-projects-api-endpoint "Permalink")
In GitLab 17.7, the [`restrict_user_defined_variables` parameter in Projects API](https://docs.gitlab.com/api/projects/#edit-a-project) is deprecated in favour of using only `ci_pipeline_variables_minimum_override_role`.
To match the same behavior of `restrict_user_defined_variables: false` set `ci_pipeline_variables_minimum_override_role` as `developer`.
##  `namespace` parameter in project import API endpoints[](https://docs.gitlab.com/api/rest/deprecations/#namespace-parameter-in-project-import-api-endpoints "Permalink")
Breaking change. [Related issue](https://gitlab.com/gitlab-org/gitlab/-/issues/511053).
In GitLab 18.7, the `namespace` parameter in the [project import and export API](https://docs.gitlab.com/api/project_import_export/) is deprecated in favor of the `namespace_id` and `namespace_path` parameters. The `namespace` parameter accepted both an ID or path, which caused ambiguity when namespace paths contained only digits.
Instead, you should use:
  * `namespace_id` when specifying a namespace by its numeric ID.
  * `namespace_path` when specifying a namespace by its path.


The `namespace` parameter will be removed in v5 of the GitLab REST API.
Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/deprecations.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/deprecations.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [geo_nodes API endpoints](https://docs.gitlab.com/api/rest/deprecations/#geo_nodes-api-endpoints)
  * [merged_by API field](https://docs.gitlab.com/api/rest/deprecations/#merged_by-api-field)
  * [merge_status API field](https://docs.gitlab.com/api/rest/deprecations/#merge_status-api-field)
  * [Null value for private_profile attribute in User API](https://docs.gitlab.com/api/rest/deprecations/#null-value-for-private_profile-attribute-in-user-api)
  * [Single merge request changes API endpoint](https://docs.gitlab.com/api/rest/deprecations/#single-merge-request-changes-api-endpoint)
  * [Managed Licenses API endpoint](https://docs.gitlab.com/api/rest/deprecations/#managed-licenses-api-endpoint)
  * [Approvers and Approver Group fields in Merge Request Approval API](https://docs.gitlab.com/api/rest/deprecations/#approvers-and-approver-group-fields-in-merge-request-approval-api)
  * [Runner usage of active replaced by paused](https://docs.gitlab.com/api/rest/deprecations/#runner-usage-of-active-replaced-by-paused)
  * [Runner status will not return paused](https://docs.gitlab.com/api/rest/deprecations/#runner-status-will-not-return-paused)
  * [Runner will not return ip_address](https://docs.gitlab.com/api/rest/deprecations/#runner-will-not-return-ip_address)
  * [default_branch_protection API field](https://docs.gitlab.com/api/rest/deprecations/#default_branch_protection-api-field)
  * [require_password_to_approve API field](https://docs.gitlab.com/api/rest/deprecations/#require_password_to_approve-api-field)
  * [Pull mirroring configuration with the projects API endpoint](https://docs.gitlab.com/api/rest/deprecations/#pull-mirroring-configuration-with-the-projects-api-endpoint)
  * [restrict_user_defined_variables parameter with the projects API endpoint](https://docs.gitlab.com/api/rest/deprecations/#restrict_user_defined_variables-parameter-with-the-projects-api-endpoint)
  * [namespace parameter in project import API endpoints](https://docs.gitlab.com/api/rest/deprecations/#namespace-parameter-in-project-import-api-endpoints)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/deprecations.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/deprecations.md)
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
