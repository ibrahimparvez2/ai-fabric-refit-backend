To run locally with Python virtual environment:

get Gemini API Key via google aistudio --> https://aistudio.google.com/welcome 

```
cd app 
create `.env` file
add GEMINI_API_KEY key ( key=value format ) 

```
**DO NOT COMMIT ANY .ENV FILES!**

```
cd app
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

start server with  ```uvicorn main:app --reload```


To test API with Postman: 


Install Postman --> https://www.postman.com/downloads/
<br>
set address to `localhost:8000/analyze_fabrics` method is `POST`
<br>
 ![alt text](image.png) <br>
 upload files via `form-data` then `files`