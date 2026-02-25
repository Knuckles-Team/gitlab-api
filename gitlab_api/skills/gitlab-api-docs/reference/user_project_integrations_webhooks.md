[Skip to main content](https://docs.gitlab.com/user/project/integrations/webhooks/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/user/project/integrations/webhooks/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/user/project/integrations/webhooks/)
    * [18.8](https://docs.gitlab.com/18.8/user/project/integrations/webhooks/)
    * [18.7](https://archives.docs.gitlab.com/18.7/user/project/integrations/webhooks/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/user/project/integrations/webhooks/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/user/project/integrations/webhooks.html)
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
[Events](https://docs.gitlab.com/user/project/integrations/webhook_events/)
[Rake tasks](https://docs.gitlab.com/administration/raketasks/web_hooks/)
[Troubleshooting](https://docs.gitlab.com/user/project/integrations/webhooks_troubleshooting/)
[REST API](https://docs.gitlab.com/api/rest/)
[GraphQL API](https://docs.gitlab.com/api/graphql/)
[OAuth 2.0 identity provider API](https://docs.gitlab.com/api/oauth2/)
[GitLab Duo CLI (duo)](https://docs.gitlab.com/user/gitlab_duo_cli/)
[GitLab CLI (glab)](https://docs.gitlab.com/cli/)
[Editor and IDE extensions](https://docs.gitlab.com/editor_extensions/)
/
  1. [GitLab Docs](https://docs.gitlab.com/)
  2. [Extend](https://docs.gitlab.com/api/)
  3. [Webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/)


* * *
# Webhooks
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


Webhooks connect GitLab to your other tools and systems through real-time notifications. When important events happen in GitLab, webhooks send that information directly to your external applications. Build automation workflows by reacting to merge requests, code pushes, and issue updates.
With webhooks, your team stays synchronized as changes occur:
  * External issue trackers update automatically when GitLab issues change.
  * Chat applications notify team members about pipeline completions.
  * Custom scripts deploy applications when code reaches the main branch.
  * Monitoring systems track development activity across your entire organization.


## Webhook events[](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-events "Permalink")
Various events in GitLab can trigger webhooks. For example:
  * Pushing code to a repository.
  * Posting a comment on an issue.
  * Creating a merge request.


## Webhook limits[](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-limits "Permalink")
GitLab.com enforces webhook limits, including:
  * Maximum number of webhooks per project or group.
  * Number of webhook calls per minute.
  * Webhook timeout duration.


For GitLab Self-Managed, administrators can modify these limits.
### Push event limits[](https://docs.gitlab.com/user/project/integrations/webhooks/#push-event-limits "Permalink")
GitLab limits webhook triggers for push events that include multiple changes:
  * Default limit: 3 branches or tags per push.
  * Behavior when exceeded: No webhooks are triggered for the entire push event.
  * Applies to: Both project webhooks and system hooks.
  * Configuration: GitLab Self-Managed administrators can modify the `push_event_hooks_limit` setting through the application settings API.


If you frequently push multiple tags or branches simultaneously and need webhook notifications, contact your GitLab administrator to increase this limit.
## Group webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#group-webhooks "Permalink")
  * Tier: Premium, Ultimate


Group webhooks are custom HTTP callbacks that send notifications for events across all projects in a group and its subgroups.
### Types of group webhook events[](https://docs.gitlab.com/user/project/integrations/webhooks/#types-of-group-webhook-events "Permalink")
You can configure group webhooks to listen for:
  * All events that occur in projects in the group and subgroups
  * Group-specific events, including group member events, project events, and subgroup events


### Webhooks in both a project and a group[](https://docs.gitlab.com/user/project/integrations/webhooks/#webhooks-in-both-a-project-and-a-group "Permalink")
If you configure identical webhooks in both a group and a project in that group, both webhooks are triggered for events in that project. This allows for flexible event handling at different levels of your GitLab organization.
## Configure webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#configure-webhooks "Permalink")
Create and configure webhooks in GitLab to integrate with your project’s workflow. Use these features to set up webhooks that meet your specific requirements.
### Create a webhook[](https://docs.gitlab.com/user/project/integrations/webhooks/#create-a-webhook "Permalink")
History
  * **Name** and **Description** [introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/141977) in GitLab 16.9.


Create a webhook to send notifications about events in your project or group.
Prerequisites:
  * For project webhooks, you must have the Maintainer or Owner role for the project.
  * For group webhooks, you must have the Owner role for the group.


To create a webhook:
  1. On the top bar, select **Search or go to** and find your project or group.
  2. Select **Settings** > **Webhooks**.
  3. Select **Add new webhook**.
  4. In **URL** , enter the URL of the webhook endpoint. Use percent-encoding for special characters.
  5. Optional. Enter a **Name** and **Description** for the webhook.
  6. Optional. In **Secret token** , enter a token to validate requests.
  7. In the **Trigger** section, select the events to trigger the webhook.
  8. Optional. To disable SSL verification, clear the **Enable SSL verification** checkbox.
  9. Select **Add webhook**.


The secret token is sent with the webhook request in the `X-Gitlab-Token` HTTP header. Your webhook endpoint can use this token to verify the legitimacy of the request.
### Mask sensitive portions of webhook URLs[](https://docs.gitlab.com/user/project/integrations/webhooks/#mask-sensitive-portions-of-webhook-urls "Permalink")
Mask sensitive portions of webhook URLs to enhance security. Masked portions are replaced with configured values when webhooks are executed, are not logged, and are encrypted at rest in the database.
To mask sensitive portions of a webhook URL:
  1. On the top bar, select **Search or go to** and find your project or group.
  2. Select **Settings** > **Webhooks**.
  3. In **URL** , enter the full URL of the webhook.
  4. To define masked portions, select **Add URL masking**.
  5. In **Sensitive portion of URL** , enter the part of the URL you want to mask.
  6. In **How it looks in the UI** , enter the value to display instead of the masked portion. Variable names must contain only lowercase letters (`a-z`), numbers (`0-9`), or underscores (`_`).
  7. Select **Save changes**.


The masked values appear hidden in the UI. For example, if you’ve defined variables `path` and `value`, the webhook URL can look like this:
```
https://webhook.example.com/{path}?key={value}
```

### Custom headers[](https://docs.gitlab.com/user/project/integrations/webhooks/#custom-headers "Permalink")
History
  * [Introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/146702) in GitLab 16.11 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `custom_webhook_headers`. Enabled by default.
  * [Generally available](https://gitlab.com/gitlab-org/gitlab/-/issues/448604) in GitLab 17.0. Feature flag `custom_webhook_headers` removed.


Add custom headers to webhook requests for authentication to external services. You can configure up to 20 custom headers per webhook.
Custom headers must:
  * Not override the values of delivery headers.
  * Contain only alphanumeric characters, periods, dashes, or underscores.
  * Start with a letter and end with a letter or number.
  * Have no consecutive periods, dashes, or underscores.


Custom headers show in **Recent events** with masked values.
### Custom webhook template[](https://docs.gitlab.com/user/project/integrations/webhooks/#custom-webhook-template "Permalink")
History
  * [Introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/142738) in GitLab 16.10 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `custom_webhook_template`. Enabled by default.
  * [Generally available](https://gitlab.com/gitlab-org/gitlab/-/issues/439610) in GitLab 17.0. Feature flag `custom_webhook_template` removed.
  * JSON serialization of interpolated field values [introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/197992) in GitLab 18.4 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `custom_webhook_template_serialization`. Disabled by default.
  * JSON serialization of interpolated field values made [generally available](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/212407) in GitLab 18.6. Feature flag `custom_webhook_template_serialization` enabled by default.
  * Feature flag `custom_webhook_template_serialization` [removed](https://gitlab.com/gitlab-org/gitlab/-/work_items/580460) in GitLab 18.10.


Create a custom payload template for your webhook to control the data sent in the request body.
#### Create a custom webhook template[](https://docs.gitlab.com/user/project/integrations/webhooks/#create-a-custom-webhook-template "Permalink")
  * For project webhooks, you must have the Maintainer or Owner role for the project.
  * For group webhooks, you must have the Owner role for the group.


To create a custom webhook template:
  1. Go to your webhook configuration.
  2. Set a custom webhook template.
  3. Ensure the template renders as valid JSON.


Use fields from the payload of an event in your template. For example:
  * `{{build_name}}` for a job event
  * `{{deployable_url}}` for a deployment event


To access nested properties, use periods to separate path segments.
#### Example custom webhook template[](https://docs.gitlab.com/user/project/integrations/webhooks/#example-custom-webhook-template "Permalink")
For this custom payload template:
json
```
{
  "event": "{{object_kind}}",
  "project_name": "{{project.name}}"
}
```

The resulting request payload for a `push` event is:
json
```
{
  "event": "push",
  "project_name": "Example"
}
```

Custom webhook templates cannot access properties in arrays. Support for this feature is proposed in [issue 463332](https://gitlab.com/gitlab-org/gitlab/-/issues/463332).
### Filter push events by branch[](https://docs.gitlab.com/user/project/integrations/webhooks/#filter-push-events-by-branch "Permalink")
Filter `push` events sent to your webhook endpoint by the branch name. Use one of these filtering options:
  * **All branches** : Receive push events from all branches.
  * **Wildcard pattern** : Receive push events from branches that match a wildcard pattern.
  * **Regular expression** : Receive push events from branches that match a regular expression (regex).


#### Use a wildcard pattern[](https://docs.gitlab.com/user/project/integrations/webhooks/#use-a-wildcard-pattern "Permalink")
To filter by using a wildcard pattern:
  1. In the webhook configuration, select **Wildcard pattern**.
  2. Enter a pattern. For example:
     * `*-stable` to match branches ending with `-stable`.
     * `production/*` to match branches in the `production/` namespace.


#### Use a regular expression[](https://docs.gitlab.com/user/project/integrations/webhooks/#use-a-regular-expression "Permalink")
To filter by using a regular expression:
  1. In the webhook configuration, select **Regular expression**.
  2. Enter a regex pattern that follows the [RE2 syntax](https://github.com/google/re2/wiki/Syntax).


For example, to exclude the `main` branch, use:
```
\b(?:m(?!ain\b)|ma(?!in\b)|mai(?!n\b)|[a-l]|[n-z])\w*|\b\w{1,3}\b|\W+
```

### Configure webhooks to support mutual TLS[](https://docs.gitlab.com/user/project/integrations/webhooks/#configure-webhooks-to-support-mutual-tls "Permalink")
  * Offering: GitLab Self-Managed


History
  * [Introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/27450) in GitLab 16.9.


Configure webhooks to support mutual TLS by setting a global client certificate in PEM format.
Prerequisites:
  * You must be a GitLab administrator.


To configure mutual TLS for webhooks:
  1. Prepare a client certificate in PEM format.
  2. Optional. Protect the certificate with a PEM passphrase.
  3. Configure GitLab to use the certificate.


  * [Linux package (Omnibus)](https://docs.gitlab.com/user/project/integrations/webhooks/)
  * [Docker](https://docs.gitlab.com/user/project/integrations/webhooks/)
  * [Self-compiled (source)](https://docs.gitlab.com/user/project/integrations/webhooks/)


  1. Edit `/etc/gitlab/gitlab.rb`:
ruby
```
gitlab_rails['http_client']['tls_client_cert_file'] = '<PATH TO CLIENT PEM FILE>'
gitlab_rails['http_client']['tls_client_cert_password'] = '<OPTIONAL PASSWORD>'
```

  2. Save the file and reconfigure GitLab:
shell
```
sudo gitlab-ctl reconfigure
```



  1. Edit `docker-compose.yml`:
yaml
```
version: "3.6"
services:
  gitlab:
    image: 'gitlab/gitlab-ee:latest'
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
         gitlab_rails['http_client']['tls_client_cert_file'] = '<PATH TO CLIENT PEM FILE>'
         gitlab_rails['http_client']['tls_client_cert_password'] = '<OPTIONAL PASSWORD>'
```

  2. Save the file and restart GitLab:
shell
```
docker compose up -d
```



  1. Edit `/home/git/gitlab/config/gitlab.yml`:
yaml
```
production: &base
  http_client:
    tls_client_cert_file: '<PATH TO CLIENT PEM FILE>'
    tls_client_cert_password: '<OPTIONAL PASSWORD>'
```

  2. Save the file and restart GitLab:
shell
```
# For systems running systemd
sudo systemctl restart gitlab.target

# For systems running SysV init
sudo service gitlab restart
```



After configuration, GitLab presents this certificate to the server during TLS handshakes for webhook connections.
### Configure firewalls for webhook traffic[](https://docs.gitlab.com/user/project/integrations/webhooks/#configure-firewalls-for-webhook-traffic "Permalink")
Configure firewalls for webhook traffic based on how GitLab sends webhooks:
  * Asynchronously from Sidekiq nodes (most common)
  * Synchronously from Rails nodes (in specific cases)


Webhooks are sent synchronously from Rails nodes when you test or retry a webhook in the UI.
When configuring firewalls, ensure both Sidekiq and Rails nodes can send webhook traffic.
## Manage webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#manage-webhooks "Permalink")
Monitor and maintain your configured webhooks in GitLab.
### View webhook request history[](https://docs.gitlab.com/user/project/integrations/webhooks/#view-webhook-request-history "Permalink")
View the history of webhook requests to monitor their performance and troubleshoot issues.
Prerequisites:
  * For project webhooks, you must have the Maintainer or Owner role for the project.
  * For group webhooks, you must have the Owner role for the group.


To view the request history for a webhook:
  1. On the top bar, select **Search or go to** and find your project or group.
  2. Select **Settings** > **Webhooks**.
  3. Select **Edit** for the webhook.
  4. Go to the **Recent events** section.


The **Recent events** section displays all requests made to a webhook in the last two days. The table includes:
  * HTTP status code:
    * Green for `200`-`299` codes
    * Red for other codes
    * `internal error` for failed deliveries
  * Triggered event
  * Elapsed time of the request
  * Relative time the request was made


[![Webhook event log showing status codes and response times](https://docs.gitlab.com/user/project/integrations/img/webhook_logs_v14_4.png)](https://docs.gitlab.com/user/project/integrations/img/webhook_logs_v14_4.png)
#### Inspect request and response details[](https://docs.gitlab.com/user/project/integrations/webhooks/#inspect-request-and-response-details "Permalink")
Prerequisites:
  * For project webhooks, you must have the Maintainer or Owner role for the project.
  * For group webhooks, you must have the Owner role for the group.


Each webhook request in **Recent events** has a **Request details** page. This page contains the body and headers of:
  * The response GitLab received from the webhook receiver endpoint
  * The webhook request GitLab sent


To inspect the request and response details of a webhook event:
  1. On the top bar, select **Search or go to** and find your project or group.
  2. Select **Settings** > **Webhooks**.
  3. Select **Edit** for the webhook.
  4. Go to the **Recent events** section.
  5. Select **View details** for the event.


To send the request again with the same data and the same `Idempotency-Key` header, select **Resend Request**. If the webhook URL has changed, you cannot resend the request. You can also resend the request programmatically through the project webhooks API.
### Test a webhook[](https://docs.gitlab.com/user/project/integrations/webhooks/#test-a-webhook "Permalink")
Test a webhook to ensure it’s working properly or to re-enable a disabled webhook.
Prerequisites:
  * For project webhooks, you must have the Maintainer or Owner role for the project.
  * For group webhooks, you must have the Owner role for the group.
  * To test `push events`, your project must have at least one commit.


To test a webhook:
  1. On the top bar, select **Search or go to** and find your project or group.
  2. Select **Settings** > **Webhooks** to see all webhooks for this project.
  3. To test a webhook directly from the list of configured webhooks:
    1. Locate the webhook you want to test.
    2. From the **Test** dropdown list, select the type of event to test.
  4. To test a webhook while editing it:
    1. Locate the webhook you want to test, and select **Edit**.
    2. Make your changes to the webhook.
    3. Select the **Test** dropdown list, then select the type of event to test.


Testing is not supported for some types of events for project and group webhooks. For more information, see [issue 379201](https://gitlab.com/gitlab-org/gitlab/-/issues/379201).
## Webhook reference[](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-reference "Permalink")
Use this technical reference to:
  * Understand how GitLab webhooks work.
  * Integrate webhooks with your systems.
  * Set up, troubleshoot, and optimize your webhook configurations.


### Webhook receiver requirements[](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-receiver-requirements "Permalink")
Implement fast and stable webhook receiver endpoints to ensure reliable webhook delivery.
Slow, unstable, or incorrectly configured receivers might be disabled automatically. Invalid HTTP responses are treated as failed requests.
To optimize your webhook receivers:
  1. Respond quickly with a `200` or `201` status:
     * Avoid processing webhooks in the same request.
     * Use a queue to handle webhooks after receiving them.
     * Respond before the timeout limit to prevent automatic disabling on GitLab.com.
  2. Handle potential duplicate events:
     * Prepare for duplicate events if a webhook times out.
     * Ensure your endpoint is consistently fast and stable.
  3. Minimize response headers and body:
     * GitLab stores response headers and body for later inspection.
     * Limit the number and size of returned headers.
     * Consider responding with an empty body.
  4. Use appropriate status codes:
     * Return client error status responses (`4xx` range) only for misconfigured webhooks.
     * For unsupported events, return `400` or ignore the payload.
     * Avoid `500` server error responses for handled events.


### Auto-disabled webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#auto-disabled-webhooks "Permalink")
History
  * [Introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/385902) for group webhooks in GitLab 15.10.
  * [Disabled on GitLab Self-Managed](https://gitlab.com/gitlab-org/gitlab/-/issues/390157) for project webhooks in GitLab 15.10 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `auto_disabling_web_hooks`.
  * **Fails to connect** and **Failing to connect** [renamed](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/166329) to **Disabled** and **Temporarily disabled** in GitLab 17.11.
  * [Changed](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/166329) to become permanently disabled after 40 consecutive failures in GitLab 17.11.


The availability of this feature is controlled by a feature flag. For more information, see the history.
GitLab automatically disables project or group webhooks that fail four consecutive times.
To view auto-disabled webhooks:
  1. On the top bar, select **Search or go to** and find your project or group.
  2. Select **Settings** > **Webhooks**.


In the webhook list, auto-disabled webhooks display as:
  * **Temporarily disabled** if they fail four consecutive times
  * **Disabled** if they fail 40 consecutive times


[![Webhook list showing disabled and temporarily disabled status badges.](https://docs.gitlab.com/user/project/integrations/img/failed_badges_v17_11.png)](https://docs.gitlab.com/user/project/integrations/img/failed_badges_v17_11.png)
#### Temporarily disabled webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#temporarily-disabled-webhooks "Permalink")
Webhooks are temporarily disabled if they fail four consecutive times. If webhooks fail 40 consecutive times, they become permanently disabled.
Failure occurs when:
  * The webhook receiver returns a response code in the `4xx` or `5xx` range.
  * The webhook experiences a timeout when attempting to connect to the webhook receiver.
  * The webhook encounters other HTTP errors.


Temporarily disabled webhooks are initially disabled for one minute, with the duration extending on subsequent failures up to 24 hours. After this period has elapsed, these webhooks are automatically re-enabled.
#### Permanently disabled webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#permanently-disabled-webhooks "Permalink")
Webhooks are permanently disabled if they fail 40 consecutive times. Unlike temporarily disabled webhooks, these webhooks are not automatically re-enabled.
Webhooks that were permanently disabled in GitLab 17.10 and earlier underwent a data migration. These webhooks might display four failures in **Recent events** even though the UI might state they have 40 failures.
#### Re-enable disabled webhooks[](https://docs.gitlab.com/user/project/integrations/webhooks/#re-enable-disabled-webhooks "Permalink")
To re-enable a disabled webhook, send a test request. The webhook is re-enabled if the test request returns a response code in the `2xx` range.
### Delivery headers[](https://docs.gitlab.com/user/project/integrations/webhooks/#delivery-headers "Permalink")
History
  * `X-Gitlab-Webhook-UUID` header [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/230830) in GitLab 16.2.
  * `Idempotency-Key` header [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/388692) in GitLab 17.4.


GitLab includes the following headers in webhook requests to your endpoint:
Header | Description | Example
---|---|---
`User-Agent` | User agent in the format `"Gitlab/<VERSION>"`. | `"GitLab/15.5.0-pre"`
`X-Gitlab-Instance` | Hostname of the GitLab instance that sent the webhook. | `"https://gitlab.com"`
`X-Gitlab-Webhook-UUID` | Unique ID for each webhook. | `"02affd2d-2cba-4033-917d-ec22d5dc4b38"`
`X-Gitlab-Event` | Webhook type name. Corresponds to event types in the format `"<EVENT> Hook"`. | `"Push Hook"`
`X-Gitlab-Event-UUID` | Unique ID for non-recursive webhooks. Recursive webhooks (triggered by earlier webhooks) share the same value. | `"13792a34-cac6-4fda-95a8-c58e00a3954e"`
`Idempotency-Key` | Unique ID consistent across webhook retries. Use to ensure idempotency in integrations. | `"f5e5f430-f57b-4e6e-9fac-d9128cd7232f"`
### Image URL display in webhook body[](https://docs.gitlab.com/user/project/integrations/webhooks/#image-url-display-in-webhook-body "Permalink")
GitLab rewrites relative image references to absolute URLs in webhook bodies.
#### Image URL rewriting example[](https://docs.gitlab.com/user/project/integrations/webhooks/#image-url-rewriting-example "Permalink")
If the original image reference in a merge request, comment, or wiki page is:
markdown
```
![A Markdown image with a relative URL.](/uploads/$sha/image.png)
```

The rewritten image reference in the webhook body would be:
markdown
```
![A Markdown image with an absolute URL.](https://gitlab.example.com/-/project/:id/uploads/<SHA>/image.png)
```

This example assumes:
  * GitLab is installed at `gitlab.example.com`.
  * The project ID is at `123`.


#### Exceptions to image URL rewriting[](https://docs.gitlab.com/user/project/integrations/webhooks/#exceptions-to-image-url-rewriting "Permalink")
GitLab does not rewrite image URLs when:
  * They already use HTTP, HTTPS, or protocol-relative URLs.
  * They use advanced Markdown features, such as link labels.


## Related topics[](https://docs.gitlab.com/user/project/integrations/webhooks/#related-topics "Permalink")
  * [Webhook events and JSON payloads](https://docs.gitlab.com/user/project/integrations/webhook_events/)
  * [Webhook limits](https://docs.gitlab.com/user/gitlab_com/#webhooks)
  * [Project webhooks API](https://docs.gitlab.com/api/project_webhooks/)
  * [Group webhooks API](https://docs.gitlab.com/api/group_webhooks/)
  * [System hooks API](https://docs.gitlab.com/api/system_hooks/)
  * [Troubleshooting webhooks](https://docs.gitlab.com/user/project/integrations/webhooks_troubleshooting/)
  * [Send SMS alerts with webhooks and Twilio](https://www.datadoghq.com/blog/send-alerts-sms-customizable-webhooks-twilio/)
  * [Applying GitLab labels automatically](https://about.gitlab.com/blog/applying-gitlab-labels-automatically/)


Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/user/project/integrations/webhooks.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/project/integrations/webhooks.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Webhook events](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-events)
  * [Webhook limits](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-limits)
  * [Push event limits](https://docs.gitlab.com/user/project/integrations/webhooks/#push-event-limits)
  * [Group webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#group-webhooks)
  * [Types of group webhook events](https://docs.gitlab.com/user/project/integrations/webhooks/#types-of-group-webhook-events)
  * [Webhooks in both a project and a group](https://docs.gitlab.com/user/project/integrations/webhooks/#webhooks-in-both-a-project-and-a-group)
  * [Configure webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#configure-webhooks)
  * [Create a webhook](https://docs.gitlab.com/user/project/integrations/webhooks/#create-a-webhook)
  * [Mask sensitive portions of webhook URLs](https://docs.gitlab.com/user/project/integrations/webhooks/#mask-sensitive-portions-of-webhook-urls)
  * [Custom headers](https://docs.gitlab.com/user/project/integrations/webhooks/#custom-headers)
  * [Custom webhook template](https://docs.gitlab.com/user/project/integrations/webhooks/#custom-webhook-template)
  * [Create a custom webhook template](https://docs.gitlab.com/user/project/integrations/webhooks/#create-a-custom-webhook-template)
  * [Example custom webhook template](https://docs.gitlab.com/user/project/integrations/webhooks/#example-custom-webhook-template)
  * [Filter push events by branch](https://docs.gitlab.com/user/project/integrations/webhooks/#filter-push-events-by-branch)
  * [Use a wildcard pattern](https://docs.gitlab.com/user/project/integrations/webhooks/#use-a-wildcard-pattern)
  * [Use a regular expression](https://docs.gitlab.com/user/project/integrations/webhooks/#use-a-regular-expression)
  * [Configure webhooks to support mutual TLS](https://docs.gitlab.com/user/project/integrations/webhooks/#configure-webhooks-to-support-mutual-tls)
  * [Configure firewalls for webhook traffic](https://docs.gitlab.com/user/project/integrations/webhooks/#configure-firewalls-for-webhook-traffic)
  * [Manage webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#manage-webhooks)
  * [View webhook request history](https://docs.gitlab.com/user/project/integrations/webhooks/#view-webhook-request-history)
  * [Inspect request and response details](https://docs.gitlab.com/user/project/integrations/webhooks/#inspect-request-and-response-details)
  * [Test a webhook](https://docs.gitlab.com/user/project/integrations/webhooks/#test-a-webhook)
  * [Webhook reference](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-reference)
  * [Webhook receiver requirements](https://docs.gitlab.com/user/project/integrations/webhooks/#webhook-receiver-requirements)
  * [Auto-disabled webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#auto-disabled-webhooks)
  * [Temporarily disabled webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#temporarily-disabled-webhooks)
  * [Permanently disabled webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#permanently-disabled-webhooks)
  * [Re-enable disabled webhooks](https://docs.gitlab.com/user/project/integrations/webhooks/#re-enable-disabled-webhooks)
  * [Delivery headers](https://docs.gitlab.com/user/project/integrations/webhooks/#delivery-headers)
  * [Image URL display in webhook body](https://docs.gitlab.com/user/project/integrations/webhooks/#image-url-display-in-webhook-body)
  * [Image URL rewriting example](https://docs.gitlab.com/user/project/integrations/webhooks/#image-url-rewriting-example)
  * [Exceptions to image URL rewriting](https://docs.gitlab.com/user/project/integrations/webhooks/#exceptions-to-image-url-rewriting)
  * [Related topics](https://docs.gitlab.com/user/project/integrations/webhooks/#related-topics)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/user/project/integrations/webhooks.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/user/project/integrations/webhooks.md)
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
