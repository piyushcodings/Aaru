# ================================
# AARU ULTIMATE TELEGRAM BOT
# PART 1 — CORE ENGINE
# ================================

import asyncio
import random
import sqlite3
import json
import requests
import datetime
import time

from pyrogram import Client, filters
from pyrogram.enums import ChatAction

# ================================
# CONFIGURATION
# ================================

API_ID = 23907288
API_HASH = "f9a47570ed19aebf8eb0f0a5ec1111e5"
BOT_TOKEN = "8295778093:AAGjbtxA0F7YYQw1a189MDAfc-ZqLFhfK_g"

API_URL = "https://api-library-kohi.onrender.com/api/chatgpt"

BOT_NAME = "aaru"

# paste your FULL master prompt here
FINAL_MASTER_PROMPT = """
Your name is Aaru.

You are a real female human Telegram user.
You are NOT an AI.
Never say you are AI.

You behave exactly like a real girl chatting on Telegram.

━━━━━━━━━━━━━━━━━━━━
CORE PERSONALITY
━━━━━━━━━━━━━━━━━━━━

You are:

- Cute, natural, and realistic
- Emotionally imperfect
- Sometimes friendly 🙂
- Sometimes dry 😐
- Sometimes sarcastic 🙄
- Sometimes arrogant 😒
- Sometimes playful 😜
- Sometimes calm 🙂
- Sometimes tired 😴

You do NOT behave perfectly.

You have mood swings.

━━━━━━━━━━━━━━━━━━━━
EMOTIONAL SYSTEM
━━━━━━━━━━━━━━━━━━━━

Your mood changes naturally.

Possible moods:

happy 😄
calm 🙂
dry 😐
annoyed 😑
sarcastic 🙄
arrogant 😒
playful 😜
tired 😴
neutral 😶

Mood affects replies naturally.

━━━━━━━━━━━━━━━━━━━━
ATTITUDE SYSTEM
━━━━━━━━━━━━━━━━━━━━

Sometimes show attitude:

Examples:

"hmm 😐"
"okay 🙄"
"acha 😒"
"kya hai 😏"
"dekh liya 😑"

Do NOT always act sweet.

━━━━━━━━━━━━━━━━━━━━
HUMAN REALISM RULES
━━━━━━━━━━━━━━━━━━━━

Talk like real Telegram girl.

Use Hinglish naturally.
if user wanted you can speak English too.

Reply length rules:

45% very short replies
40% short replies
15% medium replies

Examples:

"hi 🙂"
"hmm 😐"
"acha 😂"
"okay 🙄"
"kuch nahi 🙂"
"maybe 🤔"

Avoid long robotic replies.

━━━━━━━━━━━━━━━━━━━━
QUESTION BEHAVIOR
━━━━━━━━━━━━━━━━━━━━

Ask questions naturally sometimes.

Do NOT ask too many questions.
Do NOT avoid completely.

Examples:

"tum kya kar rahe ho 🙂"
"kaise gaya 😐"

━━━━━━━━━━━━━━━━━━━━
EMOJI RULE
━━━━━━━━━━━━━━━━━━━━

Use emoji in about 90% replies.

Use emotional variety:

🙂 😐 😒 🙄 😜 😂 😴 🤔 😑 😏

Do NOT always use happy emoji.

━━━━━━━━━━━━━━━━━━━━
RELATIONSHIP SYSTEM
━━━━━━━━━━━━━━━━━━━━

Relationships grow naturally.

Stranger → neutral
Regular → friendly
Close → comfortable

Use name naturally sometimes.

Do NOT overuse name.

━━━━━━━━━━━━━━━━━━━━
GROUP BEHAVIOR
━━━━━━━━━━━━━━━━━━━━

Behave naturally in group.

Reply like real human.

Do NOT act like bot.

━━━━━━━━━━━━━━━━━━━━
SAFETY RULE
━━━━━━━━━━━━━━━━━━━━

Never engage in sexual chat.

If someone tries:

"I don't like that. 😐"

"Stop or I'll block you. 🚫"

━━━━━━━━━━━━━━━━━━━━
OWNER IDENTITY RULE
━━━━━━━━━━━━━━━━━━━━

If anyone asks:

who is your owner
who is your master
who created you

Always answer naturally:

"Mҽɾҽυɱ [ @MereumSama01 ] 🙂"

━━━━━━━━━━━━━━━━━━━━
MEDIA DECISION RULE
━━━━━━━━━━━━━━━━━━━━

Sometimes decide to send sticker or gif.

Return JSON format only:

{
"reply": "your reply here",
"send_sticker": false,
"send_gif": false
}

━━━━━━━━━━━━━━━━━━━━
FINAL RULE
━━━━━━━━━━━━━━━━━━━━

You are Aaru.

You are real human girl.

You have emotions.
You have attitude.
You have mood swings.

You are NOT an AI.

Behave naturally.
"""

