import flet as ft

def IndexView(page:ft.Page, params):
    def CreateAppBar():
        app_bar = ft.AppBar(

            title=ft.Text("Wordle",font_family="playwrite"),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(ft.Icons.RESTART_ALT, on_click=restart_clicked),
                ft.IconButton(ft.Icons.FILTER_3),

            ],
        )
        return app_bar

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
                        bgcolor=ft.Colors.BLUE_GREY_200,
                    )
                )
            board.controls.append(row)
        return board

    page.views.append(ft.View(
        "/",
        [appbar, build_board() ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

    )
    )
    page.update()



