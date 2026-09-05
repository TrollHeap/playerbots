"""A real human guild join schedules varied, staggered bot welcomes."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "playerbot/PlayerbotAI.cpp"


def main() -> None:
    source = SOURCE.read_text()
    outgoing = source.split("void PlayerbotAI::HandleBotOutgoingPacket", 1)[1].split(
        "void PlayerbotAI::SpellInterrupted", 1
    )[0]
    assert "case SMSG_GUILD_EVENT" in outgoing
    assert "GE_JOINED" in outgoing
    assert "joined->isRealPlayer()" in outgoing
    assert "QueueGuildWelcome" in outgoing

    queued = source.split("void PlayerbotAI::QueueGuildWelcome", 1)[1].split("}", 1)[0]
    assert "GuildWelcomeDelay" in queued
    assert '"__guild_welcome "' in queued

    delay = source.split("time_t GuildWelcomeDelay", 1)[1].split(
        "std::string GuildWelcomeText", 1
    )[0]
    assert "wave.next >= 3" in delay
    assert "return 0" in delay

    commands = source.split("void PlayerbotAI::HandleCommands", 1)[1].split(
        "void PlayerbotAI::UpdateAIInternal", 1
    )[0]
    assert 'command.find("__guild_welcome ") == 0' in commands
    assert "SayToGuild(GuildWelcomeText" in commands

    guild_chat = source.split("bool PlayerbotAI::SayToGuild", 1)[1].split(
        "void PlayerbotAI::QueueGuildWelcome", 1
    )[0]
    assert "bot->isAFK()" in guild_chat
    assert "bot->ToggleAFK()" in guild_chat

    welcome = source.split("std::string GuildWelcomeText", 1)[1].split("}", 1)[0]
    lines = [line.strip() for line in welcome.splitlines() if '"' in line and "name" in line]
    assert len(lines) >= 20
    assert len(lines) == len(set(lines))
    assert all("bienvenue" in line.lower() or "welcome" in line.lower() for line in lines)
    assert "Bonne route avec nous" not in welcome
    assert "Welcome parmi nous" not in welcome
    assert "si t'as besoin" in welcome
    assert "amuse-toi bien" in welcome


if __name__ == "__main__":
    main()
