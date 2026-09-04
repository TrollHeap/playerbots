"""Natural guild-invite requests use the verified Playerbots action, not the LLM."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "playerbot/PlayerbotAI.cpp"


def main() -> None:
    source = SOURCE.read_text()
    helper = source.split("bool IsNaturalGuildInviteRequest", 1)[1].split("}", 1)[0]
    assert 'text.find("guilde")' in helper
    assert '"peux m\'inviter"' in helper
    assert '"invite-moi"' in helper

    chat = source.split("case SMSG_MESSAGECHAT", 1)[1].split("case SMSG_EMOTE", 1)[0]
    natural = chat.split("Player* speaker =", 1)[1].split("Player* selectedPlayer", 1)[0]
    assert "msgtype == CHAT_MSG_WHISPER" in natural
    assert "!isFromFreeBot" in natural
    assert "DoSpecificAction(" in natural and '"guild invite"' in natural
    assert "Invitation de guilde envoyée" in natural
    assert "Je ne peux pas t'inviter dans ma guilde" in natural
    assert chat.index("IsNaturalGuildInviteRequest(message)") < chat.index("QueueChatResponse(")


if __name__ == "__main__":
    main()
