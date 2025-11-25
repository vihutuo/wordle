import flet as ft
from mypack import  misc

def IndexView(page:ft.Page, params):
    def CreateAppBar():
        app_bar = ft.AppBar(

            title=ft.Text("Wordle",font_family="playwrite",size=45),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            toolbar_height=150,
            actions=[
                ft.IconButton(ft.Icons.RESTART_ALT, on_click=restart_clicked,icon_size=40),
                ft.IconButton(ft.Icons.LIGHTBULB,icon_size=40,on_click=hint),

            ],
        )
        return app_bar
    def hint(e):
        dlg =ft.AlertDialog(title=ft.Text("Sorry No Hint for You :-} "))
        page.open(dlg)
    def restart_clicked(e):
         dlg = ft.AlertDialog(title=ft.Text("New Game!"))
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

    def build_board(rows=5, cols=5):
        board = ft.Column()

        for _ in range(rows):
            row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

            for _ in range(cols):

                row.controls.append(
                    ft.Container(
                        width=75,
                        height=75,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        border_radius=10

                    )
                )
            board.controls.append(row)
        return board

    Guess = ft.TextField(label="Guess The Word",max_length=5,width=250)
    wordle_words = misc.ReadCSV("data/wordle_words.txt")
    print(wordle_words)
    page.views.append(ft.View(
        "/",
        [appbar, build_board(),Guess ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

    )
    )
    page.update()



