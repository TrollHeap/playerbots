#pragma once

namespace ai
{
    constexpr bool HasEquipmentContribution(unsigned armor, unsigned block, float damage, bool hasSpell)
    {
        return armor || block || damage > 0.0f || hasSpell;
    }
}
