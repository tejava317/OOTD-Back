from fastapi import APIRouter, HTTPException, Query
from app.services.kakao_auth import get_kakao_access_token, get_kakao_user_info, save_or_get_user
from app.schemas.user import KakaoUserInfo

router = APIRouter()

@router.get("/oauth/kakao/callback", response_model=KakaoUserInfo)
async def kakao_login_callback(code: str = Query(...)):
    try:
        access_token = get_kakao_access_token(code)
        user_info = get_kakao_user_info(access_token)
        user = save_or_get_user(user_info)
        return KakaoUserInfo(
            kakao_id=user.kakao_id,
            nickname=user.nickname,
            email=user.email,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
