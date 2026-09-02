"""Source contract for optional quest-progress chat."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    header = (ROOT / "playerbot/PlayerbotAIConfig.h").read_text()
    config = (ROOT / "playerbot/PlayerbotAIConfig.cpp").read_text()
    config_dist = (ROOT / "playerbot/aiplayerbot.conf.dist.in").read_text()
    quest_action = (
        ROOT / "playerbot/strategy/actions/QuestAction.cpp"
    ).read_text()

    assert "bool tellQuestProgress;" in header
    assert (
        'config.GetBoolDefault("AiPlayerbot.TellQuestProgress", true)'
        in config
    )
    assert "AiPlayerbot.TellQuestProgress = 1" in config_dist
    assert quest_action.count("sPlayerbotAIConfig.tellQuestProgress") == 5


if __name__ == "__main__":
    main()
