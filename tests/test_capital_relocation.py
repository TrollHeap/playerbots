"""Capital visitors should attract idle same-faction bots to RPG destinations."""

from pathlib import Path

source = (
    Path(__file__).resolve().parents[1] / "playerbot/RandomPlayerbotMgr.cpp"
).read_text()
start = source.index("void RandomPlayerbotMgr::RandomTeleportForLevel")
end = source.index("void RandomPlayerbotMgr::RandomTeleport(Player* bot)", start)
body = source[start:end]

assert "randomBotTeleportNearPlayer" in body
assert "candidate->GetTeam() != bot->GetTeam()" in body
assert "WorldPosition(candidate).HasAreaFlag(AREA_FLAG_CAPITAL)" in body
assert "RandomTeleportForRpg(bot, activeOnly);" in body
