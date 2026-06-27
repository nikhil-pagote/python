from datetime import datetime
import aiohttp
from utils.keyloader import SUPABASE_ANON_KEY, SUPABASE_URL


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def save_message(session_id, role, message):
    payload = {
        "session_id": session_id,
        "role": role,
        "message": message,
        "timestamp": timestamp(),
    }

    print("📤 Sending to Supabase:", payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{SUPABASE_URL}/rest/v1/chat_messages",
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            json=payload,
        ) as resp:
            print(f"📥 Supabase response: {resp.status} {await resp.text()}")
            if resp.status >= 400:
                print("❌ Error saving message to Supabase!")


async def load_chat_history(session_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{SUPABASE_URL}/rest/v1/chat_messages",
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                "Accept": "application/json",
            },
            params={"session_id": f"eq.{session_id}", "order": "id.asc"},
        ) as resp:
            data = await resp.json()
            if isinstance(data, dict) and "message" in data:
                print(f"❌ Supabase error: {data}")
                return []
            return data


async def clear_chat_history(session_id):
    async with aiohttp.ClientSession() as session:
        await session.delete(
            f"{SUPABASE_URL}/rest/v1/chat_messages",
            headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            },
            params={"session_id": f"eq.{session_id}"},
        )