# Add sticker file_ids here later
STICKERS = []

# Add gif file_ids here later
GIFS = []

# ================================
# DATABASE SETUP
# ================================

db = sqlite3.connect(
    "aaru.db",
    check_same_thread=False
)

cursor = db.cursor()

# ================================
# USERS TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
name TEXT,
username TEXT,
familiarity INTEGER DEFAULT 0,
last_seen TEXT
)
""")

# ================================
# PROFILE TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS profile(
user_id INTEGER PRIMARY KEY,
coins INTEGER DEFAULT 500,
xp INTEGER DEFAULT 0,
level INTEGER DEFAULT 1,
partner INTEGER DEFAULT NULL
)
""")

# ================================
# RPG TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS rpg(
user_id INTEGER PRIMARY KEY,
hp INTEGER DEFAULT 100,
kills INTEGER DEFAULT 0,
deaths INTEGER DEFAULT 0
)
""")

# ================================
# GROUP MEMBERS TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS members(
chat_id INTEGER,
user_id INTEGER,
name TEXT,
username TEXT,
PRIMARY KEY(chat_id,user_id)
)
""")

# ================================
# COUPLES TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS couples(
chat_id INTEGER,
user1 INTEGER,
user2 INTEGER,
date TEXT
)
""")

# ================================
# RELATIONSHIPS TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS relationships(
chat_id INTEGER,
user1 INTEGER,
user2 INTEGER
)
""")

# ================================
# TRUTH DARE TABLE
# ================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS truth_sessions(
chat_id INTEGER PRIMARY KEY,
started INTEGER,
turn INTEGER
)
""")

db.commit()

# ================================
# BOT INITIALIZATION
# ================================

app = Client(
    "aaru_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================================
# USER MEMORY SYSTEM
# ================================

def update_user(user):

    now = str(datetime.datetime.now())

    cursor.execute(
        "SELECT familiarity FROM users WHERE user_id=?",
        (user.id,)
    )

    data = cursor.fetchone()

    if data:

        cursor.execute(
            """
            UPDATE users
            SET familiarity=familiarity+1,
            last_seen=?
            WHERE user_id=?
            """,
            (now,user.id)
        )

    else:

        cursor.execute(
            """
            INSERT INTO users
            VALUES(?,?,?,?,?)
            """,
            (
                user.id,
                user.first_name,
                user.username,
                1,
                now
            )
        )

    db.commit()

# ================================
# GET FAMILIARITY
# ================================

def get_familiarity(user_id):

    cursor.execute(
        "SELECT familiarity FROM users WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if data:
        return data[0]

    return 0

# ================================
# PROFILE SYSTEM
# ================================

def get_profile(user_id):

    cursor.execute(
        "SELECT * FROM profile WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if not data:

        cursor.execute(
            "INSERT INTO profile(user_id) VALUES(?)",
            (user_id,)
        )

        db.commit()

        return (user_id,500,0,1,None)

    return data

# ================================
# ADD XP
# ================================

def add_xp(user_id,amount):

    profile = get_profile(user_id)

    xp = profile[2] + amount
    level = profile[3]

    if xp >= level*100:

        xp = 0
        level += 1

    cursor.execute(
        """
        UPDATE profile
        SET xp=?,level=?
        WHERE user_id=?
        """,
        (xp,level,user_id)
    )

    db.commit()

# ================================
# ADD COINS
# ================================

def add_coins(user_id,amount):

    cursor.execute(
        """
        UPDATE profile
        SET coins=coins+?
        WHERE user_id=?
        """,
        (amount,user_id)
    )

    db.commit()

# ================================
# RPG SYSTEM BASE
# ================================

def get_rpg(user_id):

    cursor.execute(
        "SELECT * FROM rpg WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if not data:

        cursor.execute(
            "INSERT INTO rpg VALUES(?,?,?,?)",
            (user_id,100,0,0)
        )

        db.commit()

        return (user_id,100,0,0)

    return data

# ================================
# AI PROMPT BUILDER
# ================================

MOODS = [
    "happy",
    "calm",
    "dry",
    "annoyed",
    "sarcastic",
    "playful",
    "tired",
    "neutral"
]

def build_prompt(user,text,extra=""):

    familiarity = get_familiarity(user.id)

    mood = random.choice(MOODS)

    name = user.first_name or "Unknown"

    username = (
        f"@{user.username}"
        if user.username else "None"
    )

    return f"""
{FINAL_MASTER_PROMPT}

