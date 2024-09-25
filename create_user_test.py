import sender_stand_request
import data
from data import user_body
from sender_stand_request import post_new_user

def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

def possitive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    print(user_response.status_code)
    assert user_response.json()["authToken"] !=  ""
    print(user_response.json()["authToken"])
    user_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert user_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()['code'] == 400
    assert user_response.json()['message'] == 'Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres.'
    print(user_response.json()['message'])
    print(user_response.status_code)

def negative_assert_no_firstname(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()['code'] == 400
    assert user_response.json()['message'] == "No se enviaron todos los parámetros necesarios"

def test_create_user_2_letter_in_first_name_get_success_response():
    possitive_assert("Aa")
    # Test 1

def test_create_user_15_letter_in_first_name_get_success_response():
    possitive_assert("Aaaaaaaaaaaaaaa")
    # Test 2

def test_create_user_1_letter_in_first_name_get_negative_response():
    negative_assert_symbol('A')
    # Test 3

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol('Аааааааааааааааа')
    # Test 4

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol('A Aaa')
    # Test 5

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")
    # Test 6

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")
    # Test 7

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)
    # Test 8

def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)
    # Test 9

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    user_response = sender_stand_request.post_new_user(user_body)
    print(user_response.status_code)
    print(user_response.json())
    assert user_response.status_code == 400