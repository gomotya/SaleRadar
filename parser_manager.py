# Файл parser_manager.py
from datetime import datetime
from parsers import kolos_parser, svyaznoy_parser, printbar_parser, istore_parser, zarina_parser, xiaomi_parser, brandshop_parser, sneakerhead_parser, justitalian_parser, noone_parser


async def run_parsers(session):
    parsers = [
                kolos_parser.parse,
                #Телефоны 
                svyaznoy_parser.parse,
                istore_parser.parse, 
                xiaomi_parser.parse,
                #Обувь  
                sneakerhead_parser.parse,
                justitalian_parser.parse,
                noone_parser.parse,
                #Футболки
                printbar_parser.parse,
                zarina_parser.parse, 
                brandshop_parser.parse
               ]

    for parser in parsers:
        await parser(session)

    print(f"Парсинг завершен {datetime.now()}")
