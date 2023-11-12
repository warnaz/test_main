import asyncio
import datetime
import random
import string
import time

# from dotenv import dotenv_values
from typing import List, Tuple
from sqlalchemy import ForeignKey, TIMESTAMP, select, update, delete
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config_models import engine


Base = declarative_base()

class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str]

    route: Mapped['Route'] = relationship(back_populates="project")


class Route(Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_name: Mapped[str]
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    project: Mapped["Project"] = relationship(back_populates="route")
    action: Mapped[List["Action"]] = relationship(back_populates="route", uselist=True)


class Action(Base):
    __tablename__ = 'action'

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("route.id"))
    action_list_id: Mapped[int] = mapped_column(ForeignKey("action_list.id"))
    pair: Mapped[str] = mapped_column(nullable=True)

    action_list: Mapped['ActionList'] = relationship(back_populates="action")
    route: Mapped['Route'] = relationship(back_populates="action")
    action_wallet: Mapped['ActionWallet'] = relationship(back_populates="action")


class ActionList(Base):
    __tablename__ = 'action_list'

    id: Mapped[int] = mapped_column(primary_key=True)
    action_name: Mapped[str]
    code: Mapped[str]

    action: Mapped[List["Action"]] = relationship(back_populates="action_list")


class ActionWallet(Base):
    __tablename__ = 'action_wallet'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str]
    amount: Mapped[float]
    gas: Mapped[int]
    # pair: Mapped[str] = mapped_column(nullable=True)

    action_id: Mapped[int] = mapped_column(ForeignKey('action.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallet.id'))

    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now)
    estimated_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True)
    completed_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True)

    wallet: Mapped['Wallet'] = relationship(back_populates="action_wallet")
    action: Mapped['Action'] = relationship(back_populates="action_wallet")


class Wallet(Base):
    __tablename__ = 'wallet'

    id: Mapped[int] = mapped_column(primary_key=True)
    primary_key: Mapped[str]
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now)

    client: Mapped['Client'] = relationship(back_populates="wallet")
    action_wallet: Mapped['ActionWallet'] = relationship(back_populates="wallet")


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_name: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now)
    token: Mapped[str] = mapped_column(nullable=True)

    wallet: Mapped["Wallet"] = relationship(back_populates="client")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now)
    desc: Mapped[str]
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("route.id"), nullable=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("action.id"), nullable=True)
    # action_wallet_id: Mapped[int] = mapped_column(ForeignKey("action_wallet.id"), nullable=True)

    client: Mapped['Client'] = relationship(backref="status")
    wallet: Mapped['Wallet'] = relationship(backref="status")
    project: Mapped['Project'] = relationship(backref="status")
    route: Mapped['Route'] = relationship(backref="status")
    action: Mapped['Action'] = relationship(backref="status")
    # action_wallet: Mapped['ActionWallet'] = relationship(backref="status")


