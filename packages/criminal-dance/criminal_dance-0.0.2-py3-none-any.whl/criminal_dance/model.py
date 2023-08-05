import asyncio
from typing import Awaitable, Callable, Optional
from pydantic import BaseModel
from ayaka import AyakaChannel
from .cat import cat, help_dict
from .config import R, config
from .overtime import set_overtime_task


class User(BaseModel):
    '''房间成员'''
    id: str
    name: str


class Room(BaseModel):
    '''房间'''
    users: list[User] = []
    cards: list[str] = []

    @property
    def info(self):
        items = ["当前房间人员\n"]
        items.extend(u.name for u in self.users)
        return "\n".join(items)

    def join(self, id: str, name: str):
        for u in self.users:
            if u.id == id:
                return
        else:
            user = User(id=id, name=name)
            self.users.append(user)
            return True

    def leave(self, id: str):
        for u in self.users:
            if u.id == id:
                self.users.remove(u)
                return True


class Player(BaseModel):
    '''玩家'''
    index: int

    id: str
    name: str

    cards: list[str] = []
    '''当前手牌'''

    is_good: bool = True
    '''天生都是好人，打出共犯或犯人后变坏'''

    game: "Game"

    fut: Optional[asyncio.Future]
    '''超时控制'''

    choose_card: Optional[Callable[[str], Awaitable]]
    '''需要执行的任务（放一张卡牌）'''

    class Config:
        arbitrary_types_allowed = True

    @property
    def index_name(self):
        '''座号+名字'''
        return f"[座号{self.index+1}] {self.name}"

    async def send(self, msg: str):
        '''发送私聊消息'''
        await cat.base_send(AyakaChannel(type="private", id=self.id), msg)

    async def check(self, card: str, max_num: int = 4, at_require: bool = False):
        '''检查牌是否可以打出'''
        if card != R.第一发现人 and not self.game.first:
            await self.game.send("第一张牌必须是第一发现人")
            return False
        if self.game.current_player.id != self.id:
            await self.game.send("没轮到您")
            return False
        if card not in self.cards:
            await self.game.send(f"{self.index_name} 没有{card}")
            return False
        if len(self.cards) > max_num:
            await self.game.send(f"{card}只能在手牌<={max_num}时打出")
            return False
        if at_require and not self.game.get_player(cat.event.at):
            await self.game.send("您需要at一个游戏中的玩家")
            return False
        return True

    async def play_card(self, card: str):
        '''打出一张牌并通知'''
        self.cards.remove(card)
        await self.game.send(f"{self.index_name} 打出{card}")
        if config.auto_card_help:
            await self.game.send(help_dict[card])

        # 结束超时任务
        if self.fut and not self.fut.done():
            self.fut.set_result(True)


class MarkItem(BaseModel):
    '''标志物'''
    target_id: str = ""
    '''目标id'''
    owner_id: str = ""
    '''主人id'''


class GiveAction(BaseModel):
    giver: Optional[Player]
    receiver: Optional[Player]
    card: Optional[str]

    @property
    def ready(self):
        return self.giver and self.receiver and self.card

    def convey(self):
        if self.ready:
            self.giver.cards.remove(self.card)
            self.receiver.cards.append(self.card)


class RoundGive(BaseModel):
    gives: list[GiveAction] = []

    def init(self, givers: list[Player]):
        self.gives = [GiveAction(giver=p) for p in givers]

    def get_give(self, giver_id: str):
        for g in self.gives:
            if g.giver.id == giver_id:
                return g

    @property
    def all_given(self):
        '''所有人给牌完毕'''
        for g in self.gives:
            if not g.card:
                return False
        return True

    def set_receivers(self):
        '''手牌给上家'''
        gs = [self.gives[-1], *self.gives[:-1]]
        rs = [g.giver for g in gs]
        for r, g in zip(rs, self.gives):
            g.receiver = r

    async def convey_all(self):
        for g in self.gives:
            g.convey()
            await g.giver.send(f"{g.receiver.index_name} 获得了您的{g.card}")

        for g in self.gives:
            await g.receiver.send(f"您获得了 {g.giver.index_name} 的{g.card}")
            items = ["您当前的手牌\n", *g.receiver.cards]
            await g.receiver.send("\n".join(items))


class Game(BaseModel):
    '''游戏'''
    start: bool = False

    players: list[Player] = []
    '''玩家列表'''
    index: int = 0
    '''玩家指针'''
    first: bool = False
    '''第一发现人是否已打出'''

    detect_num: int = 0
    '''剩余侦探数量'''
    cert_num: int = 0
    '''剩余不在场证明数量'''

    dog: MarkItem = MarkItem()
    '''神犬标志物'''
    police: MarkItem = MarkItem()
    '''警部标志物'''

    lock: asyncio.Lock = asyncio.Lock()
    '''同步锁，保证用户操作的原子性，防止一个用户因某种情况连出两牌的情况'''
    group_id: str = ""
    '''群聊号'''

    round_give: RoundGive = RoundGive()
    '''环绕给牌'''

    class Config:
        arbitrary_types_allowed = True

    def init(self, room: Room, group_id: str):
        '''将房间成员转换为游戏玩家'''
        # 保存群号
        self.group_id = group_id

        # 将room成员转换为玩家
        self.players = [
            Player(
                id=u.id, name=u.name,
                index=i, game=self,
                cards=room.cards[i*4:(i+1)*4],
            )
            for i, u in enumerate(room.users)
        ]

        # 统计牌数
        self.detect_num = 0
        self.cert_num = 0
        for card in room.cards:
            if card == R.侦探:
                self.detect_num += 1
            elif card == R.不在场证明:
                self.cert_num += 1

        # 设置玩家指针
        for i, p in enumerate(self.players):
            if R.第一发现人 in p.cards:
                self.index = i
                break

        # 第一发现人未打出
        self.first = False

        # 正式开始
        self.start = True

    async def send(self, msg: str):
        '''发送群聊消息'''
        await cat.base_send(AyakaChannel(type="group", id=self.group_id), msg)

    @property
    def current_player(self):
        return self.players[self.index]

    def set_state(self, state: str):
        '''在群聊、私聊均可用'''
        cat.set_state(state, AyakaChannel(type="group", id=self.group_id))

    async def turn_next(self):
        '''转移至下一个有牌的玩家'''
        n = len(self.players)
        for i in range(n):
            self.index = (self.index+1) % n
            if self.current_player.cards:
                break

        await cat.send(f"现在轮到 {self.current_player.index_name} 出牌")
        set_overtime_task(self.current_player)

    def get_player(self, uid: str):
        for p in self.players:
            if p.id == uid:
                return p

    async def end(self, good_win: bool):
        '''游戏终结，给出输赢'''
        goods = []
        bads = []
        for p in self.players:
            if p.is_good:
                goods.append(p.name)
            else:
                bads.append(p.name)

        if good_win:
            winners, losers = goods, bads
        else:
            winners, losers = bads, goods

        items = [
            "，".join(winners) + "赢了",
            "，".join(losers) + "输了",
        ]
        await self.send("\n".join(items))
        await self.send("已返回房间")
        self.set_state("room")
        
        self.start = False


Player.update_forward_refs()
