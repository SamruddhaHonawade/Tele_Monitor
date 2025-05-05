from telethon import TelegramClient, events
import asyncio
import threading
from queue import Queue

class TelegramMonitor:
    def __init__(self):
        self.client = None
        self.loop = None
        self.thread = None

    def start_monitoring(self, company_name, keywords, results_queue):
        async def main():
            from app.config import API_ID, API_HASH, PHONE_NUMBER
            self.client = TelegramClient('session_name', API_ID, API_HASH)
            await self.client.start(PHONE_NUMBER)
            
            @self.client.on(events.NewMessage)
            async def handler(event):
                if event.message.text:
                    text = event.message.text.lower()
                    if (company_name.lower() in text and 
                        any(kw in text for kw in keywords.split(','))):
                        results_queue.put({
                            'content': event.message.text[:200],
                            'channel': str(event.chat_id),
                            'date': event.message.date.isoformat()
                        })
            
            print("Monitoring started...")
            await self.client.run_until_disconnected()
        
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.thread = threading.Thread(target=self.loop.run_forever)
        self.thread.daemon = True
        self.thread.start()
        
        asyncio.run_coroutine_threadsafe(main(), self.loop)