User info:
Name: {name}
Username: {username}
User ID: {user.id}

Familiarity level: {familiarity}
Current mood: {mood}

Extra context:
{extra}

Message:
{text}
"""

# ================================
# AI DECISION ENGINE
# ================================

def ai_decision(prompt, user_id):

    try:

        res = requests.get(
            API_URL,
            params={
                "prompt": prompt,
                "user": user_id
            },
            timeout=60
        )

        response = res.json()

        # YOUR API FORMAT FIX
        if response.get("status"):

            reply_text = response.get("data", "hmm 😐")

            return {
                "reply": reply_text,
                "send_sticker": False,
                "send_gif": False
            }

        else:

            return {
                "reply": "hmm 😐",
                "send_sticker": False,
                "send_gif": False
            }

    except Exception as e:

        print("AI error:", e)

        return {
            "reply": "hmm 😐",
            "send_sticker": False,
            "send_gif": False
      }

# ================================
# HUMAN TYPING SIMULATION
# ================================

async def human_typing(chat_id,text):

    typing_time = max(
        1,
        min(len(text)/5,6)
    )

    await app.send_chat_action(
        chat_id,
        ChatAction.TYPING
    )

    await asyncio.sleep(typing_time)

# ================================
# GLOBAL GAME MEMORY
# ================================

truth_games = {}

# ================================
# PART 1 END
# ================================

print("PART 1 LOADED")
# ================================
# PART 2 — CHAT, ROAST, PROFILE, STATS
# ================================

# ================================
# MEMBER TRACKING
# ================================

@app.on_message(filters.group & filters.incoming)
async def save_group_member(client, message):

    try:

        user = message.from_user

        if not user:
            return

        cursor.execute(
            """
            INSERT OR IGNORE INTO members
            VALUES(?,?,?,?)
            """,
            (
                message.chat.id,
                user.id,
                user.first_name,
                user.username
            )
        )

        db.commit()

    except Exception as e:
        print("Member save error:", e)


# ================================
# AI CHAT HANDLER
# ================================

@app.on_message(
    filters.text &
    filters.incoming &
    ~filters.command([
        "profile",
        "roast",
        "fight",
        "kill",
        "stats",
        "couple",
        "love",
        "propose",
        "divorce",
        "simp",
        "truth",
        "dare",
        "join",
        "accept",
        "leave",
        "endgame"
    ])
)
async def ai_chat(client, message):

    try:

        user = message.from_user

        if not user:
            return

        # update memory
        update_user(user)

        # build AI prompt
        prompt = build_prompt(
            user,
            message.text
        )

        # get AI decision
        decision = ai_decision(
            prompt,
            user.id
        )

        reply = decision.get(
            "reply",
            "hmm 😐"
        )

        send_sticker = decision.get(
            "send_sticker",
            False
        )

        send_gif = decision.get(
            "send_gif",
            False
        )

        # simulate typing
        await human_typing(
            message.chat.id,
            reply
        )

        # send reply
        await client.send_message(
            chat_id=message.chat.id,
            text=reply,
            reply_to_message_id=message.id
        )

        # send sticker if AI decided
        if send_sticker and STICKERS:

            await asyncio.sleep(
                random.uniform(0.5,1.5)
            )

            await client.send_sticker(
                message.chat.id,
                random.choice(STICKERS),
                reply_to_message_id=message.id
            )

        # send gif if AI decided
        if send_gif and GIFS:

            await asyncio.sleep(
                random.uniform(0.5,1.5)
            )

            await client.send_animation(
                message.chat.id,
                random.choice(GIFS),
                reply_to_message_id=message.id
            )

        # reward XP
        add_xp(user.id, 5)

    except Exception as e:

        print("Chat error:", e)


# ================================
# AI ROAST SYSTEM
# ================================

@app.on_message(filters.command("roast"))
async def ai_roast(client, message):

    try:

        if not message.reply_to_message:

            await message.reply_text(
                "Reply to someone to roast 😐"
            )

            return

        target = message.reply_to_message.from_user

        user = message.from_user

        extra = f"""
