import flet as ft
from mypack import  misc
import random
import asyncio


def IndexView(page: ft.Page, params):
    tile_size = params.get("tile_size")
    def CreateAppBar():
        app_bar = ft.AppBar(

            title=ft.Row([ft.Text("Wordle ",font_family="font2",size=45),
                          ft.IconButton(ft.Icons.RESTART_ALT, on_click= restart_clicked, icon_size=40),
                          ft.IconButton(ft.Icons.LIGHTBULB, icon_size=40, on_click=show_hint)

                          ],
                         alignment=ft.MainAxisAlignment.CENTER,),

            bgcolor= "#1A1C1E",
            toolbar_height=110,


        )
        return app_bar




    def show_hint(e):
        dlg =ft.AlertDialog(title=ft.Text(hint,font_family="font3",size=35),)
        page.open(dlg)





    def restart_clicked(e):

        nonlocal current_row, Answer, hint ,wins
        current_row = 0
        Guess.disabled = False
        Guess.value = ""
        Answer, hint = random.choice(word_list)
        wins = 0
        winstreak.value = f"🏆 WinStreak: {wins}"
        message.value = "Guess the Word"

        for r in range(rows):
            for c in range(cols):
                boxes_txt[r][c].value = ""
                boxes[r][c].bgcolor = ft.Colors.BLUE_GREY_700
        print("Answer:", Answer)
        page.update()
        dlg = ft.AlertDialog(title=ft.Text("New Game started!",font_family="font3",size=30),)
        page.open(dlg)






    def win(e):

        nonlocal current_row, Answer, hint
        current_row = 0
        Guess.disabled = False
        Guess.value = ""
        Answer, hint = random.choice(word_list)
        message.value = "Correct! Try another One!"

        next_game_btn.visible=False

        for r in range(rows):
            for c in range(cols):
                boxes_txt[r][c].value = ""
                boxes[r][c].bgcolor = ft.Colors.BLUE_GREY_700
        print("Answer:", Answer)
        page.update()



    def btn_question1_clicked(e):
        page.go("/question/1")

    def btn_question2_clicked(e):
        page.go("/question/2")

    def btn_simple_clicked(e):
        page.go("/simple_view")










    def build_board(rows, cols,tile_size):
        board = ft.Column()

        boxes_txt = []
        boxes = []

        for _ in range(rows):
            row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            row_boxes = []
            row_box_txt = []

            for _ in range(cols):
                txt = ft.Text(
                    value="",
                    color=ft.Colors.WHITE,
                    size=tile_size * 0.5,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                )
                box = ft.Container(
                    width=tile_size,
                    height=tile_size,

                    bgcolor=ft.Colors.BLUE_GREY_900,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    content=txt,
                    animate=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
                    rotate=ft.Rotate(
                        angle=0,
                        alignment=ft.alignment.center
                    ),
                    animate_rotation=300,

                )

                row.controls.append(box)
                row_boxes.append(box)

                row_box_txt.append(txt)

            boxes_txt.append(row_box_txt)
            boxes.append(row_boxes)
            board.controls.append(row)
        return board, boxes, boxes_txt

    async def check_guess(e):
        nonlocal current_row, Answer, wins

        guess = Guess.value.strip().upper()

        if guess not in valid_list:
            message.value = "Please Enter a valid Word"
            message.color = ft.Colors.RED_300
            page.update()
            return()

        for i, ch in enumerate(guess):
            boxes_txt[current_row][i].value = ch
            if guess[i] == Answer[i]:
                board.controls[current_row].controls[i].bgcolor = "GREEN"

            elif ch in Answer:
                board.controls[current_row].controls[i].bgcolor = "YELLOW"

            else:
                board.controls[current_row].controls[i].bgcolor = "GREY"

            #board.controls[current_row].controls[i].rotate.angle += 2 * 3.14
            #box_txt[current_row][i].rotate.angle += 2 * 3.14
            page.update()
            await asyncio.sleep(0.36)

        """answer_list = list(Answer)
        color_list = ["dark"] * cols

        for i in range(cols):
            if guess[i] == answer_list[i]:
                color_list[i] = "green"

        for i in range(cols):
            if color_list[i] == "green":
                continue
            if guess[i] in answer_list:
                color_list[i] = "yellow"
                j = answer_list.index(guess[i])
                answer_list[j] = None

        for i, color in enumerate(color_list):
            box = boxes[current_row][i]

            if color == "green":
                box.bgcolor = ft.Colors.GREEN
            elif color == "yellow":
                box.bgcolor = ft.Colors.YELLOW
            else:
                box.bgcolor = ft.Colors.BLUE_GREY_900 """

        if guess == Answer:
            message.value = f" Correct! The word was {Answer}."
            message.color = ft.Colors.GREEN
            Guess.disabled = True
            correct_sfx.pause()
            correct_sfx.play()
            wins += 1
            winstreak.value = f"🏆 WinStreak: {wins}"
            next_game_btn.visible = True
            next_game_btn.on_click = win


        else:
            current_row += 1
            if current_row >= rows:
                message.value = f" Out of tries! The word was {Answer}."
                Guess.disabled = True
                wins = 0
                winstreak.value =f"🏆 WinStreak: {wins}"
                wrong_sfx.pause()
                wrong_sfx.play()

        Guess.value = ""
        Guess.focus()

        page.update()
        return wins

    wins = 0
    winstreak = ft.Text(value=f"🏆 WinStreak: {wins}",font_family="font3")

    next_game_btn = ft.ElevatedButton(content= ft.Text("Continue", font_family="font3"), visible=False )



    Guess = ft.TextField(label="Type here", max_length=5, width=250, on_submit=check_guess, text_size=28,
                         autofocus=True)

    message = ft.Text(
        value="Guess the Word", text_align=ft.TextAlign.CENTER, size=25, font_family="font1")
    page.update()

    current_row = 0
    rows = 5
    cols = 5
    board, boxes, boxes_txt = build_board(rows, cols, tile_size)
    appbar = CreateAppBar()



    wordle_words = misc.ReadCSV("data/wordle_words.txt")
    word_list = [
        (row[0].strip().upper(), row[1].strip())
        for row in wordle_words
    ]

    valid_list = misc.GetAllWords("data/5-letter-words.txt") #returns set
    print(list(valid_list)[:10])
    Answer, hint = random.choice(word_list)
    correct_sfx = ft.Audio(
        src="Audio/correct3.wav",
        volume=0.9,
        autoplay=False,
    )
    wrong_sfx = ft.Audio(
        src="Audio/wrong3.wav",
        volume=0.9,
        autoplay=False,
    )

    page.overlay.append(correct_sfx)
    page.overlay.append(wrong_sfx)







    print("Answer:", Answer)
    page.views.append(ft.View(
        "/",
        [appbar, board, Guess, message,
         ft.Row([winstreak,next_game_btn

        ],alignment=ft.MainAxisAlignment.CENTER,)],bgcolor = "#0f1115",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,scroll=ft.ScrollMode.AUTO

    )
    )

    page.update()


