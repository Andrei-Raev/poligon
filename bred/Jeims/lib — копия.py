command = [i for i in input().split()]
#del command[0]
#del command[0]
print(command)
def open_floader(a):
    if 'дом' in a[0].lower:
        print('Домашняя деректория')
    elif 'загруз' in a[0].lower:
        print('загрузки')
    elif ('кастомн' in a[0].lower or 'свой' in a[0].lower) and 'путь' in a[1].lower:
        put = input('Введите абсолютный путь: ')
def task(a):
    if 'открой' in a[0]:
        del a[0]
        del a[0]
        open_floader(a)
            
task(command)