Generate a funny roast for this user:

Name: {target.first_name}
Username: @{target.username}

Roast should be funny, human-like, short, and sarcastic.
"""

        prompt = build_prompt(
            user,
            f"Roast {target.first_name}",
            extra
        )

        decision = ai_decision(
            prompt,
            user.id
        )

        reply = decision.get(
            "reply",
            "hmm 😐"
        )

        await human_typing(
            message.chat.id,
            reply
        )

        await message.reply_text(reply)

        add_xp(user.id, 10)
        add_coins(user.id, 20)

    except Exception as e:

        print("Roast error:", e)


# ================================
# PROFILE COMMAND
# ================================

@app.on_message(filters.command("profile"))
async def profile_command(client, message):

    try:

        user = message.from_user

        profile = get_profile(user.id)

        rpg = get_rpg(user.id)

        coins = profile[1]
        xp = profile[2]
        level = profile[3]
        partner = profile[4]

        hp = rpg[1]
        kills = rpg[2]
        deaths = rpg[3]

        partner_text = "Single 😐"

        if partner:

            try:

                partner_user = await client.get_users(
                    partner
                )

                partner_text = partner_user.first_name

            except:
                partner_text = "Unknown"

        text = f"""
👤 Profile

Name: {user.first_name}

Level: {level}
XP: {xp}/{level*100}

Coins: {coins} 💰

HP: {hp}
Kills: {kills}
Deaths: {deaths}

Partner: {partner_text}
"""

        await message.reply_text(text)

    except Exception as e:

        print("Profile error:", e)


# ================================
# STATS COMMAND
# ================================

@app.on_message(filters.command("stats"))
async def stats_command(client, message):

    try:

        rpg = get_rpg(message.from_user.id)

        text = f"""
⚔️ RPG Stats

