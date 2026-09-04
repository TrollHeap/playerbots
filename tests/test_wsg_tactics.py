"""Regression contracts for Warsong Gulch tactical decisions."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TACTICS = ROOT / "playerbot/strategy/actions/BattleGroundTactics.cpp"
TACTICS_HEADER = ROOT / "playerbot/strategy/actions/BattleGroundTactics.h"
STRATEGY = ROOT / "playerbot/strategy/generic/BattlegroundStrategy.cpp"
TRIGGERS = ROOT / "playerbot/strategy/triggers/PvpTriggers.cpp"
TRIGGER_CONTEXT = ROOT / "playerbot/strategy/triggers/TriggerContext.h"
CONFIG_HEADER = ROOT / "playerbot/PlayerbotAIConfig.h"
CONFIG_SOURCE = ROOT / "playerbot/PlayerbotAIConfig.cpp"
CONFIG_DIST = ROOT / "playerbot/aiplayerbot.conf.dist.in"
PLAYERBOT_AI = ROOT / "playerbot/PlayerbotAI.cpp"


def section(source: str, start: str, end: str) -> str:
    return source.split(start, 1)[1].split(end, 1)[0]


def main() -> None:
    tactics = TACTICS.read_text()
    tactics_header = TACTICS_HEADER.read_text()
    playerbot_ai = PLAYERBOT_AI.read_text()
    assert '#include "Movement/MoveSpline.h"' not in playerbot_ai
    select_objective = tactics.split("bool BGTactics::selectObjective", 1)[1]
    wsg = section(select_objective, "case BATTLEGROUND_WS:", "case BATTLEGROUND_AB:")
    strategy = section(
        STRATEGY.read_text(),
        "void WarsongStrategy::InitNonCombatTriggers",
        "void WarsongStrategy::InitCombatTriggers",
    )
    triggers = TRIGGERS.read_text()

    assert "bool advancedBgTactics;" in CONFIG_HEADER.read_text()
    assert 'GetBoolDefault("AiPlayerbot.AdvancedBgTactics", false)' in CONFIG_SOURCE.read_text()
    assert "AiPlayerbot.AdvancedBgTactics = 0" in CONFIG_DIST.read_text()
    assert "sPlayerbotAIConfig.advancedBgTactics" in wsg
    legacy_wsg = wsg.split("else if (!sPlayerbotAIConfig.advancedBgTactics)", 1)[1].split(
        "else if (bothFlagsTaken)", 1
    )[0]
    assert "bool supporter = role < 4" in legacy_wsg
    assert "Follow(teamFC)" in legacy_wsg
    assert "role > 9" in legacy_wsg
    assert "GetRandomPoint" in legacy_wsg
    assert "if (sPlayerbotAIConfig.advancedBgTactics)" in strategy
    advanced_strategy = strategy.split(
        "if (sPlayerbotAIConfig.advancedBgTactics)", 1
    )[1].split("else", 1)[0]
    assert "bot->GetInstanceId()" in tactics
    assert "enemyStrategy" in tactics
    assert "enemyStrategy == 2" in tactics
    assert "defenderCount" in wsg
    assert "wsgDefenderCount(bot, bg)" in wsg
    defender_count = section(tactics, "static uint32 wsgDefenderCount", "std::vector<uint32> const vFlagsAB")
    assert "BG_WS_STATE_CAPTURES_ALLIANCE" in defender_count
    assert "BG_WS_STATE_CAPTURES_HORDE" in defender_count
    assert "std::min<uint32>(3" in defender_count
    assert "std::max<uint32>(1" in defender_count
    assert "? 6 : 3" not in defender_count
    assert "bool IsWsgFlagRunner" in tactics
    assert "bool IsWsgEnemyFlagAtBase" in tactics
    assert "IsActiveEvent(GetTeamIndexByTeamId(enemyFlag), 0)" in tactics
    assert "bg->GetPlayers()" in tactics
    assert "player->GetPlayerbotAI()" in tactics
    assert "bothFlagsTaken" in wsg
    assert 'AI_VALUE(Unit*, "enemy flag carrier")' in wsg
    assert 'AI_VALUE(Unit*, "team flag carrier")' in wsg
    assert "WS_FLAG_HIDE_ALLIANCE" in wsg
    assert "WS_FLAG_HIDE_HORDE" in wsg
    assert "GetRandomPoint" in wsg
    assert 'new NextAction("bg protect fc"' in strategy
    assert 'new NextAction("bg move to objective", 80.0f)' in strategy
    assert '"wsg flag runner"' in strategy
    assert 'new NextAction("bg move to objective", 85.0f)' in strategy
    assert '"jump::position bg objective"' not in advanced_strategy
    assert '"rocket boots"' not in advanced_strategy

    execute = section(
        tactics,
        'if (getName() == "protect fc")',
        'if (getName() == "move to objective")',
    )
    assert "defenderCount" in execute
    assert "wsgDefenderCount(bot, bg)" in execute
    assert "role < defenderCount" in execute
    assert "IsInCombat(bot)" in execute
    assert "return protectFC();" in execute

    wsg_objective = section(tactics, "case BATTLEGROUND_WS:", "case BATTLEGROUND_AB:")
    assert "IsWsgFlagRunner(bot, bg) && IsWsgEnemyFlagAtBase(bot, bg)" in wsg_objective

    move_execute = section(
        tactics,
        'if (getName() == "move to objective")',
        'if (getName() == "use buff")',
    )
    assert "wsgFlagRunner" not in move_execute
    assert 'posMap["wsg corridor objective"]' in move_execute
    assert "ai->StopMoving()" in move_execute
    assert "MovementExpired()" not in move_execute

    start = section(tactics, "bool BGTactics::moveToStart", "bool BGTactics::selectObjective")
    assert "WS_WAITING_POS_HORDE_3" in start
    assert "WS_WAITING_POS_ALLIANCE_3" in start

    reset = section(tactics, "bool BGTactics::resetObjective", "bool BGTactics::moveToObjectiveWp")
    assert "advancedBgTactics" in reset
    assert "urand(0, 99) < 2" in reset

    paths = section(tactics, "bool BGTactics::selectObjectiveWp", "bool BGTactics::resetObjective")
    wsg_path_dispatch = paths.split("if (bgType == BATTLEGROUND_WS", 1)[1].split("#ifndef", 1)[0]
    assert "followWsgCorridor()" in wsg_path_dispatch
    assert "WsgCorridorResult::Moved" in wsg_path_dispatch
    assert "WsgCorridorResult::Interrupted" in wsg_path_dispatch
    assert "interrupted = true" in wsg_path_dispatch
    assert "if (wsgRoofJump())" in wsg_path_dispatch
    assert "return wsgPaths();" in wsg_path_dispatch
    assert "atAllianceGY" not in wsg_path_dispatch
    assert "atHordeGY" not in wsg_path_dispatch
    assert "chosenPathScore" in paths
    assert "closestPointDistanceToBot" in paths
    assert "distanceToDestination" in paths
    assert "chosenReverse ? chosenPoint + 1 : chosenPoint - 1" in paths

    corridor = section(tactics, "WsgCorridorResult BGTactics::followWsgCorridor()", "bool BGTactics::wsgPaths()")
    assert "bot->GetGUIDLow()" in corridor
    assert "bot->GetInstanceId()" in corridor
    assert "routeVariant = routeSeed % 3" in corridor
    assert "routeStride = 1 + (routeSeed / 3) % 3" in corridor
    assert "(routeSeed / 9) % 7" in corridor
    assert "* 0.80f" in corridor
    assert "bool towardAlliance = pos.x > 1227.0f" in corridor
    assert "laneOffset" in corridor
    assert "vPath_WSG_HordeTunnel_to_AllianceTunnel_1" in corridor
    assert "vPath_WSG_HordeTunnel_to_AllianceTunnel_2" in corridor
    assert "vPath_WSG_HordeGYJump_to_AllianceFlagRoom" in corridor
    assert "vPath_WSG_AllianceGYJump_to_HordeFlagRoom" in corridor
    assert "urand(" not in corridor
    assert "frand(" not in corridor
    assert 'posMap["wsg corridor objective"]' in corridor
    assert "ai->StopMoving()" in corridor
    assert "MovementExpired()" not in corridor
    assert "bot->IsInCombat()" in corridor
    assert "closestDistance > 50.0f" in corridor
    assert "IsWsgEnemyFlagAtBase(bot, bg)" in corridor
    assert "carrier == bot" in corridor
    assert "carriesEnemyFlag" in corridor
    assert "&& !flagTaken()" not in corridor
    assert "setRandomPosition" not in wsg
    assert "pos.Set(defendPos.x, defendPos.y, defendPos.z" in wsg

    update_ai = section(
        playerbot_ai,
        "void PlayerbotAI::UpdateAI(uint32 elapsed, bool minimal)",
        "void PlayerbotAI::UpdateFaceTarget",
    )
    assert "!bot->movespline->Finalized()" not in update_ai
    assert "WSG_MOVEMENT_RECOVERY" not in update_ai

    protect_fc = section(tactics, "bool BGTactics::protectFC()", "bool BGTactics::useBuff()")
    protect_fc_compact = " ".join(protect_fc.split())
    escort_slot = section(tactics, "int32 GetWsgEscortSlot", "bool IsWsgFlagRunner")
    assert "int32 GetWsgEscortSlot(Player* bot, BattleGround* bg, Unit* teamFC);" in tactics_header
    assert "escortCount = 2 +" in escort_slot
    assert "% 3" in escort_slot
    assert "bg->GetPlayers()" in escort_slot
    assert 'GetValue<uint32>("bg role")' in escort_slot
    assert "candidateRole < defenderCount" in escort_slot
    assert "player->GetGUIDLow() < bot->GetGUIDLow()" in escort_slot
    assert "GetWsgEscortSlot(bot, bg, teamFC)" in execute
    assert "escortSlot < 0" in execute
    assert "IsWithinDistInMap(teamFC, 20.0f)" in protect_fc
    assert "M_PI_F / 4.0f" in protect_fc
    assert "escortSlot * 2 + 1" in protect_fc
    assert "8.0f + 3.0f" in protect_fc
    assert "if (bot->IsWithinLOS" in protect_fc_compact
    assert "&& MoveTo(bot->GetMapId(), escortX, escortY" in protect_fc_compact
    assert "return MoveNear(teamFC, escortDistance);" in protect_fc
    assert "return Follow(teamFC);" not in protect_fc
    assert "urand(" not in protect_fc
    assert "frand(" not in protect_fc
    assert "return true;" in protect_fc

    wsg_paths = section(tactics, "bool BGTactics::wsgPaths()", "bool BGTactics::wsgRoofJump()")
    assert "laneOffset" not in wsg_paths
    assert "moveToLane" not in wsg_paths
    assert "routePreference" not in wsg_paths

    enemy_near = section(
        triggers,
        "bool EnemyFlagCarrierNear::IsActive()",
        "bool TeamFlagCarrierNear::IsActive()",
    )
    team_near = section(
        triggers,
        "bool TeamFlagCarrierNear::IsActive()",
        "bool WsgFlagRunnerTrigger::IsActive()",
    )
    assert "100.0f" in enemy_near
    assert "bot->GetBattleGroundTypeId() != BATTLEGROUND_WS" in enemy_near
    assert "distToEnemy + 15.0f < distToFC" in enemy_near
    assert "bothFlagsTaken" not in team_near
    assert "GetWsgEscortSlot(bot, bg, carrier) >= 0" in team_near
    assert "200.0f" in team_near

    assert "int32 escortSlot = GetWsgEscortSlot(bot, bg, teamFC);" in wsg_objective
    both_flags = section(wsg_objective, "else if (bothFlagsTaken)", "else if (enemyFC)")
    assert "escortSlot >= 0 ? teamFC : enemyFC" in both_flags
    own_carrier = section(wsg_objective, "else if (teamFC)", "else if (IsWsgFlagRunner")
    assert "else if (escortSlot >= 0)" in own_carrier
    assert "WS_FLAG_POS_HORDE" in own_carrier
    assert "WS_FLAG_POS_ALLIANCE" in own_carrier

    assert "bool WsgFlagRunnerTrigger::IsActive()" in triggers
    assert "IsWsgFlagRunner(bot, bg)" in triggers
    runner = section(
        triggers,
        "bool WsgFlagRunnerTrigger::IsActive()",
        "bool PlayerWantsInBattlegroundTrigger::IsActive()",
    )
    assert "bot->IsInCombat()" in runner
    assert "IsWsgEnemyFlagAtBase(bot, bg)" in runner
    assert "GetFlagState" not in runner
    assert "GetFlagCarrierGuid" not in runner
    assert 'creators["wsg flag runner"]' in TRIGGER_CONTEXT.read_text()

    execute = section(tactics, "bool BGTactics::Execute", "bool BGTactics::moveToStart")
    assert "bool corridorInterrupted = false" in execute
    assert "selectObjectiveWp(*vPaths, corridorInterrupted)" in execute
    assert "if (corridorInterrupted)" in execute


if __name__ == "__main__":
    main()
