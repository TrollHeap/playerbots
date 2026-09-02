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

    assert "move through graveyard (BUGGED)" not in wsg_paths
    assert "1055.182251f, 1396.967529f, 339.361511f" not in wsg_paths
    assert "if (Preference < 4 && !atHordeGY)" in wsg_paths
    assert "else { // all other preference: run down the ramp" in wsg_paths
    ramp = wsg_paths.split(
        "else { // all other preference: run down the ramp", 1
    )[1].split("if (bot->GetPositionX() < 1227.f)", 1)[0]
    assert ramp.count("return MoveTo(") == 6
    assert (
        "return MoveTo(bg->GetMapId(), 1031.764282f, 1454.516235f, "
        "343.337860f);"
        in wsg_paths
    )


if __name__ == "__main__":
    main()
