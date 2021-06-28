import psycopg2
from psycopg2.extras import RealDictCursor

from config import DATABASE


class Database:
    def __init__(self):
        self.connect, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()
        self.cursor.close()

    @staticmethod
    def _connect():
        """
        Метод подключения к бд
        :return:
        """
        config_connect = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connect = psycopg2.connect(config_connect.format(**DATABASE))
        return connect, connect.cursor(cursor_factory=RealDictCursor)

    def _execute(self, query, row=None):
        if isinstance(row, str) or isinstance(row, int):
            row = (row,)

        response = None
        try:
            if row:
                self.cursor.execute(query, row)
            else:
                self.cursor.execute(query)
            self.connect.commit()
        except psycopg2.Error as e:
            pass
        finally:
            try:
                response = self.cursor.fetchall()
            except psycopg2.Error as e:
                print(e.pgerror)
        return response

    def get_books(self, writer_id):
        query = """
            select json_build_object('id', w.id, 'name', w.name, 'books', json_agg((SELECT x FROM (SELECT b.id, b.name) AS x)))
            from book b
            left join writer w on b.author_id = w.id
            where w.id=1
            group by w.id
            limit 1
        """
        return self._execute(query, writer_id)

    def create_book_model(self):
        query = """
            create table book
            (
                id        serial  not null
                    constraint book_pk
                        primary key,
                author_id integer not null
                    constraint book_writer_id_fk
                        references writer,
                name      text    not null
            );
            
            alter table book
                owner to postgres;
            
            create unique index book_id_uindex
                on book (id);
            
            create unique index book_name_uindex
                on book (name);
        """
        return self._execute(query)

    def create_write_model(self):
        query = """
            create table writer
            (
                id   serial not null
                    constraint writer_pk
                        primary key,
                name text   not null
            );
            
            alter table writer
                owner to postgres;
            
            create unique index writer_id_uindex
                on writer (id);
            
            create unique index writer_name_uindex
                on writer (name);
        """
        return self._execute(query)

    def create_test_rows(self):
        query = "insert into writer (name) values ('Рубина Дина Ильинична') returning id"
        writer_id = self._execute(query)[0].get('id')
        query = "insert into book (author_id, name) values (%s, 'Почерк Леонард')"
        self._execute(query, writer_id)
        query = "insert into book (author_id, name) values (%s, 'Медная шкатулка')"
        self._execute(query, writer_id)
        query = "insert into book (author_id, name) values (%s, 'Необыкновенное обыкновенное чудо')"
        self._execute(query, writer_id)
        query = "insert into writer (name) values ('Антонина Крейн') returning id"
        writer_id = self._execute(query)[0].get('id')
        query = "insert into book (author_id, name) values (%s, 'Тень разрастается')"
        self._execute(query, writer_id)
        query = "insert into book (author_id, name) values (%s, 'Академия Буря')"
        self._execute(query, writer_id)
        query = "insert into book (author_id, name) values (%s, 'Теневые блики')"
        return self._execute(query, writer_id)
