import hashlib, os
import sqlite3 as sql

class Security():
    """
    A class for handling usernames and passwords for the website. Can add users to a database and log them in using
    their credentials

    Note: You MUST only refer to this class as using a with statement, e.g. with Security() as <variable>. This is so
    that the database closes once the object's use has finished

    Class variables:
        self.__iterations
        Type: Int
        Holds the amount of iterations required when hashing a password

        self.__min_length
        Type: Int
        Holds the minimum length of passwords

        self.__max_length
        Type: Int
        Holds the maximum length of passwords

        self.__self_length
        Type: Int
        Specifies the length of the salt to be generated

        self.con
        Type: object (database)
        Stores the database file of users

        self.cur
        Type: object (database cursor)
    """
    def __init__(self):
        self.__iterations = 100000
        self.__min_length = 8
        self.__max_length = 128
        self.__salt_length = 32
        self.con = sql.connect("Databases/users.db")
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Ensures that the database is closed once the object's use has finished
        self.con.close()

    def hash_new_password(self, password):
        """
        Function for creating a salted hash based upon a given password

        Arguments:
            Password
            Type: String
            This should contain the user's password

        Returns:
            A tuple of values;
            The first element contains the password_hash, which is a bytes object.
            The second element contains the salt, which is a bytes object
        """
        # Check to see if the password is too long or short
        if len(password) < self.__min_length:
            raise ValueError("Your password is too short")
        if len(password) > self.__max_length:
            raise ValueError("Your password is too long")
        # Generate a salt and make sure it doesn't match any of the salts in the database
        match = True
        self.cur.execute("select salt from users")
        while match == True:
            salt = os.urandom(self.__salt_length)
            print(type(salt))
            match = False
            for row in self.cur:
                if row[1] != salt:
                    pass
                else:
                    match = True
                    break
        password_hash = hashlib.pbkdf2_hmac("sha512", bytes(password,"utf-8"), salt, self.__iterations)
        return (password_hash,salt)


    def register(self,username, password):
        """
        Function for adding a new user to the database

        Arguments:
            username
            Type: String
            This should be the chosen username of the user

            password
            Type: String
            This should be the chosen password of the user

        Returns:
            True (bool)
        """
        # Check to see if the username given has been taken
        self.cur.execute("select count(*) from users where username = ?;", (username,))
        if int(self.cur.fetchone()[0]) != 0:
            raise ValueError("Username already taken")
        # Create a new hash-salt pair
        password_details = self.hash_new_password(password)
        # Add the new user to the database
        self.cur.execute("""insert into users (username,salt,iterations,hash)
        values (?,?,?,?);""",(username,sql.Binary(password_details[1]),self.__iterations,password_details[0]))
        self.con.commit()
        return True

    def log_on(self,username,password):
        """
        Authenticate a user that has registered with the site.
        Arguments:
            username
            Type: String
            This should be the chosen username of the user

            password
            Type: String
            This should be the chosen password of the user

        Returns:
            True (bool)

        """
        # See if the user is in the database
        try:
            self.cur.execute("select username,salt,iterations,hash from users where username = ?",(username,))
            user = self.cur.fetchone()
        except:
            raise ValueError("Username or Password Incorrect")
        password_hash = hashlib.pbkdf2_hmac("sha512", bytes(password,"utf-8"),user[1],user[2])
        # See if the password given is the one that matches in the database
        if password_hash != user[3]:
            raise ValueError("Username or Password Incorrect")
        else:
            return True


