
from sqlalchemy import text

def adjust_geopackage(metadata, engine):
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
            result = connection.execute(text(f"PRAGMA table_info({layer});"))
            columns = [(column[1], column[2]) for column in result.fetchall()]

            primary_keys_dict = {"gm_gmn":"gm_gmn_pk", "gm_gmw":"gm_gmw_pk", "gm_gld":"gm_gld_pk", 
                            "gm_gmn_measuringpoint":"gm_gmn_measuringpoint_pk", 
                            "gm_gmw_monitoringtube": "gm_gmw_monitoringtube_pk"}
            
            foreign_keys_dict = {
                "gm_gmn":[], 
                "gm_gmw":[], 
                "gm_gld":["gm_gmw_monitoringtube_fk"], 
                "gm_gmn_measuringpoint":["gm_gmn_fk", "gm_gmw_monitoringtube_fk"], 
                "gm_gmw_monitoringtube": ["gm_gmw_fk"]
                }

            if 'standardized_location' in [column[0] for column in columns]:
                # Create new table without the 'standardized_location' column
                columns = [(name, type) for name, type in columns if name != 'standardized_location']

                primary_key = [primary_keys_dict[layer]]
                foreign_keys = foreign_keys_dict[layer]

                # Create the foreign key SQL for the new table
                if len(foreign_keys) > 0:
                    foreign_key_sql = ', '.join([f"FOREIGN KEY ({fk}) REFERENCES {fk[:-3]}({fk[:-2]}pk)" for fk in foreign_keys])
                else:
                    foreign_key_sql = ','.join(foreign_keys)

                # Create the primary key SQL for the new table
                primary_key_sql = ', '.join(primary_key)

                # Create the column SQL for the new table
                column_sql = ', '.join([f"{name} {type}" for name, type in columns])

                # Create the new table with the foreign keys
                if foreign_key_sql:
                    connection.execute(text(f"""
                        CREATE TABLE {layer}_new (
                            {column_sql},
                            PRIMARY KEY ({primary_key_sql}),
                            {foreign_key_sql}
                        );
                    """))
                # Create the new table without the foreign keys (if there are none)
                else:
                    connection.execute(text(f"""
                        CREATE TABLE {layer}_new (
                            {column_sql},
                            PRIMARY KEY ({primary_key_sql})
                        );
                    """))

                connection.execute(text(f"INSERT INTO {layer}_new SELECT {', '.join(name for name, type in columns)} FROM {layer};"))
                connection.execute(text(f"DROP TABLE {layer};"))
                connection.execute(text(f"ALTER TABLE {layer}_new RENAME TO {layer};"))
    
    metadata.clear()
    metadata.reflect(engine)