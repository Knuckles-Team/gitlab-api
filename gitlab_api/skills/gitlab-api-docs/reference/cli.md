[Skip to main content](https://docs.gitlab.com/cli/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/cli/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/cli/)
    * [18.8](https://docs.gitlab.com/18.8/cli/)
    * [18.7](https://archives.docs.gitlab.com/18.7/cli/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/cli/)
    * [16.11](https://archives.docs.gitlab.com/16.11/cli/index.html)
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
[glab alias](https://docs.gitlab.com/cli/alias/)
[glab api](https://docs.gitlab.com/cli/api/)
[glab attestation](https://docs.gitlab.com/cli/attestation/)
[glab auth](https://docs.gitlab.com/cli/auth/)
[glab changelog](https://docs.gitlab.com/cli/changelog/)
[check-update](https://docs.gitlab.com/cli/check-update/)
[glab ci](https://docs.gitlab.com/cli/ci/)
[glab cluster](https://docs.gitlab.com/cli/cluster/)
[glab completion](https://docs.gitlab.com/cli/completion/)
[glab config](https://docs.gitlab.com/cli/config/)
[glab deploy-key](https://docs.gitlab.com/cli/deploy-key/)
[glab duo](https://docs.gitlab.com/cli/duo/)
[glab gpg-key](https://docs.gitlab.com/cli/gpg-key/)
[glab incident](https://docs.gitlab.com/cli/incident/)
[glab issue](https://docs.gitlab.com/cli/issue/)
[glab iteration](https://docs.gitlab.com/cli/iteration/)
[glab job](https://docs.gitlab.com/cli/job/)
[glab label](https://docs.gitlab.com/cli/label/)
[glab mcp](https://docs.gitlab.com/cli/mcp/)
[glab milestone](https://docs.gitlab.com/cli/milestone/)
[glab mr](https://docs.gitlab.com/cli/mr/)
[glab opentofu](https://docs.gitlab.com/cli/opentofu/)
[glab release](https://docs.gitlab.com/cli/release/)
[glab repo](https://docs.gitlab.com/cli/repo/)
[glab runner-controller](https://docs.gitlab.com/cli/runner-controller/)
[glab schedule](https://docs.gitlab.com/cli/schedule/)
[glab securefile](https://docs.gitlab.com/cli/securefile/)
[glab Snippet](https://docs.gitlab.com/cli/snippet/)
[glab ssh-key](https://docs.gitlab.com/cli/ssh-key/)
[glab stack](https://docs.gitlab.com/cli/stack/)
[glab token](https://docs.gitlab.com/cli/token/)
[glab user](https://docs.gitlab.com/cli/user/)
[glab variable](https://docs.gitlab.com/cli/variable/)
[glab version](https://docs.gitlab.com/cli/version/)
[Editor and IDE extensions](https://docs.gitlab.com/editor_extensions/)
/
  1. [GitLab Docs](https://docs.gitlab.com/)
  2. [Extend](https://docs.gitlab.com/api/)
  3. [GitLab CLI (glab)](https://docs.gitlab.com/cli/)


* * *
# GitLab CLI (glab)
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


GLab is an open source GitLab CLI tool. It brings GitLab to your terminal, next to where you are already working with `git` and your code, without switching between windows and browser tabs. While it’s powerful for issues and merge requests, `glab` does even more:
  * View, manage, and retry CI/CD pipelines directly from your CLI.
  * Create changelogs.
  * Create and manage releases.
  * Ask GitLab Duo Chat (Classic) questions about Git.
  * Manage GitLab agents for Kubernetes.


`glab` is available for repositories hosted on GitLab.com, GitLab Dedicated, and GitLab Self-Managed. It supports multiple authenticated GitLab instances, and automatically detects the authenticated hostname from the remotes available in your working Git directory.
[![command example](https://docs.gitlab.com/cli/img/glabgettingstarted.gif)](https://docs.gitlab.com/cli/img/glabgettingstarted.gif)
## Install the CLI[](https://docs.gitlab.com/cli/#install-the-cli "Permalink")
Installation instructions are available in the GLab [`README`](https://gitlab.com/gitlab-org/cli/#installation).
## Authenticate with GitLab[](https://docs.gitlab.com/cli/#authenticate-with-gitlab "Permalink")
GLab supports multiple authentication methods including OAuth and personal access tokens. To get started, run `glab auth login` and follow the interactive setup.
For detailed authentication instructions, see the [Authentication section](https://gitlab.com/gitlab-org/cli#authentication) in the main README.
## Environment Variables[](https://docs.gitlab.com/cli/#environment-variables "Permalink")
Variable | Description
---|---
`BROWSER` | The web browser to use for opening links. Can be set in the config with ‘glab config set browser mybrowser’.
`DEBUG` | Set to true to output more logging information, including underlying Git commands, expanded aliases and DNS error details.
`FORCE_HYPERLINKS` | Set to true to force hyperlinks in output, even when not outputting to a TTY.
`GITLAB_CLIENT_ID` | Provide custom ‘client_id’ generated by GitLab OAuth 2.0 application. Defaults to the ‘client-id’ for GitLab.com.
`GITLAB_HOST or GL_HOST` | If GitLab Self-Managed or GitLab Dedicated, specify the URL of the GitLab server. (Example: `https://gitlab.example.com`) Defaults to `https://gitlab.com`.
`GITLAB_TOKEN` | An authentication token for API requests. Set this variable to avoid prompts to authenticate. Overrides any previously-stored credentials. Can be set in the config with ‘glab config set token xxxxxx’.
`GLAB_CHECK_UPDATE` | Set to true to force an update check. By default the cli tool checks for updates once a day.
`GLAB_CONFIG_DIR` | Set to a directory path to override the global configuration location.
`GLAB_DEBUG_HTTP` | Set to true to output HTTP transport information (request / response).
`GLAB_SEND_TELEMETRY` | Set to false to disable telemetry being sent to your GitLab instance. Can be set in the config with ‘glab config set telemetry false’. See <https://docs.gitlab.com/administration/settings/usage_statistics/> for more information
`GLAMOUR_STYLE` | The environment variable to set your desired Markdown renderer style. Available options: dark, light, notty. To set a custom style, read <https://github.com/charmbracelet/glamour#styles>
`NO_COLOR` | Set to any value to avoid printing ANSI escape sequences for color output.
`NO_PROMPT` | Set to true to disable prompts.
`REMOTE_ALIAS or GIT_REMOTE_URL_VAR` | A ‘git remote’ variable or alias that contains the GitLab URL. Can be set in the config with ‘glab config set remote_alias origin’.
`VISUAL, EDITOR (in order of precedence)` | The editor tool to use for authoring text. Can be set in the config with ‘glab config set editor vim’.
`GLAB_ENABLE_CI_AUTOLOGIN [EXPERIMENTAL]` | Set to `true` to enable auto-login in GitLab CI. CI auto-login detects if glab is running in a GitLab CI job by checking the predefined CI/CD variable `GITLAB_CI`. If detected, it uses predefined CI/CD variables like `CI_SERVER_FQDN` and `CI_JOB_TOKEN` to log in, and ignores other variables like `GITLAB_HOST` or `GITLAB_TOKEN`. Only glab commands that support `CI_JOB_TOKEN` are available. For a list of supported commands, see the CI/CD job token documentation: <https://docs.gitlab.com/ci/jobs/ci_job_token/#job-token-access>. This flag is experimental. Use with caution and leave feedback in issue 8071: <https://gitlab.com/gitlab-org/cli/-/work_items/8071>.
## Options[](https://docs.gitlab.com/cli/#options "Permalink")
```
  -h, --help      Show help for this command.
  -v, --version   show glab version information
```

## Commands[](https://docs.gitlab.com/cli/#commands "Permalink")
  * [`glab alias`](https://docs.gitlab.com/cli/alias/)
  * [`glab api`](https://docs.gitlab.com/cli/api/)
  * [`glab attestation`](https://docs.gitlab.com/cli/attestation/)
  * [`glab auth`](https://docs.gitlab.com/cli/auth/)
  * [`glab changelog`](https://docs.gitlab.com/cli/changelog/)
  * [`glab check-update`](https://docs.gitlab.com/cli/check-update/)
  * [`glab ci`](https://docs.gitlab.com/cli/ci/)
  * [`glab cluster`](https://docs.gitlab.com/cli/cluster/)
  * [`glab completion`](https://docs.gitlab.com/cli/completion/)
  * [`glab config`](https://docs.gitlab.com/cli/config/)
  * [`glab deploy-key`](https://docs.gitlab.com/cli/deploy-key/)
  * [`glab duo`](https://docs.gitlab.com/cli/duo/)
  * [`glab gpg-key`](https://docs.gitlab.com/cli/gpg-key/)
  * [`glab incident`](https://docs.gitlab.com/cli/incident/)
  * [`glab issue`](https://docs.gitlab.com/cli/issue/)
  * [`glab iteration`](https://docs.gitlab.com/cli/iteration/)
  * [`glab job`](https://docs.gitlab.com/cli/job/)
  * [`glab label`](https://docs.gitlab.com/cli/label/)
  * [`glab mcp`](https://docs.gitlab.com/cli/mcp/)
  * [`glab milestone`](https://docs.gitlab.com/cli/milestone/)
  * [`glab mr`](https://docs.gitlab.com/cli/mr/)
  * [`glab opentofu`](https://docs.gitlab.com/cli/opentofu/)
  * [`glab release`](https://docs.gitlab.com/cli/release/)
  * [`glab repo`](https://docs.gitlab.com/cli/repo/)
  * [`glab runner-controller`](https://docs.gitlab.com/cli/runner-controller/)
  * [`glab schedule`](https://docs.gitlab.com/cli/schedule/)
  * [`glab securefile`](https://docs.gitlab.com/cli/securefile/)
  * [`glab snippet`](https://docs.gitlab.com/cli/snippet/)
  * [`glab ssh-key`](https://docs.gitlab.com/cli/ssh-key/)
  * [`glab stack`](https://docs.gitlab.com/cli/stack/)
  * [`glab token`](https://docs.gitlab.com/cli/token/)
  * [`glab user`](https://docs.gitlab.com/cli/user/)
  * [`glab variable`](https://docs.gitlab.com/cli/variable/)
  * [`glab version`](https://docs.gitlab.com/cli/version/)


## Report issues[](https://docs.gitlab.com/cli/#report-issues "Permalink")
Open an issue in the [`gitlab-org/cli` repository](https://gitlab.com/gitlab-org/cli/issues/new) to send us feedback.
Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/cli/edit/main/-/docs/source/_index.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/cli/-/blob/main/docs/source/_index.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Install the CLI](https://docs.gitlab.com/cli/#install-the-cli)
  * [Authenticate with GitLab](https://docs.gitlab.com/cli/#authenticate-with-gitlab)
  * [Environment Variables](https://docs.gitlab.com/cli/#environment-variables)
  * [Options](https://docs.gitlab.com/cli/#options)
  * [Commands](https://docs.gitlab.com/cli/#commands)
  * [Report issues](https://docs.gitlab.com/cli/#report-issues)


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
  * [View page source](https://gitlab.com/gitlab-org/cli/-/blob/main/docs/source/_index.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/cli/edit/main/-/docs/source/_index.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Feditor_extensions%2F&_biz_t=1771981755529&_biz_i=Editor%20extensions%20%7C%20GitLab%20Docs&_biz_n=191&rnd=888029&cdn_o=a&_biz_z=1771981755749)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fwikis%2F&_biz_t=1771981755645&_biz_i=Project%20wikis%20API%20%7C%20GitLab%20Docs&_biz_n=192&rnd=157717&cdn_o=a&_biz_z=1771981755750)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=6cd0908ec84a42fec9a17ce4b3f900fc&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fcli%2F&_biz_t=1771981755748&_biz_i=GitLab%20CLI%20\(glab\)%20%7C%20GitLab%20Docs&_biz_n=193&rnd=725887&cdn_o=a&_biz_z=1771981755750)
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
