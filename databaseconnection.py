import mysql.connector


class DatabaseConnection():

    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "chat_bot"
    }

    def __init__(self):
        self.db = mysql.connector.connect(**self.config)
        self.cursor = self.db.cursor()

# user query tables

    def insert_user_query(self, user_query):
        my_cursor = self.cursor
        sql = "INSERT INTO user_queries (query) VALUES (%s);"
        val = user_query
        my_cursor.execute(sql, (val,))
        self.db.commit()
        print("Data inserted successfully")

    def get_response(self, user_query):
        my_cursor = self.cursor
        sql = "SELECT bot_responses FROM user_queries where query = (%s);"
        val = user_query
        my_cursor.execute(sql, (val,))
        results = my_cursor.fetchall()
        print(f"get_response found this as a response: {results}")
        return results


# level 1,2,3,4 queries

    def get_all_grade_level(self):
        try:
            my_cursor = self.cursor
            sql = """SELECT payload FROM level_1;"""
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            print(f"get_all_grade_level found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_all_program(self):
        try:
            my_cursor = self.cursor
            sql = """SELECT payload FROM level_2;"""
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            print(f"get_all_program found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_all_degree(self):
        try:
            my_cursor = self.cursor
            sql = """SELECT payload FROM level_3;"""
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            print(f"get_all_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_all_query(self):
        try:
            my_cursor = self.cursor
            sql = """SELECT payload FROM level_4;"""
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            print(f"get_all_query found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_grade_level_list(self):
        try:
            my_cursor = self.cursor
            sql = """SELECT title, payload FROM level_1;"""
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            print(f"get_grade_level_list found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_program_list(self, program):
        try:
            my_cursor = self.cursor
            sql = """SELECT level_2.title,level_2.payload FROM level_2 
            INNER JOIN level_1 on level_1.level_1_id = level_2.level_1_id_fk WHERE level_1.payload = (%s);"""
            val = program
            my_cursor.execute(sql, (val,))
            results = my_cursor.fetchall()
            print(f"get_program_list found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    # def get_degree_list(self, grade_level, program):
    #     try:
    #         my_cursor = self.cursor
    #         sql = """SELECT level_3.title, level_3.payload FROM level_3 
    #         INNER JOIN level_2 on level_3.level_2_id_fk = level_2.level_2_id 
    #         INNER JOIN level_1 on level_2.level_1_id_fk = level_1.level_1_id 
    #         WHERE level_1.payload = (%s) AND level_2.payload = (%s);"""
    #         my_cursor.execute(sql, (grade_level, program))
    #         results = my_cursor.fetchall()
    #         print(f"get_degree_list found this as a response: {results}")
    #         return results
    #     except Exception as err:
    #         print("Err:", err)

    def get_degree_list(self, grade_level, program):
        try:
            my_cursor = self.cursor
            sql = """select l3.title, l3.payload
                    from level_3 l3 LEFT JOIN
                        level_2 l2 ON l3.level_2_id_fk = l2.level_2_id LEFT JOIN
                        level_1 l1 ON l2.level_1_id_fk = l1.level_1_id
                    where l1.payload = (%s) AND l2.payload = (%s);"""
            my_cursor.execute(sql, (grade_level, program))
            results = my_cursor.fetchall()
            print(f"get_degree_list found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_query_list(self, program, degree, course):
        try:
            my_cursor = self.cursor
            sql = """SELECT level_4.title, level_4.payload FROM level_4 
            INNER JOIN level_3 on level_4.level_3_id_fk = level_3.level_3_id 
            INNER JOIN level_2 on level_3.level_2_id_fk = level_2.level_2_id 
            INNER JOIN level_1 on level_2.level_1_id_fk = level_1.level_1_id 
            WHERE level_3.payload = (%s) AND level_2.payload = (%s) AND level_1.payload = (%s);"""
            my_cursor.execute(sql, (course, degree, program))
            results = my_cursor.fetchall()
            print(f"get_query_list found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    def get_query_response(self, program, degree, course, query):
        try:
            my_cursor = self.cursor
            sql = """SELECT details FROM level_5 
            INNER JOIN level_4 ON level_4.level_4_id = level_5.level_4_id_fk 
            INNER JOIN level_3 ON level_3.level_3_id = level_4.level_3_id_fk 
            INNER JOIN level_2 ON level_2.level_2_id = level_3.level_2_id_fk 
            INNER JOIN level_1 on level_1.level_1_id = level_2.level_1_id_fk 
            WHERE level_1.payload = (%s) AND  level_2.payload = (%s) AND  level_3.payload = (%s) AND level_4.payload = (%s);"""
            my_cursor.execute(sql, (program, degree, course, query))
            results = my_cursor.fetchall()
            print(f"get_query_response found this as a response: {results}")
            return results
        except Exception as err:
            print("Err:", err)

    # query 1
    def get_grade_from_program(self, program):
        try:
            my_cursor = self.cursor
            sql = """(select l1.title, l1.payload 
            from level_2 l2 LEFT JOIN
            level_1 l1 ON l2.level_1_id_fk = l1.level_1_id
            where l2.payload in (%s))
            UNION
            (select title, payload
            from level_1 l1
            where (select count(level_1_id_fk) cnt
                            from level_2 l2
                            where l2.payload in (%s)) = 0);
            """
            my_cursor.execute(sql, (program, program))
            results = my_cursor.fetchall()
            print(
                f"get_grade_from_program found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_grade_from_program", err)

    # query 1 tuple
    def get_grade_from_program_tuple(self, program):
        try:
            l = []
            for i in program:
                for j in i:
                    l.append(j)
            program_tuple = tuple(l)
            my_cursor = self.cursor
            sql_len_1 = """(select l1.title, l1.payload 
            from level_2 l2 LEFT JOIN
            level_1 l1 ON l2.level_1_id_fk = l1.level_1_id
            where l2.payload in ('{}'))
            UNION
            (select title, payload
            from level_1 l1
            where (select count(level_1_id_fk) cnt
                            from level_2 l2
                            where l2.payload in ('{}')) = 0);
            """
            sql = """(select l1.title, l1.payload 
            from level_2 l2 LEFT JOIN
            level_1 l1 ON l2.level_1_id_fk = l1.level_1_id
            where l2.payload in {})
            UNION
            (select title, payload
            from level_1 l1
            where (select count(level_1_id_fk) cnt
                            from level_2 l2
                            where l2.payload in {}) = 0);
            """
            print(sql.format(program_tuple, program_tuple))
            if (len(program_tuple) > 1):
                my_cursor.execute(sql.format(program_tuple, program_tuple))
            else:
                my_cursor.execute(sql_len_1.format(str(program_tuple[0]), str(program_tuple[0])))
            results = my_cursor.fetchall()
            print(
                f"get_grade_from_program found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_grade_from_program_tuple", err)

    # query 2
    def get_program_from_degree(self, degree):
        try:
            my_cursor = self.cursor
            sql = """
            (select l2.title, l2.payload from level_3 l3 LEFT JOIN
            level_2 l2 ON l3.level_2_id_fk = l2.level_2_id where l3.payload in ((%s)))
            UNION
            (select title, payload from level_2 l2 where 
            (select count(level_2_id_fk) cnt from level_3 l3 
            where l3.payload in ((%s))) = 0);"""
            my_cursor.execute(sql, (degree, degree))
            results = my_cursor.fetchall()
            print(
                f"get_program_from_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_program_from_degree", err)

    def get_program_from_grade_level(self, grade_level):
        try:
            my_cursor = self.cursor
            sql = """
            (select l2.title, l2.payload from level_3 l3 LEFT JOIN
            level_2 l2 ON l3.level_2_id_fk = l2.level_2_id where l3.payload in ((%s)))
            UNION
            (select title, payload from level_2 l2 where 
            (select count(level_2_id_fk) cnt from level_3 l3 
            where l3.payload in ((%s))) = 0);"""
            my_cursor.execute(sql, (grade_level ))
            results = my_cursor.fetchall()
            print(
                f"get_program_from_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_program_from_degree", err)

    # query 2 payload
    def get_program_from_degree_payload(self, degree):
        try:
            my_cursor = self.cursor
            sql = """
            (select l2.payload from level_3 l3 LEFT JOIN
            level_2 l2 ON l3.level_2_id_fk = l2.level_2_id where l3.payload in ((%s)))
            UNION
            (select payload from level_2 l2 where 
            (select count(level_2_id_fk) cnt from level_3 l3 
            where l3.payload in ((%s))) = 0);"""
            my_cursor.execute(sql, (degree, degree))
            results = my_cursor.fetchall()
            print(
                f"get_program_from_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_program_from_degree", err)

    def get_program_from_grade_program(self, degree, grade_level):
        try:
            my_cursor = self.cursor
            sql = """
            select level_2.payload from level_2
            left join level_1 on level_1.level_1_id = level_2.level_1_id_fk
            right join level_3 on level_2.level_2_id = level_3.level_2_id_fk
            where level_3.payload = (%s) and level_1.payload = (%s);
            """
            my_cursor.execute(sql, (degree, grade_level))
            results = my_cursor.fetchall()
            print(
                f"get_program_from_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_program_from_degree", err)

    def get_program_title_from_grade_program(self, grade_level, program):
        try:
            my_cursor = self.cursor
            sql = """
            SELECT level_2.title FROM level_2
            LEFT JOIN level_1 on level_1.level_1_id = level_2.level_1_id_fk
            WHERE level_2.payload = (%s) and level_1.payload = (%s);
            """
            my_cursor.execute(sql, (program, grade_level))
            results = my_cursor.fetchall()
            print(
                f"get_program_from_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_program_from_degree", err)

    def get_degree_title_from_program_degree(self, program, degree):
        try:
            my_cursor = self.cursor
            sql = """
            SELECT level_3.title FROM level_3
            LEFT JOIN level_2 on level_2.level_2_id = level_3.level_2_id_fk
            WHERE level_2.payload = (%s) and level_3.payload = (%s);
            """
            my_cursor.execute(sql, (program, degree))
            results = my_cursor.fetchall()
            print(
                f"get_program_from_degree found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_program_from_degree", err)

    # def get_grade_from_degree(self, degree):
    #     try:
    #         my_cursor = self.cursor
    #         sql = """SELECT title, payload FROM level_1 WHERE level_1_id IN (SELECT level_1_id_fk FROM level_2 WHERE level_2_id
    #         IN (SELECT level_2_id_fk FROM level_3 WHERE lower(payload) = (%s)))"""
    #         my_cursor.execute(sql, (degree,))
    #         results = my_cursor.fetchall()
    #         print(f"get_program_from_course found this as a response: {results}")
    #         return results
    #     except Exception as err:
    #         print("Err:",err)

    # def get_grade_from_program(self, degree):
    #     try:
    #         my_cursor = self.cursor
    #         sql = """SELECT title, payload FROM level_1 WHERE level_1_id IN
    #         (SELECT level_1_id_fk FROM level_2 WHERE payload = (%s))"""
    #         my_cursor.execute(sql, (degree,))
    #         results = my_cursor.fetchall()
    #         print(f"get_program_from_degree found this as a response: {results}")
    #         return results
    #     except Exception as err:
    #         print("Err:",err)

# feedback query

    def insert_user_feedback(self, feedback):
        try:
            my_cursor = self.cursor
            sql = """insert into user_feedback values(null, (%s))"""
            my_cursor.execute(sql, (feedback,))
            self.db.commit()
            print("Data inserted successfully")
        except Exception as err:
            print("Err:", err)


# get email list
    
    def get_email_list(self):
        try:
            my_cursor = self.cursor
            sql = """select users_name, email_address from email_address_directory;"""
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            print(
                f"get_email_list found this as a response: {results}")
            return results
        except Exception as err:
            print("Err: get_email_list", err)

    # def get_degree_from_program(self, program):
    #     try:
    #         my_cursor = self.cursor
    #         sql = """SELECT title, payload FROM level_2 WHERE level_2_id IN (SELECT level_2_id_fk FROM level_3
    #         WHERE lower(payload) = (%s))"""
    #         my_cursor.execute(sql, (program,))
    #         results = my_cursor.fetchall()
    #         print(f"get_degree_from_program found this as a response: {results}")
    #         return results
    #     except Exception as err:
    #         print("Err:",err)
