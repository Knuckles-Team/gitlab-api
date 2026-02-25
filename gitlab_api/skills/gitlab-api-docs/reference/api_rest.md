[Skip to main content](https://docs.gitlab.com/api/rest/#skipTarget) [Go to GitLab Docs homepage](https://docs.gitlab.com/)
`/`
[What's new?](https://about.gitlab.com/releases/whats-new/)
English
  * Language
  * English
  * 日本語


v18.10
  *     * [18.10 (not yet released)](https://docs.gitlab.com/api/rest/)
  *     * [18.9 (recently released)](https://docs.gitlab.com/18.9/api/rest/)
    * [18.8](https://docs.gitlab.com/18.8/api/rest/)
    * [18.7](https://archives.docs.gitlab.com/18.7/api/rest/)
  *     * [17.11](https://archives.docs.gitlab.com/17.11/api/rest/)
    * [16.11](https://archives.docs.gitlab.com/16.11/ee/api/rest/index.html)
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


* * *
# REST API
  * Tier: Free, Premium, Ultimate
  * Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated


Automate your workflows and build integrations with the GitLab REST API:
  * Create custom tools to manage your GitLab resources at scale without manual intervention.
  * Improve collaboration by integrating GitLab data directly into your applications.
  * Manage CI/CD processes across multiple projects with precision.
  * Control user access programmatically to maintain consistent permissions across your organization.


The REST API uses standard HTTP methods and JSON data formats for compatibility with your existing tools and systems.
## Make a REST API request[](https://docs.gitlab.com/api/rest/#make-a-rest-api-request "Permalink")
To make a REST API request:
  * Submit a request to an API endpoint by using a REST API client.
  * The GitLab instance responds to the request. It returns a status code and if applicable, the requested data. The status code indicates the outcome of the request and is useful when [troubleshooting](https://docs.gitlab.com/api/rest/troubleshooting/).


A REST API request must start with the root endpoint and the path.
  * The root endpoint is the GitLab host name.
  * The path must start with `/api/v4` (`v4` represents the API version).


In the following example, the API request retrieves the list of all projects on GitLab host `gitlab.example.com`:
shell
```
curl --request GET \
  --url "https://gitlab.example.com/api/v4/projects"
```

Access to some endpoints require authentication. For more information, see [Authentication](https://docs.gitlab.com/api/rest/authentication/).
## Rate limits[](https://docs.gitlab.com/api/rest/#rate-limits "Permalink")
REST API requests are subject to rate limit settings. These settings reduce the risk of a GitLab instance being overloaded.
  * For details, see [Rate limits](https://docs.gitlab.com/security/rate_limits/).
  * For details of the rate limit settings used by GitLab.com, see [GitLab.com-specific rate limits](https://docs.gitlab.com/user/gitlab_com/#rate-limits-on-gitlabcom).


## Response format[](https://docs.gitlab.com/api/rest/#response-format "Permalink")
REST API responses are returned in JSON format. Some API endpoints also support plain text format. To confirm which content type an endpoint supports, see the [REST API resources](https://docs.gitlab.com/api/api_resources/).
## Request requirements[](https://docs.gitlab.com/api/rest/#request-requirements "Permalink")
Some REST API requests have specific requirements, including the data format and encoding used.
### Request payload[](https://docs.gitlab.com/api/rest/#request-payload "Permalink")
API requests can use parameters sent as [query strings](https://en.wikipedia.org/wiki/Query_string) or as a [payload body](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-p3-payload-14#section-3.2). GET requests usually send a query string, while PUT or POST requests usually send the payload body:
  * Query string:
shell
```
curl --request POST \
  --url "https://gitlab.example.com/api/v4/projects?name=<example-name>&description=<example-description>"
```

  * Request payload (JSON):
shell
```
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"name":"<example-name>", "description":"<example-description>"}' "https://gitlab.example.com/api/v4/projects"
```



URL-encoded query strings have a length limitation. Requests that are too large result in a `414 Request-URI Too Large` error message. This can be resolved by using a payload body instead.
### Path parameters[](https://docs.gitlab.com/api/rest/#path-parameters "Permalink")
If an endpoint has path parameters, the documentation displays them with a preceding colon.
For example:
```
DELETE /projects/:id/share/:group_id
```

The `:id` path parameter needs to be replaced with the project ID, and the `:group_id` needs to be replaced with the ID of the group. The colons `:` shouldn’t be included.
The resulting cURL request for a project with ID `5` and a group ID of `17` is then:
shell
```
curl --request DELETE \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --url "https://gitlab.example.com/api/v4/projects/5/share/17"
```

Path parameters that are required to be URL-encoded must be followed. If not, it doesn’t match an API endpoint and responds with a 404. If there’s something in front of the API (for example, Apache), ensure that it doesn’t decode the URL-encoded path parameters.
###  `id` vs `iid`[](https://docs.gitlab.com/api/rest/#id-vs-iid "Permalink")
Some API resources have two similarly-named fields. For example, [issues](https://docs.gitlab.com/api/issues/), [merge requests](https://docs.gitlab.com/api/merge_requests/), and [project milestones](https://docs.gitlab.com/api/milestones/). The fields are:
  * `id`: ID that is unique across all projects.
  * `iid`: Additional, internal ID (displayed in the web UI) that’s unique in the scope of a single project.


If a resource has both the `iid` field and the `id` field, the `iid` field is usually used instead of `id` to fetch the resource.
For example, suppose a project with `id: 42` has an issue with `id: 46` and `iid: 5`. In this case:
  * A valid API request to retrieve the issue is `GET /projects/42/issues/5`.
  * An invalid API request to retrieve the issue is `GET /projects/42/issues/46`.


Not all resources with the `iid` field are fetched by `iid`. For guidance regarding which field to use, see the documentation for the specific resource.
### Encoding[](https://docs.gitlab.com/api/rest/#encoding "Permalink")
When making a REST API request, some content must be encoded to account for special characters and data structures.
#### Namespaced paths[](https://docs.gitlab.com/api/rest/#namespaced-paths "Permalink")
If using namespaced API requests, make sure that the `NAMESPACE/PROJECT_PATH` is URL-encoded.
For example, `/` is represented by `%2F`:
```
GET /api/v4/projects/diaspora%2Fdiaspora
```

A project’s path isn’t necessarily the same as its name. A project’s path is found in the project’s URL or in the project’s settings, under **General** > **Advanced** > **Change path**.
#### File path, branches, and tags name[](https://docs.gitlab.com/api/rest/#file-path-branches-and-tags-name "Permalink")
If a file path, branch or tag contains a `/`, make sure it is URL-encoded.
For example, `/` is represented by `%2F`:
```
GET /api/v4/projects/1/repository/files/src%2FREADME.md?ref=master
GET /api/v4/projects/1/branches/my%2Fbranch/commits
GET /api/v4/projects/1/repository/tags/my%2Ftag
```

#### Array and hash types[](https://docs.gitlab.com/api/rest/#array-and-hash-types "Permalink")
You can request the API with `array` and `hash` types parameters:
#####  `array`[](https://docs.gitlab.com/api/rest/#array "Permalink")
`import_sources` is a parameter of type `array`:
shell
```
curl --request POST \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  -d "import_sources[]=github" \
  -d "import_sources[]=bitbucket" \
  --url "https://gitlab.example.com/api/v4/some_endpoint"
```

#####  `hash`[](https://docs.gitlab.com/api/rest/#hash "Permalink")
`override_params` is a parameter of type `hash`:
shell
```
curl --request POST \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --form "namespace=email" \
  --form "path=impapi" \
  --form "file=@/path/to/somefile.txt" \
  --form "override_params[visibility]=private" \
  --form "override_params[some_other_param]=some_value" \
  --url "https://gitlab.example.com/api/v4/projects/import"
```

##### Array of hashes[](https://docs.gitlab.com/api/rest/#array-of-hashes "Permalink")
`variables` is a parameter of type `array` containing hash key/value pairs `[{ 'key': 'UPLOAD_TO_S3', 'value': 'true' }]`:
shell
```
curl --globoff --request POST \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --url "https://gitlab.example.com/api/v4/projects/169/pipeline?ref=master&variables[0][key]=VAR1&variables[0][value]=hello&variables[1][key]=VAR2&variables[1][value]=world"

curl --request POST \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{ "ref": "master", "variables": [ {"key": "VAR1", "value": "hello"}, {"key": "VAR2", "value": "world"} ] }' \
  --url "https://gitlab.example.com/api/v4/projects/169/pipeline"
```

#### Encoding `+` in ISO 8601 dates[](https://docs.gitlab.com/api/rest/#encoding--in-iso-8601-dates "Permalink")
If you need to include a `+` in a query parameter, you may need to use `%2B` instead, due to a [W3 recommendation](https://www.w3.org/Addressing/URL/4_URI_Recommentations.html) that causes a `+` to be interpreted as a space. For example, in an ISO 8601 date, you may want to include a specific time in ISO 8601 format, such as:
```
2017-10-17T23:11:13.000+05:30
```

The correct encoding for the query parameter would be:
```
2017-10-17T23:11:13.000%2B05:30
```

## Evaluating a response[](https://docs.gitlab.com/api/rest/#evaluating-a-response "Permalink")
In some circumstances the API response may not be as you expect. Issues can include null values and redirection. If you receive a numeric status code in the response, see [Status codes](https://docs.gitlab.com/api/rest/troubleshooting/#status-codes).
###  `null` vs `false`[](https://docs.gitlab.com/api/rest/#null-vs-false "Permalink")
In API responses, some boolean fields can have `null` values. A `null` boolean has no default value and is neither `true` nor `false`. GitLab treats `null` values in boolean fields the same as `false`.
In boolean arguments, you should only set `true` or `false` values (not `null`).
### Redirects[](https://docs.gitlab.com/api/rest/#redirects "Permalink")
History
  * Introduced in GitLab 16.4 [with a flag](https://docs.gitlab.com/administration/feature_flags/) named `api_redirect_moved_projects`. Disabled by default.
  * [Generally available](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/137578) in GitLab 16.7. Feature flag `api_redirect_moved_projects` removed.


After [path changes](https://docs.gitlab.com/user/project/repository/#repository-path-changes) the REST API might respond with a message noting that the endpoint has moved. When this happens, use the endpoint specified in the `Location` header.
Example of a project moved to a different path:
shell
```
curl --request GET \
  --verbose \
  --url "https://gitlab.example.com/api/v4/projects/gitlab-org%2Fold-path-project"
```

The response is:
```
...
< Location: http://gitlab.example.com/api/v4/projects/81
...
This resource has been moved permanently to https://gitlab.example.com/api/v4/projects/81
```

## Pagination[](https://docs.gitlab.com/api/rest/#pagination "Permalink")
GitLab supports the following pagination methods:
  * Offset-based pagination. The default method and available on all endpoints except, in GitLab 16.5 and later, the `users` endpoint.
  * Keyset-based pagination. Added to selected endpoints but being [progressively rolled out](https://gitlab.com/groups/gitlab-org/-/epics/2039).


For large collections, you should use keyset pagination (when available) instead of offset pagination, for performance reasons.
### Offset-based pagination[](https://docs.gitlab.com/api/rest/#offset-based-pagination "Permalink")
History
  * The `users` endpoint was [deprecated](https://gitlab.com/gitlab-org/gitlab/-/issues/426547) for offset-based pagination in GitLab 16.5 and is planned for removal in 17.0. This change is a breaking change. Use keyset-based pagination for this endpoint instead.
  * The `users` endpoint enforces keyset-based pagination when the number of requested records is greater than 50,000 in GitLab 17.0.


Sometimes, the returned result spans many pages. When listing resources, you can pass the following parameters:
Parameter | Description
---|---
`page` | Page number (default: `1`).
`per_page` | Number of items to list per page (default: `20`, max: `100`).
The following example lists 50 [namespaces](https://docs.gitlab.com/api/namespaces/) per page:
shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --url "https://gitlab.example.com/api/v4/namespaces?per_page=50"
```

There is a [max offset allowed limit](https://docs.gitlab.com/administration/instance_limits/#max-offset-allowed-by-the-rest-api-for-offset-based-pagination) for offset pagination. You can change the limit in GitLab Self-Managed instances.
#### Pagination `Link` header[](https://docs.gitlab.com/api/rest/#pagination-link-header "Permalink")
[`Link` headers](https://www.w3.org/wiki/LinkHeader) are returned with each response. They have `rel` set to `prev`, `next`, `first`, or `last` and contain the relevant URL. Be sure to use these links instead of generating your own URLs.
For GitLab.com users, [some pagination headers may not be returned](https://docs.gitlab.com/user/gitlab_com/#pagination-response-headers).
The following cURL example limits the output to three items per page (`per_page=3`), and requests the second page (`page=2`) of [comments](https://docs.gitlab.com/api/notes/) of the issue with ID `8` which belongs to the project with ID `9`:
shell
```
curl --request GET \
  --head \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --url "https://gitlab.example.com/api/v4/projects/9/issues/8/notes?per_page=3&page=2"
```

The response is:
http
```
HTTP/2 200 OK
cache-control: no-cache
content-length: 1103
content-type: application/json
date: Mon, 18 Jan 2016 09:43:18 GMT
link: <https://gitlab.example.com/api/v4/projects/8/issues/8/notes?page=1&per_page=3>; rel="prev", <https://gitlab.example.com/api/v4/projects/8/issues/8/notes?page=3&per_page=3>; rel="next", <https://gitlab.example.com/api/v4/projects/8/issues/8/notes?page=1&per_page=3>; rel="first", <https://gitlab.example.com/api/v4/projects/8/issues/8/notes?page=3&per_page=3>; rel="last"
status: 200 OK
vary: Origin
x-next-page: 3
x-page: 2
x-per-page: 3
x-prev-page: 1
x-request-id: 732ad4ee-9870-4866-a199-a9db0cde3c86
x-runtime: 0.108688
x-total: 8
x-total-pages: 3
```

#### Other pagination headers[](https://docs.gitlab.com/api/rest/#other-pagination-headers "Permalink")
GitLab also returns the following additional pagination headers:
Header | Description
---|---
`x-next-page` | The index of the next page.
`x-page` | The index of the current page (starting at 1).
`x-per-page` | The number of items per page.
`x-prev-page` | The index of the previous page.
`x-total` | The total number of items.
`x-total-pages` | The total number of pages.
For GitLab.com users, [some pagination headers may not be returned](https://docs.gitlab.com/user/gitlab_com/#pagination-response-headers).
### Keyset-based pagination[](https://docs.gitlab.com/api/rest/#keyset-based-pagination "Permalink")
Keyset-pagination allows for more efficient retrieval of pages and - in contrast to offset-based pagination - runtime is independent of the size of the collection.
This method is controlled by the following parameters. `order_by` and `sort` are both mandatory.
Parameter | Required | Description
---|---|---
`pagination` | yes |  `keyset` (to enable keyset pagination).
`per_page` | no | Number of items to list per page (default: `20`, max: `100`).
`order_by` | yes | Column by which to order by.
`sort` | yes | Sort order (`asc` or `desc`)
The following example lists 50 [projects](https://docs.gitlab.com/api/projects/) per page, ordered by `id` ascending.
shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --url "https://gitlab.example.com/api/v4/projects?pagination=keyset&per_page=50&order_by=id&sort=asc"
```

The response header includes a link to the next page. For example:
http
```
HTTP/1.1 200 OK
...
Link: <https://gitlab.example.com/api/v4/projects?pagination=keyset&per_page=50&order_by=id&sort=asc&id_after=42>; rel="next"
Status: 200 OK
...
```

The link to the next page contains an additional filter `id_after=42` that excludes already-retrieved records.
As another example, the following request lists 50 [groups](https://docs.gitlab.com/api/groups/) per page ordered by `name` ascending using keyset pagination:
shell
```
curl --request GET \
  --header "PRIVATE-TOKEN: YOUR_TOKEN" \
  --url "https://gitlab.example.com/api/v4/groups?pagination=keyset&per_page=50&order_by=name&sort=asc"
```

The response header includes a link to the next page:
http
```
HTTP/1.1 200 OK
...
Link: <https://gitlab.example.com/api/v4/groups?pagination=keyset&per_page=50&order_by=name&sort=asc&cursor=eyJuYW1lIjoiRmxpZ2h0anMiLCJpZCI6IjI2IiwiX2tkIjoibiJ9>; rel="next"
Status: 200 OK
...
```

The link to the next page contains an additional filter `cursor=eyJuYW1lIjoiRmxpZ2h0anMiLCJpZCI6IjI2IiwiX2tkIjoibiJ9` that excludes already-retrieved records.
The `X-NEXT-CURSOR` header contains the cursor value for retrieving the next page’s records, while the `X-PREV-CURSOR` header contains the cursor value for retrieving the previous page’s, when available.
The type of filter depends on the `order_by` option used, and you can have more than one additional filter.
The `Links` header was removed to be aligned with the [W3C `Link` specification](https://www.w3.org/wiki/LinkHeader). The `Link` header should be used instead.
When the end of the collection is reached and there are no additional records to retrieve, the `Link` header is absent and the resulting array is empty.
You should use only the given link to retrieve the next page instead of building your own URL. Apart from the headers shown, no additional pagination headers are exposed.
#### Supported resources[](https://docs.gitlab.com/api/rest/#supported-resources "Permalink")
Keyset-based pagination is supported only for selected resources and ordering options:
Resource | Options | Availability
---|---|---
[Group audit events](https://docs.gitlab.com/api/audit_events/#list-all-group-audit-events) |  `order_by=id`, `sort=desc` only | Authenticated users only.
[Groups](https://docs.gitlab.com/api/groups/#list-groups) |  `order_by=name`, `sort=asc` only | Unauthenticated users only.
[Instance audit events](https://docs.gitlab.com/api/audit_events/#list-all-instance-audit-events) |  `order_by=id`, `sort=desc` only | Authenticated users only.
[Package pipelines](https://docs.gitlab.com/api/packages/#list-package-pipelines) |  `order_by=id`, `sort=desc` only | Authenticated users only.
[Project jobs](https://docs.gitlab.com/api/jobs/#list-all-jobs-for-a-project) |  `order_by=id`, `sort=desc` only | Authenticated users only.
[Project audit events](https://docs.gitlab.com/api/audit_events/#list-all-project-audit-events) |  `order_by=id`, `sort=desc` only | Authenticated users only.
[Projects](https://docs.gitlab.com/api/projects/) |  `order_by=id` only | Authenticated and unauthenticated users.
[Users](https://docs.gitlab.com/api/users/) |  `order_by=id`, `order_by=name`, `order_by=username`, `order_by=created_at`, or `order_by=updated_at`. | Authenticated and unauthenticated users. [Introduced](https://gitlab.com/gitlab-org/gitlab/-/issues/419556) in GitLab 16.5.
[Registry Repository Tags](https://docs.gitlab.com/api/container_registry/) |  `order_by=name`, `sort=asc`, or `sort=desc` only. | Authenticated users only.
[List repository tree](https://docs.gitlab.com/api/repositories/#list-all-repository-trees-in-a-project) | N/A | Authenticated and unauthenticated users. [Introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/154897) in GitLab 17.1.
[Project issues](https://docs.gitlab.com/api/issues/#list-all-project-issues) |  `order_by=created_at`, `order_by=updated_at`, `order_by=title`, `order_by=id`, `order_by=weight`, `order_by=due_date`, `order_by=relative_position`, `sort=asc`, or `sort=desc` only. | Authenticated and unauthenticated users. [Introduced](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/199887/) in GitLab 18.3.
### Pagination response headers[](https://docs.gitlab.com/api/rest/#pagination-response-headers "Permalink")
For performance reasons, if a query returns more than 10,000 records, GitLab doesn’t return the following headers:
  * `x-total`.
  * `x-total-pages`.
  * `rel="last"` `link`


## Versioning and deprecations[](https://docs.gitlab.com/api/rest/#versioning-and-deprecations "Permalink")
The REST API version complies with the semantic versioning specification. The major version number is `4`. Backward-incompatible changes require this version number to change.
  * The minor version isn’t explicit, which allows for a stable API endpoint.
  * New features are added to the API in the same version number.
  * Major API version changes, and removal of entire API versions, are done in tandem with major GitLab releases.
  * All deprecations and changes between versions are noted in the documentation.


The following are excluded from the deprecation process and can be removed at any time without notice:
  * Elements labeled in the [REST API resources](https://docs.gitlab.com/api/api_resources/) as [experimental or beta](https://docs.gitlab.com/policy/development_stages_support/).
  * Fields behind a feature flag and disabled by default.


For GitLab Self-Managed, [reverting](https://docs.gitlab.com/update/convert_to_ee/revert/) from an EE instance to CE causes breaking changes.
Was this page helpful?YesNo
Edit this page
  *     * [ Open in Web IDE`.`Quickly and easily edit multiple files. ](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/_index.md)
    * [ View page sourceEdit this file only. ](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/_index.md)
    * [ Create an issueSuggest improvements. ](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)


  * [Make a REST API request](https://docs.gitlab.com/api/rest/#make-a-rest-api-request)
  * [Rate limits](https://docs.gitlab.com/api/rest/#rate-limits)
  * [Response format](https://docs.gitlab.com/api/rest/#response-format)
  * [Request requirements](https://docs.gitlab.com/api/rest/#request-requirements)
  * [Request payload](https://docs.gitlab.com/api/rest/#request-payload)
  * [Path parameters](https://docs.gitlab.com/api/rest/#path-parameters)
  * [id vs iid](https://docs.gitlab.com/api/rest/#id-vs-iid)
  * [Encoding](https://docs.gitlab.com/api/rest/#encoding)
  * [Namespaced paths](https://docs.gitlab.com/api/rest/#namespaced-paths)
  * [File path, branches, and tags name](https://docs.gitlab.com/api/rest/#file-path-branches-and-tags-name)
  * [Array and hash types](https://docs.gitlab.com/api/rest/#array-and-hash-types)
  * [Encoding + in ISO 8601 dates](https://docs.gitlab.com/api/rest/#encoding--in-iso-8601-dates)
  * [Evaluating a response](https://docs.gitlab.com/api/rest/#evaluating-a-response)
  * [null vs false](https://docs.gitlab.com/api/rest/#null-vs-false)
  * [Redirects](https://docs.gitlab.com/api/rest/#redirects)
  * [Pagination](https://docs.gitlab.com/api/rest/#pagination)
  * [Offset-based pagination](https://docs.gitlab.com/api/rest/#offset-based-pagination)
  * [Pagination Link header](https://docs.gitlab.com/api/rest/#pagination-link-header)
  * [Other pagination headers](https://docs.gitlab.com/api/rest/#other-pagination-headers)
  * [Keyset-based pagination](https://docs.gitlab.com/api/rest/#keyset-based-pagination)
  * [Supported resources](https://docs.gitlab.com/api/rest/#supported-resources)
  * [Pagination response headers](https://docs.gitlab.com/api/rest/#pagination-response-headers)
  * [Versioning and deprecations](https://docs.gitlab.com/api/rest/#versioning-and-deprecations)


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
  * [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/rest/_index.md)
  * [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/api/rest/_index.md)
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
