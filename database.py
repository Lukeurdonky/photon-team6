# file that is used for connecting to and interacting with the PostgreSQL database

# database imports that should be on the VM
try:
    import psycopg2
except ImportError:
    psycopg2 = None

# params to be referenced later (testing no user)
DB_PARAMS = {
    "dbname": "photon"#,
    # "user": "student"
}


class PlayerDatabase:
    def __init__(self, params = DB_PARAMS):
        self.conn = None # by default set to None

        # break if psycopg2 is absent
        if psycopg2 is None:
            print("psycopg2 not installed - running without the database.")
            return
        
        # try catch block for safety :)
        try:
            # assign self.conn
            self.conn = psycopg2.connect(**params)
            # Every INSERT saves immediately, no manual commit needed
            self.conn.autocommit = True
            print("Connected to database:", params["dbname"])
        except psycopg2.Error as error:
            print("Could not connect to the database:", error)

    #### helpful class functions

    # getter for connection
    def is_connected(self):
        return self.conn is not None

    # closes database if needed
    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    #### DB needs to be able to add players and get their codenames by player ID

    # add a player (returns False if failure)
    def add_player(self,  player_id, codename):
        # break if disconnected
        if not self.is_connected():
            return False

        # try catch block for safety :)
        try:
            with self.conn.cursor() as cursor: # freaky "with statement" assigns self to 'cursor'
                # executes SQL INSERT code
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                print(f"[DB] Added player {player_id} ({codename}), rows inserted: {cursor.rowcount}")
            return True
        except psycopg2.Error as error: # return false if failure
            print("Database insert failed:", error)
            return False

    # search for player codename by ID (returns None if not found)
    def get_codename(self, player_id):
        # break if disconnected
        if not self.is_connected():
            return None

        # try catch block for safety :)
        try:
            with self.conn.cursor() as cursor: # freaky "with statement" assigns self to 'cursor'
                # executes SQL SELECT code
                cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
                # assigns findings to 'row' var
                row = cursor.fetchone()
            return row[0] if row else None # returns row or None
        except psycopg2.Error as error: # return None if failure
            print("Database lookup failed:", error)
            return None

    #### end of class

# connection test:  python database.py
# adds a test player, reads it back, then deletes it so the table is unchanged
if __name__ == "__main__":
    db = PlayerDatabase()
    if not db.is_connected():
        print("[TEST] FAILED - could not connect (see above)")
    else:
        print("[TEST] Player 1 is:", db.get_codename(1))
        if db.add_player(999999, "ConnectionTest") and db.get_codename(999999) == "ConnectionTest":
            print("[TEST] PASSED - lookup and insert both work")
        else:
            print("[TEST] FAILED - insert or lookup did not work")
        with db.conn.cursor() as cursor:
            cursor.execute("DELETE FROM players WHERE id = %s;", (999999,))
        db.close()