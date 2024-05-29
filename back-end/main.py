from fastapi import FastAPI
import uvicorn
from app.routers import user, datos_usuario_pastilla, auth, pastillasTablaInfo, data_user_pills_filter_tablet_all
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # Agrega PATCH a la lista de métodos permitidos,
    allow_headers=["*"],
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
#     allow_headers=["Authorization"],
# )


app.include_router(user.router)
app.include_router(datos_usuario_pastilla.router)
app.include_router(pastillasTablaInfo.router)
app.include_router(auth.router)
app.include_router(data_user_pills_filter_tablet_all.router)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)