import json
import os.path
from typing import Optional

import requests

from .exceptions import *
from .models import *


class HelixClient:
    client_id: str
    client_secret: str
    redirect_uri: str = None
    scope: List[str] = None
    access_token: str = None
    refresh_token: str = None
    app_token: str = None
    tokenfilename: str = None

    def __init__(self, client_id: str, client_secret: str, tokefilename: str = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tokenfilename = tokefilename

    def with_user_token(self, redirect_uri: str, scope: List[str]):
        self.redirect_uri = redirect_uri
        self.scope = scope
        if self.tokenfilename and os.path.exists(self.tokenfilename):
            with open(self.tokenfilename) as tokenfile:
                token = json.load(tokenfile)
                if set(token['scope']) == set(self.scope):
                    self.access_token = token['access_token']
                    self.refresh_token = token['refresh_token']
                    self.scope = token['scope']
                else:
                    self._get_code_input()
        else:
            self._get_code_input()
        return self

    def with_app_token(self):
        self._get_app_token()
        return self

    def _save_token(self):
        if self.tokenfilename:
            with open(self.tokenfilename, 'w') as tokenfile:
                json.dump({
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'scope': self.scope,
                    'app_token': self.app_token,
                }, tokenfile)

    def _get_code_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scope),
            'state': 'mystate',
        }
        query = '&'.join(f'{key}={item}' for key, item in params.items())
        url = 'https://id.twitch.tv/oauth2/authorize'
        if query:
            url = f'{url}?{query}'
        return url

    def _get_code_input(self):
        url = self._get_code_url()
        print(f'Go to {url}')
        code = input('Enter the code from the redirect url')
        self._get_token(code)

    def _get_token(self, code: str):
        r = requests.post('https://id.twitch.tv/oauth2/token', params={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
        })
        data = r.json()
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.scope = data['scope']
        self._save_token()

    def _refresh(self):
        r = requests.post('https://id.twitch.tv/oauth2/token', params={
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        data = r.json()
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.scope = data['scope']
        self._save_token()

    def _get_app_token(self):
        r = requests.post('https://id.twitch.tv/oauth2/token', params={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        })
        self.app_token = r.json()['access_token']
        self._save_token()

    def _request(self, method: str, endpoint: str, params: dict, json: dict, *,
                 partial: list = None):
        token = self.access_token or self.app_token
        if 'eventsub' in endpoint:
            token = self.app_token
        if token is None:
            raise ValueError('no appropriate token provided')
        headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': self.client_id,
        }
        r = requests.request(method, f'https://api.twitch.tv/helix/{endpoint}', params=params, json=json,
                             headers=headers)
        if r.status_code == 200:
            j = r.json()
            if 'pagination' in j:
                if partial is None:
                    partial = j['data']
                else:
                    partial += j['data']
                if 'cursor' in j['pagination']:
                    params['after'] = j['pagination']['cursor']
                    return self._request(method, endpoint, params, json, partial=partial)
                else:
                    return partial
            else:
                return j['data']
        if r.status_code == 202:
            return r.json()['data']
        if r.status_code == 204:
            return None
        if r.status_code == 400:
            raise HelixMissingParameter()
        if r.status_code == 401:
            reason = r.json()['message']
            if reason == 'Invalid OAuth token':
                raise HelixExpiredToken()
            else:
                raise HelixError()
        if r.status_code == 500:
            raise HelixInternalServerError()
        raise HelixError()

    def request(self, method: str, endpoint: str, params: dict = None, json: dict = None):
        try:
            return self._request(method, endpoint, params, json)
        except HelixExpiredToken:
            self._refresh()
            return self._request(method, endpoint, params, json)

    def get_user(self, id: str = None, login_name: str = None) -> Optional[User]:
        params = {}
        if id:
            params['id'] = id
        if login_name:
            params['login'] = login_name
        r = self.request('get', 'users', params)
        if r:
            return User.from_json(r[0])
        return None

    def get_channel_info(self, broadcaster_id: str) -> ChannelInfo:
        r = self.request('get', 'channels', params={'broadcaster_id': broadcaster_id})
        return ChannelInfo.from_json(r[0])

    def modify_channel_info(self, broadcaster_id: str, channel_info: ChannelInfo):
        self.request('patch', 'channels', params={'broadcaster_id': broadcaster_id},
                     json=channel_info.to_json())

    def _update_reward_redemption(self, id: str, broadcaster_id: str, reward_id: str, status: str) -> RewardRedemption:
        r = self.request(
            'patch',
            'channel_points/custom_rewards/redemptions',
            params={
                'id': id,
                'broadcaster_id': broadcaster_id,
                'reward_id': reward_id,
            },
            json={
                'status': status
            }
        )
        return RewardRedemption.from_json(r[0])

    def fulfill_reward_redemption(self, id: str, broadcaster_id: str, reward_id: str) -> RewardRedemption:
        return self._update_reward_redemption(id, broadcaster_id, reward_id, 'FULFILLED')

    def cancel_reward_redemption(self, id: str, broadcaster_id: str, reward_id: str) -> RewardRedemption:
        return self._update_reward_redemption(id, broadcaster_id, reward_id, 'CANCELED')

    def eventsub_subscribe(self, type: str, version: str, condition: Condition, transport: Transport):
        return self.request('post', 'eventsub/subscriptions', json={
            'type': type,
            'version': version,
            'condition': condition.to_json(),
            'transport': transport.to_json(),
        })

    def eventsub_delete(self, id: str):
        return self.request('delete', 'eventsub/subscriptions', params={'id': id})

    def eventsub_list(self):
        # TODO add filter options
        return self.request('get', 'eventsub/subscriptions')

    def get_game(self, id: str = None, name: str = None, igdb_id: str = None) -> Optional[Game]:
        params = {}
        if id:
            params['id'] = id
        elif name:
            params['name'] = name
        elif igdb_id:
            params['igdb_id'] = igdb_id
        else:
            raise ValueError('provide at least one filter')
        r = self.request('get', 'games', params)
        if r:
            return Game.from_json(r[0])
        return None

    def get_streams(
            self,
            user_id: str = None,
            user_login: str = None,
            game_id: str = None,
            language: str = None,
    ) -> List[Stream]:
        params = {}
        if user_id:
            params['user_id'] = user_id
        if user_login:
            params['user_login'] = user_login
        if game_id:
            params['game_id'] = game_id
        if language:
            params['language'] = language
        r = self.request('get', 'streams', params)
        return [Stream.from_json(s) for s in r]
