"""Static regression contract for observable, bounded bot conversations."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    config_h = (ROOT / "playerbot/PlayerbotAIConfig.h").read_text()
    config_cpp = (ROOT / "playerbot/PlayerbotAIConfig.cpp").read_text()
    config_dist = (ROOT / "playerbot/aiplayerbot.conf.dist.in").read_text()
    action_h = (ROOT / "playerbot/strategy/actions/SayAction.h").read_text()
    action_cpp = (ROOT / "playerbot/strategy/actions/SayAction.cpp").read_text()
    trigger_h = (ROOT / "playerbot/strategy/triggers/GenericTriggers.h").read_text()
    trigger_cpp = (ROOT / "playerbot/strategy/triggers/GenericTriggers.cpp").read_text()
    strategy_h = (ROOT / "playerbot/strategy/generic/DebugStrategy.h").read_text()
    strategy_cpp = (ROOT / "playerbot/strategy/generic/DebugStrategy.cpp").read_text()
    transport = (ROOT / "playerbot/PlayerbotLLMInterface.cpp").read_text()

    assert "llmBotConversationChance" in config_h
    assert 'GetIntDefault("AiPlayerbot.LLMBotConversationChance", 0)' in config_cpp
    assert "AiPlayerbot.LLMBotConversationChance = 0" in config_dist
    assert "AiPlayerbot.LLMBotConversationInterval = 30" in config_dist
    assert "AiPlayerbot.LLMBotConversationCooldown = 300" in config_dist
    assert "AiPlayerbot.LLMBotConversationExpiration = 20" in config_dist

    assert "class BotConversationAction" in action_h
    assert "std::future<BotConversationResult>" in action_h
    assert "std::vector<uint32> participantGuids" in action_h
    assert "BotConversationAction::ValidateScene" in action_cpp
    assert action_cpp.count("ValidateScene()") >= 2
    assert "std::async(std::launch::async" in action_cpp
    assert "sRandomPlayerbotMgr.ForEachPlayerbot" in action_cpp
    assert "ReapAbandonedFutures" in action_cpp
    assert "abandonedFutures.push_back(std::move(future))" in action_cpp
    assert "std::min(sPlayerbotAIConfig.llmGenerationTimeout" in action_cpp
    assert "Utf8toWStr" in action_cpp
    assert "player->IsAlive() && !player->IsInCombat()" in action_cpp
    worker = action_cpp.split("std::async(std::launch::async", 1)[1].split(");", 1)[0]
    for forbidden in ("Player*", "Group*", "Map*", "WorldSession*", "WorldPacket"):
        assert forbidden not in worker
    assert "LLMBotToBotChatChance" not in action_cpp
    assert "detach()" not in action_cpp
    assert "urand(3000, 5000)" in action_cpp
    assert "result.lines.size() == 4" in action_cpp
    assert "result.lines.empty() || result.lines.size() > 4" in action_cpp
    assert '\\"context\\"' in action_cpp and "AREA_FLAG_CAPITAL" in action_cpp
    assert "matched.size() == 2" in action_cpp
    assert "for (uint32 guid : participantGuids)" in action_cpp
    assert "speaker->isAFK()" in action_cpp and "speaker->ToggleAFK()" in action_cpp
    assert action_cpp.count("WorldTimer::getMSTime()") == 3
    speak = action_cpp.split("bool BotConversationAction::SpeakLine()", 1)[1].split(
        "void BotConversationAction::Reset()", 1
    )[0]
    battleground_delivery = speak.split("else if (channel == Channel::BATTLEGROUND)", 1)[1].split(
        "else if", 1
    )[0]
    assert "SayToRaid(lines[line].message)" in battleground_delivery
    assert "sServerFacade.SendPacket(observer, data)" not in battleground_delivery

    assert "class BotConversationTrigger" in trigger_h
    assert "llmBotConversationInterval" in trigger_h
    assert "BotConversationTrigger::IsActive" in trigger_cpp
    assert "sPlayerbotAIConfig.llmEnabled <= 0" not in trigger_cpp
    assert "action->IsPending()" in trigger_cpp
    assert 'creators["bot conversation"]' in (
        (ROOT / "playerbot/strategy/actions/ActionContext.h").read_text()
        + (ROOT / "playerbot/strategy/triggers/TriggerContext.h").read_text()
    )
    assert "InitNonCombatTriggers" in strategy_h
    assert 'new NextAction("bot conversation"' in strategy_cpp
    assert "GenerateAt" in transport and "/v1/bot-conversations" in action_cpp


if __name__ == "__main__":
    main()
