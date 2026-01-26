'''
Implement users services
'''
import secrets
from fastapi import APIRouter,Depends, HTTPException, Request,Response
import jwt
from pydantic import Field
from app.core.config import settings
from app.core.db import get_db_connection
from app.services.user import UserService
from app.model.models import User, UserRegister,UserUpdate,UserToDelete
from app.core.security import create_access_token,create_refresh_token,protected_pages
from app.core.emailConf import sendMail
from aiocache import Cache

cache = Cache(Cache.MEMORY)
router = APIRouter()

# test api
@router.get("/")
def test_api():
    return {"message":"Hello World"}


@router.post("/register")
async def register(user: UserRegister, db = Depends(get_db_connection)):
    # check if user already exist
    service = UserService(db)

    username = service.get_user_by_username(user.username)

    if username:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    token: str = secrets.token_urlsafe(32)

    # store credential
    await cache.set(key=token,value=user,ttl=3600)

    # send mail
    sent = sendMail(user.email,token)

    if not sent:
        return {"status":500,"message":"smtp email server error"}
    
    return {"status":200,"detail":"check your email to verify"}

# get user info from cache
@router.get("/auth/verify_email/{token}") # we assume we get user is verified
async def register_after_verification(response: Response,token: str, db = Depends(get_db_connection)):
    # retrive info from cache
    
    user : UserRegister = await cache.get(token)

    if not user:
        raise HTTPException(
            status_code=403,
            detail="your link expired"
        )

    service = UserService(db)

    is_created = service.create_user(user)

    if not is_created:
        HTTPException(
            status_code=501,
            detail="failed to create user"
        )
    # generate pair token and send to user
    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username,db)

    if not refresh_token:
        raise HTTPException(status_code=405, detail="Database connectivity")

    response.set_cookie(
        key="access_token",
        value=access_token
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token
    )

    return {
            "status":200,
            "message":"User created"
        }



@router.post("/login")
def login(response:Response,user: User, db = Depends(get_db_connection)):
    service = UserService(db)

    if not service.authenticate(user):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # generate pair token and send to user
    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username,db)

    if not refresh_token:
        raise HTTPException(status_code=405, detail="Database connectivity")

    response.set_cookie(
        key="access_token",
        value=access_token
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token
    )

    return {"message":"login successfully"}


@router.patch("/update-profile")
def update_profile(user: UserUpdate,request: Request,db = Depends(get_db_connection),authorized=Depends(protected_pages)):
    service = UserService(db)
    return service.update_profile(user,request)


@router.delete("/delete-account")
def delete_account(username: UserToDelete, db=Depends(get_db_connection),authorized=Depends(protected_pages)):
    service = UserService(db)
    return service.delete_user(username)


@router.post("/logout")
def logout(request:Request,response:Response,db = Depends(get_db_connection),authorized=Depends(protected_pages)):

    access_token = request.cookies.get("access_token")

    decoded_payload = jwt.decode(access_token,settings.JWT_SECRET,algorithms=settings.JWT_ALGORITHM)
    # Extract the issuer claim
    issuer = decoded_payload.get('iss') 
    # delete from db
    sql = "delete from tokenUsage where username=%s"
    val = (issuer,)
    connection = db.cursor()

    try:
        connection.execute(sql,val)
        db.commit()
        connection.close()
    except Exception as e:
        return {"error":e}
    
    # delete token
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "User logged out"}
