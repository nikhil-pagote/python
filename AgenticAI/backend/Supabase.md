## Steps to Use Supabase REST API Only

#### Step 1: Manually Create Table in Supabase

Go to your Supabase project, then:

Click "SQL Editor".

Paste and run:

```sql
create table if not exists chat_messages (
  id serial primary key,
  session_id text,
  role text,
  message text,
  timestamp text
);
```

Go to Table Editor → chat_messages to confirm.

Done ✅

#### Step 2: Ensure REST Access is Enabled

Your table should have Row Level Security (RLS) OFF during development.

If RLS is enabled:

- Go to your chat_messages table.

- Under "Authentication" tab, disable RLS or add a rule like:

```sql
-- allow full access to anon key
CREATE POLICY "Allow anon" ON chat_messages
FOR ALL USING (true);
```

Same goes for reading (GET) and deleting (DELETE) chat messages.
This is fully functional, and you never need to call asyncpg.connect(...) again.

---

## How to Reset the Sequence (Only if You Really Want To)

If you truncate the table and want the id to reset back to 1, use:

```sql
TRUNCATE TABLE chat_messages RESTART IDENTITY;
```

> ⚠️ Be careful — this will delete all rows and reset the id counter.
