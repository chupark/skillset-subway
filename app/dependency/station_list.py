from fastapi import HTTPException, Query, Header
from typing_extensions import Annotated

stations_list=["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]

async def get_station_name(station_name: Annotated[str, Query()]):
    if station_name not in stations_list:
        raise HTTPException(status_code=200, detail=f"3호선에서 {station_name}역을 찾을 수 없습니다.")