import os, time
from typing import Callable
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

__JS_DROP_FILE__ = "var tgt=arguments[0],e=document.createElement('input');e.type='"+\
"file';e.addEventListener('change',function(event){var dataTrans" +\
"fer={dropEffect:'',effectAllowed:'all',files:e.files,items:{},t" +\
"ypes:[],setData:function(format,data){},getData:function(format" +\
"){}};var emit=function(event,target){var evt=document.createEve" +\
"nt('Event');evt.initEvent(event,true,false);evt.dataTransfer=da"+\
"taTransfer;target.dispatchEvent(evt);};emit('dragenter',tgt);em"+\
"it('dragover',tgt);emit('drop',tgt);document.body.removeChild(e"+\
");},false);document.body.appendChild(e);return e;"

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

    def __click__(self, sentence: 'Executor.__Sentence__') -> 'Executor':
        self.__driver__.execute_script('arguments[0].click();', self.__get_element__(sentence))

        return self

    def __send_keys__(self, sentence: 'Executor.__Sentence__', keys: str) -> 'Executor':
        element = self.__get_element__(sentence)
        element.clear()
        element.send_keys(keys)
        return self
    
    def __drag_file__(self, sentence: 'Executor.__Sentence__', file_path: str) -> 'Executor':
        element = self.__get_element__(sentence)
        temp: WebElement = self.__driver__.execute_script(__JS_DROP_FILE__, element)
        temp.send_keys(os.path.abspath(file_path))

    def __select__(self, sentence: 'Executor.__Sentence__', index: int) -> 'Executor':
        sentence.__path__ = f'{sentence.__path__}/option[{index}]'
        self.__get_element__(sentence).click()
        
        return self
    
    def __exec_raw__(self, sentence: 'Executor.__Sentence__', func: Callable[[WebElement], None]) -> 'Executor':
        func(self.__get_element__(sentence))

        return self
    
    def __get_element__(self, sentence: 'Executor.__Sentence__') -> WebElement:
        return self.__wait__.until(sentence.__until__((sentence.__by__, sentence.__path__)))

    def find(self, path: str) -> 'Executor.__Sentence__':
        return Executor.__Sentence__(self, path)
        
    def wait(self, mills: float) -> 'Executor':
        time.sleep(mills / 1000)

        return self

    class __Sentence__:
        def __init__(self, executor: 'Executor', path: str) -> None:
            self.__executor__ = executor
            self.__path__ = path
            self.__by__: str = By.XPATH
            self.__until__ = EC.presence_of_element_located

        def by(self, by: str) -> 'Executor.__Sentence__':
            self.__by__ = by
            return self

        def until(self, method) -> 'Executor.__Sentence__':
            self.__until__ = method
            return self

        def then(self) -> 'Executor.__Proxy__':
            return Executor.__Proxy__(self)

    class __Proxy__:
        def __init__(self, sentence: 'Executor.__Sentence__') -> None:
            self.__sentence__ = sentence

        def click(self) -> 'Executor':
            return self.__sentence__.__executor__.__click__(self.__sentence__)

        def select(self, index: int) -> 'Executor':
            return self.__sentence__.__executor__.__select__(self.__sentence__, index)
    
        def send(self, message: str) -> 'Executor':
            return self.__sentence__.__executor__.__send_keys__(self.__sentence__, message)

        def drag(self, file_path: str) -> 'Executor':
            return self.__sentence__.__executor__.__drag_file__(self.__sentence__, file_path)
        
        def exec_raw(self, func: Callable[[WebElement], None]) -> 'Executor':
            return self.__sentence__.__executor__.__exec_raw__(self.__sentence__, func)



# //*[@id="pet-select"]
# //*[@id="pet-select"]/option[3]
# //*[@id="pet-select"]/option[2]“