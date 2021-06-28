from fastapi import APIRouter
from base.provider import Database
router = APIRouter()


@router.get("/writers/{writer_id}")
def get_writer(writer_id: int):
    db = Database()
    return db.get_books(writer_id).get('json_build_object')
