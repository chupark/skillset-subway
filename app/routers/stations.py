import httpx
from functools import lru_cache
from typing_extensions import Annotated, Union
from ..dependency.station_list import get_station_name
from ..dependency.auth import get_token_header
from .. import config

from fastapi import APIRouter, HTTPException, Depends, Query

router = APIRouter(
    prefix="/station",
    tags=["station"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@lru_cache
def get_settings():
    return config.Settings()

_eta_description = """3호선 역의 도착 정보를 알려줍니다. 역 정보 조회시 다음 규칙을 따릅니다.
- 역이름 뒤에 오는 '역' 글자는 제외합니다.
- 오금역 조회시, /eta/오금 을 사용합니다.
- 고속터미널역 조회시, /eta/고속터미널 을 사용합니다."""
@router.get("/eta", dependencies=[Depends(get_station_name)],
                    status_code=200,
                    description="3호선 지하철(Orange line) 역 도착 정보를 알려줍니다.",
                    operation_id="getOrangeLineInfo",
                    summary=_eta_description)
async def get_eta(settings: Annotated[config.Settings, Depends(get_settings)], station_name: Annotated[str, Query()]):
    API_URL = f"http://swopenAPI.seoul.go.kr/api/subway/{settings.SUBWAY_API_KEY}/json/realtimeStationArrival/0/20/"
    res = get_3rd_station_eta(api_url=API_URL, station_name=station_name)

    return res


class SubwayMessage():
    _type: str
    _destination: str
    _eta : str
    _recent: str

def get_3rd_station_eta(api_url : str, station_name: str):
    upline = []
    downline = []
    uri = f"{api_url}{station_name}"
    with httpx.Client() as client:
        res = client.get(url=uri)
    
    eta_list = res.json()["realtimeArrivalList"]

    for eta in eta_list:
        if eta['subwayId'] == '1003' and eta['updnLine'] == '상행':
            subwayMessage = SubwayMessage()
            subwayMessage._type = "상행"
            subwayMessage._destination = eta['bstatnNm'] + "행"
            if eta['arvlCd'] == '99':
                subwayMessage._eta = str(eta['arvlMsg2']).split(" 후")[0]
            else :
                subwayMessage._eta = eta['arvlMsg2']
            subwayMessage._recent = eta['arvlMsg3']
            upline.append(subwayMessage.__dict__)
        if eta['subwayId'] == '1003' and eta['updnLine'] == '하행':
            subwayMessage = SubwayMessage()
            subwayMessage._type = "하행"
            subwayMessage._destination = eta['bstatnNm'] + "행"
            if eta['arvlCd'] == '99':
                subwayMessage._eta = str(eta['arvlMsg2']).split(" 후")[0]
            else :
                subwayMessage._eta = eta['arvlMsg2']
            subwayMessage._recent = eta['arvlMsg3']
            downline.append(subwayMessage.__dict__)
    
    message = {
        "상행선": upline,
        "하행선": downline
    }

    return message