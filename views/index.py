import flet as ft
from mypack import  misc
import random

def IndexView(page:ft.Page, params):
    def CreateAppBar():
        app_bar = ft.AppBar(

            title=ft.Row([ft.Text("Wordle ",font_family="font2",size=45),
                          ft.IconButton(ft.Icons.RESTART_ALT, on_click=restart_clicked, icon_size=40),
                          ft.IconButton(ft.Icons.LIGHTBULB, icon_size=40, on_click=hint)

                          ],
                         alignment=ft.MainAxisAlignment.CENTER,),

            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            toolbar_height=120,


        )
        return app_bar
    def hint(e):
        dlg =ft.AlertDialog(title=ft.Text(hint))
        page.open(dlg)
    def restart_clicked(e):

        nonlocal current_row, Answer,hint
        current_row =0
        Guess.disabled=False
        Guess.value=""
        Answer,hint = random.choice(word_list)
        message.value="Guess the Word"

        for r in range(rows):
            for c in range(cols):
                box_txt[r][c].value = ""
        print("Answer:",Answer)
        page.update()
        dlg = ft.AlertDialog(title=ft.Text("New Game started!"))
        page.open(dlg)



    def btn_question1_clicked(e):
        page.go("/question/1")

    def btn_question2_clicked(e):
        page.go("/question/2")

    def btn_simple_clicked(e):
        page.go("/simple_view")




    #btn_question1 = ft.ElevatedButton("Question1", on_click=btn_question1_clicked)
    #btn_question2 = ft.ElevatedButton("Question2", on_click=btn_question2_clicked)
    #btn_simple = ft.ElevatedButton("Simple View", on_click=btn_simple_clicked)

    appbar = CreateAppBar()

    def build_board(rows, cols):
        board = ft.Column()

        box_txt = []

        for _ in range(rows):
            row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            row_box_txt = []

            for _ in range(cols):
                txt = ft.Text(
                    value="",
                    color= ft.Colors.WHITE,
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                )
                row.controls.append(
                    ft.Container(
                    width=75,
                    height=75,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    content=txt
                )
                )

                row_box_txt.append(txt)

            box_txt.append(row_box_txt)
            board.controls.append(row)
        return board,  box_txt



    def check_guess(e):
        nonlocal current_row, Answer

        if current_row >= rows or Guess.disabled:
            return

        guess = Guess.value.strip().upper()

        if len(guess) != cols or not guess.isalpha():
            message.value = "Please Enter 5 letters."
            page.update()
            return

        for i, ch in enumerate(guess):
            box_txt[current_row][i].value = ch

        if guess == Answer:
            message.value = f" Correct! The word was {Answer}."
            message.color= ft.Colors.GREEN
            Guess.disabled = True
        else:
            current_row += 1
            if current_row >= rows:
                message.value = f" Out of tries! The word was {Answer}."
                Guess.disabled = True

        Guess.value = ""
        page.update()




    Guess = ft.TextField(label="Type here", max_length=5, width=250, on_submit=check_guess,text_size=28,autofocus=True)

    message = ft.Text(
        value="Guess the Word",text_align=ft.TextAlign.CENTER,size=25,font_family="font1")
    page.update()




    board,  box_txt = build_board(rows=5, cols=5)
    current_row = 0
    rows = 5
    cols = 5



    wordle_words = misc.ReadCSV("data/wordle_words.txt")
    word_list = [
        (row[0].strip().upper(), row[1].strip())
        for row in wordle_words
    ]

    Answer, hint = random.choice(word_list)



    print(wordle_words)
    print("Answer:",Answer)
    page.views.append(ft.View(
        "/",
        [appbar, board,Guess, message ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

    )
    )
    page.update()