import sqlalchemy
import sqlalchemy as db
from config import settings
from sqlalchemy import create_engine, select, insert, update
from sqlalchemy.orm import Session
from models import member, event
import asyncio
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import Literal, Optional

metadata = db.MetaData()


async def test():
    engine = create_async_engine(f"mysql+aiomysql://KEK:{settings['bd_pass']}@##server_ip_port/members")
    async with AsyncSession(engine) as db:
        qr = await db.execute(select(member))
        user = qr.scalars().one()
        print(
            f"index - {user.id}, username - {user.username}, region - {user.region}, ping - {user.ping}, affiliation - {user.affiliation}, language - {user.language}")


def test_():
    engine = create_engine(f"mysql+pymysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
    else:
        print("Connection to DB failed")
    with Session(autoflush=False, bind=engine) as db:
        print("Started session")
        user = db.query(member)
        for row in user:
            print(f"row ID - {row.id}, username - {row.username}, region - {row.region}, ping - {row.ping}, affiliation - {row.affiliation}, language - {row.language}")

        db.close()
async def check(discord_id):
    engine = create_async_engine(f"mysql+aiomysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
        result = ("Connection to DB estabilished")
    else:
        print("Connection to DB failed")
        result = ("Connection to DB failed")
        return (result)
    async with AsyncSession(engine) as db:
        print("Started session")
        try:
            qr = await db.execute(select(member).filter(member.discord_id == discord_id))
            user = qr.scalars().one()
            found = True
            print(f"query, {user.id}, {found}")
        except:
            print("error")
            found = False
            print(found)
        return(found, result)
async def registrate(discord_id, discord_name):
    engine = create_async_engine(f"mysql+aiomysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
        result = ("Connection to DB estabilished")
    else:
        print("Connection to DB failed")
        result = ("Connection to DB failed")
        return (result)
    async with AsyncSession(engine) as db:
        print("Started session")
        reg_add = member(
            discord_username = discord_name,
            discord_id = str(discord_id)
        )
        print(reg_add)
        db.add(reg_add)
        await db.commit()
        await db.close()
        return(result)
async def members_list():
    engine = create_async_engine(
        f"mysql+aiomysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
        result = ("Connection to DB estabilished")
    else:
        print("Connection to DB failed")
        result = ("Connection to DB failed")
        return (result)
    async with AsyncSession(engine) as db:
        qr = await db.execute(select(member))
        user = qr.scalars()
        result_dict = [row.__dict__ for row in user]
        print(result_dict)
        await db.close()
        return(result_dict, result)
async def update_member(discord_id : int, username, region, ping, affiliation : Optional[str], language : str, records : Optional[str], fighter_pic : str):
    engine = create_async_engine(
        f"mysql+aiomysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
        async with AsyncSession(engine) as db:
            found, result = await check(discord_id)
            result1 = result
            if found == True:
                qr = await db.execute(select(member).filter(member.discord_id == discord_id))
                reg_add = {'username' : f'{username}', 'region' : f'{region}', 'ping' : f'{ping}', 'language' : f'{language}',
                           'fighter_pic' : f'{fighter_pic}', 'reg' : 1}
                if affiliation is not None:
                    reg_add.update({'affiliation' : f'{affiliation}'})
                else: pass
                if records is not None and len(records) == 2:
                    reg_add.update({'wins' : int(records[0])})
                    reg_add.update({'loses': int(records[1])})
                else: pass
                await db.execute(update(member).where(member.discord_id == discord_id).values(reg_add))
                print(reg_add)
                await db.commit()
                await db.close()
                result = "Succesfully registrated member"
                return(result)
            else:
                result = "Targeted member is not in database, member needs to send $reg"
                print(result)
                return(result)
    else:
        print("Connection to DB failed")
        result = ("Connection to DB failed")
        return(result)
async def change_member(discord_id : int, username : Optional[str], region : Optional[str], ping : Optional[str], affiliation : Optional[str], language : Optional[str], records : Optional[str], fighter_pic : Optional[str]):
    print(locals())
    args = locals()
    reg_add = {}
    if args['records'] is not None and len(args['records']) == 2:
        wins = int(args['records'][0])
        loses = int(args['records'][1])
        args.update({'wins' : wins, 'loses' : loses})
        del args['records']
    else:
        del args['records']
    for row in args:
        print(row, args[f"{row}"])
        if args[f"{row}"] is not None:

            reg_add.update({f'{row}' : f'{args[f"{row}"]}'})
        else:pass
    print(reg_add, "------ reg")
    engine = create_async_engine(
        f"mysql+aiomysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
        async with AsyncSession(engine) as db:
            found, result = await check(discord_id)
            result1 = result
            if found == True:
                await db.execute(update(member).where(member.discord_id == discord_id).values(reg_add))
                print(reg_add)
                await db.commit()
                await db.close()
                result = "Succesfully changed member"
                return(result)
            else:
                result = "Targeted member is not in database, member needs to send $reg"
                print(result)
                return(result)
    else:
        print("Connection to DB failed")
        result = ("Connection to DB failed")
        return(result)
async def registrate_list(user_list):
    engine = create_async_engine(f"mysql+aiomysql://{settings['username']}:{settings['bd_pass']}@{settings['serv']}/members")
    if engine:
        print("Connection to DB estabilished")
        result = ("Connection to DB estabilished")
    else:
        print("Connection to DB failed")
        result = ("Connection to DB failed")
        return (result)
    async with AsyncSession(engine) as db:
        print("Started session")
        await db.execute(insert(member).values(user_list))
        await db.commit()
        await db.close()
        return(result)