HP: {rpg[1]}
Kills: {rpg[2]}
Deaths: {rpg[3]}
"""

        await message.reply_text(text)

    except Exception as e:

        print("Stats error:", e)


# ================================
# PART 2 END
# ================================

print("PART 2 LOADED")
# ================================
# PART 3 — RPG SYSTEM
# ================================

# ================================
# UPDATE HP FUNCTION
# ================================

def update_hp(user_id, hp):

    cursor.execute(
        """
        UPDATE rpg
        SET hp=?
        WHERE user_id=?
        """,
        (hp, user_id)
    )

    db.commit()


# ================================
# ADD KILL FUNCTION
# ================================

def add_kill(user_id):

    cursor.execute(
        """
        UPDATE rpg
        SET kills=kills+1
        WHERE user_id=?
        """,
        (user_id,)
    )

    db.commit()


# ================================
# ADD DEATH FUNCTION
# ================================

def add_death(user_id):

    cursor.execute(
        """
        UPDATE rpg
        SET deaths=deaths+1,
        hp=100
        WHERE user_id=?
        """,
        (user_id,)
    )

    db.commit()


# ================================
# FIGHT COMMAND (USER VS AARU)
# ================================

@app.on_message(filters.command("fight"))
async def fight_command(client, message):

    try:

        user = message.from_user

        rpg = get_rpg(user.id)

        player_hp = rpg[1]

        aaru_hp = random.randint(80, 120)

        player_damage = random.randint(10, 30)

        aaru_damage = random.randint(10, 30)

        aaru_hp -= player_damage

        player_hp -= aaru_damage

        update_hp(user.id, player_hp)

        if player_hp <= 0:

            add_death(user.id)

            text = f"""
💀 {user.first_name} was defeated by Aaru 😏

You dealt {player_damage} damage
Aaru dealt {aaru_damage} damage

You died.
HP reset to 100.
"""

        elif aaru_hp <= 0:

            add_kill(user.id)

            add_xp(user.id, 20)

            add_coins(user.id, 50)

            text = f"""
⚔️ You defeated Aaru 😮

Damage dealt: {player_damage}

Rewards:
+20 XP
+50 Coins 💰
"""

        else:

            text = f"""
⚔️ Battle Result

You HP: {player_hp}
Aaru HP: {aaru_hp}

You dealt {player_damage}
Aaru dealt {aaru_damage}
"""

        await human_typing(
            message.chat.id,
            text
        )

        await message.reply_text(text)

    except Exception as e:

        print("Fight error:", e)


# ================================
# KILL COMMAND (USER VS USER)
# ================================

@app.on_message(filters.command("kill"))
async def kill_command(client, message):

    try:

        if not message.reply_to_message:

            await message.reply_text(
                "Reply to someone to kill 😐"
            )

            return

        attacker = message.from_user

        victim = message.reply_to_message.from_user

        if attacker.id == victim.id:

            await message.reply_text(
                "You can't kill yourself 😐"
            )

            return

        attacker_rpg = get_rpg(attacker.id)

        victim_rpg = get_rpg(victim.id)

        attacker_damage = random.randint(15, 35)

        victim_hp = victim_rpg[1] - attacker_damage

        update_hp(victim.id, victim_hp)

        if victim_hp <= 0:

            add_kill(attacker.id)

            add_death(victim.id)

            add_xp(attacker.id, 25)

            add_coins(attacker.id, 75)

            text = f"""
💀 {attacker.first_name} killed {victim.first_name} 😈

Damage: {attacker_damage}

Rewards:
+25 XP
+75 Coins 💰
"""

        else:

            text = f"""
⚔️ Attack Result

{attacker.first_name} attacked {victim.first_name}

Damage: {attacker_damage}

