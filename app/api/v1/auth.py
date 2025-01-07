from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
from app.models.user_info import UserInfo
from app.schemas.user import KakaoUserInfo
from app.db.session import get_db

router = APIRouter()

logger = logging.getLogger("kakao_user_logger")

@router.post("/save-user-info")
async def save_kakao_user_info(user_info: KakaoUserInfo, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received Kakao ID: {user_info.kakao_id}")

        existing_user = db.query(UserInfo).filter(
            UserInfo.kakao_id == user_info.kakao_id
        ).first()
        if existing_user:
            return {"message": "Existing user information verified successfully"}

        new_user = UserInfo(
            kakao_id = user_info.kakao_id,
            nickname=user_info.nickname,
            profile_image=user_info.profile_image
        )
        print()
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "New user information saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to verify user information: {str(e)}")
