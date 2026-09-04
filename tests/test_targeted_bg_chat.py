"""A selected Playerbot is the sole LLM /say respondent inside a battleground."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "playerbot/PlayerbotAI.cpp"


def main() -> None:
    source = SOURCE.read_text()
    chat = source.split("case SMSG_MESSAGECHAT", 1)[1].split("case SMSG_EMOTE", 1)[0]
    targeted = chat.split("Player* speaker =", 1)[1].split("ChatChannelSource", 1)[0]

    assert "sObjectMgr.GetPlayer(guid1);" in targeted
    assert "speaker->GetSelectionGuid()" in targeted
    assert "selectedPlayer->GetPlayerbotAI()" in targeted
    assert "!selectedPlayer->GetPlayerbotAI()->IsRealPlayer()" in targeted
    assert "selectedPlayer != bot" in targeted
    assert "msgtype == CHAT_MSG_SAY" in targeted
    assert "bot->InBattleGround()" in targeted
    selected_guard = targeted.split("Player* selectedPlayer =", 1)[1]
    assert selected_guard.count("return;") == 1


if __name__ == "__main__":
    main()
