def convert_data_type(source_db, target_db, data_type):
    data_type_mappings = {
        # Numeric types
        'mysql': {
            'integer': 'INTEGER',
            'decimal': 'DECIMAL',
        },
        'oracle': {
            'number': 'NUMBER',
            'decimal': 'DECIMAL',
        },
        'postgresql': {
            'integer': 'INTEGER',
            'decimal': 'DECIMAL',
        },

        # Date and time types
        'mysql': {
            'datetime': 'DATETIME',
            'date': 'DATE',
            'time': 'TIME',
        },
        'oracle': {
            'date': 'DATE',
            'timestamp': 'TIMESTAMP',
        },
        'postgresql': {
            'timestamp': 'TIMESTAMP',
            'date': 'DATE',
            'time': 'TIME',
        },

        # Character types
        'mysql': {
            'char': 'CHAR',
            'varchar': 'VARCHAR',
        },
        'oracle': {
            'char': 'CHAR',
            'varchar2': 'VARCHAR2',
            'nchar': 'NCHAR',
            'nvarchar2': 'NVARCHAR2',
        },
        'postgresql': {
            'char': 'CHARACTER',
            'varchar': 'VARCHAR',
        },
    }
    return data_type_mappings[source_db][data_type.lower()] if source_db != target_db else data_type.upper()
