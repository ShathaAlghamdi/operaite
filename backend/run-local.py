import uvicorn

uvicorn.run('uvicorn app:app',
                port=4242, reload=True, debug=True)

# port=4242 reload=True debug=True