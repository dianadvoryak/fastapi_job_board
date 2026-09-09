uvicorn main:app --reload
alembic init -t async migrations  
http://127.0.0.1:8000/docs  


pip3 freeze > requirements.txt

```  
ДЕБАГ  

print('дошли до сюда')  
print(error_msg)  
exit()  

print("\n" + "=" * 50)
print("ДОШЛИ ДО СЮДА!")
print(f"Ошибка БД: {error_msg}")
print("=" * 50 + "\n")
exit()

from fastapi import Response, HTTPException
return Response(content="дошли до сюда", media_type="text/plain")
raise HTTPException(status_code=200, detail="дошли до сюда")

raise HTTPException(
    status_code=400,
    detail={
        "status": "error",
        "message": "Ошибка при работе с базой данных",
        "database_error": error_msg  # Тут будет точный текст (например, duplicate key)
    }
)

# Флаг debug=True активирует подробный вывод ошибок в ответе app = FastAPI(debug=True)

breakpoint()
1. Вы делаете запрос к эндпоинту.
2. В терминале, где запущен сервер, выполнение кода останавливается, и появляется интерактивная строка (Pdb).
3. Вы можете писать имена переменных (например, ввести x или y), чтобы увидеть их текущие значения.
4. Напишите c (continue) и нажмите Enter, чтобы программа побежала дальше.
```