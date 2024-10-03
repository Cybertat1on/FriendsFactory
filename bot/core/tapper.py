import asyncio
import random
import sys
import traceback
from itertools import cycle
from time import time
from urllib.parse import unquote

import aiohttp
import requests
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.raw.functions.messages import RequestAppWebView
from bot.core.agents import generate_random_user_agent
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers
from random import randint
import urllib3
from datetime import datetime, timezone

def convert_to_unix(time_stamp: str):
    dt_obj = datetime.strptime(time_stamp, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    return dt_obj.timestamp()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Tapper:
    def __init__(self, tg_client: Client, multi_thread: bool):
        self.multi_thread = multi_thread
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.first_name = ''
        self.last_name = ''
        self.user_id = ''
        self.auth_token = ""
        self.access_token = ""
        self.logged = False
        self.refresh_token_ = ""
        self.user_data = None
        self.balance = 0
        self.access_token_created = 0
        self.enery = 1000
        self.energy_boost = 6
        self.last_boost_used = 0
        self.factory_id = 0
        self.wokers = 0
        self.my_ref = "ref_2008453"
    async def get_tg_web_data(self, proxy: str | None) -> str:
        try:
            if settings.REF_LINK == "":
                ref_param = "ref_2008453"
            else:
                ref_param = settings.REF_LINK.split("=")[1]
        except:
            logger.error(f"<cyan>{self.session_name}</cyan> | Ref link invaild please check again !")
            sys.exit()

        actual = random.choices([self.my_ref, ref_param], weights=[30, 70], k=1)
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('fabrika')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"<light-yellow><cyan>{self.session_name}</cyan></light-yellow> | FloodWait {fl}")
                    logger.info(f"<light-yellow><cyan>{self.session_name}</cyan></light-yellow> | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=actual[0]
            ))

            auth_url = web_view.url
            # print(auth_url)
            tg_web_data = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            # print(tg_web_data)
            # await asyncio.sleep(100)
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"<light-yellow><cyan>{self.session_name}</cyan></light-yellow> | Unknown error during Authorization: "
                         f"🚨 {error}")
            await asyncio.sleep(delay=3)


    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy):
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5),)
            ip = (await response.json()).get('origin')
            logger.info(f"<cyan>{self.session_name}</cyan> | Proxy IP: <green><green>{ip}</green></green>")
            return True
        except Exception as error:
            logger.error(f"<cyan>{self.session_name}</cyan> | Proxy: {proxy} | Error: 🚨 {error}")
            return False

    def skip_onboarding(self, session: requests.Session):
        try:
            head1 = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Access-Control-Request-Headers': 'content-type',
                'Access-Control-Request-Method': 'PATCH',
                'Priority': "u=1, i",
                'Origin': 'https://ffabrika.com',
                'Referer': 'https://ffabrika.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Ch-Ua-mobile': '?1',
                'Sec-Ch-Ua-platform': '"Android"',
                'User-Agent': headers['User-Agent']
            }
            requests.options("https://api.ffabrika.com/api/v1/profile", headers=head1)
            payload = {
                "isOnboarded": True
            }
            res = session.patch("https://api.ffabrika.com/api/v1/profile", json=payload)

            res.raise_for_status()
        except:
            logger.error(f"<cyan>{self.session_name}</cyan> | <red>Unknown error while trying to skip onboarding... {res.text}</red>")

    async def get_user_info(self, session: requests.Session):
        res = session.get("https://api.ffabrika.com/api/v1/profile")
        if res.status_code == 200:
            user_data = res.json()
            check_new_user = user_data['data']['isOnboarded']
            if check_new_user is False:
                session.get("https://api.ffabrika.com/api/v1/friends/present")
                logger.info(f"<cyan>{self.session_name}</cyan> | Attempt to create new account...")
                await asyncio.sleep(randint(2, 5))
                attempt = 3
                while True:
                    self.skip_onboarding(session)
                    res = session.get("https://api.ffabrika.com/api/v1/profile")
                    user_data = res.json()
                    check_new_user = user_data['data']['isOnboarded']
                    if check_new_user or attempt == 0:
                        self.user_data = user_data['data']
                        break
                    attempt -= 1
                    await asyncio.sleep(randint(1,3))
            else:
                self.user_data = user_data['data']
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | Can't get user info: {res.text}")

    def join_squad(self, session: requests.Session):
        sid = settings.SQUAD_ID
        res = session.post(f"https://api.ffabrika.com/api/v1/squads/joining/{sid}")
        if res.status_code == 204 or res.status_code == 401:
            return res.status_code
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to join squad: {res.text}</yellow>")

    def do_task(self, session: requests.Session, task_id, task_des):
        res = session.post(f"https://api.ffabrika.com/api/v1/tasks/completion/{task_id}")
        if res.status_code == 201:
            data_ = res.json()['data']
            logger.success(f"<cyan>{self.session_name}</cyan> | Successfully completed task <green>{task_des}</green> | 💰 Balance: <yellow>{data_['score']['balance']}</yellow>")
        elif res.status_code == 401:
            self.refresh_token(session)
            self.do_task(session, task_id, task_des)
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to do task <green>{task_des}</green>: {res.text}</yellow>")

    def need_to_work(self, session: requests.Session):
        res = session.get(f"https://api.ffabrika.com/api/v1/factories/{self.factory_id}/workers?page=1")
        if res.status_code == 200:
            workers = res.json()['data']
            for worker in workers:
                if worker['task'] is None:
                    return True
        return False


    def login(self, session: requests.Session):

        head1 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': 'content-type',
            'Access-Control-Request-Method': 'POST',
            'Priority': "u=1, i",
            'Origin': 'https://ffabrika.com',
            'Referer': 'https://ffabrika.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Ch-Ua-mobile': '?1',
            'Sec-Ch-Ua-platform': '"Android"',
            'User-Agent': headers['User-Agent']
        }
        session.options("https://api.ffabrika.com/api/v1/auth/login-telegram", headers=head1)

        payload = {
            "webAppData": {
                "payload": self.auth_token
            }
        }

        response = session.post("https://api.ffabrika.com/api/v1/auth/login-telegram", json=payload)
        if response.status_code == 201:
            logger.success(f"<cyan>{self.session_name}</cyan> | Logged in ✔️")
            for cookie in response.cookies:
                if cookie.name == "acc_uid":
                    session.headers.update({"Cookie": f"{cookie.name}={cookie.value}"})

            # print(session.headers)
            res_data = response.json()['data']
            self.access_token = res_data['accessToken']['value']
            self.refresh_token_ = res_data['refreshToken']['value']
            return True
        else:
            print(response.json())
            logger.warning(f"<cyan>{self.session_name}</cyan> | <red>Failed to login</red>")
            return False

    def fetch_tasks(self, session: requests.Session):
        res = session.get("https://api.ffabrika.com/api/v1/tasks")
        if res.status_code == 200:
            tasks = res.json()['data']
            return tasks
        elif res.status_code == 401:
            self.refresh_token(session)
            self.fetch_tasks(session)
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to fetch tasks: {res.text}</yellow>")
            return []

    def tap(self, session: requests.Session, tap_count: int):
        payload = {
            "count": tap_count
        }
        res = session.post("https://api.ffabrika.com/api/v1/scores", json=payload)
        if res.status_code == 201:
            data = res.json()['data']
            logger.success(f"<cyan>{self.session_name}</cyan> | Successfully tapped <cyan>{tap_count}</cyan> times | Earned <cyan>{tap_count}</cyan> - Balance: <yellow>{data['score']['balance']}</yellow> | Energy left: <red>{data['energy']['balance']}</red>")
            self.enery = data['energy']['balance']
            self.balance = data['score']['balance']
        elif res.status_code == 401:
            self.refresh_token(session)
            self.tap(session, tap_count)
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to tap: {res.text}</yellow>")


    def boost_energy(self, session: requests.Session):
        res = session.post("https://api.ffabrika.com/api/v1/energies/recovery")
        if res.status_code == 201:
            logger.success(f"<cyan>{self.session_name}</cyan> | <green>Successfully use energy boost !</green>")
            data = res.json()
            self.enery = data['data']['balance']
            self.energy_boost = data['data']['currentRecoveryLimit']
            self.last_boost_used = data['data']['lastRecoveryAt']
            return True
        elif res.status_code == 401:
            self.refresh_token(session)
            self.boost_energy(session)
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to boost energy: {res.text}</yellow>")
        return False

    def check_time(self, available_time):
        # print(f"{convert_to_unix(available_time)} | {time()}")
        if available_time == 0:
            return True
        if convert_to_unix(available_time) < time() - 3600:
            return True
        else:
            return False

    def get_factory_info(self, session: requests.Session):
        res = session.get(f"https://api.ffabrika.com/api/v1/factories/{self.factory_id}")
        if res.status_code == 200:
            return res.json()['data']
        elif res.status_code == 401:
            self.refresh_token(session)
            self.get_factory_info(session)
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to get factory info: {res.text}</yellow>")
            return None
    def purchase(self, session: requests.Session, worker_id):
        res = session.post(f"https://api.ffabrika.com/api/v1/market/workers/{worker_id}/purchase")
        if res.status_code == 204:
            return True
        else:
            logger.info(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to purchase worker {worker_id}: {res.text}</yellow>")
            return False


    def get_score(self, session):
        res = session.get("https://api.ffabrika.com/api/v1/scores")
        if res.status_code == 200:
            data_ = res.json()
            logger.info(f"<cyan>{self.session_name}</cyan> | Balance: <cyan>{data_['data']['balance']}</cyan>")
            self.balance = data_['data']['balance']

    def get_user_info2(self, session: requests.Session):
        res = session.get("https://api.ffabrika.com/api/v1/profile")
        if res.status_code == 200:
            data = res.json()['data']
            logger.info(f"<cyan>{self.session_name}</cyan> | Balance: <cyan>{data['score']['balance']}</cyan>")
    def get_workers_data(self, session: requests.Session):
        res = session.get("https://api.ffabrika.com/api/v1/market/workers?page=1&limit=20")
        if res.status_code == 200:
            worker_data = res.json()['data']
            for worker in worker_data:
                if self.wokers >= settings.MAX_NUMBER_OF_WORKER_TO_BUY:
                    break
                if worker['isProtected']:
                    continue
                elif worker['isProtected'] is False:
                    if self.purchase(session, worker['id']):
                        self.wokers += 1
                        logger.success(
                            f"<cyan>{self.session_name}</cyan> | 🤝  Successfully bought worker: <green>{worker['nickname']}</green>")
                        self.get_score(session)

    def collect_reward(self, session: requests.Session, value):
        res = session.post("https://api.ffabrika.com/api/v1/factories/my/rewards/collection")
        if res.status_code == 204:
            logger.success(f"<cyan>{self.session_name}</cyan> | Successfully claimed <yellow>{value}</yellow>")
            self.get_user_info2(session)
    async def send_worker_to_work(self, session: requests.Session):
        payload = {
            "type": "fastest"
        }
        res = session.post(f"https://api.ffabrika.com/api/v1/factories/my/workers/tasks/assignment", json=payload)
        if res.status_code == 204:
            logger.success(f"<cyan>{self.session_name}</cyan> | <green>Successfully sent all worker to work!</green>")
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to send worker to work: {res.text}</yellow>")


    def refresh_token(self, session: requests.Session):
        headers['Cookie'] = f"ref_uid={self.refresh_token}"
        res = session.post("https://api.ffabrika.com/api/v1/auth/refresh", json={})
        if res.status_code == 201:
            data_ = res.json()['data']
            for cookie in res.cookies:
                if cookie.name == "acc_uid":
                    session.headers.update({"Cookie": f"{cookie.name}={cookie.value}"})

            self.refresh_token_ = data_['refreshToken']['value']
            logger.success(f"<cyan>{self.session_name}</cyan> | <green>Refresh token successfully !</green>")
        else:
            logger.warning(f"<cyan>{self.session_name}</cyan> | <yellow>Failed to refresh token:</yellow> {res.text}")
    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        headers["User-Agent"] = generate_random_user_agent(device_type='android', browser_type='chrome')
        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)

        session = requests.Session()
        session.headers.update(headers)

        if proxy:
            proxy_check = await self.check_proxy(http_client=http_client, proxy=proxy)
            if proxy_check:
                proxy_type = proxy.split(':')[0]
                proxies = {
                    proxy_type: proxy
                }
                session.proxies.update(proxies)
                logger.info(f"<cyan>{self.session_name}</cyan> | bind with proxy ip: {proxy}")

        token_live_time = randint(3400, 3600)
        while True:
            try:
                if time() - access_token_created_time >= token_live_time:
                    tg_web_data = await self.get_tg_web_data(proxy=proxy)
                    self.auth_token = tg_web_data
                    access_token_created_time = time()
                    token_live_time = randint(3400, 3600)

                # print(self.logged)
                if self.login(session):
                    await self.get_user_info(session)
                    self.balance = int(self.user_data['score']['balance'])
                    self.enery = self.user_data['energy']['balance']
                    self.energy_boost = self.user_data['energy']['currentRecoveryLimit']
                    self.last_boost_used = self.user_data['energy']['lastRecoveryAt'] if self.user_data['energy']['lastRecoveryAt'] else 0
                    self.factory_id = self.user_data['factory']['id']

                    if self.user_data['squad'] is None:
                        squad = "No squad"
                    else:
                        squad = self.user_data['squad']['title']
                    user_stats = f"""
<cyan>==={self.user_data['username']}===</cyan>
Status: <green>{self.user_data['status']}</green>
Total Earned: <yellow>{self.user_data['score']['total']}</yellow>
Balance: <yellow>{self.user_data['score']['balance']}</yellow>
Squad: <red>{squad}</red>
Daily Reward:
    -------------
     Streak: <cyan>{self.user_data['dailyReward']['daysCount']}</cyan>
     Claimed: <red>{self.user_data['dailyReward']['isRewarded']}</red>
    -------------                """
                    logger.info(f"<cyan>{self.session_name}</cyan> | User stats 📊 \n{user_stats}")

                    if self.user_data['dailyReward']['isRewarded'] is False:
                        res = session.post("https://api.ffabrika.com/api/v1/daily-rewards/receiving")

                        if res.status_code == 401:
                            self.refresh_token(session)
                            continue
                        elif res.status_code == 204:
                            res = session.get("https://api.ffabrika.com/api/v1/scores")
                            if res.status_code == 200:
                                logger.success(f"<cyan>{self.session_name}</cyan> | Claimed daily reward! | Balance: <yellow>{res.json()['data']['balance']}</yellow>")
                                await asyncio.sleep(random.uniform(2,5))
                        else:
                            logger.warning(f"<cyan>{self.session_name}</cyan> <yellow>Failed to claim daily reward: {res.text}</yellow>")

                    if squad == "No squad":
                        res_code = self.join_squad(session)
                        if res_code == 204:
                            res = session.get(f"https://api.ffabrika.com/api/v1/squads/{settings.SQUAD_ID}")
                            if res.status_code == 200:
                                logger.success(f"<cyan>{self.session_name}</cyan> | <green>Joined squad: <cyan>{res.json()['data']['title']}</cyan></green>")

                        elif res_code == 401:
                            self.refresh_token(session)
                            continue

                    if settings.AUTO_TASK:
                        task_list = self.fetch_tasks(session)
                        # print(task_list)
                        if task_list is not None:
                            for task in task_list:
                                if task['isCompleted'] is False:
                                    self.do_task(session, task['id'], task['description'])

                if settings.AUTO_MANAGE_FACTORY:
                    factory_info = self.get_factory_info(session)
                    if factory_info:
                        self.wokers = factory_info['totalWorkersCount']
                        if factory_info['totalWorkersCount'] < settings.MAX_NUMBER_OF_WORKER_TO_BUY:
                            self.get_workers_data(session)

                        if factory_info['rewardCount'] > 0:
                            self.collect_reward(session,factory_info['rewardCount'])

                        if self.need_to_work(session):
                            await self.send_worker_to_work(session)




                if settings.AUTO_TAP:
                    i = randint(5, 15)
                    while i > 0:
                        i -= 1
                        tap_count = randint(settings.TAP_COUNT[0], settings.TAP_COUNT[1])
                        if self.enery > settings.SLEEP_BY_MIN_ENERGY:
                            tap_count = min(tap_count, self.enery)
                            self.tap(session, tap_count)
                            sleep_ = random.uniform(settings.SLEEP_BETWEEN_TAPS[0], settings.SLEEP_BETWEEN_TAPS[1])
                            logger.info(f"<cyan>{self.session_name}</cyan> | 💤 Sleep <red>{round(sleep_)}s...</red>")
                            await asyncio.sleep(sleep_)
                        else:
                            if settings.AUTO_BOOST:
                                if self.energy_boost > 1:
                                    if self.check_time(self.last_boost_used):
                                        self.boost_energy(session)
                                        await asyncio.sleep(random.uniform(1, 3))
                                    else:
                                        logger.info(f"<cyan>{self.session_name}</cyan> | 😵 Not time to use boost!")
                                        break
                                else:
                                    logger.info(f"<cyan>{self.session_name}</cyan> | 😖 No energy boost left...")
                                    break
                            else:
                                break

                if self.multi_thread:
                    sleep_ = randint(500, 1000)
                    logger.info(f"<cyan>{self.session_name}</cyan> | 💤 Sleep <red>{round(sleep_)}s...</red>")
                    await asyncio.sleep(sleep_)
                else:
                    logger.info(f"==<cyan><cyan>{self.session_name}</cyan></cyan>==")
                    await http_client.close()
                    session.close()
                    break
            except InvalidSession as error:
                raise error

            except Exception as error:
                traceback.print_exc()
                logger.error(f"<cyan>{self.session_name}</cyan> | Unknown error: 🚨 {error}")
                await asyncio.sleep(delay=randint(60, 120))

async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        sleep_ = randint(1, 15)
        logger.info(f"{tg_client.name} | start after {round(sleep_)}s")
        # await asyncio.sleep(sleep_)
        await Tapper(tg_client=tg_client, multi_thread=True).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")

async def run_tapper1(tg_clients: list[Client], proxies):
    proxies_cycle = cycle(proxies) if proxies else None
    while True:
        for tg_client in tg_clients:
            try:
                await Tapper(tg_client=tg_client, multi_thread=False).run(next(proxies_cycle) if proxies_cycle else None)
            except InvalidSession:
                logger.error(f"{tg_client.name} | Invalid Session")

            sleep_ = randint(settings.DELAY_EACH_ACCOUNT[0], settings.DELAY_EACH_ACCOUNT[1])
            logger.info(f"💤 Sleep <red>{round(sleep_)}s...</red>")
            await asyncio.sleep(sleep_)

        sleep_ = randint(520, 700)
        logger.info(f"💤 Sleep <red>{round(sleep_)}s...</red>")
        await asyncio.sleep(sleep_)