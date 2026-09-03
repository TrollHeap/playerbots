"""Regression contract for the WSG graveyard exit route."""

from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "playerbot/strategy/actions/BattleGroundTactics.cpp"
)
MOVEMENT_HEADER = SOURCE.parents[0] / "MovementActions.h"
MOVEMENT_SOURCE = SOURCE.parents[0] / "MovementActions.cpp"


def main() -> None:
    source = SOURCE.read_text()
    movement_header = MOVEMENT_HEADER.read_text()
    movement_source = MOVEMENT_SOURCE.read_text()
    wsg_paths = source.split("bool BGTactics::wsgPaths()", 1)[1].split(
        "bool BGTactics::wsgRoofJump()", 1
    )[0]

    assert "if (Preference < 4 && !atHordeGY)" in wsg_paths
    assert "else if (atHordeGY || Preference < 7)" in wsg_paths
    assert "bool JumpTo(const WorldPosition& dest);" in movement_header
    jump_to = movement_source.split("bool JumpAction::JumpTo", 1)[1].split(
        "bool JumpAction::Execute", 1
    )[0]
    assert "if (ai->IsJumping())" in jump_to
    assert "return true;" in jump_to
    assert "1045.764f, 1389.831f, 340.825f" in wsg_paths
    assert "1057.076f, 1393.081f, 339.505f" in wsg_paths
    jump = "jump.JumpTo(WorldPosition(bg->GetMapId(), 1075.233f, 1398.645f, 323.669f))"
    assert f"if ({jump})" in wsg_paths
    assert f"return {jump};" not in wsg_paths
    assert "MoveTo(bg->GetMapId(), 1076.778076f" not in wsg_paths
    assert "1407.234f, 1551.658f, 343.432f" in wsg_paths
    assert "jump.JumpTo(WorldPosition(bg->GetMapId(), 1385.325f, 1544.592f, 322.047f))" in wsg_paths
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
