import hashlib, os, pickle

class Security():
    def __init__(self):
        self.__iterations = 100000
        self.__min_length = 8
        self.__max_length = 128
        self.__salt_length = 32
        try:
            f = open("passwords.txt","rb")
            self.password_file = pickle.load(f,encoding="UTF-8")
        except IOError:
            f = open("passwords.txt","wb")
            self.password_file = []
        finally:
            f.close()

    def hash_new_password(self, password):
        if len(password) < self.__min_length:
            raise ValueError("Your password is too short")
        if len(password) > self.__max_length:
            raise ValueError("Your password is too long")
        salt = None
        try:
            while salt is None or salt in [item["salt"] for item in self.password_file]:
                salt = os.urandom(self.__salt_length)
        except KeyError:
            pass
        password_hash = hashlib.pbkdf2_hmac("sha512", password, salt, self.__iterations)
        return (password_hash,salt)


    def register(self,username, password):
        for item in self.password_file:
            if item["username"] == username:
                raise ValueError("The username specified has already been taken")
        password_details = self.hash_new_password(password)
        self.password_file.append({"username":username,"salt":password_details[1],"password":password_details[0],"iterations":self.__iterations,"reset":False})
        try:
            f = open("passwords.txt","wb")
            pickle.dump(self.password_file,f)
            f.close()
        except IOError:
            raise IOError("Couldn't write to the file, registration failed")

    def log_on(self,username,password):
        user_file = None
        for i in range(len(self.password_file)):
            if username == self.password_file[i]["username"]:
                user_file = self.password_file[i]
        if user_file is None:
            raise ValueError("Username not found")
        password_hash = hashlib.pbkdf2_hmac("sha512", password,user_file["salt"],user_file["iterations"])
        if password_hash != user_file["password"]:
            raise ValueError("The password given doesn't match the one in our database")
        else:
            return True

    def reset_all(self):
        for i in range(len(self.password_file)):
            self.password_file[i]["reset"] = True
        f = open("passwords.txt","wb")
        pickle.dump(self.password_file,f)
        f.close()

