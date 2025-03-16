from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
def get_data():
    return {"message": "Данные успешно получены"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5002)
    
    from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

