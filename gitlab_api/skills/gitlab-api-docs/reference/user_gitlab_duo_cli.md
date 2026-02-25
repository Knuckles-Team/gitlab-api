[Skip to main content](https://docs.gitlab.com/user/gitlab_duo_cli/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/user/gitlab_duo_cli/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/user/gitlab_duo_cli/)
    * [18.8](https://docs.gitlab.com/18.8/user/gitlab_duo_cli/)
    * [18.7](https://archives.docs.gitlab.com/18.7/user/gitlab_duo_cli/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/user/gitlab_duo_cli/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/user/gitlab_duo_cli/index.html)
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
  3. [GitLab Duo CLI (duo)](https://docs.gitlab.com/user/gitlab_duo_cli/)


* * *
# GitLab Duo CLI (`duo`)
  * Tier: Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated
  * Status: Experiment


Model information
  * [Default LLM](https://docs.gitlab.com/user/duo_agent_platform/model_selection/#default-models)
  * Available on [GitLab Duo with self-hosted models](https://docs.gitlab.com/administration/gitlab_duo_self_hosted/)


History
  * Introduced as [experiment](https://docs.gitlab.com/policy/development_stages_support/#experiment) in GitLab 18.9.


The GitLab Duo CLI is a command-line interface tool that brings [GitLab Duo Chat (Agentic)](https://docs.gitlab.com/user/gitlab_duo_chat/agentic_chat/) to your terminal. Available for use with any operating system and editor, use `duo` to ask complex questions about your codebase and to autonomously perform actions on your behalf.
The GitLab Duo CLI can help you:
  * Understand your codebase structure, cross-file functionality, and individual code snippets.
  * Build, modify, refactor, and modernize code.
  * Troubleshoot errors and fix code issues.
  * Automate CI/CD configuration, troubleshoot pipeline errors, and optimize pipelines.
  * Perform multi-step development tasks autonomously.


The GitLab Duo CLI (`duo`) is a separate tool from the [GitLab CLI](https://docs.gitlab.com/cli/) (`glab`). While `glab` provides command-line access to GitLab features like issues and merge requests, `duo` provides autonomous AI capabilities to complete tasks and assist you while you work.
A unified experience is proposed in [epic 20826](https://gitlab.com/groups/gitlab-org/-/work_items/20826).
The GitLab Duo CLI offers two modes:
  * Interactive mode: Provides a chat experience similar to GitLab Duo Chat in the GitLab UI or in editor extensions.
  * Headless mode: Enables non-interactive use in runners, scripts, and other automated workflows.


## Install the GitLab Duo CLI[](https://docs.gitlab.com/user/gitlab_duo_cli/#install-the-gitlab-duo-cli "Permalink")
You can install the GitLab Duo CLI as an npm package or a compiled binary.
### npm package[](https://docs.gitlab.com/user/gitlab_duo_cli/#npm-package "Permalink")
Prerequisites:
  * Node.js 22 or later.
  * For GitLab Self-Managed with a self-signed certificate, either:
    * Node.js LTS 22.20.0 or later
    * Node.js 23.8.0 or later


To install the GitLab Duo CLI as an npm package, run:
shell
```
npm install --global @gitlab/duo-cli
```

### Compiled binary[](https://docs.gitlab.com/user/gitlab_duo_cli/#compiled-binary "Permalink")
To install the GitLab Duo CLI as a compiled binary, download and run the install script.
  * [macOS and Linux](https://docs.gitlab.com/user/gitlab_duo_cli/)
  * [Windows](https://docs.gitlab.com/user/gitlab_duo_cli/)


shell
```
bash <(curl --fail --silent --show-error --location "https://gitlab.com/gitlab-org/editor-extensions/gitlab-lsp/-/raw/main/packages/cli/scripts/install_duo_cli.sh")
```

shell
```
irm "https://gitlab.com/gitlab-org/editor-extensions/gitlab-lsp/-/raw/main/packages/cli/scripts/install_duo_cli.ps1" | iex
```

## Authenticate with GitLab[](https://docs.gitlab.com/user/gitlab_duo_cli/#authenticate-with-gitlab "Permalink")
The first time you run the GitLab Duo CLI, a configuration screen appears with a prompt to set a **GitLab Instance URL** and **GitLab Token** for authentication.
Prerequisites:
  * A [personal access token](https://docs.gitlab.com/user/profile/personal_access_tokens/) with `api` permissions.


To authenticate:
  1. Enter a **GitLab Instance URL** and then press `Enter`. For example, `https://gitlab.com`.
  2. For **GitLab Token** , enter your personal access token.
  3. To save and exit the CLI, press `Control`+`S`.
  4. To restart the CLI, run `duo` in your terminal.


To modify the configuration after initial setup, use `duo config edit`.
## Use the GitLab Duo CLI[](https://docs.gitlab.com/user/gitlab_duo_cli/#use-the-gitlab-duo-cli "Permalink")
Prerequisites:
  * You must be working with a GitLab project that has a remote repository configured, or set a [default GitLab Duo namespace](https://docs.gitlab.com/user/profile/preferences/#set-a-default-gitlab-duo-namespace).


### Use the GitLab Duo CLI in interactive mode[](https://docs.gitlab.com/user/gitlab_duo_cli/#use-the-gitlab-duo-cli-in-interactive-mode "Permalink")
To use the GitLab Duo CLI in interactive mode, use the command `duo`:
  1. Start the interactive UI in your terminal:
shell
```
duo
```

  2. `Duo` appears in your terminal window. After the prompt, enter your question or request and press `Enter`.
For example:
```
What is this repository about?

Which issues need my attention?

Help me implement issue 15.

The pipelines in MR 23 are failing. Please help me fix them.
```



### Use the GitLab Duo CLI in headless mode[](https://docs.gitlab.com/user/gitlab_duo_cli/#use-the-gitlab-duo-cli-in-headless-mode "Permalink")
Use headless mode with caution and in a controlled sandbox environment.
To run a workflow in non-interactive mode, use the command `duo run`:
shell
```
duo run --goal "Your goal or prompt here"
```

For example, you can run an ESLint command and pipe errors to the GitLab Duo CLI to resolve:
shell
```
duo run --goal "Fix these errors: $eslint_output"
```

When you use headless mode, the GitLab Duo CLI:
  * Bypasses manual tool approvals and automatically approves all tools for use.
  * Does not maintain context from previous conversations. A new workflow starts every time you execute `duo run`.


## Model Context Protocol (MCP) connections[](https://docs.gitlab.com/user/gitlab_duo_cli/#model-context-protocol-mcp-connections "Permalink")
To connect the GitLab Duo CLI to local or remote MCP servers, use the same MCP configuration as the GitLab IDE extensions. For instructions, see [configure MCP servers](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_clients/#configure-mcp-servers).
## Options[](https://docs.gitlab.com/user/gitlab_duo_cli/#options "Permalink")
The GitLab Duo CLI supports these options:
  * `-C, --cwd <path>`: Change the working directory.
  * `-h, --help` : Display help for the GitLab Duo CLI or a specific command. For example, `duo --help` or `duo run --help`.
  * `--log-level <level>`: Set the logging level (`debug`, `info`, `warn`, `error`).
  * `-v`, `--version`: Display version information.


Additional options for headless mode:
  * `--ai-context-items <contextItems>`: JSON-encoded array of additional context items for reference.
  * `--existing-session-id <sessionId>`: ID of an existing session to resume.
  * `--gitlab-auth-token <token>`: Authentication token for a GitLab instance.
  * `--gitlab-base-url <url>`: Base URL of a GitLab instance (default: `https://gitlab.com`).


## Commands[](https://docs.gitlab.com/user/gitlab_duo_cli/#commands "Permalink")
  * `duo`: Start interactive mode.
  * `duo config`: Manage the configuration and authentication settings.
  * `duo log`: View and manage logs.
    * `duo log last`: Open the last log file.
    * `duo log list`: List all log files.
    * `duo log tail <args...>`: Display the tail of the last log file. Supports standard tail arguments.
    * `duo log clear`: Remove all existing log files.
  * `duo run`: Start headless mode.


## Environment variables[](https://docs.gitlab.com/user/gitlab_duo_cli/#environment-variables "Permalink")
You can configure the GitLab Duo CLI using environment variables:
  * `DUO_WORKFLOW_GIT_HTTP_PASSWORD`: Git HTTP authentication password.
  * `DUO_WORKFLOW_GIT_HTTP_USER`: Git HTTP authentication username.
  * `GITLAB_BASE_URL` or `GITLAB_URL`: GitLab instance URL.
  * `GITLAB_OAUTH_TOKEN` or `GITLAB_TOKEN`: Authentication token.
  * `LOG_LEVEL`: Logging level.


## Proxy and custom certificate configuration[](https://docs.gitlab.com/user/gitlab_duo_cli/#proxy-and-custom-certificate-configuration "Permalink")
If your network uses an HTTPS-intercepting proxy or requires custom SSL certificates, you might need additional configuration.
### Proxy configuration[](https://docs.gitlab.com/user/gitlab_duo_cli/#proxy-configuration "Permalink")
The GitLab Duo CLI respects standard proxy environment variables:
  * `HTTP_PROXY` or `http_proxy`: Proxy URL for HTTP requests.
  * `HTTPS_PROXY` or `https_proxy`: Proxy URL for HTTPS requests.
  * `NO_PROXY` or `no_proxy`: Comma-separated list of hosts to exclude from proxying.


### Custom SSL certificates[](https://docs.gitlab.com/user/gitlab_duo_cli/#custom-ssl-certificates "Permalink")
If your organization uses a custom Certificate Authority (CA), for an HTTPS-intercepting proxy or similar, you might encounter certificate errors.
```
Error: unable to verify the first certificate
Error: self-signed certificate in certificate chain
```

To resolve certificate errors, use one of the following methods:
  * Use the system certificate store (recommended): If your CA certificate is installed in your operating system’s certificate store, configure Node.js to use it. Requires Node.js 22.15.0, 23.9.0, or 24.0.0 and later.
shell
```
export NODE_OPTIONS="--use-system-ca"
```

  * Specify a CA certificate file: For older Node.js versions, or when the CA certificate is not in the system store, point Node.js to the certificate file directly. The file must be in PEM format.
shell
```
export NODE_EXTRA_CA_CERTS=/path/to/custom-ca.pem
```



### Ignore certificate errors[](https://docs.gitlab.com/user/gitlab_duo_cli/#ignore-certificate-errors "Permalink")
If you still encounter certificate errors, you can disable certificate verification.
Disabling certificate verification is a security risk. You should not disable verification in production environments.
Certificate errors alert you to potential security breaches, so you should disable certificate verification only when you are confident that it is safe to do so.
Prerequisites:
  * You verified the certificate chain in your browser, or your administrator confirmed that this error is safe to ignore.


To disable certificate verification:
shell
```
export NODE_TLS_REJECT_UNAUTHORIZED=0
```

## Update the GitLab Duo CLI[](https://docs.gitlab.com/user/gitlab_duo_cli/#update-the-gitlab-duo-cli "Permalink")
To update the GitLab Duo CLI to the latest version, run:
shell
```
npm install --global @gitlab/duo-cli@latest
```

## Contribute to the GitLab Duo CLI[](https://docs.gitlab.com/user/gitlab_duo_cli/#contribute-to-the-gitlab-duo-cli "Permalink")
For information on contributing to the GitLab Duo CLI, see the [development guide](https://gitlab.com/gitlab-org/editor-extensions/gitlab-lsp/-/blob/main/packages/cli/docs/development.md).
## Related topics[](https://docs.gitlab.com/user/gitlab_duo_cli/#related-topics "Permalink")
  * [Security considerations for editor extensions](https://docs.gitlab.com/editor_extensions/security_considerations/)


Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/user/gitlab_duo_cli/_index.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/gitlab_duo_cli/_index.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Install the GitLab Duo CLI](https://docs.gitlab.com/user/gitlab_duo_cli/#install-the-gitlab-duo-cli)
  * [npm package](https://docs.gitlab.com/user/gitlab_duo_cli/#npm-package)
  * [Compiled binary](https://docs.gitlab.com/user/gitlab_duo_cli/#compiled-binary)
  * [Authenticate with GitLab](https://docs.gitlab.com/user/gitlab_duo_cli/#authenticate-with-gitlab)
  * [Use the GitLab Duo CLI](https://docs.gitlab.com/user/gitlab_duo_cli/#use-the-gitlab-duo-cli)
  * [Use the GitLab Duo CLI in interactive mode](https://docs.gitlab.com/user/gitlab_duo_cli/#use-the-gitlab-duo-cli-in-interactive-mode)
  * [Use the GitLab Duo CLI in headless mode](https://docs.gitlab.com/user/gitlab_duo_cli/#use-the-gitlab-duo-cli-in-headless-mode)
  * [Model Context Protocol (MCP) connections](https://docs.gitlab.com/user/gitlab_duo_cli/#model-context-protocol-mcp-connections)
  * [Options](https://docs.gitlab.com/user/gitlab_duo_cli/#options)
  * [Commands](https://docs.gitlab.com/user/gitlab_duo_cli/#commands)
  * [Environment variables](https://docs.gitlab.com/user/gitlab_duo_cli/#environment-variables)
  * [Proxy and custom certificate configuration](https://docs.gitlab.com/user/gitlab_duo_cli/#proxy-and-custom-certificate-configuration)
  * [Proxy configuration](https://docs.gitlab.com/user/gitlab_duo_cli/#proxy-configuration)
  * [Custom SSL certificates](https://docs.gitlab.com/user/gitlab_duo_cli/#custom-ssl-certificates)
  * [Ignore certificate errors](https://docs.gitlab.com/user/gitlab_duo_cli/#ignore-certificate-errors)
  * [Update the GitLab Duo CLI](https://docs.gitlab.com/user/gitlab_duo_cli/#update-the-gitlab-duo-cli)
  * [Contribute to the GitLab Duo CLI](https://docs.gitlab.com/user/gitlab_duo_cli/#contribute-to-the-gitlab-duo-cli)
  * [Related topics](https://docs.gitlab.com/user/gitlab_duo_cli/#related-topics)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/gitlab_duo_cli/_index.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/user/gitlab_duo_cli/_index.md)
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


%20%7C%20GitLab%20Docs&_biz_n=209&rnd=639415&cdn_o=a&_biz_z=1771981776246)
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
