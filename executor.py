from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

class Executor:

    @staticmethod
    def open(url: str) -> 'Executor':
        driver = webdriver.Chrome(ChromeDriverManager().install())
        result = Executor(driver)

        driver.get(url)

        return result

    def __init__(self, driver: WebDriver) -> None:
        self.__driver__ = driver
        self.__wait__ = WebDriverWait(self.__driver__, 10)

    def __click__(self, element: WebElement) -> 'Executor':
        self.__driver__.execute_script('arguments[0].click();', element)
        return self

    def __send_keys__(self, element: WebElement, keys: str) -> 'Executor':
        element.send_keys(keys)
        return self
    
    def __drag_file__(self, element: WebElement, file_path: str) -> 'Executor':
        pass

    def find(self, path: str) -> 'Executor.__Sentence__':
        return Executor.__Sentence__(self, path)

    class __Sentence__:
        def __init__(self, executor: 'Executor', path: str) -> None:
            self.__executor__ = executor
            self.__path__ = path
            self.__by__: str = None
            self.__until__ = EC.presence_of_element_located

        def by(self, by: str) -> 'Executor.__Sentence__':
            self.__by__ = by
            return self

        def until(self, method) -> 'Executor.__Sentence__':
            self.__until__ = method
            return self

        def And(self) -> 'Executor.__Proxy__':
            return Executor.__Proxy__(self)

    class __Proxy__:
        def __init__(self, sentence: 'Executor.__Sentence__') -> None:
            self.__sentence__ = sentence

        def click(self) -> 'Executor':
            return self.__sentence__.__executor__.__click__(self.__get_target_element__())

        def select(self, index: int) -> 'Executor':
            self.__sentence__.__path__ = f'{self.__sentence__.__path__}/option[{index}]'
            self.__get_target_element__().click()

            return self.__sentence__.__executor__
    
        def send(self, message: str) -> 'Executor':
            return self.__sentence__.__executor__.__send_keys__(self.__get_target_element__(), message)

        def drag(self, file_path: str) -> 'Executor':
            return self.__sentence__.__executor__.__drag_file__(self.__get_target_element__(), file_path)
        
        def __get_target_element__(self) -> WebElement:
            print(f'path: {self.__sentence__.__path__}')
            element = self.__sentence__.__executor__.__wait__.until(
                self.__sentence__.__until__((self.__sentence__.__by__, self.__sentence__.__path__)))

            print('get element')
            return element


# //*[@id="pet-select"]
# //*[@id="pet-select"]/option[3]
# //*[@id="pet-select"]/option[2]