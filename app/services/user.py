'''
What user can do to our system
'''
import jwt
from mysql.connector import Error,MySQLConnection
from pydantic import EmailStr
from app.model.models import User, UserRegister,UserUpdate,UserToDelete
from fastapi import HTTPException, Request
from app.core.config import settings

class UserService:
    def __init__(self, conn: MySQLConnection):
        self.connection = conn
    
    #==================== api utilities
    def get_user_by_username(self, username: str):
        sql = "select username from Users where username = %s"
        val = (username,)

        conn = self.connection.cursor()

        try:
            conn.execute(sql,val)
            _user = conn.fetchone()

            return _user

        except Error as err:
            raise Exception(f"Database error: {err}")

        finally:
            conn.close()


    def get_user_by_email(self,email: EmailStr):
        sql = "select email from Users where email = %s"
        val = (email,)

        conn = self.connection.cursor()

        try:
            conn.execute(sql,val)
            _email = conn.fetchone()
            return _email

        except Error as err:
            raise Exception(f"Database error: {err}")

        finally:
            conn.close()
    
    def authenticate(self,user: User):
        # use username for auth
        if user.username:
            db_user = self.get_user_by_username(user.username)

            if not db_user:
                return None
            
            return db_user
        
        # use password
        if user.email:
            db_user = self.get_user_by_email(user.email)

            if not db_user:
                return None
            
            return db_user



    #======================= Business logic

    '''
     create user
    '''
    def create_user(self, user: UserRegister):

        if user.email:
            sql = "insert into Users (username,email,password,age,gender,country,region) values(%s,%s, %s ,%s,%s,%s,%s)"
            values = (user.username,user.email,user.password,user.age,user.gender,user.country,user.region)
        else:
            sql = "insert into Users (username,password,age,gender,country,region) values(%s,%s,%s,%s,%s,%s)"
            values = (user.username,user.password,user.age,user.gender,user.country,user.region)

        conn = self.connection.cursor()
        try:
            conn.execute(sql,values)
            self.connection.commit()
        except Error as err:
            raise Exception(f"Database error: {err}")
        finally:
            conn.close()
        
        return True

    
    '''
    # update user
    '''
    def update_profile(self,userUpdated: UserUpdate,request:Request):
        # check if is not supplied args
        if not userUpdated:
            raise HTTPException(
            status_code=401, 
            detail="You didnt pass any data"
        )
        
        # check validity of jwt token

        # check if user is in db
        '''
        # This username need to be from jwt token
        '''
        access_token = request.cookies.get("access_token")
        '''
        implement Token Expired 
        In this
        '''
        try:
            decoded_payload = jwt.decode(access_token,settings.JWT_SECRET,algorithms=settings.JWT_ALGORITHM)
            # Extract the issuer claim
            issuer = decoded_payload.get('iss')
        except jwt.exceptions as e:
            HTTPException(
                status=403,
                detail=str(e)
            )

        user = self.get_user_by_username(issuer)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        '''
        # get another username from UserUpdated
        '''

        match userUpdated.updateType:
            case "email":

                # update  email
                
                sql = "UPDATE Users SET email = %s WHERE username = %s"
                values = (userUpdated.email,issuer)

                conn = self.connection.cursor()
                try:
                    conn.execute(sql,values)
                    self.connection.commit()
                except Error as err:
                    raise Exception(f"Database error: {err}")

                finally:
                    conn.close()

                return {
                    "status":200,
                    "message":"email Updated successfully"
                }

            case "username":
                # update  username
                
                sql = "UPDATE Users SET username = %s WHERE username = %s"
                values = (userUpdated.username,issuer) # later check this to be from jwt token

                conn = self.connection.cursor()
                try:
                    conn.execute(sql,values)
                    self.connection.commit()
                except Error as err:
                    raise Exception(f"Database error: {err}")

                finally:
                    conn.close()

                return {
                    "status":200,
                    "message":"username Updated successfully"
                }

            case "password":
                # update  password
                
                sql = "UPDATE Users SET password = %s WHERE username = %s"
                values = (userUpdated.password,issuer)

                conn = self.connection.cursor()
                try:
                    conn.execute(sql,values)
                    self.connection.commit()
                except Error as err:
                    raise Exception(f"Database error: {err}")

                finally:
                    conn.close()

                return {
                    "status":200,
                    "message":"password Updated successfully"
                }



        return {
            "status":200,
            "message":"nothing updated"
        }


    '''
    delete user (delete an account)
    '''
    def delete_user(self,delUser: UserToDelete):
        # use jwt to verify if it is real a same user who created account want to del
        # check validity of jwt token

        #verify if user is available to delete
        user = self.get_user_by_username(delUser.username)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not Found.",
            )
        
        sql = "delete from Users where username= %s"
        val = (delUser.username,)
        conn = self.connection.cursor()

        try:
            conn.execute(sql,val)
            self.connection.commit()
        except Error as err:
            raise Exception(f"Database error: {err}")

        finally:
            conn.close()
        
        return {
            "status":200,
            "message":"User deleted successfully"
        }
