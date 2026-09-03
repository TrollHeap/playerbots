"""Regression contracts for Arathi Basin tactical decisions."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TACTICS = ROOT / "playerbot/strategy/actions/BattleGroundTactics.cpp"


def main() -> None:
    source = TACTICS.read_text()
    select_objective = source.split("bool BGTactics::selectObjective", 1)[1]
    arathi = select_objective.split("case BATTLEGROUND_AB:", 1)[1].split(
        "case BATTLEGROUND_EY:", 1
    )[0]

    assert "bot->GetInstanceId()" in arathi
    assert "sPlayerbotAIConfig.advancedBgTactics" in arathi
    legacy = arathi.split("if (!advanced)", 1)[1].split("std::vector<std::pair", 1)[0]
    assert "botSelectedObjectives" in legacy
    assert "botObjectiveSelectionTime" in legacy
    assert "WorldTimer::getMSTime()" in legacy
    assert "defenderCount" in arathi
    assert "friendlyContested" in arathi
    assert "enemyOccupied" in arathi
    assert "friendlyOccupied" in arathi
    assert "attackObjectives" in arathi
    assert "std::sort" in arathi
    assert "role %" in arathi
    assert "bot->Say" not in arathi


if __name__ == "__main__":
    main()
