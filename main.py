import flet as ft
from views.index import IndexView
from views.question import QuestionView
from views.simple_view import SimpleView

def main(page: ft.Page):
  page.title = "CS Project 2025 - Class 12 A Sci "
  page.expand=True
  page.theme_mode = ft.ThemeMode.DARK
  page.bgcolor = "#020617"

  if page.width <= 400:
      tile_size = 42
  elif page.width <= 600:
      tile_size = 52
  else:
      tile_size = 75

  page.fonts = {
    "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
    "playwrite": "fonts/playwrite.ttf",
      "font1":"fonts/ShadowsIntoLight-Regular.ttf",
      "font2":"fonts/FontdinerSwanky-Regular.ttf",
      "font3":"fonts/MedievalSharp-Regular.ttf",
  }

  def route_change(route):
      page.views.clear()
      troute = ft.TemplateRoute(page.route)
      IndexView(page, {"tile_size": tile_size})

      if troute.match("/question/:id"):
          params = {"id": troute.id}
          QuestionView(page, params)
      elif troute.match("/simple_view"):
          SimpleView(page, {})

  def view_pop(view):
      if len(page.views) > 1:
          page.views.pop()
          top_view = page.views[-1]
          page.go(top_view.route)
      else:
          page.go("/")

  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go(page.route)
#ft.app(target=main)
ft.app(target=main,assets_dir="assets",view=ft.AppView.WEB_BROWSER)
