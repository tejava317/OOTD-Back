from pydantic import BaseModel

class KakaoUserInfo(BaseModel):
    kakao_id = int
    nickname: str
    email: str | None
