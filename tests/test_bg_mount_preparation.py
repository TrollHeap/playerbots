"""Source contract: bots stay unmounted in the BG preparation area."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = (
        ROOT / "playerbot/strategy/actions/CheckMountStateAction.cpp"
    ).read_text()
    useful = source[source.index("bool CheckMountStateAction::isUseful()") :]

    assert (
        "bot->GetBattleGroundTypeId() == BATTLEGROUND_WS &&\n"
        "            bg->GetStatus() == STATUS_WAIT_JOIN)\n"
        "            return false;"
    ) in useful
    assert "GetStartDelayTime() > BG_START_DELAY_30S" not in useful


if __name__ == "__main__":
    main()
