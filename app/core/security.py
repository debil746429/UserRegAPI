# create access token

# generate password hash


# verify password depends on first alorithm we used to encrypt the first time

from fastapi import Depends, HTTPException, Request, Response
import jwt,secrets
from datetime import datetime,timezone,timedelta
from app.core.config import settings
from app.core.db import get_db_connection


def create_access_token(issuer: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "iss": str(issuer)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(issuer: str, conn: Depends(get_db_connection)) -> str:
    refresh_token = secrets.token_urlsafe(32)
    # what if username already has refresh_token
    # replace with new one

    sql = "select * from tokenUsage where username=%s"
    val = (issuer,)
    connection = conn.cursor()
    connection.execute(sql,val)

    _user = connection.fetchone()
    if _user:
        sql = "update tokenUsage set refresh_token=%s, expires_at=%s where username=%s"
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRY_DAYS)
        values = (refresh_token, expires_at, issuer)
        connection.execute(sql,values)
        conn.commit()

        return refresh_token

    # store in db
    sql = "insert into tokenUsage(username,refresh_token,expires_at) values(%s,%s,%s)"
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRY_DAYS)
    values = (issuer,refresh_token,expires_at)

    connection.execute(sql,values)

    conn.commit()
    connection.close()
    return refresh_token

def protected_pages(response:Response,request:Request,conn = Depends(get_db_connection)):
    # get token
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    # if one doesnt exist the exit
    if not access_token or not refresh_token:
        raise HTTPException(
            status_code=401, 
            detail="You are not authorized on this page"
        )

    #check if jwt are valid
    try:
        jwt.decode(access_token,settings.JWT_SECRET,algorithms=settings.JWT_ALGORITHM)

    except jwt.exceptions.ExpiredSignatureError:
        # if expired, decode without verification to get issuer
        decoded_payload = jwt.decode(access_token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, options={"verify_exp": False})
        
        # Extract the issuer claim
        issuer = decoded_payload.get('iss')
        # check if it is valid refresh_token and not expired
        sql = "select * from tokenUsage where username=%s"
        val = (issuer,)
        connection = conn.cursor()
        connection.execute(sql,val)

        # get user data
        _user = connection.fetchone()
        user_expiry = _user[2].replace(tzinfo=timezone.utc)
        current_time = datetime.now(tz=timezone.utc)
        if current_time < user_expiry:
            # generate new token
            new_access_token = create_access_token(issuer)
            new_refresh_token = create_refresh_token(issuer,conn)

            if not new_refresh_token:
                raise HTTPException(status_code=405, detail="Database connectivity")

            # set them
            response.set_cookie(
                key="access_token",
                value=new_access_token
            )

            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token
            )

            return True
        
        raise HTTPException(
            status_code=401, 
            detail="expired token"
        )
        
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=401, 
            detail="Invalid token"
        )

    return True

    

    