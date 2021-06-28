from base.provider import Database


class Processor:
    @classmethod
    def get_books(cls, writer_id):
        db = Database()
        return db.get_books(writer_id)[0].get('json_build_object')