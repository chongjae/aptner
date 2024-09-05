import asyncio
from datetime import datetime, timedelta

import json

import aiohttp

from .const import APTNER_URL, AUTH_URL, CAR_LIST_URL, FEE_URL, RESERVATION_URL, RESERVATION_LIST_URL


class Aptner:
    headers = {'Content-Type': 'application/json'}
    token = None
    id = None
    password = None
    hass = None

    def __init__(self, hass, user_id, password):
        self.hass = hass
        self.id = user_id
        self.password = password
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers=self.headers
        )

    async def auth(self):
        """로그인을 수행합니다."""
        try:
            resp = await self.session.post(
                url=f"{APTNER_URL}{AUTH_URL}",
                data=json.dumps({'id': self.id, 'password': self.password})
            )
            resp.raise_for_status()
            self.token = await resp.json()
            self.headers['Authorization'] = 'Bearer ' + self.token['accessToken']
        except Exception as ex:
            raise ex

    async def get(self, get_request):
        async with aiohttp.ClientSession() as session:
            async with session.get(APTNER_URL + get_request, headers=self.headers) as response:
                if response.status == 401:
                    await self.auth()
                    async with aiohttp.ClientSession() as new_session:
                        async with new_session.get(APTNER_URL + get_request, headers=self.headers) as new_response:
                            new_response.raise_for_status()
                            return await new_response.json()
                else:
                    return await response.json()

    async def post(self, post_request, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        async with aiohttp.ClientSession() as session:
            async with session.post(APTNER_URL + post_request, headers=self.headers, data=data) as response:
                if response.status == 401:
                    await self.auth()
                    async with aiohttp.ClientSession() as new_session:  # Create a new session
                        async with new_session.post(APTNER_URL + post_request, headers=self.headers,
                                                    data=data) as new_response:
                            new_response.raise_for_status()
                            return await new_response.json()
                else:
                    return await response.json()

    async def find_car(self):
        try:
            monthly_access_history = await self.get(CAR_LIST_URL)
            now = datetime.now()
            for monthly_parking_history in monthly_access_history['monthlyParkingHistoryList']:
                first_history = monthly_parking_history['visitCarUseHistoryReportList'][0]
                out_datetime_str = first_history['outDatetime']
                out_datetime = datetime.strptime(out_datetime_str, '%Y.%m.%d %H:%M')
                time_diff = now - out_datetime
                if time_diff > timedelta(minutes=1):
                    return None
                else:
                    return first_history['carNo']
        except Exception as e:
            raise e

    async def get_cost(self):
        try:
            cost_detail = await self.get(FEE_URL)
            cost = json.dumps(cost_detail['feeList'], indent=2, ensure_ascii=False)
            cost = json.loads(cost)
            first_item = cost[0]
            formattedFee = "{:,}".format(first_item['currentFee'])
            formatted_str = f"{first_item['year']}년 {first_item['month']}월 관리비는 {formattedFee}원 입니다."
            return formatted_str
        except Exception as e:
            raise e

    async def reservation_car(self, car_no):
        try:
            cur_date = datetime.today().strftime('%Y.%m.%d')
            reservation_form = {'visitDate': cur_date, 'purpose': '지인/가족방문', 'carNo': str(car_no).strip(), 'days': 1,
                                'phone': '01012345678'}
            await self.post(RESERVATION_URL, reservation_form)
        except Exception as e:
            raise e

    async def get_current_reservation_list(self):
        try:
            reservation_list = await self.get(RESERVATION_LIST_URL)
            json_form = json.dumps(reservation_list, indent=2, ensure_ascii=False)
            json_form = json.loads(json_form)
            reserve_list = json_form['reserveList']
            reserve_formed_list = [f'잔여 예약 시간 : {json_form["visitConfig"]["availableLimitText"]}']
            for reserve in reserve_list:
                reserve_formed_list.append(f"방문 날짜 : {reserve['visitDate']}, 차량 번호 : {reserve['carNo']}")

            return reserve_formed_list
        except Exception as e:
            raise e