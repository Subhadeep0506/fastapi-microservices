import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .core import routes
from .core.auth_bearer import JWTBearer
from .database.database import Base, SessionLocal, engine
from .models.user import User
from .schema.password import ChangePassword
from .schema.token import TokenSchema
from .schema.user import UserCreate, UserLogin, UserUpdate


Base.metadata.create_all(engine)
async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register")
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    return routes.register_user(user=user, user_model=User, session=session)


@app.post("/login", response_model=TokenSchema)
async def login(request: UserLogin, session: Session = Depends(get_session)):
    return routes.login_user(db=session, request=request)


@app.get("/me/info")
async def get_user_info(
    dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    return routes.get_user_info(dependencies=dependencies, db=session)


@app.post("/me/logout")
async def logout(dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)):
    return routes.logout_user(dependencies=dependencies, db=session)


@app.get("/users")
async def get_users(
    dependencies=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    return routes.list_users(dependencies=dependencies, db=session)


@app.post("/me/change-password")
async def change_password(
    request: ChangePassword,
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return routes.change_password(
        request=request, dependencies=dependencies, db=session
    )


@app.put("/me/update")
async def update_user_info(
    user_update: UserUpdate,
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return routes.update_user(
        user_update,
        dependencies=dependencies,
        db=session,
    )


@app.delete("/me/delete")
async def delete_user(
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return routes.delete_user(
        dependencies=dependencies,
        db=session,
    )


@app.delete("/delete/{user_id}")
async def delete_user_by_id(
    user_id: str,
    dependencies=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return routes.delete_user_by_id(
        user_id=user_id,
        dependencies=dependencies,
        db=session,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8089, reload=True)
