from core import MainCore

mc = MainCore()


class lib:
    def main(self, stroka):
        if stroka == 'тест':
            try:
                mc.talk('test')
                print(mc.command())
                mc.talk('Все в порядке')
            except Exception:
                mc.talk('Что то пошло не так...')
        elif stroka.lower().strip() == 'привет':
            try:
                mc.talk('И тебя приветствую я')
                print(mc.command())
                mc.talk('Все в порядке')
            except Exception:
                mc.talk('Что то пошло не так...')
