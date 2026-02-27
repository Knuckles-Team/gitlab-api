[Skip to main content](https://docs.gitlab.com/api/get_started/get_started_extending/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/get_started/get_started_extending/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/get_started/get_started_extending/)
    * [18.8](https://docs.gitlab.com/18.8/api/get_started/get_started_extending/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/get_started/get_started_extending/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/get_started/get_started_extending/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/get_started/get_started_extending.html)
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
[OAuth 2.0 identity provider API](https://docs.gitlab.com/api/oauth2/)
[GitLab Duo CLI (duo)](https://docs.gitlab.com/user/gitlab_duo_cli/)
[GitLab CLI (glab)](https://docs.gitlab.com/cli/)
[Editor and IDE extensions](https://docs.gitlab.com/editor_extensions/)
/
  1. [GitLab Docs](https://docs.gitlab.com/)
  2. [Extend](https://docs.gitlab.com/api/)
  3. [Getting started](https://docs.gitlab.com/api/get_started/get_started_extending/)


* * *
# Get started extending GitLab
Interact programmatically with GitLab. Automate tasks, integrate with other tools, and create custom workflows. GitLab also supports plugins and custom hooks.
Follow these steps to learn more about extending GitLab.
## Step 1: Set up integrations[](https://docs.gitlab.com/api/get_started/get_started_extending/#step-1-set-up-integrations "Permalink")
GitLab has several major integrations that can help streamline your development workflow.
These integrations cover a variety of areas, including:
  * **Authentication** : OAuth, SAML, LDAP
  * **Planning** : Jira, Bugzilla, Redmine, Pivotal Tracker
  * **Communication** : Slack, Microsoft Teams, Mattermost
  * **Security** : Checkmarx, Veracode, Fortify


For more information, see:
  * [The list of integrations](https://docs.gitlab.com/integration/)


## Step 2: Set up webhooks[](https://docs.gitlab.com/api/get_started/get_started_extending/#step-2-set-up-webhooks "Permalink")
Use webhooks to notify external services about GitLab events.
Webhooks listen for specific events like pushes, merges, and commits. When one of those events occurs, GitLab sends an HTTP POST payload to the webhook’s configured URL. The payload sent by the webhook provides details about the event, like the event name, project ID, and user and commit details. Then the external system identifies and processes the event.
As an example, you can have a webhook that triggers a new Jenkins build every time code is pushed to GitLab.
You can configure webhooks per project or for the entire GitLab instance. Per-project webhooks listen to events for one particular project.
You can use webhooks to integrate GitLab with a variety of external tools, including CI/CD systems, chat and messaging platforms, and monitoring and logging tools.
For more information, see:
  * [Webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/)


## Step 3: Use the APIs[](https://docs.gitlab.com/api/get_started/get_started_extending/#step-3-use-the-apis "Permalink")
Use the REST API or GraphQL API to interact programmatically with GitLab and build custom integrations, retrieve data, or automate processes. The APIs cover various aspects of GitLab, including projects, issues, merge requests, and repositories.
The GitLab REST APIs follow RESTful principles and use JSON as the data format for requests and responses. You can authenticate these requests and responses by using personal access tokens or OAuth 2.0 tokens.
GitLab also offers a GraphQL API, which is more flexible and efficient when querying data.
Start by exploring the APIs with cURL or a REST client to understand the requests and responses. Then use the API to automate tasks, like creating projects and adding members to groups.
For more information, see:
  * [The REST API](https://docs.gitlab.com/api/api_resources/)
  * [The GraphQL API](https://docs.gitlab.com/api/graphql/reference/)


## Step 4: Use the GitLab CLI[](https://docs.gitlab.com/api/get_started/get_started_extending/#step-4-use-the-gitlab-cli "Permalink")
The GitLab CLI can help you complete various GitLab operations and manage your GitLab instance.
You can use the GitLab CLI to do all kinds of bulk tasks more quickly, like:
  * Creating new projects, groups, and other GitLab resources
  * Managing users and permissions
  * Importing and exporting projects between GitLab instances
  * Triggering CI/CD pipelines


For more information, see:
  * [Install the GitLab CLI](https://gitlab.com/gitlab-org/cli/#installation)


Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/get_started/get_started_extending.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/get_started/get_started_extending.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Step 1: Set up integrations](https://docs.gitlab.com/api/get_started/get_started_extending/#step-1-set-up-integrations)
  * [Step 2: Set up webhooks](https://docs.gitlab.com/api/get_started/get_started_extending/#step-2-set-up-webhooks)
  * [Step 3: Use the APIs](https://docs.gitlab.com/api/get_started/get_started_extending/#step-3-use-the-apis)
  * [Step 4: Use the GitLab CLI](https://docs.gitlab.com/api/get_started/get_started_extending/#step-4-use-the-gitlab-cli)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/get_started/get_started_extending.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/get_started/get_started_extending.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fgeo_nodes%2F&_biz_t=1772174270022&_biz_i=Geo%20Nodes%20API%20\(deprecated\)%20%7C%20GitLab%20Docs&_biz_n=54&rnd=252099&cdn_o=a&_biz_z=1772174270295)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fget_started%2Fget_started_extending%2F&_biz_t=1772174270293&_biz_i=Get%20started%20extending%20GitLab%20%7C%20GitLab%20Docs&_biz_n=55&rnd=449793&cdn_o=a&_biz_z=1772174270295)
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
