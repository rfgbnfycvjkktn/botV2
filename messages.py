def start_menu():
    return u'\U00002705' + "<b>Умный рантье (поиск облигации)</b> - сервис подбора ликвидных облигаций. Бот " \
                           "предоставляет обработанную для пользователя информацию с серверов Московской биржи." + \
           '\n\n' + u'\U00002757' + 'Бот предоставляет информацию на основе данных последней завершенной торговой ' \
                                    'сессии (НЕ текущий день).' + \
           '\n' + u'\U00002757' + "<b>Важно.</b> Информация, полученная с помощью данного сервиса, не является " \
                                  "индивидуальной рекомендацией. " \
                                  "Носит исключительно " \
                                  "информационно-аналитический " \
                                  "характер и не должна " \
                                  "рассматриваться как " \
                                  "предложение либо рекомендация " \
                                  "к инвестированию, покупке, " \
                                  "продаже какого-либо актива, " \
                                  "торговых операций по " \
                                  "финансовым инструментам. "


def help_menu():
    return '<b>Параметры, используемые при поиске:</b>' \
           + '\n\n' + u'\U00000031' + u'\U000020E3' + ' Купонная доходность бумаги (% годовых). ' \
           + '\n' + u'\U00000032' + u'\U000020E3' + ' Цена (% от номинала). Рыночная цена в процентах от номинальной. ' \
                                                    'Обычно номинальная цена равна 1000 рублей (100 %) ' \
           + '\n' + u'\U00000033' + u'\U000020E3' + ' Дюрация (количество месяцев) — эффективный срок до погашения ' \
                                                    'облигации. Эффективный срок учитывает все купонные платежи, ' \
                                                    'выплаченные в разное время, и различные особенности облигации, ' \
                                                    'такие как амортизация или оферта. Если купонных платежей, ' \
                                                    'амортизации и оферты нет, то дюрация совпадает со сроком до ' \
                                                    'погашения облигации. ' \
           + '\n' + u'\U00000034' + u'\U000020E3' + ' Объем торгов бумагой (количество штук). На данный момент ' \
                                                    'анализируются последние 2 недели торгов бумагой. ' \
           + '\n\n' + u'\U0001F4B3' + '<b>Расширенный поиск:</b>' \
           + '\n\n' + u'\U00000031' + u'\U000020E3' + 'Предоставляет более гибкие настройки для фильтрации данных.'


def search_menu():
    return '<b>Поиск облигаций.</b>' \
           + '\n\n' + u'\U00002757 В <b>базовом</b> варианте поиск осуществляется по ' \
                                              u'ограниченному набору параметров. Доходность бумаг от 5 до 8 ' \
                                              u'процентов. Цена 98-100 процентов от номинала. Значение объема ' \
                                              u'сделок по бумаге предопределено и составляет более 3000 штук за ' \
                                              u'последние 2 недели. Дюрация 8-36 месяцев. ' \
           + '\n\n' + u'\U00002757 Разработка <b>расширенного</b> функционала в процессе тестирования ... '
