from dotenv import load_dotenv
load_dotenv('../.env')

import uvicorn
import sys
from base.provider import Database

if __name__ == '__main__':
    argv = sys.argv[1]
    if argv == 'init':
        db = Database()
        db.create_write_model()
        db.create_book_model()
        db.create_test_rows()

    elif argv == 'start':
        uvicorn.run("__init__:app", host='0.0.0.0', port=8888, reload=True)
