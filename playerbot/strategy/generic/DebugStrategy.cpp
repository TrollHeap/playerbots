
#include "playerbot/playerbot.h"
#include "DebugStrategy.h"

using namespace ai;

void AIChatStrategy::InitNonCombatTriggers(std::list<TriggerNode*>& triggers)
{
    triggers.push_back(new TriggerNode(
        "bot conversation",
        NextAction::array(0, new NextAction("bot conversation", 1.01f), NULL)));
}
