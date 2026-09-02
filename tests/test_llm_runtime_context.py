"""Regression contract for the verified Playerbots runtime snapshot."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "playerbot/strategy/actions/SayAction.cpp"
INVITES = Path(__file__).resolve().parents[1] / "playerbot/strategy/actions/InviteToGroupAction.cpp"


def main() -> None:
    source = SOURCE.read_text()
    llm = source.split("if (player)", 1)[1].split("std::string llmPromptCustom", 1)[0]
    assert 'placeholders["<bot state>"]' in llm
    assert 'placeholders["<bot target>"]' in llm
    assert 'placeholders["<bot health state>"]' in llm
    assert 'placeholders["<bot mounted>"]' in llm
    assert 'placeholders["<bot target type>"]' in llm
    assert 'placeholders["<bot target level>"]' in llm
    assert 'bot->IsAlive()' in llm
    assert 'bot->IsInCombat()' in llm
    assert 'bot->IsMoving()' in llm
    assert 'bot->GetVictim()' in llm
    assert 'bot->GetHealthPercent()' in llm
    assert 'bot->IsMounted()' in llm
    assert 'botTarget->GetTypeId()' in llm
    assert 'botTarget->GetLevel()' in llm
    assert 'AI_VALUE(TravelTarget*, "travel target")' in llm
    assert 'placeholders["<bot activity>"]' in llm
    assert 'placeholders["<bot destination>"]' in llm
    assert 'placeholders["<bot invite reason>"]' in llm
    assert 'placeholders["<bot group type>"]' in llm
    assert 'placeholders["<bot group size>"]' in llm
    assert 'placeholders["<bot group leader>"]' in llm
    assert 'placeholders["<player in group>"]' in llm
    assert "bot->GetGroup()" in llm
    assert "GetMembersCount()" in llm
    assert "IsRaidGroup()" in llm
    assert "GetLeaderName()" in llm
    assert "IsMember(player->GetObjectGuid())" in llm
    assert 'placeholders["<bot battleground>"]' in llm
    assert 'placeholders["<bot battleground status>"]' in llm
    assert 'placeholders["<bot carries flag>"]' in llm
    assert "bot->InBattleGround()" in llm
    assert "bot->GetBattleGroundTypeId()" in llm
    assert "bot->GetBattleGround()->GetStatus()" in llm
    assert "BG_WS_SPELL_WARSONG_FLAG" in llm
    assert "BG_WS_SPELL_SILVERWING_FLAG" in llm
    for state in (
        "travel_quest_pickup",
        "quest_pickup",
        "travel_quest",
        "questing",
        "travel_quest_turnin",
        "quest_turnin",
        "travel_rpg",
        "travel_explore",
    ):
        assert f'botActivity = "{state}"' in llm

    invites = INVITES.read_text()
    assert '"nearby_group"' in invites
    assert '"guild_group"' in invites
    assert '"requested_invite"' in invites
    assert 'SET_AI_VALUE(std::string, "manual string::llm invite player"' in invites
    assert 'SET_AI_VALUE(time_t, "manual time::llm invite expires"' in invites
    assert 'AI_VALUE(std::string, "manual string::llm invite player") == playerName' in llm
    assert "time(0) + 300" in invites


if __name__ == "__main__":
    main()
