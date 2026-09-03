# Upstream behavior references

## AzerothCore mod-playerbots

- Repository: <https://github.com/mod-playerbots/mod-playerbots>
- Reference commit: `2f7d9f774987d0157c6a0d0cc08c40bec3db3945`
- License: GNU GPL v2 or later
- Adapted behavior: `BGTactics::wsJumpDown`, three-way Warsong staging,
  flag-carrier priorities and proximity triggers, stable team strategies,
  weighted route selection, and Arathi node-state priorities.

The behavior is adapted to the existing CMaNGOS Classic APIs and route graph.
AzerothCore core APIs, packets, hooks, and WotLK-only behavior are not imported.
Set `AiPlayerbot.AdvancedBgTactics = 0` to restore the original objective and
route selection without reverting the fork.
