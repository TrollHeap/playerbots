"""Regression contract for the WSG graveyard exit route."""

from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "playerbot/strategy/actions/BattleGroundTactics.cpp"
)


def main() -> None:
    source = SOURCE.read_text()
    wsg_paths = source.split("bool BGTactics::wsgPaths()", 1)[1].split(
        "bool BGTactics::wsgRoofJump()", 1
    )[0]

    assert "if (Preference < 4 && !atHordeGY)" in wsg_paths
    assert "else if (atHordeGY || Preference < 7)" in wsg_paths
    assert (
        "MoveTo(bg->GetMapId(), 1055.182251f, 1396.967529f, "
        "339.361511f, false, false, true)"
        in wsg_paths
    )
    assert (
        "MoveTo(bg->GetMapId(), 1076.778076f, 1396.0f, 324.0f, "
        "false, false, true)"
        in wsg_paths
    )
    assert "run down the ramp if the graveyard jump is rejected" in wsg_paths
    ramp = wsg_paths.split(
        "run down the ramp if the graveyard jump is rejected", 1
    )[1].split("if (bot->GetPositionX() < 1227.f)", 1)[0]
    assert ramp.count("return MoveTo(") == 6
    assert (
        "return MoveTo(bg->GetMapId(), 1031.764282f, 1454.516235f, "
        "343.337860f);"
        in wsg_paths
    )


if __name__ == "__main__":
    main()
