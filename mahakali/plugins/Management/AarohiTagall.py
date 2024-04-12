from stenzle import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ " ** ഹലോ എന്തൊക്കെയുണ്ട് ?🥱** ",
           " **ഓൺലൈൻ ഒക്കെ ഉണ്ടോ ആവോ ** ",
           " **𝐕𝐜 വാ പാട്ടുകേള്ക്കാം 😃** ",
           " **നിന്റെ കല്യാണം കഴിഞ്ഞു എന്ന് അറിഞ്ഞു 😒എന്നിട്ട് ഒരുവാക്ക് പറഞ്ഞില്ല 🤷‍♂️??🥲** ",
           " **ഈ ഗ്രൂപ്പ്ഒക്കെ ഇഷ്ടപ്പെട്ടോ? 🥺** ",
           " **ഞാൻ ഇഷ്ടമാണ് എന്ന് പറയാന് ഇരിക്കുവായിരുന്നു 🤭എന്തായാലും ഇനി ഞാൻ പറയില .** ",
           " **പെട്രോളിന്റെ വില കുതിച്ച് ഉയരുന്നുണ്ട് . അല്ലേ ? നമ്മളെ കൊണ്ട് സങ്കടപ്പെടാന് അല്ലേ കഴിയൂ 🤨** ",
           " **നിന്നെ ദോണ്ടെ 👈ലവന് മണ്ടന് എന്ന് പറഞ്ഞു . നിനക്കു വിവരം ഇല്ല എന്നാണ് അവന്റെ കണ്ടു പിടിത്തം 🙂** ",
           " **എനിക്കു റോസ് മോളെ കെട്ടിച്ച് തരോ ??🥲** ",
           " **ഈ ടെലിഗ്രാമില് ഇരിക്കുന്നത് അല്ലാതെ സ്വന്തമായി സേവിംഗ്സ് ഒക്കെ ഉണ്ടോ???😋** ",
           " **ഞാൻ ഇന്നലെ ഒരു സ്വപ്നം കണ്ടു .😍.. നമ്മുടെ കല്യാണം 👧** ",
           " **എനിക്ക്ഒരു താരാട്ടു പാടിത്തരുമോ ???😅😅** ",
           " **ഇന്ന് എണ്ണയും പഞ്ചാരെയും കൊറേ പോകും 🤔** ",
           " **താങ്ക്സ് മാത്രേ ഉള് അല്ലേ ????🙄🙄** ",
           " **ധൈര്യം ഉണ്ടെങ്കില് നിന്റെ പേരിന്റെ കൂടെ എന്റെ പേര് ചേര്ത്ത് 24 മണിക്കൂര് ഇരിക്കൂ 😕** ",
           " **നീ എവിടുന്നനേടാ കുറ്റിയും പറിച്ചു വന്നത് ??🙃** ",
           " **𝐇𝐞𝐥𝐥𝐨 𝐍𝐚𝐦𝐚𝐬𝐭𝐞😛** ",
           " **𝐇𝐞𝐥𝐥𝐨🤔** ",
           " **എന്റെ പ്രിയതമനോട് ചോദിക്കാന് എന്ത് ചോദ്യമാണ് നിനക്ക് ഉള്ളത് ???** ",
           " **ആരുടെ എങ്കിലും  ഇന്സ്റ്റാഗ്രാം റീൽ എടുക്കണോ? `/reel` {username} ഇങ്ങനെ കൊടുക്കൂ 🤗** ",
           " **അന്ന് പോയതാ .. പിന്നെ ഇന്നാ നിന്റെ പേര് തന്നെ കാണുന്നത് 😇നീ മായാവിടെ ആരെങ്കിലും ആണോ?** ",
           " **ഈ ഭൂലോകത്തിന്റെ ഓരോ സ്പന്ദനവും കണക്കിൽ ആണ് എന്ന് പറയുന്നത് വിശ്വാസിക്കുന്നുണ്ടോ?🤭** ",
           " **നാളെ ഈ ടെലിഗ്രാം അവസാനിച്ചാല് നിന്റെ അവസാന ആഗ്രഹം എന്താവും ?🥺🥺** ",
           " **നിനക്കു ആരാകാൻ ആണ് ഇഷ്ടം ?എന്തുകൊണ്ട് ?😶** ",
           " **ഈ ഗ്രൂപ്പില് നിനക്കു ഏറ്റവും ഇഷ്ടപ്പെട്ട വ്യക്തി?എന്തുകൊണ്ട് ?🤔** ",
           " **𝐎𝐲𝐞 ഈ നിമിഷം നീ മന്ത്രി ആയാല് മാറ്റാന് ആഗ്രഹക്കുന്ന നിയമം ?😜** ",
           " **നീ കൃഷ്ണ ഭക്ത ആണോ ?🙂** ",
           " **എന്റെ ഫ്രണ്ട് 😪** ",
           " **𝐍𝐢𝐜𝐞 𝐓𝐨 𝐌𝐞𝐞𝐭 𝐔𝐡☺** ",
           " **𝐇𝐞𝐥𝐥𝐨🙊** ",
           " **പ്ലീസ്സ് hide യുവർ number ??😺** ",
           " **എന്നതെങ്കിലും ഓണ് പറ 🥲** ",
           " **ഞാൻ നിന്നെ പോലെ ആണോ ??😅** ",
           " **എന്റെ കൃഷ്ണാ .. ഇത്തിരിയെങ്കിലും ബുദ്ധി ഉണ്ടായിരുന്നു എങ്കില് മന്ദബുദ്ധി എന്നെങ്കിലും വിളിക്കാമായിരുന്നു 😅** ",
           " **എന്നെ ഇഷ്ടപ്പെട്ടോ?😆😆😆** ",
           " **രാഘവോ .. രാജപ്പോ.... 😉** ",
           " **𝐈 𝐋𝐨𝐯𝐞 𝐘𝐨𝐮🙈🙈🙈** ",
           " **𝐃𝐨 𝐘𝐨𝐮 𝐋𝐨𝐯𝐞 𝐌𝐞..?👀** ",
           " **ഹിന്ദി അറിയാമോ 🙉** ",
           " **ഞാൻ പറഞ്ഞത് ആരോടും പറയല്ലേ 😹** ",
           " **നീ അറിഞ്ഞോ മേലെ മാനത്ത് 1000 ഷാപ്പുകൾ തുറക്കുന്നുണ്ട് 😻** ",
           " **ഇന്സ്റ്റാഗ്രാമില് നിനക്കു എത്ര ഫോളോവേർസ് ഉണ്ട് ??🙃** ",
           " **is,was,where ഇതൊക്കെ എവിടെയാ ചേർക്കുന്നേ എന്നൊക്കെ അറിയാമോ ?😕** ",
           " **ഇങ്ങനെ എന്നെ പോലെ തല കുത്തി നില്ക്കാൻ പറ്റുമോ ?🙃** ",
           " **കുഞ്ഞിരാമായണത്തിലെ ഇഷ്ടമുള്ള ഒരു ഡയലോഗ് പറ ?🙃** ",
           " **എത്ര പേര് ഉണ്ട് നിനക്കു ?😊** ",
           " **കേൾക്കുന്നുണ്ടോ?അതോ പോത്തിന്റെ ചെവിയില് ആണോ വേദം ഓതിക്കൊണ്ടിരുന്നത് 🧐** ",
           " **നീ ഇന്നലെ പറഞ്ഞ കാര്യം എന്തായി?** ",
           " **നിനക്കു ഇവിടുന്നു പോകാൻ ഇഷ്ടമില്ലാത്ത ഒരു വ്യക്തിയുടെ പേര് പറ😠** ",
           " **സ്നേഹം ദിവ്യമാണ് .. തേങ്ങയാണ് എന്നൊക്കെ ആരേലും പറഞ്ഞിട്ടുണ്ടോ?❤** ",
           " **അരെ  𝐊𝐲𝐚 𝐇𝐮𝐚..?👱** ",
           " **നേരെ എഴുതിയാല് ചെറുതും തലകുത്തനെ പിടിച്ചാല് വലുതും ആകുന്ന സംഖ്യ ?🤧❣️** ",
           ]

@app.on_message(filters.command(["tagall", "all", "tagmember"], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("This command can be used in groups and channels!")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("Only admin can use this command! . ")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall 👈 Try this or reply any message ...")
    else:
        return await message.reply("/tagall 👈 Try this or reply any message ..")
    if chat_id in spam_chats:
        return await message.reply("𝐏𝐥𝐞𝐚𝐬𝐞 𝐀𝐭 𝐅𝐢𝐫𝐬𝐭 𝐒𝐭𝐨𝐩 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐏𝐫𝐨𝐜𝐞𝐬𝐬 ...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command(["cancel", "stop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("No active mention process is started by me.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("This command is only for admins. You can't use this command.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♦ Mention process stopped ♦")
