import requests
from fastapi import HTTPException
from app.core.config import settings
from app.schemas.user import KakaoUserInfo
from app.db.session import SessionLocal
from app.models.user_info import UserInfo

def get_kakao_access_token(auth_code: str) -> str:
    url = f"{settings.KAKAO_AUTH_URL}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_CLIENT_ID,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "code": auth_code,
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch access token")

    return response.json().get("access_token")

def get_kakao_user_info(access_token: str) -> KakaoUserInfo:
    url = f"{settings.KAKAO_API_URL}/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    user_info = response.json()
    return KakaoUserInfo(
        kakao_id=user_info.get("id"),
        nickname=user_info.get("properties", {}).get("nickname"),
        email=user_info.get("kakao_account", {}).get("email"),
    )

def save_or_get_user(user_info: KakaoUserInfo):
    db = SessionLocal()
    user = db.query(UserInfo).filter(UserInfo.kakao_id == user_info.kakao_id).first()
    if not user:
        user = UserInfo(
            kakao_id=user_info.kakao_id,
            nickname=user_info.nickname,
            email=user_info.email,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user