# -*- coding: utf-8 -*-
"""
Главная точка входа в приложение «Магазин обуви» (ShoeShop).
Запуск графического интерфейса каталога и авторизации.
"""
import sys
import os

from catalog import main

if __name__ == '__main__':
    if getattr(sys, "frozen", False):
        # При запуске из упакованного EXE устанавливаем рабочую директорию рядом с исполняемым файлом
        os.chdir(os.path.dirname(sys.executable))
    main()
