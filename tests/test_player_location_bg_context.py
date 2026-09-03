"""The live location log must expose enough context to diagnose battleground routing."""

from pathlib import Path

source = (Path(__file__).resolve().parents[1] / "playerbot/RandomPlayerbotMgr.cpp").read_text()

assert 'out << bot->GetInstanceId() << ",";' in source
assert 'GetValue<uint32>("bg role")->Get()' in source
assert 'HasAura(BG_WS_SPELL_WARSONG_FLAG)' in source
assert 'HasAura(BG_WS_SPELL_SILVERWING_FLAG)' in source
assert 'GetPlayerScoresBegin()' in source
assert 'GetPlayerScoresEnd()' in source
assert 'GetAttr1()' in source
assert 'GetAttr2()' in source
assert 'GetFlagCarrierGuid(TEAM_INDEX_ALLIANCE)' in source
assert 'GetFlagCarrierGuid(TEAM_INDEX_HORDE)' in source
