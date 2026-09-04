#pragma once

#include "playerbot/strategy/Action.h"
#include "QuestAction.h"

#include <atomic>
#include <future>
#include <map>
#include <mutex>

struct ParsedUrl;

namespace ai
{
    class SayAction : public Action, public Qualified
    {
    public:
        SayAction(PlayerbotAI* ai);
        virtual bool Execute(Event& event) override;
        virtual bool isUseful() override;
        virtual std::string getName() override { return "say::" + qualifier; }
        virtual bool isUsefulWhenStunned() override { return true; }

    private:
    };

    typedef std::pair<WorldPacket, uint32> delayedPacket;
    typedef std::vector<delayedPacket> delayedPackets;
    typedef std::future<delayedPackets> futurePackets;

    struct BotConversationLine
    {
        std::string speaker;
        std::string message;
    };

    struct BotConversationResult
    {
        std::vector<BotConversationLine> lines;
    };

    class BotConversationAction : public Action
    {
    public:
        BotConversationAction(PlayerbotAI* ai) : Action(ai, "bot conversation") {}
        virtual ~BotConversationAction();
        virtual bool Execute(Event& event) override;
        virtual bool isUseful() override { return true; }
        bool IsPending() const;
        bool CanStart();
        void Cancel();

    private:
        enum class Channel : uint8 { NONE, SAY, GUILD, PARTY, RAID, BATTLEGROUND };

        bool ValidateScene() const;
        bool SpeakLine();
        std::string BuildRequest(Player* observer, Player* other) const;
        static BotConversationResult Generate(const std::string& json, const ParsedUrl& endpoint,
            const std::string& first, const std::string& second, uint32 timeoutSeconds);
        static void ReapAbandonedFutures();
        void Reset();

        Channel channel = Channel::NONE;
        uint32 observerGuid = 0;
        uint32 otherGuid = 0;
        time_t expires = 0;
        uint32 nextLine = 0;
        bool prepared = false;
        bool canceled = false;
        bool ownsFlight = false;
        std::future<BotConversationResult> future;
        std::vector<BotConversationLine> lines;
        size_t line = 0;

        static std::atomic<bool> inFlight;
        static std::mutex cooldownMutex;
        static std::map<uint32, time_t> observerCooldowns;
        static std::vector<std::future<BotConversationResult>> abandonedFutures;
    };

    class ChatReplyAction : public Action
    {
    public:
        ChatReplyAction(PlayerbotAI* ai) : Action(ai, "chat message") {}
        virtual bool Execute(Event& event) override { return true; }
        bool isUseful() override;
        virtual bool isUsefulWhenStunned() override { return true; }

        static void GetAIChatPlaceholders(std::map<std::string, std::string>& placeholders, Unit* sender = nullptr, Unit* receiver = nullptr);
        static void GetAIChatPlaceholders(std::map<std::string, std::string>& placeholders, Unit* unit, const std::string preFix = "bot", Player* observer = nullptr);
        static WorldPacket GetPacketTemplate(Opcodes op, uint32 type, Unit* sender, Unit* target = nullptr, std::string channelName = "");
        static delayedPackets LinesToPackets(const std::vector<std::string>& lines, WorldPacket packetTemplate, bool debug = false, uint32 MsPerChar = 0, WorldPacket emoteTemplate = WorldPacket(), uint32 timeDiff = 0);

        static delayedPackets GenerateResponsePackets(const std::string json
            , const WorldPacket chatTemplate, const WorldPacket emoteTemplate, const WorldPacket systemTemplate, const std::string startPattern, const std::string endPattern, const std::string deletePattern, const std::string splitPattern, bool debug = false);

        static void ChatReplyDo(Player* bot, uint32 type, uint32 guid1, uint32 guid2, std::string msg, std::string chanName, std::string name);
        static bool HandleThunderfuryReply(Player* bot, ChatChannelSource chatChannelSource, std::string msg, std::string name);
        static bool HandleToxicLinksReply(Player* bot, ChatChannelSource chatChannelSource, std::string msg, std::string name);
        static bool HandleWTBItemsReply(Player* bot, ChatChannelSource chatChannelSource, std::string msg, std::string name);
        static bool HandleLFGQuestsReply(Player* bot, ChatChannelSource chatChannelSource, std::string msg, std::string name);
        static bool SendGeneralResponse(Player* bot, ChatChannelSource chatChannelSource, std::string responseMessage, std::string name);
        static std::string GenerateReplyMessage(Player* bot, std::string incomingMessage, uint32 guid1, std::string name);
    };

    class SpeakAction : public Action, public Qualified
    {
    public:
        SpeakAction(PlayerbotAI* ai) : Action(ai, "speak"), Qualified() {};
        virtual bool Execute(Event& event) override;
        virtual bool isUsefulWhenStunned() override { return true; }

#ifdef GenerateBotHelp
        virtual std::string GetHelpName() { return "speak"; } //Must equal iternal name
        virtual std::string GetHelpDescription()
        {
            return "This action wil make bots speak a certain line\n"
                   "Use \\p, \\1 \\y ect to make bots use different channels.";
        }
        virtual std::vector<std::string> GetUsedActions() { return {}; }
        virtual std::vector<std::string> GetUsedValues() { return {""}; }
#endif    
    };
}
