"""Source contract for the opt-in remote battleground queue command."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    header = (ROOT / "playerbot/PlayerbotAIConfig.h").read_text()
    config = (ROOT / "playerbot/PlayerbotAIConfig.cpp").read_text()
    config_dist = (ROOT / "playerbot/aiplayerbot.conf.dist.in").read_text()
    manager = (ROOT / "playerbot/PlayerbotMgr.cpp").read_text()
    random_manager = (ROOT / "playerbot/RandomPlayerbotMgr.cpp").read_text()
    handler_start = manager.index("PlayerbotHolder::HandleRemoteBgQueue")
    handler = manager[
        handler_start : manager.index("PlayerbotHolder::HandleGroup", handler_start)
    ]

    assert "bool remotePlayerBgQueue;" in header
    assert (
        'config.GetBoolDefault("AiPlayerbot.RemotePlayerBgQueue", false)'
        in config
    )
    assert "AiPlayerbot.RemotePlayerBgQueue = 0" in config_dist
    assert 'm_holderHandlers["bgqueue"]' in manager
    assert "CanJoinToBattleground()" in manager
    assert "HasFreeBattleGroundQueueId()" in manager
    assert "GetBGAccessByLevel(bgTypeId)" in manager
    assert "AddGroup(playerGuid" in manager
    assert "[queueTypeId, playerGuid, info, bgTypeId, bracketId, mapId, queueReserved]" in handler
    assert "ScheduleQueueUpdate" in manager
    assert "File WSG bot-only amorcee" in manager
    assert "sRandomPlayerbotMgr.ForEachPlayerbot" in manager
    assert "GetMinPlayersPerTeam()" in manager
    assert "candidates[bracketId][team][i]" in manager
    assert "randomBotAutoJoinBG" not in handler
    assert "InBattleGroundQueueForBattleGroundQueueType(queueTypeId)" in handler
    assert "BgBots[queueTypeId][bracketId][team]++" in handler
    assert "queuePlayer(candidates[bracketId][team][i], true)" in handler
    assert random_manager.count("BgCheckTimer + 5") == 2
    assert "BgCheckTimer + 30" not in random_manager


if __name__ == "__main__":
    main()
