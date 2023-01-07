import discord
import json
from operator import iadd
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

bot = commands.Bot(command_prefix="iyz!",help_command=None,intents=discord.Intents.all())

##備註
##1058263622071103538
GUILD = ("1028427998396940379")

##上線回應
@bot.event
async def on_ready():
    print(f'>>{bot.user}上線<<')
    game = discord.Game("機器人編寫中，暫停使用")
    channel = bot.get_channel(1058263622071103538)
    await channel.send("Bot上線通知")


##訊息複誦-錯誤中
@bot.command()
async def sayd(self, ctx, *,msg):
    await ctx.message.delete()
    await ctx.send(+msg)

##BUG回報
@bot.command()
async def a(ctx,*,msg):
    A=ctx.author.id
    channel = bot.get_channel(1058263622071103538)
    await ctx.send("感謝您的訊息")
    user_msg = await bot.fetch_user(1009412927754866728)
    embed=discord.Embed(title="新的BUG回報", description=F"回報者:<@{A}>\nID:{A}\n回報內容{msg}", color=0x18e21b)
    embed.set_thumbnail(url="")
    embed.set_footer(text="請盡速回覆|有權限者")
    await channel.send(embed=embed)
    user_msg = await bot.fetch_user(1026305151100788736)
    await user_msg.send(f"回報者<@{A}>(他的id {A} )回報內容:"+msg)

##BUG回覆
@bot.command()
async def 回覆(ctx,id,*,msg):
    if ctx.author==91009412927754866728 or 1026305151100788736 or 864362079459475477 :
        user_msg = await bot.fetch_user(id)
        await user_msg.send(msg)
    else:
        return    


##我在哪
@bot.command()
async def 我在哪(ctx):
    await ctx.send(F"{ctx.author}你好,你現在在{ctx.guild.name}的{ctx.channel.mention}")
    channel = bot.get_channel(1058263622071103538)
    await channel.send(F"{ctx.author}在{ctx.guild.name}使用我在哪指令")  

@bot.command()
@commands.has_permissions(administrator=True)
async def clean(self, ctx, num:int):
    await ctx.channel.purge(limil=num+1)

##我是誰
@bot.command()
async def 我是誰(ctx):
    await ctx.send(F"你是**{ctx.author}**你連自己是誰都不知道嗎?")
    channel = bot.get_channel(1058263622071103538)
    await channel.send(F"{ctx.author}在{ctx.guild.name}使用我是誰指令")  

##歡迎加入
@bot.event
async def on_member_join(member):
    print(F"{member}join")
    channel = bot.get_channel(1042238181921271820)
    await channel.send(F"歡迎{member}光臨|盡情的聊天|使用服務吧")

##謝謝光臨
@bot.event
async def on_member_remove(member):
    print(F"{member}leave")
    channel = bot.get_channel(1042238181921271820)
    await channel.send(F"謝謝{member}光臨|記得回來喔")

@bot.slash_command(description="設置反應身分組")
async def reaction_role(ctx,
                        內容: Option(str, "嵌入訊息內容"),
                        role: Option(discord.Role, "要領取的身分組"),
                        emoji: Option(discord.PartialEmoji, "要添加的反應")):  # 斜線指令選項
    await ctx.defer()  # 延遲回覆
    if not ctx.author.guild_permissions.administrator:  # 如果使用者沒管理權限
        await ctx.respond(F"{ctx.author}只有管理員能使用此指令")
        return  # 結束運行
    embed = discord.Embed(title="領取身分組", description=內容)
    message = await ctx.send(embed=embed)  # 傳送領取訊息
    await message.add_reaction(emoji)  # 加入第一個反應
    with open("role.json", "r") as file:  # 用閱讀模式開啟資料儲存檔案
        data = json.load(file)  # data = 資料裡的字典{}
    with open("role.json", "w") as file:  # 用write模式開啟檔案
        data[str(message.id)] = {"role": role.id, "emoji": emoji.id}  # 新增字典資料
        json.dump(data, file, indent=4)  # 上載新增後的資料
    await ctx.respond("設置完畢", delete_after=3)


@bot.event
async def on_raw_reaction_add(payload):  # 偵測到添加反應
    with open("role.json", "r") as file:  # 用read模式開啟檔案
        data = json.load(file)  # 讀取檔案內容
    if not str(payload.message_id) in data:  # 如果檔案裡沒有資料
        return  # 結束運行
    if data[str(payload.message_id)]["emoji"] != payload.emoji.id:  # 判斷添加的反應是否是設置的反應
        return  # 結束運行
    guild = await bot.fetch_guild(payload.guild_id)  # 取得群組
    role = guild.get_role(data[str(payload.message_id)]["role"])  # 取得身分組
    await payload.member.add_roles(role, reason="反應身分組系統")  # 給予身份組
    try:
        await payload.member.send(F"已給予 {role}", delete_after=10)  # 私訊給予訊息
    except:
        pass

@bot.event
async def on_raw_reaction_remove(payload):  # 偵測到添加反應
    with open("role.json", "r") as file:  # 用read模式開啟檔案
        data = json.load(file)  # 讀取檔案內容
    if not str(payload.message_id) in data:  # 如果檔案裡沒有資料
        return  # 結束運行
    if data[str(payload.message_id)]["emoji"] != payload.emoji.id:  # 判斷添加的反應是否是設置的反應
        return  # 結束運行
    guild = await bot.fetch_guild(payload.guild_id)  # 取得群組
    role = guild.get_role(data[str(payload.message_id)]["role"])  # 取得身分組
    member = await guild.fetch_member(payload.user_id)
    await member.remove_roles(role, reason="反應身分組系統")  # 移除身分組
    try:
        await member.send(F"已移除 {role}", delete_after=10)  # 私訊給予訊息
    except:
        pass

##錯誤中
@slash_command()
@bot.slash_command(name="公告發布",description="發布公告(管管專屬)")
async def 公告發布(ctx,標題,*,內容,):
    embed=discord.Embed(title=標題, description=內容 , color=0x53f90b)
    channel = bot.get_channel(1042297731567321099)
    await channel.send(embed=embed)
    channel = bot.get_channel(1058263622071103538)
    await channel.send(F"{ctx.author}發布公告了!注意")
    await channel.send(embed=embed)
    

    
    
    

    

    

bot.run("MTA1Nzg4MDY2NTA5NTQyMTk4Mg.GQQ5_z.TPZvMnyOMfuKdnYpbiURFIynle-Pj766xMGnFo") 