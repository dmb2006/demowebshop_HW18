from allure_commons.types import AttachmentType
from requests import Response
from selene import browser, have
import pytest
import requests
import allure
import allure
import json


LOGIN = 'test@qwerty.ru'
PASSWORD = 'qwerty'
WEB_URL = 'https://demowebshop.tricentis.com/'
API_URL = 'https://demowebshop.tricentis.com/'

@allure.link('https://demowebshop.tricentis.com', 'demowebshop')
@allure.title('Добавление товара в корзину авторизованным пользователем')
def test_login_through_api(browser_config):
    with allure.step('Авторизация через api'):
        response = requests.post(API_URL + '/login', data={'Email': LOGIN, 'Password': PASSWORD, 'RememberMe': False},
        allow_redirects = False)
        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(response.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with allure.step('Получение куки через api'):
        cookie = response.cookies.get('NOPCOMMERCE.AUTH')

    with allure.step('Установка куки через api'):
        browser.open(WEB_URL)
        browser.driver.add_cookie({'name': 'NOPCOMMERCE.AUTH', 'value': cookie})
        browser.open(WEB_URL)

    with allure.step('Проверка успешной авторизации'):
        browser.element('.account').should(have.text(LOGIN))
        browser.open(WEB_URL)

    with allure.step('Добавление товара в корзину через API'):
        response = requests.post(url=WEB_URL + 'addproducttocart/catalog/43/1/1',
                                cookies={'NOPCOMMERCE.AUTH': cookie})
        response = requests.post(url=API_URL + 'addproducttocart/catalog/45/1/1',
                                 cookies={'NOPCOMMERCE.AUTH': cookie})

    with allure.step('Проверка что в корзине товар отображается'):
        browser.element('[class="cart-qty"]').click()
        browser.all('[class="cart-item-row"]')[0].should(have.text('Smartphone'))
        browser.all('[class="cart-item-row"]')[1].should(have.text('Fiction'))
        browser.element('[class="ico-logout"]').click()
        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")


@allure.link('https://demowebshop.tricentis.com', 'demowebshop')
@allure.title('Добавление товара в корзину не авторизованным пользователем')
def test_added_product_in_basket_no_auth(browser_config):
    with allure.step('Добавление товара в корзину через API'):
        response = requests.post(API_URL + 'addproducttocart/catalog/14/1/1')
        cookie = response.cookies.get('Nop.customer')
        response = requests.post(API_URL + 'addproducttocart/catalog/51/1/1', cookies={'Nop.customer': cookie})
        cookie = response.cookies.get('Nop.customer')
    with allure.step('Проверка что в корзине товар отображается'):
        browser.open(WEB_URL)
        browser.driver.add_cookie({'name': 'Nop.customer', 'value': cookie})
        browser.open(WEB_URL)
        browser.element('[class="cart-qty"]').click()
        browser.all('[class="cart-item-row"]')[0].should(have.text('Diamond Heart'))
        browser.all('[class="cart-item-row"]')[1].should(have.text('Music'))
        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")


