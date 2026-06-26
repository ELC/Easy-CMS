# Queue all authorized actions with deterministic state transitions

CMS Studio queues every action the signed-in Site User is authorized to take, including Publish, Send back, Unpublish, Hard delete, Site User changes, and Subscriber management. The Sync Server applies each queued change through deterministic TypeState transitions; Article content conflicts can require CMS Studio resolution, while non-content races produce applied or Superseded change outcomes so the Article or Site never enters an inconsistent state.

## Consequences

- Offline work is consistent across Writer, Editor, and Site Admin responsibilities instead of limiting the queue to Article content.
- CMS Studio must show a clear notification when one of its queued changes becomes a Superseded change.
- The Sync Server, not CMS Studio, is the final authority for role checks and transition validity when queued changes arrive.
