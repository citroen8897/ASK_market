import user
import product
import get_users_data_base
import get_products_data_base
import password_generator
import re
import status_de_zakaz

while True:
    user_input_1 = input('S.P.Q.R.\n'
                         '___________________________________________\n'
                         '1 - вход в маркет\n'
                         '2 - регистрация\n'
                         '0 - выход из программы\n'
                         '___________________________________________\n'
                         'Ваш выбор: ')

    users_data_base = get_users_data_base.get_users_db()
    products_data_base = get_products_data_base.get_products_db()

    if user_input_1 == '1':
        user_email = input('Введите Ваш e-mail: ')
        user_password = input('Введите Ваш пароль: ')
        user_password = password_generator.generator_de_password(user_password)
        authorization_list = [[element.email, element.password] for element
                              in users_data_base]

        if [user_email, user_password] in authorization_list:
            print('Авторизация успешна...')
            for element in users_data_base:
                if element.email == user_email:
                    current_user = element
            break
        else:
            print('Пользователь с такими данными не найден!')

    elif user_input_1 == '2':
        new_user = user.User(0, '', '', '', '', '', 'user')
        if new_user.email not in \
                [element.email for element in users_data_base] and \
                new_user.telephone not in \
                [element.telephone for element in users_data_base]:
            new_user.add_user_data_base()
        else:
            print('Пользователь с таким e-mail или номером телефона уже '
                  'зарегистрирован!')

    elif user_input_1 == '0':
        input('Для выхода из программы нажмите Enter...')
        exit()

