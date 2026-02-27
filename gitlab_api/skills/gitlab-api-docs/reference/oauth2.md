[Skip to main content](https://docs.gitlab.com/api/oauth2/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/oauth2/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/oauth2/)
    * [18.8](https://docs.gitlab.com/18.8/api/oauth2/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/oauth2/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/oauth2/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/oauth2.html)
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
  3. [OAuth 2.0 identity provider API](https://docs.gitlab.com/api/oauth2/)


* * *
# OAuth 2.0 identity provider API
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


Use this API to allow third-party services to access GitLab resources for a user with the [OAuth 2.0](https://oauth.net/2/) protocol. For more information, see [Configure GitLab as an OAuth 2.0 authentication identity provider](https://docs.gitlab.com/integration/oauth_provider/).
This functionality is based on the [doorkeeper Ruby gem](https://github.com/doorkeeper-gem/doorkeeper).
## Cross-origin resource sharing[](https://docs.gitlab.com/api/oauth2/#cross-origin-resource-sharing "Permalink")
History
  * CORS preflight request support [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/364680) in GitLab 15.1.


Many `/oauth` endpoints support cross-origin resource sharing (CORS). From GitLab 15.1, the following endpoints also support [CORS preflight requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS):
  * `/oauth/revoke`
  * `/oauth/token`
  * `/oauth/userinfo`


Only certain headers can be used for preflight requests:
  * The headers listed for [simple requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests).
  * The `Authorization` header.


For example, the `X-Requested-With` header can’t be used for preflight requests.
## Supported OAuth 2.0 flows[](https://docs.gitlab.com/api/oauth2/#supported-oauth-20-flows "Permalink")
GitLab supports the following authorization flows:
  * **Authorization code with[Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)**: Most secure. Without PKCE, you’d have to include client secrets on mobile clients, and is recommended for both client and server apps.
  * **Authorization code** : Secure and common flow. Recommended option for secure server-side apps.
  * **Resource owner password credentials** : To be used **only** for securely hosted, first-party services. GitLab recommends against use of this flow.
  * **Device Authorization Grant** (GitLab 17.1 and later) Secure flow oriented toward devices without browser access. Requires a secondary device to complete the authorization flow.


The draft specification for [OAuth 2.1](https://oauth.net/2.1/) specifically omits both the Implicit grant and Resource Owner Password Credentials flows.
Refer to the [OAuth RFC](https://www.rfc-editor.org/rfc/rfc6749) to find out how all those flows work and pick the right one for your use case.
Authorization code (with or without PKCE) flow requires `application` to be registered first via the `/user_settings/applications` page in your user’s account. During registration, by enabling proper scopes, you can limit the range of resources which the `application` can access. Upon creation, you obtain the `application` credentials: _Application ID_ and _Client Secret_. The _Client Secret_ **must be kept secure**. It is also advantageous to keep the _Application ID_ secret when your application architecture allows.
For a list of scopes in GitLab, see [the provider documentation](https://docs.gitlab.com/integration/oauth_provider/#view-all-authorized-applications).
### Prevent CSRF attacks[](https://docs.gitlab.com/api/oauth2/#prevent-csrf-attacks "Permalink")
To [protect redirect-based flows](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-13#section-3.1), the OAuth specification recommends the use of “One-time use CSRF tokens carried in the state parameter, which are securely bound to the user agent”, with each request to the `/oauth/authorize` endpoint. This can prevent [CSRF attacks](https://wiki.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29).
### Use HTTPS in production[](https://docs.gitlab.com/api/oauth2/#use-https-in-production "Permalink")
For production, use HTTPS for your `redirect_uri`. For development, GitLab allows insecure HTTP redirect URIs.
As OAuth 2.0 bases its security entirely on the transport layer, you should not use unprotected URIs. For more information, see the [OAuth 2.0 RFC](https://www.rfc-editor.org/rfc/rfc6749#section-3.1.2.1) and the [OAuth 2.0 Threat Model RFC](https://www.rfc-editor.org/rfc/rfc6819#section-4.4.2.1).
In the following sections you can find detailed instructions on how to obtain authorization with each flow.
### Authorization code with Proof Key for Code Exchange (PKCE)[](https://docs.gitlab.com/api/oauth2/#authorization-code-with-proof-key-for-code-exchange-pkce "Permalink")
History
  * Group SAML SSO support for OAuth applications [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/461212) in GitLab 18.2 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `ff_oauth_redirect_to_sso_login`. Disabled by default.
  * Group SAML SSO support for OAuth applications [enabled on GitLab.com, GitLab Self-Managed and GitLab Dedicated](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/200682) in GitLab 18.3.
  * [Generally available](https://gitlab.com/gitlab-org/gitlab/-/issues/561778) in GitLab 18.5. Feature flag `ff_oauth_redirect_to_sso_login` removed.


The [PKCE RFC](https://www.rfc-editor.org/rfc/rfc7636#section-1.1) includes a detailed flow description, from authorization request through access token. The following steps describe our implementation of the flow.
The Authorization code with PKCE flow, PKCE for short, makes it possible to securely perform the OAuth exchange of client credentials for access tokens on public clients without requiring access to the _Client Secret_ at all. This makes the PKCE flow advantageous for single page JavaScript applications or other client side apps where keeping secrets from the user is a technical impossibility.
Before starting the flow, generate the `STATE`, the `CODE_VERIFIER` and the `CODE_CHALLENGE`.
  * The `STATE` a value that can’t be predicted used by the client to maintain state between the request and callback. It should also be used as a CSRF token.
  * The `CODE_VERIFIER` is a random string, between 43 and 128 characters in length, which use the characters `A-Z`, `a-z`, `0-9`, `-`, `.`, `_`, and `~`.
  * The `CODE_CHALLENGE` is a URL-safe base64-encoded string of the SHA256 hash of the `CODE_VERIFIER`:
    * The SHA256 hash must be in binary format before encoding.
    * In Ruby, you can set that up with `Base64.urlsafe_encode64(Digest::SHA256.digest(CODE_VERIFIER), padding: false)`.
    * For reference, a `CODE_VERIFIER` string of `ks02i3jdikdo2k0dkfodf3m39rjfjsdk0wk349rj3jrhf` when hashed and encoded using the previous Ruby snippet produces a `CODE_CHALLENGE` string of `2i0WFA-0AerkjQm4X4oDEhqA17QIAKNjXpagHBXmO_U`.


  1. Request authorization code. To do that, you should redirect the user to the `/oauth/authorize` page with the following query parameters:
```
https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=STATE&scope=REQUESTED_SCOPES&code_challenge=CODE_CHALLENGE&code_challenge_method=S256&root_namespace_id=ROOT_NAMESPACE_ID
```

This page asks the user to approve the request from the app to access their account based on the scopes specified in `REQUESTED_SCOPES`. The user is then redirected back to the specified `REDIRECT_URI`. The [scope parameter](https://docs.gitlab.com/integration/oauth_provider/#view-all-authorized-applications) is a space-separated list of scopes associated with the user. For example,`scope=read_user+profile` requests the `read_user` and `profile` scopes. The `root_namespace_id` is the root namespace ID associated with the project. This optional parameter should be used when [SAML SSO](https://docs.gitlab.com/user/group/saml_sso/) is configured for the associated group. The redirect includes the authorization `code`, for example:
```
https://example.com/oauth/redirect?code=1234567890&state=STATE
```

  2. With the authorization `code` returned from the previous request (denoted as `RETURNED_CODE` in the following example), you can request an `access_token`, with any HTTP client. The following example uses Ruby’s `rest-client`:
ruby
```
parameters = 'client_id=APP_ID&code=RETURNED_CODE&grant_type=authorization_code&redirect_uri=REDIRECT_URI&code_verifier=CODE_VERIFIER'
RestClient.post 'https://gitlab.example.com/oauth/token', parameters
```

Example response:
json
```
{
 "access_token": "de6780bc506a0446309bd9362820ba8aed28aa506c71eedbe1c5c4f9dd350e54",
 "token_type": "bearer",
 "expires_in": 7200,
 "refresh_token": "8257e65c97202ed1726cf9571600918f3bffb2544b26e00a61df9897668c33a1",
 "created_at": 1607635748
}
```

  3. To retrieve a new `access_token`, use the `refresh_token` parameter. Refresh tokens may be used even after the `access_token` itself expires. This request:
     * Invalidates the existing `access_token` and `refresh_token`.
     * Sends new tokens in the response.
ruby
```
  parameters = 'client_id=APP_ID&refresh_token=REFRESH_TOKEN&grant_type=refresh_token&redirect_uri=REDIRECT_URI'
  RestClient.post 'https://gitlab.example.com/oauth/token', parameters
```

Example response:
json
```
{
  "access_token": "c97d1fe52119f38c7f67f0a14db68d60caa35ddc86fd12401718b649dcfa9c68",
  "token_type": "bearer",
  "expires_in": 7200,
  "refresh_token": "803c1fd487fec35562c205dac93e9d8e08f9d3652a24079d704df3039df1158f",
  "created_at": 1628711391
}
```



The `redirect_uri` must match the `redirect_uri` used in the original authorization request.
You can now make requests to the API with the access token.
### Authorization code flow[](https://docs.gitlab.com/api/oauth2/#authorization-code-flow "Permalink")
History
  * Group SAML SSO support for OAuth applications [introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/461212) in GitLab 18.2 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `ff_oauth_redirect_to_sso_login`. Disabled by default.
  * Group SAML SSO support for OAuth applications [enabled on GitLab.com, GitLab Self-Managed and GitLab Dedicated](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/200682) in GitLab 18.3.
  * [Generally available](https://gitlab.com/gitlab-org/gitlab/-/issues/561778) in GitLab 18.5. Feature flag `ff_oauth_redirect_to_sso_login` removed.


Check the [RFC spec](https://www.rfc-editor.org/rfc/rfc6749#section-4.1) for a detailed flow description.
The authorization code flow is essentially the same as [authorization code flow with PKCE](https://docs.gitlab.com/api/oauth2/#authorization-code-with-proof-key-for-code-exchange-pkce),
Before starting the flow, generate the `STATE`. It is a value that can’t be predicted used by the client to maintain state between the request and callback. It should also be used as a CSRF token.
  1. Request authorization code. To do that, you should redirect the user to the `/oauth/authorize` page with the following query parameters:
```
https://gitlab.example.com/oauth/authorize?client_id=APP_ID&redirect_uri=REDIRECT_URI&response_type=code&state=STATE&scope=REQUESTED_SCOPES&root_namespace_id=ROOT_NAMESPACE_ID
```

This page asks the user to approve the request from the app to access their account based on the scopes specified in `REQUESTED_SCOPES`. The user is then redirected back to the specified `REDIRECT_URI`. The [scope parameter](https://docs.gitlab.com/integration/oauth_provider/#view-all-authorized-applications) is a space-separated list of scopes associated with the user. For example,`scope=read_user+profile` requests the `read_user` and `profile` scopes. The `root_namespace_id` is the root namespace ID associated with the project. This optional parameter should be used when [SAML SSO](https://docs.gitlab.com/user/group/saml_sso/) is configured for the associated group. The redirect includes the authorization `code`, for example:
```
https://example.com/oauth/redirect?code=1234567890&state=STATE
```

  2. With the authorization `code` returned from the previous request (shown as `RETURNED_CODE` in the following example), you can request an `access_token`, with any HTTP client. The following example uses Ruby’s `rest-client`:
ruby
```
parameters = 'client_id=APP_ID&client_secret=APP_SECRET&code=RETURNED_CODE&grant_type=authorization_code&redirect_uri=REDIRECT_URI'
RestClient.post 'https://gitlab.example.com/oauth/token', parameters
```

Example response:
json
```
{
 "access_token": "de6780bc506a0446309bd9362820ba8aed28aa506c71eedbe1c5c4f9dd350e54",
 "token_type": "bearer",
 "expires_in": 7200,
 "refresh_token": "8257e65c97202ed1726cf9571600918f3bffb2544b26e00a61df9897668c33a1",
 "created_at": 1607635748
}
```

  3. To retrieve a new `access_token`, use the `refresh_token` parameter. Refresh tokens may be used even after the `access_token` itself expires. This request:
     * Invalidates the existing `access_token` and `refresh_token`.
     * Sends new tokens in the response.
ruby
```
  parameters = 'client_id=APP_ID&client_secret=APP_SECRET&refresh_token=REFRESH_TOKEN&grant_type=refresh_token&redirect_uri=REDIRECT_URI'
  RestClient.post 'https://gitlab.example.com/oauth/token', parameters
```

Example response:
json
```
{
  "access_token": "c97d1fe52119f38c7f67f0a14db68d60caa35ddc86fd12401718b649dcfa9c68",
  "token_type": "bearer",
  "expires_in": 7200,
  "refresh_token": "803c1fd487fec35562c205dac93e9d8e08f9d3652a24079d704df3039df1158f",
  "created_at": 1628711391
}
```



The `redirect_uri` must match the `redirect_uri` used in the original authorization request.
You can now make requests to the API with the access token returned.
### Device authorization grant flow[](https://docs.gitlab.com/api/oauth2/#device-authorization-grant-flow "Permalink")
History
  * [Introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/332682) in GitLab 17.2 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `oauth2_device_grant_flow`.
  * [Enabled](https://gitlab.com/gitlab-org/gitlab/-/issues/468479) by default in 17.3.
  * [Generally available](https://gitlab.com/gitlab-org/gitlab/-/issues/505557) in GitLab 17.9. Feature flag `oauth2_device_grant_flow` removed.


Check the [RFC spec](https://datatracker.ietf.org/doc/html/rfc8628#section-3.1) for a detailed description of the device authorization grant flow, from device authorization request to token response from the browser login.
The device authorization grant flow makes it possible to securely authenticate your GitLab identity from input constrained devices where browser interactions are not an option.
This makes the device authorization grant flow ideal for users attempting to use GitLab services from headless servers or other devices with no, or limited, UI.
  1. To request device authorization, a request is sent from the input-limited device client to `https://gitlab.example.com/oauth/authorize_device`. For example:
ruby
```
  parameters = 'client_id=UID&scope=read'
  RestClient.post 'https://gitlab.example.com/oauth/authorize_device', parameters
```

After a successful request, a response containing a `verification_uri` is returned to the user. For example:
json
```
{
    "device_code": "GmRhmhcxhwAzkoEqiMEg_DnyEysNkuNhszIySk9eS",
    "user_code": "0A44L90H",
    "verification_uri": "https://gitlab.example.com/oauth/device",
    "verification_uri_complete": "https://gitlab.example.com/oauth/device?user_code=0A44L90H",
    "expires_in": 300,
    "interval": 5
}
```

  2. The device client displays the `user_code` and `verification_uri` from the response to the requesting user. That user then, on a secondary device with browser access:
    1. Goes to the provided URI.
    2. Enters the user code.
    3. Completes an authentication as prompted.
  3. Immediately after displaying the `verification_uri` and `user_code`, the device client begins polling the token endpoint with the associated `device_code` returned in the initial response:
ruby
```
parameters = 'grant_type=urn:ietf:params:oauth:grant-type:device_code
&device_code=GmRhmhcxhwAzkoEqiMEg_DnyEysNkuNhszIySk9eS
&client_id=1406020730'
RestClient.post 'https://gitlab.example.com/oauth/token', parameters
```

  4. The device client receives a response from the token endpoint. If the authorization was successful, a success response is returned, otherwise, an error response is returned. Potential error responses are categorized by either of the following:
     * Those defined by the OAuth Authorization Framework access token error responses.
     * Those specific to the device authorization grant flow described here.
Those error responses specific to the device flow are described in the following content. For more information on each potential response, see the relevant [RFC spec for device authorization grant](https://datatracker.ietf.org/doc/html/rfc8628#section-3.5) and the [RFC spec for authorization tokens](https://datatracker.ietf.org/doc/html/rfc6749#section-5.2).
Example response:
json
```
{
  "error": "authorization_pending",
  "error_description": "..."
}
```

On receipt of this response, the device client continues polling.
If the polling interval is too short, a slow down error response is returned. For example:
json
```
{
  "error": "slow_down",
  "error_description": "..."
}
```

On receipt of this response, the device client reduces its polling rate and continues polling at the new rate.
If the device code expires before authentication is complete, an expired token error response is returned. For example:
json
```
{
  "error": "expired_token",
  "error_description": "..."
}
```

At that point, the device-client should stop and initiate a new device authorization request.
If the authorization request was denied, an access denied error response is returned. For example:
json
```
{
  "error": "access_denied",
  "error_description": "..."
}
```

The authentication request has been rejected. The user should verify their credentials or contact their system administrator
  5. After the user successfully authenticates, a success response is returned:
json
```
{
    "access_token": "TOKEN",
    "token_type": "Bearer",
    "expires_in": 7200,
    "scope": "read",
    "created_at": 1593096829
}
```



At this point, the device authentication flow is complete. The returned `access_token` can be provided to GitLab to authenticate the user identity when accessing GitLab resources, such as when cloning over HTTPS or accessing the API.
A sample application that implements the client side device flow can be found at: <https://gitlab.com/johnwparent/git-auth-over-https>.
### Resource owner password credentials flow[](https://docs.gitlab.com/api/oauth2/#resource-owner-password-credentials-flow "Permalink")
Check the [RFC spec](https://www.rfc-editor.org/rfc/rfc6749#section-4.3) for a detailed flow description.
Resource owner password credentials are disabled for users with [two-factor authentication](https://docs.gitlab.com/user/profile/account/two_factor_authentication/) turned on and [enterprise users](https://docs.gitlab.com/user/enterprise_user/) with [password authentication disabled for their group](https://docs.gitlab.com/user/enterprise_user/#restrict-authentication-methods). These users can access the API using [personal access tokens](https://docs.gitlab.com/user/profile/personal_access_tokens/) instead.
Ensure the [**Allow password authentication for Git over HTTP(S)**](https://docs.gitlab.com/administration/settings/sign_in_restrictions/#allow-password-authentication-for-git-over-https) checkbox is selected for the GitLab instance to support the password credentials flow.
In this flow, a token is requested in exchange for the resource owner credentials (username and password).
The credentials should only be used when:
  * There is a high degree of trust between the resource owner and the client. For example, the client is part of the device operating system or a highly privileged application.
  * Other authorization grant types are not available (such as an authorization code).


Never store the user’s credentials and only use this grant type when your client is deployed to a trusted environment, in 99% of cases [personal access tokens](https://docs.gitlab.com/user/profile/personal_access_tokens/) are a better choice.
Even though this grant type requires direct client access to the resource owner credentials, the resource owner credentials are used for a single request and are exchanged for an access token. This grant type can eliminate the need for the client to store the resource owner credentials for future use, by exchanging the credentials with a long-lived access token or refresh token.
To request an access token, you must make a POST request to `/oauth/token` with the following parameters:
json
```
{
  "grant_type"    : "password",
  "username"      : "user@example.com",
  "password"      : "secret"
}
```

Example cURL request:
shell
```
echo 'grant_type=password&username=<your_username>&password=<your_password>' > auth.txt
curl --request POST \
  --url "https://gitlab.example.com/oauth/token" \
  --data "@auth.txt"
```

You can also use this grant flow with registered OAuth applications, by using HTTP Basic Authentication with the application’s `client_id` and `client_secret`:
shell
```
echo 'grant_type=password&username=<your_username>&password=<your_password>' > auth.txt
curl --request POST \
  --url "https://gitlab.example.com/oauth/token" \
  --data "@auth.txt" \
  --user client_id:client_secret
```

Then, you receive a response containing the access token:
json
```
{
  "access_token": "1f0af717251950dbd4d73154fdf0a474a5c5119adad999683f5b450c460726aa",
  "token_type": "bearer",
  "expires_in": 7200
}
```

By default, the scope of the access token is `api`, which provides complete read/write access.
For testing, you can use the `oauth2` Ruby gem:
ruby
```
client = OAuth2::Client.new('the_client_id', 'the_client_secret', :site => "https://example.com")
access_token = client.password.get_token('user@example.com', 'secret')
puts access_token.token
```

## Access GitLab API with `access token`[](https://docs.gitlab.com/api/oauth2/#access-gitlab-api-with-access-token "Permalink")
The `access token` allows you to make requests to the API on behalf of a user. You can pass the token either as GET parameter:
```
GET https://gitlab.example.com/api/v4/user?access_token=OAUTH-TOKEN
```

or you can put the token to the Authorization header:
shell
```
curl --header "Authorization: Bearer OAUTH-TOKEN" "https://gitlab.example.com/api/v4/user"
```

## Access Git over HTTPS with `access token`[](https://docs.gitlab.com/api/oauth2/#access-git-over-https-with-access-token "Permalink")
A token with [scope](https://docs.gitlab.com/integration/oauth_provider/#view-all-authorized-applications) `read_repository` or `write_repository` can access Git over HTTPS. Use the token as the password. You can set the username to any string value. You should use `oauth2`:
```
https://oauth2:<your_access_token>@gitlab.example.com/project_path/project_name.git
```

Alternatively, you can use a [Git credential helper](https://docs.gitlab.com/user/profile/account/two_factor_authentication/#oauth-credential-helpers) to authenticate to GitLab with OAuth. This handles OAuth token refresh automatically.
## Retrieve the token information[](https://docs.gitlab.com/api/oauth2/#retrieve-the-token-information "Permalink")
To verify the details of a token, use the `token/info` endpoint provided by the Doorkeeper gem. For more information, see [`/oauth/token/info`](https://github.com/doorkeeper-gem/doorkeeper/wiki/API-endpoint-descriptions-and-examples#get----oauthtokeninfo).
You must supply the access token, either:
  * As a parameter:
```
GET https://gitlab.example.com/oauth/token/info?access_token=<OAUTH-TOKEN>
```

  * In the Authorization header:
shell
```
curl --header "Authorization: Bearer <OAUTH-TOKEN>" "https://gitlab.example.com/oauth/token/info"
```



The following is an example response:
json
```
{
    "resource_owner_id": 1,
    "scope": ["api"],
    "expires_in": null,
    "application": {"uid": "1cb242f495280beb4291e64bee2a17f330902e499882fe8e1e2aa875519cab33"},
    "created_at": 1575890427
}
```

### Deprecated fields[](https://docs.gitlab.com/api/oauth2/#deprecated-fields "Permalink")
The fields `scopes` and `expires_in_seconds` are included in the response but are now deprecated. The `scopes` field is an alias for `scope`, and the `expires_in_seconds` field is an alias for `expires_in`. For more information, see [Doorkeeper API changes](https://github.com/doorkeeper-gem/doorkeeper/wiki/Migration-from-old-versions#api-changes-5).
## Revoke a token[](https://docs.gitlab.com/api/oauth2/#revoke-a-token "Permalink")
To revoke a token, use the `revoke` endpoint. The API returns a 200 response code and an empty JSON hash to indicate success.
ruby
```
parameters = 'client_id=APP_ID&client_secret=APP_SECRET&token=TOKEN'
RestClient.post 'https://gitlab.example.com/oauth/revoke', parameters
```

## OAuth 2.0 tokens and GitLab registries[](https://docs.gitlab.com/api/oauth2/#oauth-20-tokens-and-gitlab-registries "Permalink")
Standard OAuth 2.0 tokens support different degrees of access to GitLab registries, as they:
  * Do not allow users to authenticate to:
    * The GitLab [container registry](https://docs.gitlab.com/user/packages/container_registry/authenticate_with_container_registry/).
    * Packages listed in the GitLab [Package registry](https://docs.gitlab.com/user/packages/package_registry/).
    * [Virtual registries](https://docs.gitlab.com/user/packages/virtual_registry/).
  * Allow users to get, list, and delete registries through the [container registry API](https://docs.gitlab.com/api/container_registry/).
  * Allow users to get, list, and delete registry objects through the [Maven virtual registry API](https://docs.gitlab.com/api/maven_virtual_registries/).


Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/oauth2.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/oauth2.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Cross-origin resource sharing](https://docs.gitlab.com/api/oauth2/#cross-origin-resource-sharing)
  * [Supported OAuth 2.0 flows](https://docs.gitlab.com/api/oauth2/#supported-oauth-20-flows)
  * [Prevent CSRF attacks](https://docs.gitlab.com/api/oauth2/#prevent-csrf-attacks)
  * [Use HTTPS in production](https://docs.gitlab.com/api/oauth2/#use-https-in-production)
  * [Authorization code with Proof Key for Code Exchange (PKCE)](https://docs.gitlab.com/api/oauth2/#authorization-code-with-proof-key-for-code-exchange-pkce)
  * [Authorization code flow](https://docs.gitlab.com/api/oauth2/#authorization-code-flow)
  * [Device authorization grant flow](https://docs.gitlab.com/api/oauth2/#device-authorization-grant-flow)
  * [Resource owner password credentials flow](https://docs.gitlab.com/api/oauth2/#resource-owner-password-credentials-flow)
  * [Access GitLab API with access token](https://docs.gitlab.com/api/oauth2/#access-gitlab-api-with-access-token)
  * [Access Git over HTTPS with access token](https://docs.gitlab.com/api/oauth2/#access-git-over-https-with-access-token)
  * [Retrieve the token information](https://docs.gitlab.com/api/oauth2/#retrieve-the-token-information)
  * [Deprecated fields](https://docs.gitlab.com/api/oauth2/#deprecated-fields)
  * [Revoke a token](https://docs.gitlab.com/api/oauth2/#revoke-a-token)
  * [OAuth 2.0 tokens and GitLab registries](https://docs.gitlab.com/api/oauth2/#oauth-20-tokens-and-gitlab-registries)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/oauth2.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/oauth2.md)
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


![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fmilestones%2F&_biz_t=1772174335855&_biz_i=Project%20milestones%20API%20%7C%20GitLab%20Docs&_biz_n=97&rnd=306290&cdn_o=a&_biz_z=1772174336263)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Fnotes%2F&_biz_t=1772174336228&_biz_i=Notes%20API%20%7C%20GitLab%20Docs&_biz_n=98&rnd=194904&cdn_o=a&_biz_z=1772174336267)![](https://cdn.bizible.com/ipv?_biz_r=&_biz_h=800054037&_biz_u=10503924d6784ad3f2d352558587a67a&_biz_l=https%3A%2F%2Fdocs.gitlab.com%2Fapi%2Foauth2%2F&_biz_t=1772174336262&_biz_i=OAuth%202.0%20identity%20provider%20API%20%7C%20GitLab%20Docs&_biz_n=99&rnd=169391&cdn_o=a&_biz_z=1772174336267)
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