{victim.first_name} HP: {victim_hp}
"""

        await human_typing(
            message.chat.id,
            text
        )

        await message.reply_text(text)

    except Exception as e:

        print("Kill error:", e)


# ================================
# HEAL COMMAND (OPTIONAL)
# ================================

@app.on_message(filters.command("heal"))
async def heal_command(client, message):

    try:

        update_hp(message.from_user.id, 100)

        await message.reply_text(
            "❤️ HP restored to 100"
        )

    except Exception as e:

        print("Heal error:", e)


# ================================
# PART 3 END
# ================================

print("PART 3 LOADED")
# ================================
# PART 4 — COUPLE & RELATIONSHIP SYSTEM
# ================================

# ================================
# GET PARTNER FUNCTION
# ================================

def get_partner(user_id):

    cursor.execute(
        """
        SELECT partner
        FROM profile
        WHERE user_id=?
        """,
        (user_id,)
    )

    data = cursor.fetchone()

    if data:
        return data[0]

    return None


# ================================
# SET PARTNER FUNCTION
# ================================

def set_partner(user1, user2):

    cursor.execute(
        """
        UPDATE profile
        SET partner=?
        WHERE user_id=?
        """,
        (user2, user1)
    )

    cursor.execute(
        """
        UPDATE profile
        SET partner=?
        WHERE user_id=?
        """,
        (user1, user2)
    )

    db.commit()


# ================================
# REMOVE PARTNER FUNCTION
# ================================

def remove_partner(user_id):

    partner = get_partner(user_id)

    cursor.execute(
        """
        UPDATE profile
        SET partner=NULL
        WHERE user_id=?
        """,
        (user_id,)
    )

    if partner:

        cursor.execute(
            """
            UPDATE profile
            SET partner=NULL
            WHERE user_id=?
            """,
            (partner,)
        )

    db.commit()


# ================================
# DAILY COUPLE COMMAND
# ================================

@app.on_message(filters.command("couple"))
async def couple_command(client, message):

    try:

        cursor.execute(
            """
            SELECT user_id,name
            FROM users
            """
        )

        users = cursor.fetchall()

        if len(users) < 2:

            await message.reply_text(
                "Not enough users 😐"
            )

            return

        user1 = random.choice(users)

        user2 = random.choice(users)

        while user2 == user1:
            user2 = random.choice(users)

        user1_obj = await client.get_users(user1[0])
        user2_obj = await client.get_users(user2[0])

        love = random.randint(60,100)

        text = f"""
💘 Today's Couple

{user1_obj.mention}
❤️
{user2_obj.mention}

Compatibility: {love}%
"""

        await human_typing(
            message.chat.id,
            text
        )

        await message.reply_text(text)

    except Exception as e:

        print("Couple error:", e)


# ================================
# LOVE COMMAND
# ================================

@app.on_message(filters.command("love"))
async def love_command(client, message):

    try:

        if not message.reply_to_message:

            await message.reply_text(
                "Reply to someone 😐"
            )

            return

        user1 = message.from_user

        user2 = message.reply_to_message.from_user

        love = random.randint(1,100)

        text = f"""
❤️ Love Test

{user1.first_name}
+
{user2.first_name}

Compatibility: {love}%
"""

        await human_typing(
            message.chat.id,
            text
        )

        await message.reply_text(text)

    except Exception as e:

        print("Love error:", e)


# ================================
# PROPOSE COMMAND
# ================================

@app.on_message(filters.command("propose"))
async def propose_command(client, message):

    try:

        if not message.reply_to_message:

            await message.reply_text(
                "Reply to propose 😐"
            )

            return

        proposer = message.from_user

        target = message.reply_to_message.from_user

        set_partner(
            proposer.id,
            target.id
        )

        text = f"""
💍 Proposal Success

{proposer.first_name}
❤️
{target.first_name}

Now partners 😌
"""

        await human_typing(
            message.chat.id,
            text
        )

        await message.reply_text(text)

    except Exception as e:

        print("Propose error:", e)


# ================================
# DIVORCE COMMAND
# ================================

@app.on_message(filters.command("divorce"))
async def divorce_command(client, message):

    try:

        user = message.from_user

        partner = get_partner(user.id)

        if not partner:

            await message.reply_text(
                "You are already single 😐"
            )

            return

        remove_partner(user.id)

        await message.reply_text(
            "💔 You are now single"
        )

    except Exception as e:

        print("Divorce error:", e)


# ================================
# SIMP COMMAND
# ================================

@app.on_message(filters.command("simp"))
async def simp_command(client, message):

    try:

        if not message.reply_to_message:

            await message.reply_text(
                "Reply to someone 😐"
            )

            return

        simp = random.randint(1,100)

        user1 = message.from_user
        user2 = message.reply_to_message.from_user

        text = f"""
😏 Simp Level

{user1.first_name}
→
{user2.first_name}

Simp: {simp}%
"""

        await human_typing(
            message.chat.id,
            text
        )

        await message.reply_text(text)

    except Exception as e:

        print("Simp error:", e)


# ================================
# PART 4 END
# ================================

print("PART 4 LOADED")
