import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename="app.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(name)s: %(lineno)d - %(message)s"
    )

# This is the main Logging function. You will se everything in app.log
# Оснавная функция Логов. Все логи можно увидеть в файле app.log