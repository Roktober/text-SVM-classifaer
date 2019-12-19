import psycopg2
import psycopg2.extras

from load_config import get_config_for_section


class ClassificatorDAO():
    """
    Contain two table with relation one to many for support multiple sources

    :classification_data: contains prepocessed text for train

    :classes: contains class for row from classification_data and source number
    """

    def __init__(self):
        self.sql_classes_insert = 'INSERT INTO classes(class_id, source, stemm_ulit_id) VALUES(%s, %s, %s)'
        self.sql_classification_data_insert = 'INSERT INTO classification_data (stemm_util) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id'
        self.sql_select_id_by_text = 'SELECT id FROM classification_data WHERE stemm_util=%s'
        config = get_config_for_section('DATABASE')
        self.database = config['database']
        self.user = config['user']
        self.password = config['password']
        self.host = config['host']
        self.port = config['port']

    def get_connection(self):
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return conn

    def select_data_for_train(self, source):
        """
        Select data for train depended on source
        """
        conn = self.get_connection()
        with conn.cursor() as cursor:
            sql = 'SELECT classification_data.stemm_util, classes.class_id FROM classification_data JOIN classes on classification_data.id = classes.stemm_ulit_id WHERE classes.source = %s'
            cursor.execute(sql, (source,))
            res = cursor.fetchall()
            return res

    def insert_data_for_train(self, data: list, classes: list, source):
        """
        Insert data for train depensed on source
        """
        conn = self.get_connection()
        with conn.cursor() as cursor:
            for stemm_util, clss in zip(data, classes):
                # Try to insert into unique field
                cursor.execute(
                    self.sql_classification_data_insert, (stemm_util,))
                res = cursor.fetchone()
                if res:  # Add class for insert semm
                    cursor.execute(
                        self.sql_classes_insert, (clss, source, res))
                else:  # If cant insert, add class for stemm
                    # TODO: solve situation when one stemm_util can have more
                    # then one class
                    cursor.execute(self.sql_select_id_by_text, (stemm_util,))
                    res = cursor.fetchone()
                    cursor.execute(
                        self.sql_classes_insert, (clss, source, res))
            conn.commit()
