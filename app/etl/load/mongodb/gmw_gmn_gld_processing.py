
from sqlalchemy import text

def adjust_geopackage(engine):
    # drop column
    with engine.begin() as connection:
        # get all trigger names
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='trigger';"))
        triggers = result.fetchall()
        # drop the triggers
        if triggers!=[]:
            for trigger in triggers:
                connection.execute(text(f"DROP TRIGGER {trigger[0]};"))
        
        # layers
        layers = ["gm_gmn", "gm_gmw", "gm_gld", "gm_gmn_measuringpoint", "gm_gmw_monitoringtube"]

        for layer in layers:
            # Get the list of columns with their data types
            result = connection.execute(f"PRAGMA table_info({layer});")
            columns = [(column[1], column[2]) for column in result.fetchall()]

            if 'standardized_location' in [column[0] for column in columns]:
                # Create new table without the 'standardized_location' column
                columns = [(name, type) for name, type in columns if name != 'standardized_location']

                result = connection.execute(f"PRAGMA table_info({layer});")
                primary_keys = [row[1] for row in result.fetchall() if row[5]]

                result = connection.execute(f"PRAGMA foreign_key_list({layer});")
                foreign_keys = result.fetchall()

                # Create the foreign key SQL for the new table
                foreign_key_sql = ', '.join([f"FOREIGN KEY ({fk[3]}) REFERENCES {fk[2]}({fk[4]})" for fk in foreign_keys])

                # Create the primary key SQL for the new table
                primary_key_sql = ', '.join(primary_keys)

                # Create the column SQL for the new table
                column_sql = ', '.join([f"{name} {type}" for name, type in columns])

                # Create the new table with the foreign keys
                if foreign_key_sql:
                    connection.execute(f"""
                        CREATE TABLE {layer}_new (
                            {column_sql},
                            PRIMARY KEY ({primary_key_sql}),
                            {foreign_key_sql}
                        );
                    """)
                # Create the new table without the foreign keys (if there are none)
                else:
                    connection.execute(f"""
                        CREATE TABLE {layer}_new (
                            {column_sql},
                            PRIMARY KEY ({primary_key_sql})
                        );
                    """)

                connection.execute(f"INSERT INTO {layer}_new SELECT {', '.join(name for name, type in columns)} FROM {layer};")
                connection.execute(f"DROP TABLE {layer};")
                connection.execute(f"ALTER TABLE {layer}_new RENAME TO {layer};")