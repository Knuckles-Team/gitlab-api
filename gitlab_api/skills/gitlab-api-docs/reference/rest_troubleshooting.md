[Skip to main content](https://docs.gitlab.com/api/rest/troubleshooting/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/rest/troubleshooting/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/rest/troubleshooting/)
    * [18.8](https://docs.gitlab.com/18.8/api/rest/troubleshooting/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/rest/troubleshooting/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/rest/troubleshooting/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/rest/troubleshooting.html)
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
  4. [Troubleshooting](https://docs.gitlab.com/api/rest/troubleshooting/)


* * *
# Troubleshooting the REST API
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


When working with the REST API, you might encounter an issue.
To troubleshoot, refer to the REST API status codes. It might also help to include the HTTP response headers and exit code.
## Status codes[](https://docs.gitlab.com/api/rest/troubleshooting/#status-codes "Permalink")
The GitLab REST API returns a status code with every response, according to context and action. The status code returned by a request can be useful when troubleshooting.
The following table gives an overview of how the API functions generally behave.
Request type | Description
---|---
`GET` | Access one or more resources and return the result as JSON.
`POST` | Returns `201 Created` if the resource is successfully created and return the newly created resource as JSON.
`GET` / `PUT` / `PATCH` | Returns `200 OK` if the resource is accessed or modified successfully. The (modified) result is returned as JSON.
`DELETE` | Returns `204 No Content` if the resource was deleted successfully or `202 Accepted` if the resource is scheduled to be deleted.
The following table shows the possible return codes for API requests.
Return values | Description
---|---
`200 OK` | The `GET`, `PUT`, `PATCH` or `DELETE` request was successful, and the resource itself is returned as JSON.
`201 Created` | The `POST` request was successful, and the resource is returned as JSON.
`202 Accepted` | The `GET`, `PUT` or `DELETE` request was successful, and the resource is scheduled for processing.
`204 No Content` | The server has successfully fulfilled the request, and there is no additional content to send in the response payload body.
`301 Moved Permanently` | The resource has been definitively moved to the URL given by the `Location` headers.
`304 Not Modified` | The resource hasn’t been modified since the last request.
`400 Bad Request` | A required attribute of the API request is missing. For example, the title of an issue is not given.
`401 Unauthorized` | The user isn’t authenticated. A valid [user token](https://docs.gitlab.com/api/rest/authentication/) is necessary.
`403 Forbidden` | The request isn’t allowed. For example, the user isn’t allowed to delete a project.
`404 Not Found` | A resource couldn’t be accessed. For example, an ID for a resource couldn’t be found, or the user isn’t authorized to access the resource.
`405 Method Not Allowed` | The request isn’t supported.
`409 Conflict` | A conflicting resource already exists.
`412 Precondition Failed` | The request was denied. This can happen if the `If-Unmodified-Since` header is provided when trying to delete a resource, which was modified in between.
`422 Unprocessable` | The entity couldn’t be processed.
`429 Too Many Requests` | The user exceeded the [application rate limits](https://docs.gitlab.com/administration/instance_limits/#rate-limits).
`500 Server Error` | While handling the request, something went wrong on the server.
`503 Service Unavailable` | The server cannot handle the request because the server is temporarily overloaded.
### Status code 400[](https://docs.gitlab.com/api/rest/troubleshooting/#status-code-400 "Permalink")
When working with the API you may encounter validation errors, in which case the API returns an HTTP `400` error.
Such errors appear in the following cases:
  * A required attribute of the API request is missing (for example, the title of an issue isn’t given).
  * An attribute did not pass the validation (for example, the user bio is too long).


When an attribute is missing, you receive something like:
http
```
HTTP/1.1 400 Bad Request
Content-Type: application/json
{
    "message":"400 (Bad request) \"title\" not given"
}
```

When a validation error occurs, error messages are different. They hold all details of validation errors:
http
```
HTTP/1.1 400 Bad Request
Content-Type: application/json
{
    "message": {
        "bio": [
            "is too long (maximum is 255 characters)"
        ]
    }
}
```

This makes error messages more machine-readable. The format can be described as follows:
json
```
{
    "message": {
        "<property-name>": [
            "<error-message>",
            "<error-message>",
            ...
        ],
        "<embed-entity>": {
            "<property-name>": [
                "<error-message>",
                "<error-message>",
                ...
            ],
        }
    }
}
```

## Include HTTP response headers[](https://docs.gitlab.com/api/rest/troubleshooting/#include-http-response-headers "Permalink")
The HTTP response headers can provide extra information when troubleshooting.
To include HTTP response headers in the response, use the `--include` option:
shell
```
curl --request GET \
  --include \
  --url "https://gitlab.example.com/api/v4/projects"
HTTP/2 200
...
```

## Include HTTP exit code[](https://docs.gitlab.com/api/rest/troubleshooting/#include-http-exit-code "Permalink")
The HTTP exit code in the API response can provide extra information when troubleshooting.
To include the HTTP exit code, include the `--fail` option:
shell
```
curl --request GET \
  --fail \
  --url "https://gitlab.example.com/api/v4/does-not-exist"
curl: (22) The requested URL returned error: 404
```

## Requests detected as spam[](https://docs.gitlab.com/api/rest/troubleshooting/#requests-detected-as-spam "Permalink")
REST API requests can be detected as spam. If a request is detected as spam and:
  * A CAPTCHA service is not configured, an error response is returned. For example:
json
```
{"message":{"error":"Your snippet has been recognized as spam and has been discarded."}}
```

  * A CAPTCHA service is configured, you receive a response with:
    * `needs_captcha_response` set to `true`.
    * The `spam_log_id` and `captcha_site_key` fields set.
For example:
json
```
{"needs_captcha_response":true,"spam_log_id":42,"captcha_site_key":"REDACTED","message":{"error":"Your snippet has been recognized as spam. Please, change the content or solve the reCAPTCHA to proceed."}}
```

    * Use the `captcha_site_key` to obtain a CAPTCHA response value using the appropriate CAPTCHA API. Only [Google reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display) is supported.
    * Resubmit the request with the `X-GitLab-Captcha-Response` and `X-GitLab-Spam-Log-Id` headers set.
shell
```
export CAPTCHA_RESPONSE="<CAPTCHA response obtained from CAPTCHA service>"
export SPAM_LOG_ID="<spam_log_id obtained from initial REST response>"

curl --request POST \
  --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" \
  --header "X-GitLab-Captcha-Response: $CAPTCHA_RESPONSE" \
  --header "X-GitLab-Spam-Log-Id: $SPAM_LOG_ID" \
  --url "https://gitlab.example.com/api/v4/snippets?title=Title&file_name=FileName&content=Content&visibility=public"
```



## Error: `404 Not Found` when using a reverse proxy[](https://docs.gitlab.com/api/rest/troubleshooting/#error-404-not-found-when-using-a-reverse-proxy "Permalink")
If your GitLab instance uses a reverse proxy, you might see `404 Not Found` errors when using a GitLab [editor extension](https://docs.gitlab.com/editor_extensions/), the GitLab CLI, or API calls with URL-encoded parameters.
This problem occurs when your reverse proxy decodes characters like `/`, `?`, and `@` before passing the parameters on to GitLab.
To resolve this problem, edit the configuration for your reverse proxy:
  * In the `VirtualHost` section, add `AllowEncodedSlashes NoDecode`.
  * In the `Location` section, edit `ProxyPass` and add the `nocanon` flag.


For example:
  * [Apache configuration](https://docs.gitlab.com/api/rest/troubleshooting/)
  * [NGINX configuration](https://docs.gitlab.com/api/rest/troubleshooting/)


```
<VirtualHost *:443>
  ServerName git.example.com

  SSLEngine on
  SSLCertificateFile     /etc/letsencrypt/live/git.example.com/fullchain.pem
  SSLCertificateKeyFile  /etc/letsencrypt/live/git.example.com/privkey.pem
  SSLVerifyClient None

  ProxyRequests     Off
  ProxyPreserveHost On
  AllowEncodedSlashes NoDecode

  <Location />
     ProxyPass http://127.0.0.1:8080/ nocanon
     ProxyPassReverse http://127.0.0.1:8080/
     Order deny,allow
     Allow from all
  </Location>
</VirtualHost>
```

```
server {
  listen       80;
  server_name  gitlab.example.com;
  location / {
     proxy_pass    http://ip:port;
     proxy_set_header        X-Forwarded-Proto $scheme;
     proxy_set_header        Host              $http_host;
     proxy_set_header        X-Real-IP         $remote_addr;
     proxy_set_header        X-Forwarded-For   $proxy_add_x_forwarded_for;
     proxy_read_timeout    300;
     proxy_connect_timeout 300;
  }
}
```

For more information, see [issue 18775](https://gitlab.com/gitlab-org/gitlab/-/issues/18775).
Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/troubleshooting.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/troubleshooting.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Status codes](https://docs.gitlab.com/api/rest/troubleshooting/#status-codes)
  * [Status code 400](https://docs.gitlab.com/api/rest/troubleshooting/#status-code-400)
  * [Include HTTP response headers](https://docs.gitlab.com/api/rest/troubleshooting/#include-http-response-headers)
  * [Include HTTP exit code](https://docs.gitlab.com/api/rest/troubleshooting/#include-http-exit-code)
  * [Requests detected as spam](https://docs.gitlab.com/api/rest/troubleshooting/#requests-detected-as-spam)
  * [Error: 404 Not Found when using a reverse proxy](https://docs.gitlab.com/api/rest/troubleshooting/#error-404-not-found-when-using-a-reverse-proxy)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/troubleshooting.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/troubleshooting.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Frest%2Ftroubleshooting%2F&_biz_t=1772174456740&_biz_i=Troubleshooting%20the%20REST%20API%20%7C%20GitLab%20Docs&_biz_n=163&rnd=646182&cdn_o=a&_biz_z=1772174456741)
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
