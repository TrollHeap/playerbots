#include "playerbot/strategy/values/EquipmentContribution.h"

#include <cassert>

int main()
{
    assert(!ai::HasEquipmentContribution(0, 0, 0.0f, false));
    assert(ai::HasEquipmentContribution(1, 0, 0.0f, false));
    assert(ai::HasEquipmentContribution(0, 1, 0.0f, false));
    assert(ai::HasEquipmentContribution(0, 0, 1.0f, false));
    assert(ai::HasEquipmentContribution(0, 0, 0.0f, true));
}
