from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models import StockMovement, User, Product
from app.dependencies.auth import verify_token, get_session
from app.schemas import StockMovementResponse
from datetime import date, datetime, time

router = APIRouter(prefix='/movements', tags=['movements'], dependencies=[Depends(verify_token)])

@router.get('/', response_model=list[StockMovementResponse])
async def list_all(
    product_code: str | None = None,
    user_id: int | None = None,
    movement_type: str | None = None,
    start: date | None = None,
    end: date | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(verify_token),
    ):
    query = session.query(StockMovement)

    if product_code:
        query = query.join(Product).filter(Product.code == product_code)
    if user_id:
        query = query.filter(StockMovement.user_id == user_id)
    if movement_type:
        query = query.filter(StockMovement.movement_type == movement_type)
    if start:
        start_datetime = datetime.combine(start, time.min)
        query = query.filter(StockMovement.created_at >= start_datetime)
    if end:
        end_datetime = datetime.combine(end, time.max)
        query = query.filter(StockMovement.created_at <= end_datetime)

    movements = (
        query.options(joinedload(StockMovement.user))
        .order_by(StockMovement.created_at.desc())
        .all()
    )
    return [StockMovementResponse.from_movement(m) for m in movements]
        
    