while True:
    commands_dict = {'user': ['1 - посмотреть каталог товаров\n',
                              '2 - добавить товар в корзину\n',
                              '3 - посмотреть корзину\n',
                              '4 - редактировать корзину\n',
                              '5 - оформить заказ\n',
                              '6 - посмотреть историю заказов\n',
                              '0 - выход из программы\n'],
                     'admin': ['1 - посмотреть каталог товаров\n',
                               '2 - посмотреть список пользователей\n',
                               '3 - изменить статус заказа\n',
                               '4 - редактирование товаров\n',
                               '5 - добавление товаров\n',
                               '6 - посмотреть историю заказов\n',
                               '0 - выход из программы\n']}

    user_input_2 = input('\n|||___///___ОСНОВНОЕ МЕНЮ МАРКЕТА___\\\\\\___|||\n'
                         '___________________________________________\n'
                         f'{commands_dict[current_user.status][0]}'
                         f'{commands_dict[current_user.status][1]}'
                         f'{commands_dict[current_user.status][2]}'
                         f'{commands_dict[current_user.status][3]}'
                         f'{commands_dict[current_user.status][4]}'
                         f'{commands_dict[current_user.status][5]}'
                         f'{commands_dict[current_user.status][6]}'
                         '___________________________________________\n'
                         'Ваш выбор: ')

    if user_input_2 == '1':
        print('\n___________________________________________'
              '\n___///ПОЛНЫЙ СПИСОК ТОВАРОВ///___\n')
        for element in products_data_base:
            print(element)

    elif user_input_2 == '2':
        if current_user.status == 'user':
            print('\nПеречень доступных к заказу товаров:')
            for element in products_data_base:
                if element.etre == 'в наличии':
                    print(f'{element.product_id} - {element.nom} - '
                          f'{element.prix}')
            user_input_3 = input('Введите через пробел номера товаров, '
                                 'которые хотите добавить в корзину: ')
            temp_list = user_input_3.split(' ')
            for i in temp_list:
                try:
                    if int(i) not in \
                            [j.product_id for j in products_data_base]:
                        print('Некорректный ввод цифрового идентификатора')
                    else:
                        for element in products_data_base:
                            if element.product_id == int(i):
                                current_user.basket.append(element)
                except ValueError:
                    print('Ошибка! Введено не число!')

        elif current_user.status == 'admin':
            print('\n___________________________________________'
                  '\n___///ПОЛНЫЙ СПИСОК КЛИЕНТОВ///___\n')
            for element in users_data_base:
                print(element)

    elif user_input_2 == '3':
        if current_user.status == 'user':
            current_user.get_basket()

        elif current_user.status == 'admin':
            current_zakaz_id = input('Введите номер заказа: ')
            while not current_zakaz_id.isdigit():
                current_zakaz_id = input('Введите номер заказа: ')

            history_des_zakazes = current_user.get_history_des_zakazes()
            list_numeros_des_zakazes = []
            for element in history_des_zakazes:
                for k, v in element.items():
                    if k == '№ заказа: ':
                        list_numeros_des_zakazes.append(str(v))

            if current_zakaz_id not in list_numeros_des_zakazes:
                print('Заказ не найден!')

            else:
                for element in history_des_zakazes:
                    for k, v in element.items():
                        if k == '№ заказа: ':
                            if v == int(current_zakaz_id):
                                current_zakaz = element

                print(f'текущий статус заказа: '
                      f'{current_zakaz["статус заказа: "]}')
                user_input_8 = input('Введите новый статус заказа согласно '
                                     'цифровому идентификатору\n'
                                     '1 - в обработке\n'
                                     '2 - обработан\n'
                                     '3 - отправлен\n'
                                     '4 - доставлен\n'
                                     '5 - выполнен\n')
                while user_input_8 not in ['1', '2', '3', '4', '5']:
                    user_input_8 = input(
                        'Введите новый статус заказа согласно '
                        'цифровому идентификатору\n'
                        '1 - в обработке\n'
                        '2 - обработан\n'
                        '3 - отправлен\n'
                        '4 - доставлен\n'
                        '5 - выполнен\n')
                list_status = ['1', 'в обработке', '2', 'обработан',
                               '3', 'отправлен', '4', 'доставлен',
                               '5', 'выполнен']
                zakaz_status = list_status[list_status.index(user_input_8) + 1]
                status_de_zakaz.choisir_status_de_zakaz(zakaz_status,
                                                        current_zakaz_id)

    elif user_input_2 == '4':
        if current_user.status == 'user':
            current_user.get_basket()
            if len(current_user.basket) != 0:
                user_input_4 = input('Введите порядковый номер товара из '
                                     'корзины, который желаете удалить: ')
                while not user_input_4.isdigit():
                    user_input_4 = input('Введите порядковый номер товара из '
                                         'корзины, который желаете удалить: ')

                if int(user_input_4) in range(len(current_user.basket) + 1):
                    current_user.basket.pop(int(user_input_4) - 1)
                    print('Товар успешно удален из корзины...')

                else:
                    print('Неверный номер товара!')

        elif current_user.status == 'admin':
            user_input_6 = input('Введите id товара: ')
            while not user_input_6.isdigit():
                user_input_6 = input('Введите id товара: ')

            if int(user_input_6) not in \
                    [i.product_id for i in products_data_base]:
                print('Товар с таким id не найден!')

            else:
                for element in products_data_base:
                    if element.product_id == int(user_input_6):
                        current_product = element
                user_input_7 = input('\n1 - изменить статус товара\n'
                                     '2 - изменить цену товара\n'
                                     '3 - изменить название товара\n')

                if user_input_7 == '1':
                    print(f'текущий статус товара: {current_product.etre}')
                    new_status = input('Необходимо задать статус наличия '
                                       'товара\n'
                                       'Выберите статус согласно цифровому '
                                       'идентификатору\n'
                                       'Возможные статусы:\n'
                                       '1 - в наличии\n'
                                       '2 - нет в наличии\n'
                                       '3 - ожидается\n'
                                       '4 - под заказ\n'
                                       '5 - снято с производства\n'
                                       'Введите статус наличия товара: ')
                    while new_status not in ['1', '2', '3', '4', '5']:
                        new_status = input('Необходимо задать статус наличия '
                                           'товара\n'
                                           'Выберите статус согласно цифровому'
                                           ' идентификатору\n'
                                           'Возможные статусы:\n'
                                           '1 - в наличии\n'
                                           '2 - нет в наличии\n'
                                           '3 - ожидается\n'
                                           '4 - под заказ\n'
                                           '5 - снято с производства\n'
                                           'Введите статус наличия товара: ')
                    current_product.choisir_status(new_status)

                elif user_input_7 == '2':
                    print(f'текущая цена товара: {current_product.prix}')
                    new_prix = input('Введите новую цену товара: ')
                    while re.findall(r'[^0-9.]', new_prix) or len(
                            new_prix) == 0:
                        new_prix = input('Введите новую цену товара: ')
                    new_prix = float(new_prix)
                    current_product.choisir_prix(new_prix)

                elif user_input_7 == '3':
                    print(f'Текущее название товара: {current_product.nom}')
                    new_nom = input('Введите новое название товара: ')
                    while not re.findall(r'[a-zA-Zа-яА-Я0-9]', new_nom):
                        new_nom = input('Введите новое название товара: ')
                    current_product.choisir_nom(new_nom)

    elif user_input_2 == '5':
        if current_user.status == 'admin':
            new_product = product.Product(0, '', '', '', '', '')
            new_product.add_product_data_base()
            products_data_base = get_products_data_base.get_products_db()

        elif current_user.status == 'user':
            numero_de_zakaz = current_user.make_zakaz()
            for element in current_user.basket:
                current_user.make_zakaz_full(numero_de_zakaz,
                                             element.product_id,
                                             element.nom,
                                             current_user.user_id,
                                             current_user.email)
            current_user.basket.clear()

    elif user_input_2 == '6':
        print('____________________________________________________\n'
              '___///___ИСТОРИЯ ЗАКАЗОВ:___///___\n')
        history_des_zakazes = current_user.get_history_des_zakazes()
        list_numeros_des_zakazes = []
        for element in history_des_zakazes:
            for k, v in element.items():
                print(f'{k}: {v}')
                if k == '№ заказа: ':
                    list_numeros_des_zakazes.append(str(v))
            print()
        user_input_5 = input('Для выхода в основное меню - нажмите Enter\n'
                             'Для детального просмотра заказа введите '
                             'его номер: ')

        if user_input_5 in list_numeros_des_zakazes:
            full_info = current_user.get_full_info_de_zakaz(int(user_input_5))
            client_id = full_info[0]['id клиента: ']
            client_info = {}
            for element in users_data_base:
                if element.user_id == client_id:
                    client_info['prenom'] = element.prenom
                    client_info['nom'] = element.nom
                    client_info['email'] = element.email
                    client_info['telephone'] = element.telephone
            print(f'______________________________________________\n'
                  f'___///___ДЕТАЛИЗАЦИЯ ЗАКАЗА___///___'
                  f'\n\n№ заказа: {user_input_5}\n'
                  f'покупатель: {client_info["prenom"]} {client_info["nom"]}\n'
                  f'e-mail: {client_info["email"]}\n'
                  f'телефон: {client_info["telephone"]}\n'
                  f'\n__||__СОСТАВ ЗАКАЗА:__||__\n')
            for element in full_info:
                for k, v in element.items():
                    if k != 'id клиента: ':
                        print(f'{k}: {v}')
                print()

    elif user_input_2 == '0':
        input('Для выхода из программы нажмите Enter...')
        exit()
