# CONN-GITLAB-API — Data model

The connector maps GitLab replies to the SDK change-proposal records. It defines no record of its own.

| GitLab reply | SDK record | Engine class | Key fields |
|---|---|---|---|
| Merge request | `ChangeProposalRef` | `:MergeRequest` | iid, head `sha`, target branch, state, draft, changed lines |
| Approval | `ReviewRecord` | `:Review` | approver, reviewer kind, state `approved`, commit |
| Resolvable discussion | `ReviewThreadRecord` | `:ReviewThread` | discussion ID, path, line, resolved flag, note IDs |
| Pipeline or job | `CheckRunRecord` | `:PipelineRun`, `:PipelineJob` | ID, commit `sha`, name, status, web URL |
| Webhook event | `ScmFeedbackEvent` | `:FeedbackEvent` | event UUID, kind, merge request, actor, actor kind, time, body digest |

A bot user has the reviewer kind `automated`. Every other user has the kind `person`.
