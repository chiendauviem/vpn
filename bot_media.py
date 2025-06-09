from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import TelegramClient, events, types, functions
import os, json, asyncio, aiofiles, requests

class bot_media:
    def __init__(self):
        self.channel = 'https://t.me/thanhxuan18c'
        self.user_channel = "@"+self.channel.split("/")[-1]
        self.name_bot = "bot_media"  
        self.default = "default"    
        self.count_done, self.count_sum = 0, 0
        
    async def default_bot(self):       
        path_bot = f"{self.default}/{self.name_bot}"
        api_id = 2834
        api_hash = "68875f756c9b437a8b916ca3de215815"
        token_bot = "5973577456:AAFSIzTa-mqOCYxFTY5tT8LifWpE_XpX3rs"

        self.slp_sms = 60   
        self.json_media = f"{self.default}/{self.name_bot}.json"
        self.list_user = ["taytrangwo", "camthiyen99", "windoutwo"]
        if not os.path.exists(self.json_media):
            with open(self.json_media, "w", encoding="utf-8") as f:
                json.dump({'messages': []}, f, ensure_ascii=False, indent=4)
        
        self.scheduler = AsyncIOScheduler()          
        self.bot = TelegramClient(session=path_bot, api_id=api_id, api_hash=api_hash)
        await self.bot.start(bot_token=token_bot)
        self.bot.add_event_handler(self.send_information, events.NewMessage)
        
    def get_emoji(self):
        data = requests.get("https://emojihub.yurace.pro/api/random").json()
        unicode_points = data["unicode"]
        emoji = ''.join([chr(int(u.replace("U+", ""), 16)) for u in unicode_points])
        return emoji
    
    async def json_add(self, data, chat_user, sms):
        await asyncio.sleep(5)
        try:
            async with aiofiles.open(self.json_media, "r", encoding="utf-8") as f:
                content = await f.read()
                existing_data = json.loads(content)

            existing_data['messages'].append(data)

            async with aiofiles.open(self.json_media, "w", encoding="utf-8") as f:
                await f.write(json.dumps(existing_data, ensure_ascii=False, indent=4))

            self.count_done += 1

            if self.count_done == self.count_sum:
                sms = await self.bot.send_message(chat_user, f"✅ {self.count_done} media", reply_to=sms)
                self.count_done, self.count_sum = 0, 0
                await asyncio.sleep(self.slp_sms)
                await sms.delete()

        except Exception as e:
            print(e)
    
    async def json_read(self):
        try:
            async with aiofiles.open(self.json_media, "r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content)

            messages = data.get('messages', [])
            if not messages:
                sms = await self.bot.send_message(self.list_user[0], "❌ Hết media rồi anh !")
                await asyncio.sleep(self.slp_sms)
                await sms.delete()
                return
            
            return messages

        except Exception as e:
            print(e)
    
    async def json_dele(self, ids):
        try:
            ids = int(ids)  
            async with aiofiles.open(self.json_media, 'r', encoding='utf-8') as f:
                content = await f.read()
                list_s = json.loads(content)

            messages = list_s.get("messages", [])
            non_matching_messages = [msg for msg in messages if msg.get("id") != ids]
            list_s["messages"] = non_matching_messages
            async with aiofiles.open(self.json_media, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(list_s, ensure_ascii=False, indent=4))

            print(f"🗑️ Đã xóa id: {ids}")
            
        except Exception as e:
            print(e)
          
    async def send_information(self, msg):           
        i_commands = [
            types.BotCommand("start", "Khởi động Bot 🦋"),
            types.BotCommand("kho", "Video còn lại 🎁")]
       
        try:
            await self.bot(functions.bots.SetBotCommandsRequest(scope=types.BotCommandScopeDefault(), lang_code='en', commands=i_commands))                 
            i_user = msg.chat.username         
            i_sms = msg.id  
            i_txt = msg.text 
            i_fwd_from = msg.fwd_from

            if i_txt == '/start':      
                i_first_name = msg.chat.first_name
                i_last_name = msg.chat.last_name 
                       
                full_name = i_first_name if i_last_name == "None" else f"{i_first_name} {i_last_name}"
                txt = f'❤️ Xin chào: {full_name}\n\n🤖 Bot auto downloads meida\n\n🤝 Nếu bạn cần một bot như tôi liên hệ ADMIN nhé'
                await self.bot.send_message(i_user, txt)
            
            elif i_txt == '/kho':
                files_media = await self.json_read()  
                if not files_media:
                    return 
                
                files_mxh = os.listdir(self.path_mxh)
                await self.bot.send_message(i_user, f"1️⃣ File media: {len(files_media)}\n\n2️⃣ File mxh: {len(files_mxh)}")
                                         
            elif i_user in self.list_user and (i_fwd_from or i_txt):          
                media = msg.photo if msg.photo else msg.video
                if media:
                    self.count_sum +=1
                    await self.json_add({'chat_id': msg.chat_id, 'id': msg.id}, i_user, i_sms)
           
            else:
                await self.bot.send_message(i_user, i_txt)
                
        except Exception as e:
            print(e)        
    
    async def up_media(self):
        files_media = await self.json_read() 
        if not files_media:
            return
        
        messages = files_media[:10]
        msgs = []
        for msg in messages:        
            msg = await self.bot.get_messages(msg['chat_id'], ids=msg['id'])
            if msg and msg.media:
                msgs.append(msg)
        
        if msgs:
            me = await self.bot.get_me()
            icon = self.get_emoji()
            van_ban = f'{icon} {icon} {icon}\n\n🤝 Một like, một share từ bạn là động lực lớn để mình phát triển nội dung hay hơn. Cảm ơn bạn! 💋\n\n🤖 Tác giả: @{me.username}'
            await self.bot.send_file(self.channel,file=msgs,album=True, caption=van_ban)        

        for m in messages:       
            await self.bot.delete_messages(m['chat_id'], m['id'])
            await self.json_dele(m['id'])

        sms = await self.bot.send_message(self.list_user[0], "✅ Post bài")
        await asyncio.sleep(self.slp_sms)
        await sms.delete()
        
    async def job_scheduled(self): 
        self.scheduler.add_job(self.up_media, 'cron', hour='6,10,14,18') 
        self.scheduler.start()

    async def run(self):
        self.version = f"Bot {self.name_bot} v1.1"       
        print(self.version)           
        try: 
            await self.default_bot()   
            await asyncio.gather(
                self.job_scheduled(),
                self.bot.run_until_disconnected())
        
        except Exception as e:
            print(f'False - {self.name_bot} - {e}')
   
asyncio.run(bot_media().run())    
     