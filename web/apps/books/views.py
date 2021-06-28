from fastapi import APIRouter

from apps.books.processor import Processor
router = APIRouter()


@router.get("/writers/{writer_id}")
def get_writer(writer_id: int):
    return Processor.get_books(writer_id)
