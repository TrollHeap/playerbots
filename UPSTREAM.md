# Fork maintenance

The runtime consumes the exact `TrollHeap/playerbots` commit pinned only in the
parent repository's `docker/Dockerfile`. The current fork-specific history
starts after CMaNGOS Playerbots commit `d557e987`.

Run the lightweight fork contracts with `make test`. A publishable change still
requires the parent repository's full Ubuntu 22.04/GCC 12 build and gates, then
the relevant in-game validation. The GitHub workflow builds the current fork
against CMaNGOS Classic `master` only as an early compatibility signal; it does
not replace the exact pinned product build.

Fork-owned behavior remains reversible:

- `AiPlayerbot.AdvancedBgTactics = 0` restores upstream BG decisions;
- `AiPlayerbot.RemotePlayerBgQueue = 0` disables the remote queue command;
- `AiPlayerbot.TellQuestProgress = 1` restores upstream quest progress chat;
- disabling LLM chat bypasses the added runtime narrative snapshot.

Before taking upstream changes, compare them from `d557e987`, select only the
relevant commits, then repeat the focused checks and full parent gates. Do not
mix an upstream intake with a local behavior change.

The repository has no root license file detectable by GitHub. Source headers
state GPL version 2 or later; clarify the canonical upstream license text before
redistribution instead of reconstructing it locally.

## External behavior reference

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
