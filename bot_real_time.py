import requests
import subprocess
import httpx
from ddgs import DDGS  # CORRECTED: Clean, updated search import structure
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters


# --- LIVE WEB SEARCH LOGIC ---
def search_the_internet(query):
    try:
        with DDGS() as ddgs:
            # Queries the web engine and aggregates the top 3 live text snapshots
            search_results = ddgs.text(query, max_results=3)
            snippets = [r.get('body', '') for r in search_results if 'body' in r]

            if not snippets:
                return "No real-time search snippets could be recovered."
            return "\n".join(snippets)
    except Exception as e:
        print(f"Internal Search Engine Error: {e}")
        return "No real-time search results found due to an engine exception."


# --- UPGRADED OLLAMA ENGINE ---
def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    # 1. Fetch live text from the open internet based on what user asked
    print(f"Interrogating the web for: {prompt}")
    live_internet_data = search_the_internet(prompt)
    print("Web text captured successfully.")

    # 2. Feed the raw contextual results straight to your Llama model
    system_instruction = (
        "You are an advanced AI companion running locally with real-time web verification tools. "
        "Use the following real-time web snippets to provide an accurate, up-to-date response. "
        "If the data is completely missing or unrelated, rely on your inner knowledge bases. "
        "Always reply using the same language spoken by the user.\n\n"
        f"Live Web Context:\n{live_internet_data}"
    )

    full_prompt = f"{system_instruction}\n\nUser's Inquiry: {prompt}"

    data = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, timeout=60)
        return response.json()['response']
    except Exception as e:
        return f"Error mapping text arrays over local port: {e}"


# --- REMOTE UPDATE COMMAND ---
async def update_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Checking for AI updates... please wait.")
    try:
        process = subprocess.run(["ollama", "pull", "llama3.2"], capture_output=True, text=True)
        if process.returncode == 0:
            await update.message.reply_text("✅ My brain (Llama 3.2 3B) is up to date.")
        else:
            await update.message.reply_text("❌ Update failed.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


# --- GLOBAL MESSAGE ROUTER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"Telegram User says: {user_text}")

    # Broadcast standard typing frame while scraping & computing text strings
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    ai_response = query_ollama(user_text)
    await update.message.reply_text(ai_response)


# --- RUN BOT APPLICATION ---
if __name__ == '__main__':
    # REPLACE WITH YOUR REAL TOKEN FROM BOTFATHER
    TOKEN = 'YOUR TOKEN'

    from telegram.request import HTTPXRequest

    bot_request = HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30.0,
        read_timeout=30.0,
    )

    # Force localized IPv4 handling loops to prevent standard drops on US broadband nodes
    bot_request._client = httpx.AsyncClient(
        transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0"),
        timeout=httpx.Timeout(30.0)
    )

    application = ApplicationBuilder().token(TOKEN).request(bot_request).build()

    application.add_handler(CommandHandler("update", update_model))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is successfully running over IPv4 with active web extraction protocols...")
    application.run_polling()
