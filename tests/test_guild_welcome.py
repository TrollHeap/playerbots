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

    commands = source.split("void PlayerbotAI::HandleCommands", 1)[1].split(
        "void PlayerbotAI::UpdateAIInternal", 1
    )[0]
    assert 'command.find("__guild_welcome ") == 0' in commands
    assert "SayToGuild(GuildWelcomeText" in commands

    welcome = source.split("std::string GuildWelcomeText", 1)[1].split("}", 1)[0]
    lines = [line.strip() for line in welcome.splitlines() if '"' in line and "name" in line]
    assert len(lines) >= 12
    assert len(lines) == len(set(lines))


if __name__ == "__main__":
    main()
