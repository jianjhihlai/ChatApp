from affairnote import AffairNote

notebook = AffairNote()
while True:
    note = input('請問您預計要做的事：')
    if note == '結束':
        print('您尚有以下工作：{}'.format(notebook.remind()))
        break
    else:
        response = notebook.inputaffair(note)
    print(response)