class CRUD():
    def __init__(self, session = None) -> None:
        if not session:
            self.session = sessionmaker(engine)
        else:
            self.session = session

    def drop_table(self):
        x = input('Вы уверены, что хотите удалить все таблицы бд? (y/n): ')

        if x == 'y':
            Base.metadata.drop_all(engine)

    async def insert_data(self, obj, **kwargs):
        with self.session() as session:
            session.add(obj)
            session.flush()
            session.refresh(obj)

            return obj

    async def insert_data_many(self, *obj, **kwargs) -> tuple:
        with self.session() as session:
            session.add_all(obj)
            session.commit()

            return obj

    async def create_client(self, name: str) -> Client:
        client = Client(client_name=name)
        result = await self.insert_data(obj=client)
        
        return result 


    def generate_token(length):
        """Generate a random token of specified length"""
        characters = string.ascii_letters + string.digits
        token = ''.join(random.choice(characters) for _ in range(length))
        return token

    async def create_wallet(self, private_key: str, client: Client) -> Wallet:
        wallet = Wallet(primary_key=private_key, client=client)
        result = await self.insert_data(obj=wallet)

        return result

    async def create_action_wallet(
            self, 
            status: str,
            amount: int,
            gas: int,
            wallet_id: int, 
            action_id: int, 
            estimated_time: datetime.datetime = None
        ) -> ActionWallet:

        action_wallet = ActionWallet(
            status=status, 
            amount=amount,
            gas=gas,
            action_id=action_id, 
            wallet_id=wallet_id, 
            estimated_time=estimated_time
        )
        result = await self.insert_data(obj=action_wallet)

        return result
    
    async def create_client_wallet(self, client_name, private_key) -> Tuple[Client, Wallet]:
        client = await self.create_client(client_name)
        wallet = await self.create_wallet(private_key, client)

        return client, wallet

    async def create_status(
            self,
            code: int, 
            desc: str,
            client: Client = None,
            wallet: Wallet = None,
            project: Project = None,
            route: Route = None,
            action: Action = None,
            data: datetime = None    
        ) -> Status:
        
        status = Status(
            code=code, 
            desc=desc, 
            created_at=data,
            client=client,
            wallet=wallet,
            project=project,
            route=route,
            action=action
        )
        result = await self.insert_data(obj=status)

        return result

    async def get_actions(self, route_id) -> ActionList:
        with self.session() as session:
            actions_list = []
            raw_sql = select(Route).where(Route.id == route_id)
            route = session.scalars(raw_sql).first()
            for item in route.action:
                raw_action = select(ActionList).where(ActionList.id == item.action_list_id)
                action = session.scalars(raw_action).first()
                actions_list.append(action)

            return actions_list
    
    async def get_single_action(self, route_id, action_id) -> Action:
        with self.session() as session:
            raw_sql = select(Action).where(Action.route_id == route_id, Action.id == action_id)
            action = session.scalars(raw_sql).first()
            
            return action

    async def get(self, id, obj):
        with self.session() as session:
            raw_sql = select(obj).where(obj.id == id)
            obj = session.scalars(raw_sql).first()
            
            return obj

    async def update(self, id, obj, **kwargs):
        with self.session() as session:
            stmt = (
                update(obj).
                where(obj.id == id).
                values(**kwargs)
            )
            session.execute(stmt)
            session.commit()
        
    async def delete(self, obj, **kwargs):
        res = input(f'Удалить данные из {obj}? (y/n): ')
        if res != 'y':
            return
        
        with self.session() as session:
            stmt = (
                delete(obj).
                where(**kwargs)
            )
            session.execute(stmt)
            session.commit()

    async def create_test_data(self):
        client_one = Client(client_name="Magomed", token="x32wdcjici9dp")
        client_two = Client(client_name="Marat", token="ch82348c299")
        client_three = Client(client_name="Rasul", token="dew9cj923j932c")

        wallet_one = Wallet(primary_key="wallet_one", client=client_one)
        wallet_two = Wallet(primary_key="wallet_two", client=client_two)
        wallet_three = Wallet(primary_key="wallet_three", client=client_three)
        wallet_four = Wallet(primary_key="wallet_four", client=client_three)
        wallet_five = Wallet(primary_key="wallet_five", client=client_two)
        wallet_six = Wallet(primary_key="wallet_six", client=client_one)

        project_one = Project(project_name="project_one")
        project_two = Project(project_name="project_two")
        project_three = Project(project_name="project_three")

        route_one = Route(route_name="route_one", project=project_one)
        route_two = Route(route_name="route_two", project=project_two)
        route_three = Route(route_name="route_three", project=project_three)

        action_list_one = ActionList(action_name="myswap", code=1)
        action_list_two = ActionList(action_name="jediswap", code=2)
        action_list_three = ActionList(action_name="avnu", code=3)
        action_list_four = ActionList(action_name="10kswap", code=4)
        action_list_five = ActionList(action_name="protoss", code=5)
        action_list_six = ActionList(action_name="sithswap", code=6)
        action_list_seven = ActionList(action_name="starknet_mint", code=7)
        action_list_eight = ActionList(action_name="pyramid_mint", code=8)
        action_list_nine = ActionList(action_name="jedi_liq", code=9)
        action_list_ten = ActionList(action_name="dmail", code=10)

        # Myswap
        one = Action(route=route_one, action_list=action_list_one)
        two = Action(route=route_one, action_list=action_list_one)
        three = Action(route=route_one, action_list=action_list_one)

        # Jediswap
        five = Action(route=route_one, action_list=action_list_two)
        six = Action(route=route_one, action_list=action_list_two)
        seven = Action(route=route_one, action_list=action_list_two)
        eight = Action(route=route_one, action_list=action_list_two)

        # Avnu
        nine = Action(route=route_one, action_list=action_list_three)
        ten = Action(route=route_one, action_list=action_list_three)
        eleven = Action(route=route_one, action_list=action_list_three)

        # 10kswap
        twl = Action(route=route_one, action_list=action_list_four)
        thrd = Action(route=route_one, action_list=action_list_four)

        # Protoss
        prot_one = Action(route=route_one, action_list=action_list_five)
        prot_two = Action(route=route_one, action_list=action_list_five)

        # SithSwap
        sith_one = Action(route=route_one, action_list=action_list_six)
        sith_two = Action(route=route_one, action_list=action_list_six)

        # Mint
        stark_min = Action(route=route_one, action_list=action_list_seven)
        pyramid_min = Action(route=route_one, action_list=action_list_eight)

        # Jedi Luqid
        jed_liq = Action(route=route_one, action_list=action_list_nine)
        
        # Dmail
        dmail_one = Action(route=route_one, action_list=action_list_ten)

        await self.insert_data_many(
            client_one, client_two, client_three,
            wallet_one, wallet_two, wallet_three, wallet_four, wallet_five, wallet_six,
            project_one, project_two, project_three,
            route_one, route_two, route_three,
            action_list_one, action_list_two, action_list_three, action_list_four, action_list_five, action_list_six, action_list_seven, action_list_eight, action_list_nine, action_list_ten,
            one, two, three, five, six, seven, eight, nine, ten, eleven, twl, thrd, prot_one, prot_two, sith_one, sith_two, stark_min, pyramid_min, jed_liq, dmail_one    
        )

        return route_one, route_two, route_three


# crud = CRUD()
# crud.drop_table()
# asyncio.run(crud.create_test_data())
