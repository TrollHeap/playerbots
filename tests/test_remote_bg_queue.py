"""Source contract for the opt-in remote battleground queue command."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    header = (ROOT / "playerbot/PlayerbotAIConfig.h").read_text()
    config = (ROOT / "playerbot/PlayerbotAIConfig.cpp").read_text()
    config_dist = (ROOT / "playerbot/aiplayerbot.conf.dist.in").read_text()
    manager = (ROOT / "playerbot/PlayerbotMgr.cpp").read_text()

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
    assert "ScheduleQueueUpdate" in manager


if __name__ == "__main__":
    main()
