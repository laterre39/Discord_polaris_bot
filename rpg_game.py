from asyncio.windows_events import NULL
from datetime import date
from os import putenv
import discord
from bot import bot
from database import conn
from nextcord.ext import commands

# 커서 획득
c = conn.cursor()

# 턴제 RPG 게임 구현

# 유저 레벨 인스턴스
class user_level:
    def __init__(self, level_id, level_exp):
        self.level_id = level_id
        self.level_exp = level_exp


# 유저 스킬 클래스
class skill_data:
    def __init__(self, skill_id, skill_name, skill_desc, skill_damage, skill_ctime):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.skill_damage = skill_damage
        self.skill_ctime = skill_ctime

# 유저 스킬 설정
        


class monstaer_data: # 개체 몬스터 타입 인스턴스 생성
    def __init__(self, level, hp, mana, attack, defense, skill_name, skill_damage):
        self.level = level
        self.hp = hp 
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.skill_name = skill_name
        self.skill_damage = skill_damage

@bot.group()
async def 게임(ctx):
    if ctx.invoked_subcommand != None: 
        return
    else:
        await ctx.send("반갑습니다 해당 봇에서 폴라리스 판타지 게임을 시작하려면 `$게임 도움말` 명령어를 입력해주십시오.")


@게임.command()
async def 도움말(ctx):
    await ctx.send("""
        [폴라리스 판타지 명령어 도움말]
        \n` $게임 내정보 `: 게임의 내 플레이어 정보를 확인합니다.
        \n` $게임 시스템 `: 어쩌구 저쩌구 """)


@게임.command()
async def 내정보(ctx):
        
    # DB에서 uuid 테이블의 모든 정보를 가져옴
    uuid_sql= "SELECT user_uuid FROM user_data WHERE user_uuid=?"
    c.execute(uuid_sql, (ctx.message.author.id,))
    uuid_table = c.fetchall()
    uuid_data = tuple(*uuid_table)


    # uuid 테이블에 유저 데이터가 있는지 체크 있으면 내정보 embed 출력을 없다면 테이블을 생성

    if ctx.message.author.id in uuid_data:

        # 유저의 아바타 이미지 링크를 임베드에 넣기 위해 설정
        avatar_url = ctx.message.author.display_avatar

        # 유저 데이터를 데이터베이스에서 가져온다
        stat_sql = "select * from user_data where user_uuid=?"
        c.execute(stat_sql, (ctx.message.author.id,))
        stat_table = c.fetchall()
        stat_data = tuple(*stat_table)

        # 클래스 데이터를 데이터베이스에서 가져온다
        class_sql = "select * from user_data where user_class=?"
        c.execute(class_sql, (ctx.message.author.id,))
        class_table = c.fetchall()
        class_data = tuple(*class_table)
        print(class_data)

        # 플레이어 정보를 Embed로 출력한다    
        embed=discord.Embed(title=f"[Lv.{stat_data[1]}] {ctx.message.author.name}님의 정보", description="플레이어의 스테이터스 데이터를 표시했습니다.", color=0xFF5733)
        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avatar_url}")

        if class_data[1] == 'normal':
            embed.add_field(name="직업" , value="모험가")

        embed.add_field(name="직업" , value=f"{class_data[2]}")

        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name="소지금", value=f"{stat_data[8]}G", inline=True)
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name="체력", value=f"[ +{stat_data[2]} ]", inline=True)
        embed.add_field(name="마나", value=f"[ +{stat_data[3]} ]", inline=True)
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name="공격력", value=f"[ +{stat_data[4]} ]", inline=True)
        embed.add_field(name="방어력", value=f"[ +{stat_data[5]} ]", inline=True)
        embed.add_field(name = chr(173), value = chr(173)) 
        embed.add_field(name="보유스킬", value=f"패치중...", inline=True)
        embed.set_footer(text="현재 폴라리스 판타지는 개발중에 있습니다.")

        if class_data[3] == None:
            pass
        else:
            embed.set_thumbnail(url=f"{class_data[4]}")

        await ctx.send(embed=embed)

    # 만약에 데이터가 없다면 데이터를 생성해준다
    else:
        await ctx.send(f'{ctx.message.author.name}님의 데이터가 없습니다 데이터를 생성합니다.')
        conn.execute("INSERT INTO user_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.message.author.id, 1, 0, 100, 40, 10, 0, 0, 'def', None, None))
        await ctx.send(f'유저 데이터 생성 성공!')
        await ctx.send(f'{ctx.message.author.name}님의 데이터가 성공적으로 생성되었습니다 `$게임 내정보`를 다시 입력해주세요.')


@게임.command()
async def 전직(ctx):
    
    # 클래스 데이터를 데이터베이스에서 가져온다
    class_sql = "select * from class_data where class_uuid=?"
    c.execute(class_sql, (ctx.message.author.id,))
    class_table = c.fetchall()
    class_data = tuple(*class_table)
    class_id = class_data[3]
     

    if class_id == 'id_normal':
        embed=discord.Embed(title=f"직업 전직", description="총 4가지의 직업을 제공 하고 있습니다.", color=0xFF5733)
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name = chr(173), value = chr(173))
        embed.add_field(name="직업 선택" , value=f"아래의 직업설명을 잘 확인하고 선택해주세요!")
        embed.add_field(name = chr(173), value = chr(173))
        #embed.add_field(name=f"{user_jobs.id_wa.jobd_name}", value= f"")
        embed.add_field(name=f"", value= f"")
        embed.add_field(name=f"", value= f"")
        embed.add_field(name=f"", value= f"")
        

    
    

# 만약에 에러가 발생된다면 값을 반환
# @게임.error
# async def rpg_error(ctx, error):
#     if isinstance(error, commands.CommandError):
#         await ctx.send('잘못된 명령어 사용입니다. `&게임 도움말`을 통해 사용하세요')
