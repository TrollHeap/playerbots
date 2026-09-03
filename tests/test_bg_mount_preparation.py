"""Source contract: bots stay unmounted in the BG preparation area."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = (
        ROOT / "playerbot/strategy/actions/CheckMountStateAction.cpp"
    ).read_text()
    tactics = (
        ROOT / "playerbot/strategy/actions/BattleGroundTactics.cpp"
    ).read_text()
    execute = source[source.index("bool CheckMountStateAction::Execute") : source.index("bool CheckMountStateAction::isUseful")]
    useful = source[source.index("bool CheckMountStateAction::isUseful()") :]

    assert "bool IsWsgStartingArea(Player* bot)" in tactics
    assert "GetDistance2d(waitPos.x, waitPos.y)" in tactics
    assert "if (IsWsgStartingArea(bot))\n        return bot->IsMounted() ? UnMount() : false;" in execute
    assert "if (IsWsgStartingArea(bot))\n        return bot->IsMounted();" in useful
    assert "bg->GetStatus() == STATUS_WAIT_JOIN" in tactics
    assert "fabs(bot->GetPositionZ() - waitPos.z) < 12.0f" in tactics
    assert "GetStartDelayTime() > BG_START_DELAY_30S" not in useful


if __name__ == "__main__":
    main()
