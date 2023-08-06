from dataclasses import dataclass
from typing import List


def decode(data, cls):
    # deal with generic types like lists
    if hasattr(cls, '__origin__'):
        assert cls.__origin__ == list
        if isinstance(data, cls.__origin__):
            assert all([isinstance(x, cls.__args__[0]) for x in data])
            return data
    # deal with primitives
    if isinstance(data, cls):
        return data
    kwargs = {}
    for key, value in data.items():
        member_type = cls.__annotations__[key]
        member = decode(value, member_type)
        kwargs[key] = member
    return cls(**kwargs)


class Model:
    @classmethod
    def from_json(cls, data: dict):
        return decode(data, cls)

    def to_json(self, encode_none: bool = False):
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Model):
                data[key] = value.to_json(encode_none)
            elif value is None:
                if encode_none:
                    data[key] = None
            # TODO handle all primitive types
            elif isinstance(value, int) or isinstance(value, str):
                data[key] = value
            else:
                raise ValueError('bad type')
        return data


@dataclass
class User(Model):
    TYPE_ADMIN = 'admin'
    TYPE_GLOBAL_MOD = 'global_mod'
    TYPE_STAFF = 'staff'

    BROADCASTER_TYPE_AFFILIATE = 'affiliate'
    BROADCASTER_TYPE_PARTNER = 'partner'

    id: str
    login: str
    display_name: str
    type: str
    broadcaster_type: str
    description: str
    profile_image_url: str
    offline_image_url: str
    view_count: int
    created_at: str
    email: str = None

    @property
    def is_admin(self):
        return self.type == self.TYPE_ADMIN

    @property
    def is_global_mod(self):
        return self.type == self.TYPE_GLOBAL_MOD

    @property
    def is_staff(self):
        return self.type == self.TYPE_STAFF

    @property
    def is_affiliate(self):
        return self.broadcaster_type == self.BROADCASTER_TYPE_AFFILIATE

    @property
    def is_partner(self):
        return self.broadcaster_type == self.BROADCASTER_TYPE_PARTNER


@dataclass
class ChannelInfo(Model):
    broadcaster_id: str = None
    broadcaster_login: str = None
    broadcaster_name: str = None
    broadcaster_language: str = None
    game_id: str = None
    game_name: str = None
    title: str = None
    delay: int = None
    tags: List[str] = None


@dataclass
class Stream(Model):
    id: str
    user_id: str
    user_login: str
    user_name: str
    game_id: str
    game_name: str
    type: str
    title: str
    tags: List[str]
    viewer_count: int
    started_at: str
    language: str
    thumbnail_url: str
    tag_ids: List[str]
    is_mature: bool

    def get_thumbnail_url(self, width: int, height: int):
        url = self.thumbnail_url
        url = url.replace('{width}', str(width))
        url = url.replace('{height}', str(height))
        return url


@dataclass
class Game(Model):
    id: str
    name: str
    box_art_url: str
    igdb_id: str

    def get_box_art_url(self, width: int, height: int):
        url = self.box_art_url
        url = url.replace('{width}', str(width))
        url = url.replace('{height}', str(height))
        return url


@dataclass
class Reward(Model):
    id: str
    title: str
    prompt: str
    cost: int


@dataclass
class RewardRedemption(Model):
    broadcaster_name: str
    broadcaster_login: str
    broadcaster_id: str
    id: str
    user_id: str
    user_name: str
    user_login: str
    user_input: str
    status: str
    redeemed_at: str
    reward: Reward


@dataclass
class Condition(Model):
    pass


@dataclass
class BroadcasterCondition(Condition):
    broadcaster_user_id: str


@dataclass
class FromToCondition(Condition):
    from_broadcaster_user_id: str = None
    to_broadcaster_user_id: str = None


@dataclass
class RewardCondition(Condition):
    broadcaster_user_id: str
    reward_id: str = None


@dataclass
class Transport(Model):
    method: str
    callback: str
    secret: str
