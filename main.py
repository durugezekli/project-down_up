import flet as ft
import platform as p
from unidecode import unidecode as ud
from time import sleep, time as st
from requests import get, post
from random import randint
from os import path
from datetime import datetime, timedelta
from threading import Thread

import logging
# logging.basicConfig(level=logging.DEBUG)

# External Threads
def audio_api_activation_thread():
    while 1:
        try: get("https://audio-recognition-api.onrender.com")
        except: pass
        sleep(60*10)

def letter_api_activation_thread():
    while 1:
        try: get("https://letter-recognition-api.onrender.com")
        except: pass
        sleep(60*10)

def shape_api_activation_thread():
    while 1:
        try: get("https://shape-recognition-api.onrender.com")
        except: pass
        sleep(60*10)

t1 = Thread(target=audio_api_activation_thread)
t1.start()

t2 = Thread(target=letter_api_activation_thread)
t2.start()

t3 = Thread(target=shape_api_activation_thread)
t3.start()

# Additional Widgets
class HintLine():
    def __init__(self, active_color: str, inactive_color: str, alignment: ft.MainAxisAlignment):
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.alignment = alignment

class Carousel(ft.UserControl):
    current_item: int = 0

    def __init__(self, page: ft.Page, items: list[ft.Control] = None, width: int = None, height: int = None, expand: None | bool | int = None, tooltip: str = None, visible: bool = None,disabled: bool = None,padding: ft.PaddingValue = None,margin: None | int | float | ft.Margin = None, alignment: ft.Alignment = None,bgcolor: str = None,gradient: ft.LinearGradient = None, border: ft.Border = None,border_radius: None | int | float | ft.BorderRadius = None,hint_lines: HintLine = False,ending_route: str = None,animated_switcher: ft.AnimatedSwitcher = ft.AnimatedSwitcher(transition=ft.AnimatedSwitcherTransition.SCALE, duration=500, reverse_duration=100, switch_in_curve=ft.AnimationCurve.BOUNCE_OUT, switch_out_curve=ft.AnimationCurve.BOUNCE_IN)):
        super().__init__()
        self.page = page
        self.width = width
        self.height = height
        self.expand = expand
        self.tooltip = tooltip
        self.visible = visible
        self.disabled = disabled
        self.padding = padding
        self.margin = margin
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.gradient = gradient
        self.border = border
        self.border_radius = border_radius
        self.ending_route = ending_route

        self.items = items
        self.hint_lines = hint_lines
        self.animated_switcher = animated_switcher
        if animated_switcher and self.items: self.animated_switcher.content = self.items[0] if items else ft.Container()
    
    def build(self):
        _controls = []
        if self.hint_lines:
            self.__hint_lines_element = ft.Row(
                controls=[ft.Container(animate_size=300, bgcolor=self.hint_lines.active_color if i == 0 else self.hint_lines.inactive_color, scale=1, border_radius=8, height=16, width=16, animate_scale=300) for i in range(len(self.items))],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                height=32
            )
            _controls.append(self.__hint_lines_element)
            self.__hint_lines_element.controls[0].bgcolor = self.hint_lines.active_color
            self.__hint_lines_element.controls[0].height = 32
        render = ft.Column([ft.Column(col=len(_controls), controls=_controls, spacing=20), self.animated_switcher], expand=True, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    
        return ft.Container(width=self.width, height=self.height, expand=self.expand, tooltip=self.tooltip, visible=self.visible, disabled=self.disabled, padding=self.padding, margin=self.margin, alignment=self.alignment, bgcolor=self.bgcolor, gradient=self.gradient, border=self.border, border_radius=self.border_radius, clip_behavior=ft.ClipBehavior.HARD_EDGE, content=render)

    def next(self, e=None):
        if self.current_item < len(self.items)-1: self.go(self.current_item + 1)
        elif self.ending_route != None: self.page.go(self.ending_route)

    def prev(self, e=None):
        if self.current_item > 0: self.go(self.current_item - 1)

    def go(self, index: int):
        if index in range(len(self.items)):
            try:
                self.current_item = index
                self.bgcolor = self.items[self.current_item].bgcolor
                try: self.page.update()
                except: pass
                self.animated_switcher.content = self.items[self.current_item]
                self.animated_switcher.expand = self.expand
                try: self.animated_switcher.update()
                except: pass

                if self.hint_lines:
                    for i, c in enumerate(self.__hint_lines_element.controls): 
                        if i <= self.current_item: c.bgcolor = self.hint_lines.active_color
                        else: c.bgcolor = self.hint_lines.inactive_color
                        c.scale = 1
                        c.height = 16
                        try: c.update()
                        except: pass

                    self.__hint_lines_element.controls[self.current_item].bgcolor = self.hint_lines.active_color
                    self.__hint_lines_element.controls[self.current_item].height = 32
                    try: self.__hint_lines_element.update()
                    except: pass
            except Exception as e: print(str(e))

def get_rich_text(text, size):
    return ft.Stack([
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text.split("+")[0] if "+" in text else text.split("-")[0],
                        ft.TextStyle(
                            size=size,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                color="#DD363E",
                                stroke_width=3,
                                stroke_join=ft.StrokeJoin.ROUND,
                                style=ft.PaintingStyle.STROKE,
                            ),
                        ),
                    ),
                    ft.TextSpan(
                        "+" if "+" in text else "-",
                        ft.TextStyle(
                            size=size,
                            color="#FFADCF"
                        ),
                    ),
                    ft.TextSpan(
                        text.split("+")[1].split("=")[0] if "+" in text else text.split("-")[1].split("=")[0],
                        ft.TextStyle(
                            size=size,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                color="#DD363E",
                                stroke_width=3,
                                stroke_join=ft.StrokeJoin.ROUND,
                                style=ft.PaintingStyle.STROKE,
                            ),
                        ),
                    ),
                    ft.TextSpan(
                        "=",
                        ft.TextStyle(
                            size=size,
                            color="#FFADCF"
                        ),
                    ),
                    ft.TextSpan(
                        text.split("=")[1],
                        ft.TextStyle(
                            size=size,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                color="#DD363E",
                                stroke_width=3,
                                stroke_join=ft.StrokeJoin.ROUND,
                                style=ft.PaintingStyle.STROKE,
                            ),
                        ),
                    ),
                ],
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text.split("+")[0] if "+" in text else text.split("-")[0],
                        ft.TextStyle(
                            size=size,
                            weight=ft.FontWeight.BOLD,
                            color="#EF3E40"
                        ),
                    ),
                    ft.TextSpan(
                        "+" if "+" in text else "-",
                        ft.TextStyle(
                            size=size,
                            color="#FFADCF"
                        ),
                    ),
                    ft.TextSpan(
                        text.split("+")[1].split("=")[0] if "+" in text else text.split("-")[1].split("=")[0],
                        ft.TextStyle(
                            size=size,
                            weight=ft.FontWeight.BOLD,
                            color="#EF3E40"
                        ),
                    ),
                    ft.TextSpan(
                        "=",
                        ft.TextStyle(
                            size=size,
                            color="#FFADCF"
                        ),
                    ),
                    ft.TextSpan(
                        text.split("=")[1],
                        ft.TextStyle(
                            size=size,
                            weight=ft.FontWeight.BOLD,
                            color="#EF3E40"
                        ),
                    ),
                ],
            ),
        ]
    )

# App
class MyApp():
    def __init__(self):
        self.section_colors = {"Alfabe": ft.colors.RED, "Şekiller": ft.colors.BLUE, "Matematik": ft.colors.GREEN}

        self.main_pages = {"ogren": self.ogren, "cizelge": self.cizelge, "profil": self.profil}
        self.last_click_position = None

        self.days_en2tr = {"Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba", "Thursday": "Perşembe", "Friday": "Cuma", "Saturday": "Cumartesi", "Sunday": "Pazar"}

        self.learn_letter_index = {} 
        for a, b in [(f"{x.upper() if x != 'i' else 'I'} Harfi", f"/learn_letter_{x}") for x in "abcçdefgğhıijklmnoöprsştuüvyz"]: self.learn_letter_index.update({a: b})
        self.draw_letter_index = {}
        for a, b in [(f"{x.upper() if x != 'i' else 'I'} Harfi Çiz", f"/draw_letter_{x}") for x in "abcçdefgğhıijklmnoöprsştuüvyz"]: self.draw_letter_index.update({a: b})
        self.letter_sequence_index = {"A-B-C-D Harfleri": "/letter_sequence_abcd", "O-Ö-U-Ü Harfleri": "/letter_sequence_oöuü", "Z-Ğ-T-P Harfleri": "/letter_sequence_zğtp", "G-F-E-R Harfleri": "/letter_sequence_gfer", "I-H-J-İ Harfleri": "/letter_sequence_ıhji"}
        
        self.learn_shape_index = {"Kare Şekli": "/learn_shape_2d_kare", "Dikdörtgen Şekli": "/learn_shape_2d_dikdörtgen", "Üçgen Şekli": "/learn_shape_2d_üçgen", "Daire Şekli": "/learn_shape_2d_daire", "Küp Şekli": "/learn_shape_3d_küp", "Küre Şekli": "/learn_shape_3d_küre", "Silindir Şekli": "/learn_shape_3d_silindir", "Koni Şekli": "/learn_shape_3d_koni"}
        self.draw_shape_index = {"Üçgen Çiz": "/draw_shape_2d_üçgen", "Kare Çiz": "/draw_shape_2d_kare", "Dikdörtgen Çiz": "/draw_shape_2d_dikdörtgen", "Daire Çiz": "/draw_shape_2d_daire"}

        self.learn_number_index = {}
        for a, b in [(f"{x} Sayısı", f"/learn_number_{x}") for x in range(21)]: self.learn_number_index.update({a: b})
        self.learn_math_index = {"Eşitlik Durumu": "/learn_symbol_eşittir", "Toplama İşlemi": "/learn_symbol_artı", "Çıkarma İşlemi": "/learn_symbol_eksi", "1+2 İşlemi": "/math_operation_1+2", "1+5 İşlemi": "/math_operation_1+5", "2+6 İşlemi": "/math_operation_2+6", "4+5 İşlemi": "/math_operation_4+5", "4-1 İşlemi": "/math_operation_4-1", "10-5 İşlemi": "/math_operation_10-5", "7-3 İşlemi": "/math_operation_7-3", "8-3 İşlemi": "/math_operation_8-3"}

        self.parent_index = {
            "Harfleri Öğren": ["Alfabe", self.learn_letter_index], "Harfleri Çiz": ["Alfabe", self.draw_letter_index], "Harfleri Oku": ["Alfabe", self.letter_sequence_index],
            "Sayıları Öğren": ["Matematik", self.learn_number_index], "Sayı İşlemleri": ["Matematik", self.learn_math_index],
            "Şekilleri Öğren": ["Şekiller", self.learn_shape_index], "Şekilleri Çiz": ["Şekiller", self.draw_shape_index],
        }
        self.coded_parent_index = {}
        for k, v in list(self.parent_index.items()): self.coded_parent_index.update({k.lower().replace(" ",""): v})
        self.current_index = None

        self.activation_time = None

    def is_level_on(self, page):
        psr = [list(i[1].values()) for i in list(self.parent_index.values())]
        ps = []
        for p in psr: ps += p
        return True if page.route in ps else False
    
    def go_to_prev_lesson(self, e):
        page = e.control.data
        self.close_dialogs(e)
        vs = list(self.coded_parent_index[self.current_index].values())
        i = vs.index(page.route)
        if i > 0: page.go(vs[i-1])
        else: page.go(f"/level_index_{self.current_index}")

    def go_to_next_lesson(self, e):
        page = e.control.data
        self.close_dialogs(e)
        vs = list(self.coded_parent_index[self.current_index][1].values())
        i = vs.index(page.route)
        if i < len(vs) - 1: page.go(vs[i+1])
        else: page.go(f"/level_index_{self.current_index}")

    def close_dialogs(self, e):
        page = e.control.data
        self.success_modal.open = False
        try: self.success_audio.stop()
        except: pass
        self.fail_modal.open = False
        try: self.fail_audio.stop()
        except: pass
        try: page.update()
        except: pass

    def intro(self, page):
        carousel = Carousel(
            page=page,
            padding=ft.Padding(30, 70, 30, 5),
            bgcolor="#EBF2F7",
            expand=True,
            ending_route="/ogren",
            animated_switcher=ft.AnimatedSwitcher(
                transition=ft.AnimatedSwitcherTransition.FADE, 
                duration=500, 
                reverse_duration=500, 
                switch_in_curve=ft.AnimationCurve.EASE_IN, 
                switch_out_curve=ft.AnimationCurve.EASE_OUT,
                expand=True,
            ),
            hint_lines=HintLine(
                active_color="blue",
                inactive_color="#53545E",
                alignment=ft.MainAxisAlignment.CENTER
            ),
            items=[
                ft.Container(
                    ft.Column([
                        ft.Image(
                            src=f"intro_1.gif",
                            width=float("inf"),
                            fit=ft.ImageFit.FIT_WIDTH,
                        ),
                        ft.Text("Merhaba! Burada Down-Up ile tanışacak, eğitimde fırsat eşitliği yolculuğuna çıkacaksınız!", height=page.height//6, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, width=float("inf"), text_align=ft.TextAlign.CENTER),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=ft.Padding(0, 10, 0, 0)
                ),
                ft.Container(
                    ft.Column([
                        ft.Image(
                            src=f"intro_2.gif",
                            width=float("inf"),
                            fit=ft.ImageFit.FIT_WIDTH,
                        ),
                        ft.Text("Menüde gördüğün bir etkinlik seç.", height=page.height//6, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, width=float("inf"), text_align=ft.TextAlign.CENTER),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=ft.Padding(0, 10, 0, 0)
                ),
                ft.Container(
                    ft.Column([
                        ft.Image(
                            src=f"intro_3.gif",
                            width=float("inf"),
                            fit=ft.ImageFit.FIT_WIDTH,
                        ),
                        ft.Text("Ardından en efektif şekilde öğrenmeye başla!", height=page.height//6, theme_style=ft.TextThemeStyle.TITLE_MEDIUM, width=float("inf"), text_align=ft.TextAlign.CENTER)
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=ft.Padding(0, 10, 0, 0),
                ),
            ],
        )

        buttons = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            controls=[
                ft.ElevatedButton(col=6, height=50, style=ft.ButtonStyle(bgcolor="white", side=ft.BorderSide(width=2, color="white")), text="Önceki", on_click=carousel.prev), 
                ft.ElevatedButton(col=6, height=50, style=ft.ButtonStyle(color="#151519", bgcolor="blue", side=ft.BorderSide(width=2, color="white")), text="Sonraki", on_click=carousel.next)
            ]
        )
        
        return ft.Container(ft.Column([carousel, buttons], expand=True), expand=True, padding=ft.Padding(30, 60, 30, 30))

    def ogren(self, page):
        self.page_name = ft.Text(value="Öğren", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Icon(ft.icons.MENU_BOOK)
        page.appbar = ft.AppBar(leading=self.page_icon, leading_width=65, title=self.page_name, center_title=True, actions=[ft.PopupMenuButton(width=60, items=[ft.PopupMenuItem(text="Bildir", on_click=lambda x: page.go("/report") )])], bgcolor="#EBF2F7", toolbar_height=70)
        def change(event):
            ix = event.page.navigation_bar.selected_index
            dests = event.page.navigation_bar.destinations
            dest = dests[ix]
            self.page_name.value = dest.label
            event.page.appbar.leading = ft.Icon(dests[ix].icon_content.name)
            self.container.content = self.main_pages[ud(dest.label.lower())](event.page)
            try: event.page.update()
            except: pass
        page.navigation_bar = ft.NavigationBar(
            bgcolor="#FFFFFF",
            height=80,
            destinations=[
                ft.NavigationDestination(
                    icon_content=ft.Icon(ft.icons.MENU_BOOK, scale=1.1),
                    selected_icon_content=ft.Icon(ft.icons.MENU_BOOK, color="blue", scale=1.1),
                    label="Öğren",
                ),
                ft.NavigationDestination(
                    icon_content=ft.Icon(ft.icons.CALENDAR_VIEW_MONTH_ROUNDED, scale=1),
                    selected_icon_content=ft.Icon(ft.icons.CALENDAR_VIEW_MONTH_ROUNDED, scale=1, color="blue"),
                    label="Çizelge",
                ),
                ft.NavigationDestination(
                    icon_content=ft.Icon(ft.icons.PERSON, scale=1.1),
                    selected_icon_content=ft.Icon(ft.icons.PERSON, scale=1.1, color="blue"),
                    label="Profil",
                ),
            ],
            on_change=change
        )

        self.get_current_time()

        if page.client_storage.contains_key("cizelge_dict"): self.cizelge_dict = page.client_storage.get("cizelge_dict")
        else: self.cizelge_dict = {"Pazartesi": [], "Salı": [], "Çarşamba": [], "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": []}
        li = self.cizelge_dict[self.day]

        def fix_color(e):
            pass
            # if e.pixels > 0: page.appbar.bgcolor = "white"
            # else:  page.appbar.bgcolor = "#EBF2F7"
            # try: page.update()
            # except: pass

        def goto(e): page.go(e.control.data)

        col = ft.Column([
            ft.ElevatedButton(content=ft.Row([
                ft.Row([
                    ft.Container(width=10, height=20, border_radius=5, bgcolor=self.section_colors[self.parent_index[ikey][0]]),
                    ft.Text("  "+ikey),
                ]),
                ft.Row([
                    ft.Text("%"+str(int((len(self.parent_index_states[ikey][0])/len(self.parent_index[ikey][1]))*100))),
                    ft.Container(ft.ProgressRing(bgcolor="grey", value=max(1/100, len(self.parent_index_states[ikey][0])/len(self.parent_index[ikey][1]))), padding=12, height=50, width=50),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            height=50, on_click=goto, data="/level_index_"+ikey.lower().replace(" ",""), width=float("inf"), style=ft.ButtonStyle(bgcolor="white", side=ft.BorderSide(width=2, color="white")))
            for ikey in list(self.parent_index.keys())
        ], scroll=ft.ScrollMode.ALWAYS, on_scroll=fix_color, expand=True, alignment=ft.alignment.top_center)

        if len(li) > 0:
            toli = [ft.DragTarget(
                group="dd",
                data=self.day,
                content=ft.Container(
                    content=ft.Column([ft.Text(self.day), ft.Row([ft.Container(content=ft.Text(txt), bgcolor=self.section_colors[txt], border_radius=5, padding=ft.Padding(10, 10, 10, 10)) for txt in li])]),
                    width=float("inf"),
                    bgcolor="#F2F6FA",
                    border_radius=5,
                    border=ft.border.all(2, "white"),
                    padding=ft.Padding(5, 5, 5, 5),
                ),
            )]
            col.controls = toli + col.controls

        # DELETE -------
        # col.controls += [ft.ElevatedButton(content=ft.Text("Android Test"), height=50, on_click=goto, data="/androidtest", width=float("inf"), style=ft.ButtonStyle(bgcolor="white", side=ft.BorderSide(width=2, color="white")))]

        return ft.Container(col, padding=ft.Padding(30, 30, 30, 10), width=float("inf"), height=page.height)

    def cizelge(self, page):
        self.get_current_time()

        if page.client_storage.contains_key("cizelge_dict"): self.cizelge_dict = page.client_storage.get("cizelge_dict")
        else: self.cizelge_dict = {"Pazartesi": [], "Salı": [], "Çarşamba": [], "Perşembe": [], "Cuma": [], "Cumartesi": [], "Pazar": []}

        def drag_will_accept(e):
            e.control.content.border = ft.border.all(3, "blue")
            try: e.control.update()
            except: pass

        def drag_accept(e):
            src = page.get_control(e.src_id)
            if not src.data in [x.content.value for x in e.control.content.content.controls[1].controls]:
                ls = ft.Container(content=ft.Text(src.data), bgcolor=self.section_colors[src.data], border_radius=5, padding=ft.Padding(10, 10, 10, 10))
                self.cizelge_dict[e.control.data].append(src.data)

                def rls(_):
                    e.control.content.content.controls[1].controls.remove(ls)
                    try: e.control.content.content.controls[1].update()
                    except: pass
                    self.cizelge_dict[e.control.data].remove(src.data)
                    page.client_storage.set("cizelge_dict", self.cizelge_dict)

                ls.on_click = rls
                e.control.content.content.controls[1].controls.append(ls)
                try:  e.control.content.content.update()
                except: pass
            e.control.content.border = ft.border.all(2, "white")
            try: e.control.update()
            except: pass

            page.client_storage.set("cizelge_dict", self.cizelge_dict)

        def drag_leave(e):
            e.control.content.border = ft.border.all(2, "white")
            try: e.control.update()
            except: pass

        def fix_color(e):
            pass
            # if e.pixels > 0: page.appbar.bgcolor = "white"
            # else:  page.appbar.bgcolor = "#EBF2F7"
            # try: page.update()
            # except: pass

        col = ft.Column(
            width=float("inf"),
            controls=[
                ft.ResponsiveRow(controls=[    
                    ft.Column(
                        col=6,
                        controls=[
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Draggable(
                                        data="Alfabe",
                                        content=ft.Container(
                                            content=ft.Text("Alfabe", weight=ft.FontWeight.NORMAL, style=ft.TextStyle(size=16, color="black", decoration_color=self.section_colors["Alfabe"])),
                                            bgcolor=self.section_colors["Alfabe"],
                                            border_radius=5,
                                            padding=ft.Padding(10, 15, 10, 15), 
                                        ),
                                        content_feedback=ft.Container(
                                            content=ft.Text("", weight=ft.FontWeight.NORMAL, style=ft.TextStyle(size=16, color="black", decoration_color=self.section_colors["Alfabe"])),
                                            bgcolor=self.section_colors["Alfabe"],
                                            border_radius=5,
                                            padding=ft.Padding(10, 13, 10, 10), 
                                            opacity=0.6,
                                            width=page.width//2-35,
                                            height=54,
                                        ),
                                    ),
                                ]
                            ),
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Draggable(
                                        data="Şekiller",
                                        content=ft.Container(
                                            content=ft.Text("Şekiller", weight=ft.FontWeight.NORMAL, style=ft.TextStyle(size=16, color="black", decoration_color=self.section_colors["Şekiller"])),
                                            bgcolor=self.section_colors["Şekiller"],
                                            border_radius=5,
                                            padding=ft.Padding(10, 15, 10, 15), 
                                        ),
                                        content_feedback=ft.Container(
                                            content=ft.Text("", weight=ft.FontWeight.NORMAL, style=ft.TextStyle(size=16, color="black", decoration_color=self.section_colors["Şekiller"])),
                                            bgcolor=self.section_colors["Şekiller"],
                                            border_radius=5,
                                            padding=ft.Padding(10, 13, 10, 10), 
                                            opacity=0.6,
                                            width=page.width//2-35,
                                            height=54,
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    ),
                    ft.Column(
                        col=6,
                        controls=[
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Draggable(
                                        data="Matematik",
                                        content=ft.Container(
                                            content=ft.Text("Matematik", weight=ft.FontWeight.NORMAL, style=ft.TextStyle(size=16, color="black", decoration_color=self.section_colors["Matematik"])),
                                            bgcolor=self.section_colors["Matematik"],
                                            border_radius=5,
                                            padding=ft.Padding(10, 15, 10, 15), 
                                        ),
                                        content_feedback=ft.Container(
                                            content=ft.Text("", weight=ft.FontWeight.NORMAL, style=ft.TextStyle(size=16, color="black", decoration_color=self.section_colors["Matematik"])),
                                            bgcolor=self.section_colors["Matematik"],
                                            border_radius=5,
                                            padding=ft.Padding(10, 13, 10, 10), 
                                            opacity=0.6,
                                            width=page.width//2-35,
                                            height=54,
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]),
                
                ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    on_scroll=fix_color,
                    expand=True,
                    width=float("inf"),
                    controls=[
                        ft.DragTarget(
                            data="Pazartesi",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Pazartesi"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5),
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                        ft.DragTarget(
                            data="Salı",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Salı"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5)
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                        ft.DragTarget(
                            data="Çarşamba",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Çarşamba"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5)
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                        ft.DragTarget(
                            data="Perşembe",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Perşembe"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5)
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                        ft.DragTarget(
                            data="Cuma",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Cuma"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5)
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                        ft.DragTarget(
                            data="Cumartesi",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Cumartesi"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5)
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                        ft.DragTarget(
                            data="Pazar",
                            content=ft.Container(
                                content=ft.Column([ft.Text("Pazar"), ft.Row([])]),
                                width=float("inf"),
                                bgcolor="#F2F6FA",
                                border_radius=5,
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5)
                            ),
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                            on_accept=drag_accept,
                        ),
                    ]
                )
            ]
        )

        def rals(e):
            e.control.data[1].content.content.controls[1].controls.remove(e.control.data[0])
            try: e.control.data[1].content.content.controls[1].update()
            except: pass
            self.cizelge_dict[e.control.data[1].data].remove(e.control.data[0].content.value)
            page.client_storage.set("cizelge_dict", self.cizelge_dict)

        for i in range(len(col.controls[1].controls)):
            for txt in self.cizelge_dict[col.controls[1].controls[i].data]:
                lsa = ft.Container(content=ft.Text(txt), bgcolor=self.section_colors[txt], border_radius=5, padding=ft.Padding(10, 10, 10, 10))
                lsa.data = [lsa, col.controls[1].controls[i]]
                lsa.on_click = rals
                col.controls[1].controls[i].content.content.controls[1].controls.append(lsa)

        return ft.Container(content=col, padding=ft.Padding(30, 30, 30, 20))

    def profil(self, page):
        self.get_current_time()

        def fix_color(e):
            pass
            # if e.pixels > 0: page.appbar.bgcolor = "white"
            # else:  page.appbar.bgcolor = "#EBF2F7"
            # try: page.update()
            # except: pass
        
        # PIE CHART
        completion_rates = self.section_colors.copy()
        for pn in list(self.parent_index.keys()):
            if type(completion_rates[self.parent_index[pn][0]]) in (int, float): completion_rates[self.parent_index[pn][0]] += len(self.parent_index_states[pn][0])
            else: completion_rates[self.parent_index[pn][0]] = len(self.parent_index_states[pn][0])

        normal_title_style = ft.TextStyle(size=16, color=ft.colors.BLACK, weight=ft.FontWeight.W_400)
        hover_title_style = ft.TextStyle(size=18, color=ft.colors.BLACK, weight=ft.FontWeight.W_400)

        def on_pie_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(pie_chart.sections):
                if idx == e.section_index:
                    section.radius = 110
                    section.title_style = hover_title_style
                else:
                    section.radius = 100
                    section.title_style = normal_title_style
            pie_chart.update()
        
        pie_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    max(0.1, completion_rates[sn]),
                    title="" if completion_rates[sn] < 0.1 and max(list(completion_rates.values())) > 0.1 else sn+" ("+str(completion_rates[sn])+")",
                    title_style=normal_title_style,
                    color=self.section_colors[sn],
                    radius=100,
                )
                for sn in list(completion_rates.keys())
            ],
            sections_space=3,
            center_space_radius=50,
            on_chart_event=on_pie_chart_event,
            width=float("inf"),
            height=page.height//3,
            scale=0.9
        )
        
        # BAR CHART
        last_weekdays_keys = {}
        for i in range(0, 8):
            od = self.current_time-timedelta(days=i)
            last_weekdays_keys.update({od.strftime("%d-%m-%Y"): self.days_en2tr[od.strftime("%A")]})

        last_week_completions = dict((v, 0) for k, v in list(last_weekdays_keys.items()))
        for dy in list(last_weekdays_keys.keys()):
            for pn in list(self.parent_index_states.keys()):
                if dy in list(last_weekdays_keys.keys()):
                    last_week_completions[last_weekdays_keys[dy]] += self.parent_index_states[pn][1]["successes"].count(dy)
        last_week_completions = {k: last_week_completions[k] for k in sorted(last_week_completions, key=lambda x: list(last_week_completions.keys()).index(x), reverse=True)}

        maxval = max(list(last_week_completions.values()))
        barcount = len(list(last_week_completions.values()))

        def on_bar_chart_event(e: ft.PieChartEvent):
            for group_index, group in enumerate(bar_chart.bar_groups):
                for rod_index, rod in enumerate(group.bar_rods):
                    rod.hovered = e.group_index == group_index and e.rod_index == rod_index
            bar_chart.update()

        bar_chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    group_vertically=True,
                    x=list(last_week_completions.keys()).index(dyn),
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=dyv,
                            width=page.width//2//barcount,
                            tooltip=dyn+" ("+str(dyv)+")",
                            border_radius=5,
                            color="blue"
                        )
                    ]
                )
                for dyn, dyv in list(last_week_completions.items())
            ],
            left_axis=ft.ChartAxis(labels_size=30, title=ft.Text(""), title_size=0),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=list(last_week_completions.keys()).index(dyn), 
                        label=ft.Container(ft.Text(dyn[:3]), padding=10), 
                    )
                    for dyn, dyv in list(last_week_completions.items())
                ],
                labels_size=40
            ),
            bgcolor="#F2F6FA",
            width=float("inf"),
            tooltip_bgcolor="white",
            height=page.height//3,
            on_chart_event=on_bar_chart_event,
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_300, width=2, dash_pattern=[3, 3]),
            max_y=maxval+5
        )

        col = ft.Column([
            pie_chart,
            ft.Container(bar_chart, margin=ft.Margin(0, 25, 0, 0), padding=ft.Padding(20, 30, 40, 10), expand=True, width=float("inf"), border=ft.border.all(2, "white"), bgcolor="#F2F6FA", border_radius=5)
        ], expand=True, alignment=ft.alignment.top_center)
        
        return ft.Container(col, padding=ft.Padding(30, 30, 30, 30), expand=True, width=float("inf"))

    def report(self, page):
        self.page_name = ft.Text(value="Bildir", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/ogren")), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        messageBox = ft.TextField(multiline=True)

        self.files = []
        def set_files(e): 
            if type(e.files) == list: 
                self.files = [f.path for f in e.files]
                file_count.value = str(len(self.files))+" dosya seçildi."
                try: file_count.update()
                except: pass
        file_picker = ft.FilePicker(on_result=set_files)
        page.overlay.append(file_picker)

        file_count = ft.Text(value="0 dosya seçildi.", theme_style=ft.TextThemeStyle.BODY_SMALL)

        send_btn = ft.ElevatedButton(text="Gönder", width=float("inf"), height=50, style=ft.ButtonStyle(color="black", bgcolor="blue", side=ft.BorderSide(width=2, color="white")))

        def send_report(e):
            if len(messageBox.value.replace(" ","")) <= 0: return None

            self.bottom_progress.open = True
            send_btn.disabled = True
            try: page.update()
            except: pass

            uname = p.uname()
            try: post("https://discord.com/api/webhooks/1189629751049076839/-BKOEs062km24QsJtpKC90igMg7B8eB8OTKP64Frwmwc6DnKeInQTYQATYaQbaRoca1q",  data={"content": messageBox.value + f" ({str(list({uname._fields[i]: uname.__getattribute__(uname._fields[i]) for i in range(len(uname._fields))}.items()))})"}, verify=False)
            except: pass
            for i in range(len(self.files)):
                try: post("https://discord.com/api/webhooks/1189629751049076839/-BKOEs062km24QsJtpKC90igMg7B8eB8OTKP64Frwmwc6DnKeInQTYQATYaQbaRoca1q", files={"fieldname": ("".join([str(randint(0, 100)) for n in range(5)])+path.splitext(self.files[i])[1], open(self.files[i], "rb").read())}, verify=False)
                except: pass

            self.files = []
            messageBox.value = ""

            self.bottom_progress.open = False
            try: page.update()
            except: pass

            def close_bs(e):
                self.bottom_progress.open = False
                try: self.bottom_progress.update()
                except: pass

            self.bottom_progress = ft.BottomSheet(
                ft.Container(
                    ft.Row([
                        ft.Text("Mesajınız iletildi."),
                        ft.TextButton("Tamam", on_click=close_bs),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    width=float("inf"),
                    padding=ft.Padding(30, 30, 30, 30),
                ),
                open=True,
            )
            page.overlay.append(self.bottom_progress)
            send_btn.disabled = False
            try: page.update()
            except: pass

        send_btn.on_click = send_report

        col = ft.Column(
            controls=[
                ft.Text(value="Mesaj"),
                messageBox,
                ft.Text(value=""),
                ft.Text(value="Dosya Seç (Opsiyonel)"),
                ft.ElevatedButton("Seçim Yap", height=40, width=float("inf"), on_click=lambda x: file_picker.pick_files(allow_multiple=True), style=ft.ButtonStyle(bgcolor="white", side=ft.BorderSide(width=2, color="white"))),
                file_count,
                ft.Text(value="", expand=True),
                send_btn
            ],
        )

        return ft.Container(content=col, padding=ft.Padding(30, 30, 30, 30))

    def level_index(self, page, index):
        ikey = list(self.parent_index.keys())[list(self.coded_parent_index.keys()).index(index)]
        self.page_name = ft.Text(value=ikey, color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/ogren")), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        self.current_index = index
        index = self.coded_parent_index[index][1]

        def fix_color(e):
            pass
            # if e.pixels > 0: page.appbar.bgcolor = "white"
            # else:  page.appbar.bgcolor = "#EBF2F7"
            # try: page.update()
            # except: pass

        def goto(e):
            if e.control.data[0]: page.go(e.control.data[1])

        items = [ft.ElevatedButton(content=ft.Row([ft.Icon(ft.icons.LOCK), ft.Text(a)], alignment=ft.MainAxisAlignment.CENTER), height=40, on_click=goto, data=[False, b], width=float("inf"), style=ft.ButtonStyle(bgcolor="white", side=ft.BorderSide(width=2, color="white"))) for a, b in list(index.items())]
        for u in range(len(self.parent_index_states[ikey][0])+1):
            if u  < len(items):
                del items[u].content.controls[0]
                items[u].data[0] = True
        col = ft.Column(items, on_scroll=fix_color, scroll=ft.ScrollMode.ALWAYS, expand=True, alignment=ft.alignment.top_center)

        return ft.Container(col, padding=ft.Padding(30, 30, 30, 40), width=float("inf"), height=page.height)

    def learn_letter(self, page, letter, event=None):
        self.page_name = ft.Text(value=letter.upper()+" Harfi", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)
        
        def toggle_letter_recording(e=None, c=None):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            if e != None: cntrl = e.control
            else: cntrl = c

            if cntrl.style.bgcolor == "blue":
                cntrl.style = ft.ButtonStyle(bgcolor="red")
                cntrl.icon = ft.icons.SQUARE
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.start_recording_audio.play()
                    except: pass

                self.activation_time = st()
            else: 
                cntrl.style = ft.ButtonStyle(bgcolor="blue")
                cntrl.icon = ft.icons.MIC
                cntrl.disabled = True
                self.bottom_progress.open = True
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.stop_recording_audio.play()
                    except: pass

                if st()-self.activation_time > 1:
                    req = post("https://audio-recognition-api.onrender.com/letter")
            
                    try: o = str(req.json())
                    except: o = ""

                    if "true" in str(o).lower(): self.act_success(page)
                    else: self.act_fail(page)
                        
                cntrl.disabled = False
                self.bottom_progress.open = False
                try: page.update()
                except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)

        def play_on_end(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed":
                sleep(0.4)
                try: 
                    if self.is_level_on(page): self.audio_object1.play()
                except: pass

        self.audio_object0 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/benimle-soyle.mp3?raw=true", autoplay=True)
        self.audio_object0.on_state_changed = play_on_end
        page.overlay.append(self.audio_object0)

        self.audio_object1 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/letters/{letter.lower()}.mp3?raw=true")
        page.overlay.append(self.audio_object1)

        def play_again(e): 
            try: self.audio_object1.update()
            except: pass
            try: 
                if self.is_level_on(page): self.audio_object1.play()
            except: pass
            try: self.audio_object1.update()
            except: pass

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        record_btn = ft.IconButton(icon=ft.icons.MIC, icon_size=32, scale=1.5, on_click=toggle_letter_recording, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Container(ft.Text(letter.upper()+letter.lower(), theme_style=ft.TextThemeStyle.DISPLAY_LARGE), border_radius=5, width=float("inf"), alignment=ft.alignment.top_center),
                ft.Row([replay_btn, record_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def clicked(e): self.last_click_position = (e.global_x, e.global_y)
        fake_gesture = ft.GestureDetector(on_tap_down=clicked)

        return ft.Container(ft.Stack([fake_gesture, col]), width=float("inf"), expand=True, padding=ft.Padding(30, 30, 30, 30))
    
    def draw_letter(self, page, letter, event=None):
        self.page_name = ft.Text(value=letter.upper()+" Harfi Çiz", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        self.audio_object = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/letters/draw/{letter.lower()}.mp3?raw=true", autoplay=True)
        page.overlay.append(self.audio_object)

        self.coords = []
        self.old_touch = (None, None)

        def pan_start(e: ft.DragStartEvent):
            self.coords.append([])
            self.old_touch = (e.local_x, e.local_y)

        def pan_update(e: ft.DragUpdateEvent):
            canvas.shapes.append(
                ft.canvas.Line(
                    self.old_touch[0], self.old_touch[1], e.local_x, e.local_y, paint=ft.Paint(stroke_width=4)
                )
            )
            canvas.shapes = canvas.shapes[-175:]
            try: canvas.update()
            except: pass
            if len(self.coords) <= 0: self.coords.append([])
            self.coords[-1].append([e.local_x, e.local_y])
            self.old_touch = (e.local_x, e.local_y)

        canvas = ft.canvas.Canvas(
            content=ft.GestureDetector(
                on_pan_start=pan_start,
                on_pan_update=pan_update,
                drag_interval=25,
            ),
            expand=False,
        )

        def check_letter(e):
            cntrl = e.control
            cntrl.disabled = True
            self.bottom_progress.open = True
            try: page.update()
            except: pass
            
            req = post("https://letter-recognition-api.onrender.com/letter", json={"coords": self.coords, "answer": letter.upper()})
            canvas.shapes = []
            try: canvas.update()
            except: pass
            self.coords = []
            
            try: o = str(req.json())
            except: o = ""

            if "true" in str(o).lower(): self.act_success(page)
            else: self.act_fail(page)
                
            cntrl.disabled = False
            self.bottom_progress.open = False
            try: page.update()
            except: pass

        def clear_canvas(e): 
            canvas.shapes = []
            try: canvas.update()
            except: pass

        clear_btn = ft.IconButton(icon=ft.icons.CLEANING_SERVICES, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")),icon_size=32, scale=1.5, on_click=clear_canvas)
        check_btn = ft.IconButton(icon=ft.icons.CHECK, icon_size=32, scale=1.5, on_click=check_letter, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Container(ft.Text(letter.upper(), theme_style=ft.TextThemeStyle.DISPLAY_LARGE), border_radius=5, width=float("inf"), alignment=ft.alignment.top_center),
                ft.Text(""),
                ft.Container(canvas, border_radius=5, width=float("inf"), expand=True, bgcolor="white", border=ft.border.all(1, "black")),
                ft.Text(""),
                ft.Row([clear_btn, check_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            #alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def clicked(e): self.last_click_position = (e.global_x, e.global_y)
        fake_gesture = ft.GestureDetector(on_tap_down=clicked)

        return ft.Container(ft.Stack([fake_gesture, col]), width=float("inf"), expand=True, padding=ft.Padding(30, 30, 30, 60))
  
    def letter_sequence(self, page, letters, event=None):
        letters = letters.replace("i","_").upper().replace("_", "İ")

        self.page_name = ft.Text(value="-".join(list(letters.upper()))+" Harfleri", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        def toggle_letter_recording(e=None, c=None):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            if e != None: cntrl = e.control
            else: cntrl = c

            if cntrl.style.bgcolor == "blue":
                cntrl.style = ft.ButtonStyle(bgcolor="red")
                cntrl.icon = ft.icons.SQUARE
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.start_recording_audio.play()
                    except: pass

                self.activation_time = st()
            else: 
                cntrl.style = ft.ButtonStyle(bgcolor="blue")
                cntrl.icon = ft.icons.MIC
                cntrl.disabled = True
                self.bottom_progress.open = True
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.stop_recording_audio.play()
                    except: pass

                if st()-self.activation_time > 1:
                    req = post("https://audio-recognition-api.onrender.com/letter-sequence")
            
                    try: o = str(req.json())
                    except: o = ""

                    if "true" in str(o).lower(): self.act_success(page)
                    else: self.act_fail(page)
                        
                cntrl.disabled = False
                self.bottom_progress.open = False
                try: page.update()
                except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)

            try: cntrl.update()
            except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)
                
        def play_queue(e):
            if e.data == "completed":
                sleep(0.2) 
                for x in self.audio_objects: 
                    if x.get_current_position() != 0: return None
                ind = self.audio_objects.index(e.control)
                if ind < len(self.audio_objects)-1: 
                    try: 
                        if self.is_level_on(page): self.audio_objects[ind+1].play()
                    except: pass

        def play_on_end(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed":
                sleep(0.4) 
                try: 
                    if self.is_level_on(page): self.audio_objects[0].play()
                except: pass

        self.audio_object0 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/harfleri-sirayla-seslendir.mp3?raw=true", autoplay=True)
        self.audio_object0.on_state_changed = play_on_end
        page.overlay.append(self.audio_object0)

        self.audio_objects = [ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/letters/{letter.lower()}.mp3?raw=true", on_state_changed=play_queue) for letter in letters]
        for self.audio_object in self.audio_objects: page.overlay.append(self.audio_object)

        def play_again(e):
            try: 
                if self.is_level_on(page): self.audio_objects[0].play()
            except: pass

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        record_btn = ft.IconButton(icon=ft.icons.MIC, icon_size=32, scale=1.5, on_click=toggle_letter_recording, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Container(ft.Text("-".join(list(letters.upper())), theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM), border_radius=5, width=float("inf"), alignment=ft.alignment.top_center),
                ft.Row([replay_btn, record_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def clicked(e): self.last_click_position = (e.global_x, e.global_y)
        fake_gesture = ft.GestureDetector(on_tap_down=clicked)

        return ft.Container(ft.Stack([fake_gesture, col]), width=float("inf"), expand=True, padding=ft.Padding(30, 30, 30, 30))
    
    def learn_shape_2d(self, page, shape_2d, event=None):
        self.page_name = ft.Text(value=shape_2d.capitalize()+" Şekli", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        def toggle_shape_2d_recording(e=None, c=None):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            if e != None: cntrl = e.control
            else: cntrl = c

            if cntrl.style.bgcolor == "blue":
                cntrl.style = ft.ButtonStyle(bgcolor="red")
                cntrl.icon = ft.icons.SQUARE
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.start_recording_audio.play()
                    except: pass

                self.activation_time = st()
            else: 
                cntrl.style = ft.ButtonStyle(bgcolor="blue")
                cntrl.icon = ft.icons.MIC
                cntrl.disabled = True
                self.bottom_progress.open = True
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.stop_recording_audio.play()
                    except: pass

                if st()-self.activation_time > 1:
                    req = post("https://audio-recognition-api.onrender.com/shape")
            
                    try: o = str(req.json())
                    except: o = ""

                    if "true" in str(o).lower(): self.act_success(page)
                    else: self.act_fail(page)
                        
                cntrl.disabled = False
                self.bottom_progress.open = False
                try: page.update()
                except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)

        def play_on_end1(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed": 
                sleep(0.4) 
                try: 
                    if self.is_level_on(page): self.audio_object1.play()
                except: pass

        def play_on_end2(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed": 
                sleep(0.4) 
                try: 
                    if self.is_level_on(page): self.audio_object2.play()
                except: pass

        self.audio_object0 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/2d-shapes/info/{shape_2d.lower()}.mp3?raw=true", autoplay=True)
        self.audio_object0.on_state_changed = play_on_end1
        page.overlay.append(self.audio_object0)

        self.audio_object1 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/benimle-soyle.mp3?raw=true")
        self.audio_object1.on_state_changed = play_on_end2
        page.overlay.append(self.audio_object1)

        self.audio_object2 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/2d-shapes/{shape_2d.lower()}.mp3?raw=true")
        page.overlay.append(self.audio_object2)

        webview_ring = ft.Container(ft.Row([ft.ProgressRing()], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER), padding=ft.padding.only(top=50))
        def hide_ring(e):
            pass
            # webview_ring.visible = False
            # try: webview_ring.update()
            # except: pass

        webview = ft.Container(
            ft.WebView(
                url=f"https://ayberkatalay0.github.io/shapes/{shape_2d.lower()}",
                width=float("inf"),
                expand=True,
                on_page_started=hide_ring,
                bgcolor="#EBF2F7",
            ), 
            border_radius=5, 
            width=float("inf"), 
            height=page.height//2.5,
        )

        def play_again(e): 
            try: 
                if self.is_level_on(page): self.audio_object2.play()
            except: pass

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        record_btn = ft.IconButton(icon=ft.icons.MIC, icon_size=32, scale=1.5, on_click=toggle_shape_2d_recording, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Stack([
                    webview_ring,
                    webview,
                ]),
                ft.Row([replay_btn, record_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def clicked(e): self.last_click_position = (e.global_x, e.global_y)
        fake_gesture = ft.GestureDetector(on_tap_down=clicked)

        return ft.Container(ft.Stack([fake_gesture, col]), width=float("inf"), expand=True, padding=ft.Padding(30, 30, 30, 30))
    
    def draw_shape_2d(self, page, shape_2d, event=None):
        self.page_name = ft.Text(value=shape_2d.capitalize()+" Çiz", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        self.audio_object = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/2d-shapes/draw/{shape_2d.lower()}.mp3?raw=true", autoplay=True)
        page.overlay.append(self.audio_object)

        self.coords = []
        self.old_touch = (None, None)

        def pan_start(e: ft.DragStartEvent):
            self.coords.append([])
            self.old_touch = (e.local_x, e.local_y)

        def pan_update(e: ft.DragUpdateEvent):
            canvas.shapes.append(
                ft.canvas.Line(
                    self.old_touch[0], self.old_touch[1], e.local_x, e.local_y, paint=ft.Paint(stroke_width=4)
                )
            )
            canvas.shapes = canvas.shapes[-175:]
            try: canvas.update()
            except: pass
            if len(self.coords) <= 0: self.coords.append([])
            self.coords[-1].append([e.local_x, e.local_y])
            self.old_touch = (e.local_x, e.local_y)
        
        canvas = ft.canvas.Canvas(
            content=ft.GestureDetector(
                on_pan_start=pan_start,
                on_pan_update=pan_update,
                drag_interval=25,
            ),
            expand=False,
        )

        def check_shape_2d(e):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            cntrl = e.control
            cntrl.disabled = True
            self.bottom_progress.open = True
            try: page.update()
            except: pass

            if self.is_level_on(page):
                try: self.stop_recording_audio.play()
                except: pass

            req = post("https://shape-recognition-api.onrender.com/shape", json={"coords": self.coords})
            canvas.shapes = []
            try: canvas.update()
            except: pass
            self.coords = []
            try: o = float(req.json())
            except: o = -1

            daire = ["daire"]
            dortgen = ["kare", "dikdörtgen"]
            ucgen = ["üçgen"]
            
            if o == float("inf"): sh = daire
            elif o != float("inf") and float(o) >= 4 and not shape_2d.lower() in ucgen: sh = dortgen
            elif o == 3 or (o == 4 and shape_2d.lower() in ucgen): sh = ucgen
            else: sh = []

            if shape_2d.lower() in sh: self.act_success(page)
            else: self.act_fail(page)
                    
            cntrl.disabled = False
            self.bottom_progress.open = False
            try: page.update()
            except: pass
        
        webview_ring = ft.Container(ft.Row([ft.ProgressRing()], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER), padding=ft.padding.only(top=50))
        def hide_ring(e):
            pass
            # webview_ring.visible = False
            # try: webview_ring.update()
            # except: pass

        webview = ft.Container(
            ft.WebView(
                url=f"https://ayberkatalay0.github.io/shapes/{shape_2d.lower()}",
                width=float("inf"),
                expand=True,
                on_page_started=hide_ring,
                bgcolor="#EBF2F7",
            ), 
            border_radius=5, 
            width=float("inf"), 
            height=page.height//4,
        )

        def clear_canvas(e): 
            canvas.shapes = []
            try: canvas.update()
            except: pass

        clear_btn = ft.IconButton(icon=ft.icons.CLEANING_SERVICES, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")),icon_size=32, scale=1.5, on_click=clear_canvas)
        check_btn = ft.IconButton(icon=ft.icons.CHECK, icon_size=32, scale=1.5, on_click=check_shape_2d, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Stack([
                    webview_ring,
                    webview,
                ]),
                ft.Container(canvas, border_radius=5, width=float("inf"), expand=True, bgcolor="white", border=ft.border.all(1, "black")),
                ft.Text(""),
                ft.Row([clear_btn, check_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
        )

        return ft.Container(col, width=float("inf"), expand=True, padding=ft.Padding(30, 15, 30, 60))

    def learn_shape_3d(self, page, shape_3d, event=None):
        self.page_name = ft.Text(value=shape_3d.capitalize()+" Şekli", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        def toggle_shape_3d_recording(e=None, c=None):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            if e != None: cntrl = e.control
            else: cntrl = c

            if cntrl.style.bgcolor == "blue":
                cntrl.style = ft.ButtonStyle(bgcolor="red")
                cntrl.icon = ft.icons.SQUARE
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.start_recording_audio.play()
                    except: pass

                self.activation_time = st()
            else: 
                cntrl.style = ft.ButtonStyle(bgcolor="blue")
                cntrl.icon = ft.icons.MIC
                cntrl.disabled = True
                self.bottom_progress.open = True
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.stop_recording_audio.play()
                    except: pass

                if st()-self.activation_time > 1:
                    req = post("https://audio-recognition-api.onrender.com/shape")
            
                    try: o = str(req.json())
                    except: o = ""

                    if "true" in str(o).lower(): self.act_success(page)
                    else: self.act_fail(page)
                        
                cntrl.disabled = False
                self.bottom_progress.open = False
                try: page.update()
                except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)

            try: cntrl.update()
            except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)

        def play_on_end1(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed": 
                sleep(0.4) 
                try: 
                    if self.is_level_on(page): self.audio_object1.play()
                except: pass

        def play_on_end2(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed": 
                sleep(0.4) 
                try: 
                    if self.is_level_on(page): self.audio_object2.play()
                except: pass

        self.audio_object0 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/3d-shapes/info/{shape_3d.lower()}.mp3?raw=true", autoplay=True)
        self.audio_object0.on_state_changed = play_on_end1
        page.overlay.append(self.audio_object0)

        self.audio_object1 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/benimle-soyle.mp3?raw=true")
        self.audio_object1.on_state_changed = play_on_end2
        page.overlay.append(self.audio_object1)

        self.audio_object2 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/3d-shapes/{shape_3d.lower()}.mp3?raw=true")
        page.overlay.append(self.audio_object2)

        webview_ring = ft.Container(ft.Row([ft.ProgressRing()], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER), padding=ft.padding.only(top=50))
        def hide_ring(e):
            pass
            # webview_ring.visible = False
            # try: webview_ring.update()
            # except: pass

        webview = ft.Container(
            ft.WebView(
                url=f"https://ayberkatalay0.github.io/shapes/{shape_3d.lower()}",
                width=float("inf"),
                expand=True,
                on_page_started=hide_ring,
                bgcolor="#EBF2F7",
            ), 
            border_radius=5, 
            width=float("inf"), 
            height=page.height//2.5,
        )

        def play_again(e): 
            try: 
                if self.is_level_on(page): self.audio_object2.play()
            except: pass

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        record_btn = ft.IconButton(icon=ft.icons.MIC, icon_size=32, scale=1.5, on_click=toggle_shape_3d_recording, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Stack([
                    webview_ring,
                    webview,
                ]),
                ft.Row([replay_btn, record_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def clicked(e): self.last_click_position = (e.global_x, e.global_y)
        fake_gesture = ft.GestureDetector(on_tap_down=clicked)

        return ft.Container(ft.Stack([fake_gesture, col]), width=float("inf"), expand=True, padding=ft.Padding(30, 0, 30, 30))

    def learn_number(self, page, number, event=None):
        self.page_name = ft.Text(value=number.upper()+" Sayısı", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)
        
        def toggle_number_recording(e=None, c=None):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            if e != None: cntrl = e.control
            else: cntrl = c

            if cntrl.style.bgcolor == "blue":
                cntrl.style = ft.ButtonStyle(bgcolor="red")
                cntrl.icon = ft.icons.SQUARE
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.start_recording_audio.play()
                    except: pass

                self.activation_time = st()
            else: 
                cntrl.style = ft.ButtonStyle(bgcolor="blue")
                cntrl.icon = ft.icons.MIC
                cntrl.disabled = True
                self.bottom_progress.open = True
                try: page.update()
                except: pass

                if self.is_level_on(page):
                    try: self.stop_recording_audio.play()
                    except: pass

                if st()-self.activation_time > 1:
                    req = post("https://audio-recognition-api.onrender.com/number")
            
                    try: o = str(req.json())
                    except: o = ""

                    if "true" in str(o).lower(): self.act_success(page)
                    else: self.act_fail(page)
                        
                cntrl.disabled = False
                self.bottom_progress.open = False
                try: page.update()
                except: pass

            while 1:
                if cntrl.style.bgcolor == "red": 
                    cntrl.scale = 1.6 if cntrl.scale != 1.6 else 1.5
                else: cntrl.scale = 1.5

                try: cntrl.update()
                except: pass
                sleep(1)

        def play_on_end(e):
            if record_btn.style.bgcolor == "red": 
                try: e.control.pause()
                except: pass
                return None
            if e.data == "completed":
                sleep(0.4) 
                try: 
                    if self.is_level_on(page): self.audio_object2.play()
                except: pass

        self.audio_object1 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/benimle-soyle.mp3?raw=true", autoplay=True)
        self.audio_object1.on_state_changed = play_on_end
        page.overlay.append(self.audio_object1)

        self.audio_object2 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/numbers/{number.lower()}.mp3?raw=true")
        page.overlay.append(self.audio_object2)

        def play_again(e):
            try: 
                if self.is_level_on(page): self.audio_object2.play()
            except: pass

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        record_btn = ft.IconButton(icon=ft.icons.MIC, icon_size=32, scale=1.5, on_click=toggle_number_recording, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))

        apple_grid = ft.GridView(
            expand=False,
            runs_count=5,
            max_extent=75,
            spacing=5,
            run_spacing=5,
            controls=[ft.Image(src="apple.png" if i < float(number) else "blank-apple.png", fit=ft.ImageFit.FIT_WIDTH) for i in range(20)]
        )

        col = ft.Column(
            controls=[
                ft.Column([
                    ft.Container(ft.Text(number.upper(), theme_style=ft.TextThemeStyle.DISPLAY_LARGE), border_radius=5, width=float("inf"), alignment=ft.alignment.top_center),
                    apple_grid,
                ], alignment=ft.alignment.top_center),
                ft.Row([replay_btn, record_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def clicked(e): self.last_click_position = (e.global_x, e.global_y)
        fake_gesture = ft.GestureDetector(on_tap_down=clicked)

        return ft.Container(ft.Stack([fake_gesture, col]), width=float("inf"), expand=True, padding=ft.Padding(30, 20, 30, 30))

    def learn_symbol(self, page, symbol, event=None):
        name2symbol = {"eksi": "-", "artı": "+", "eşittir": "="}
        name2operation = {"eksi": "Çıkarma", "artı": "Toplama", "eşittir": "Eşitlik"}
        name2example = {"eksi": ("7", "-", "4", "=", "3"), "artı": ("2", "+", "3", "=", "5"), "eşittir": ("5", "=", "5")}

        self.page_name = ft.Text(value=f"{name2operation[symbol.lower()]} Sembolü", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        self.audio_listening_completed = False
        def play_on_end(e):
            if e.data == "completed":
                sleep(0.2) 
                self.audio_listening_completed = True

        self.audio_object = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/symbols/{name2symbol[symbol.lower()]}.mp3?raw=true", autoplay=True)
        self.audio_object.on_state_changed = play_on_end
        page.overlay.append(self.audio_object)

        def play_again(e):
            try: 
                if self.is_level_on(page): self.audio_object.play()
            except: pass

        def check_symbol(e):
            if self.audio_listening_completed: self.act_success(page)
            else: self.act_fail(page)

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        check_btn = ft.IconButton(icon=ft.icons.CHECK, icon_size=32, scale=1.5, on_click=check_symbol, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white"), animation_duration=200))

        col = ft.Column(
            controls=[
                ft.Container(ft.Text(f"{symbol.capitalize()} ({name2symbol[symbol.lower()]})", theme_style=ft.TextThemeStyle.DISPLAY_SMALL), border_radius=5, width=float("inf"), alignment=ft.alignment.top_center),
                ft.Column([ft.Container(ft.Text(" ".join(name2example[symbol.lower()]), theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM), width=float("inf"), alignment=ft.alignment.top_center, bgcolor="#F2F6FA", padding=ft.Padding(15, 15, 15, 15), border_radius=5, border=ft.border.all(2, "white")),
                ft.Container(
                    ft.Column([
                        ft.GridView(
                            expand=False,
                            runs_count=5,
                            max_extent=50,
                            run_spacing=1,
                            controls=[ft.Image(src="apple.png", fit=ft.ImageFit.FIT_WIDTH) for i in range(int(float(a)))]
                        )
                        if str(a).isnumeric() else
                        ft.Container(ft.Text(a, theme_style=ft.TextThemeStyle.DISPLAY_SMALL), width=float("inf"), alignment=ft.alignment.top_center)
                        
                        for a in name2example[symbol.lower()]
                    ], 
                    alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor="#F2F6FA", padding=ft.Padding(15, 15, 15, 15), border_radius=5, border=ft.border.all(2, "white")),
                ]),
                ft.Row([replay_btn, check_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        return ft.Container(col, width=float("inf"), expand=True, padding=ft.Padding(30, 20, 30, 30))

    def math_operation(self, page, operation, event=None):
        self.page_name = ft.Text(value=f"{operation} İşlemi", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/level_index_"+self.current_index)), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)
        answer = eval(operation)

        oplist = []
        oplist += [operation.split("+")[0]] if "+" in operation else [operation.split("-")[0]]
        oplist += ["+"] if "+" in operation else ["-"]
        oplist += [operation.split("+")[1]] if "+" in operation else [operation.split("-")[1]]
        oplist += ["="]
        oplist += [str(answer)]

        def play_on_end(e):
            if e.data == "completed":
                sleep(0.4)
                try: 
                    if self.is_level_on(page): self.audio_object1.play()
                except: pass

        self.audio_object0 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/math-operations/{operation}.mp3?raw=true", autoplay=True)
        self.audio_object0.on_state_changed = play_on_end
        page.overlay.append(self.audio_object0)

        self.audio_object1 = ft.Audio(volume=0, release_mode=ft.audio.ReleaseMode.STOP, src=f"https://github.com/durugezekli/project-down_up/blob/audio-assets/gorsel-olarak-ifade-et.mp3?raw=true")
        page.overlay.append(self.audio_object1)

        self.current_op = ["0", "+", "0", "=", "0"]
        self.result_label = ft.Container(get_rich_text(" ".join(self.current_op), size=40), width=float("inf"), alignment=ft.alignment.top_center)

        def drag_will_accept(e):
            if e.control.group == page.get_control(e.target).group:
                e.control.content.border = ft.border.all(3, "blue")
                try: e.control.update()
                except: pass

        def drag_accept(e):
            src = page.get_control(e.src_id)

            if e.control.group == "Elma":
                apwidth, apheight = e.control.content.width//3, e.control.content.width//3
                tot = (e.control.content.width*e.control.content.height)//(apwidth*apheight)

                if len(e.control.content.content.controls) < tot:
                    vc = e.control.content.height//apheight
                    hc = tot//vc
                    e.control.content.content.max_extent = e.control.content.width//hc

                    ap = ft.Container(ft.Image("apple.png", fit=ft.ImageFit.FIT_WIDTH), width=apwidth-5, height=apheight-5, border_radius=5)
                    e.control.content.content.controls += [ap]

                self.current_op[e.control.content.data] = str(len(e.control.content.content.controls))
                self.current_op[-1] = str(eval("".join(self.current_op[:3])))
                self.result_label.content = get_rich_text(" ".join(self.current_op), size=40)
                try: self.result_label.update()
                except: pass
            elif e.control.group == "İşaret":
                e.control.content.content.name = src.content.content.name
                e.control.content.bgcolor = src.content.bgcolor

                self.current_op[1] = "+" if src.content.content.name == "add" else "-"
                self.current_op[-1] = str(eval("".join(self.current_op[:3])))
                self.result_label.content = get_rich_text(" ".join(self.current_op), size=40)
                try: self.result_label.update()
                except: pass

            e.control.content.border = ft.border.all(2, "white")
            try: e.control.update()
            except: pass

        def drag_leave(e):
            e.control.content.border = ft.border.all(2, "white")
            try: e.control.update()
            except: pass

        def clean_isaret_target(e):
            e.control.content.name = None
            e.control.bgcolor = "#F2F6FA"
            try: e.control.update()
            except: pass

        def clean_elma_target(e):
            e.control.content.controls = e.control.content.controls[:-1]
            try: e.control.update()
            except: pass

            self.current_op[e.control.data] = str(len(e.control.content.controls))
            self.current_op[-1] = str(eval("".join(self.current_op[:3])))
            self.result_label.content = get_rich_text(" ".join(self.current_op), size=40)
            try: self.result_label.update()
            except: pass

        def check_operation(e):
            if self.current_op in (oplist, oplist[:3][::-1]+["=", str(answer)]): self.act_success(page)
            else: self.act_fail(page)

        def play_again(e):
            try: 
                if self.is_level_on(page): self.audio_object0.play()
            except: pass

        replay_btn = ft.IconButton(icon=ft.icons.REPLAY, style=ft.ButtonStyle(bgcolor="#F2F6FA", color="#0061A4", side=ft.BorderSide(width=2, color="white")), icon_size=32, scale=1.5, on_click=play_again)
        check_btn = ft.IconButton(icon=ft.icons.CHECK, icon_size=32, scale=1.5, on_click=check_operation, animate_opacity=750, animate_scale=750, style=ft.ButtonStyle(bgcolor="blue", color="black", animation_duration=200))
        
        col = ft.Column(
            controls=[
                ft.Column([
                    ft.Container(ft.Text(" ".join(oplist), theme_style=ft.TextThemeStyle.DISPLAY_SMALL), border_radius=5, width=float("inf"), alignment=ft.alignment.top_center),
                    ft.Text(""),
                    ft.Row([
                        ft.Draggable(group="Elma", content=ft.Container(ft.Image("apple.png", fit=ft.ImageFit.FIT_WIDTH), width=75, height=75, bgcolor="#71BFFF", padding=ft.Padding(10, 10, 10, 10), border_radius=5)), 
                        ft.Draggable(group="İşaret", content=ft.Container(ft.Icon(ft.icons.ADD), width=75, height=75, bgcolor="#FFADCF", padding=ft.Padding(10, 10, 10, 10), border_radius=page.width)), 
                        ft.Draggable(group="İşaret", content=ft.Container(ft.Icon(ft.icons.REMOVE), width=75, height=75, bgcolor="#FFADCF", padding=ft.Padding(10, 10, 10, 10), border_radius=page.width)),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Text(""),
                    ft.Row([
                        ft.DragTarget(
                            group="Elma",
                            content=ft.Container(
                                data=0,
                                content=ft.GridView(expand=1, runs_count=5, max_extent=40, child_aspect_ratio=1.0, spacing=5, run_spacing=5),
                                bgcolor="#F2F6FA",
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5),
                                width=page.width//4,
                                height=page.width//3,
                                border_radius=5,
                                on_click=clean_elma_target
                            ),
                            on_accept=drag_accept,
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                        ),
                        ft.DragTarget(
                            group="İşaret",
                            content=ft.Container(
                                content=ft.Icon(),
                                bgcolor="#F2F6FA",
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5),
                                width=75,
                                height=75,
                                border_radius=page.width,
                                on_click=clean_isaret_target
                            ),
                            on_accept=drag_accept,
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                        ),
                        ft.DragTarget(
                            group="Elma",
                            content=ft.Container(
                                data=2,
                                content=ft.GridView(expand=1, runs_count=5, max_extent=40, child_aspect_ratio=1.0, spacing=5, run_spacing=5),
                                bgcolor="#F2F6FA",
                                border=ft.border.all(2, "white"),
                                padding=ft.Padding(5, 5, 5, 5),
                                width=page.width//4,
                                height=page.width//3,
                                border_radius=5,
                                on_click=clean_elma_target
                            ),
                            on_accept=drag_accept,
                            on_will_accept=drag_will_accept,
                            on_leave=drag_leave,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Text(""),
                    self.result_label
                ]),
                ft.Row([replay_btn, check_btn], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        return ft.Container(col, width=float("inf"), expand=True, padding=ft.Padding(30, 0, 30, 30))

    def androidtest(self, page):
        self.page_name = ft.Text(value=f"Android Test", color="#151519", text_align=ft.TextAlign.LEFT, size=20)
        self.page_icon = ft.Container()
        page.appbar = ft.AppBar(leading=ft.Container(content=ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, icon_size=40, on_click=lambda x: page.go("/ogren")), padding=ft.Padding(4, 0, 0, 0)), title=self.page_name, center_title=True, actions=[self.page_icon], bgcolor="#EBF2F7", toolbar_height=70)

        # recorder1 = ft.AudioRecorder(src="aa")
        # page.overlay.append(recorder1)

        # def toggle_recording(event):
        #     if event.control.text == "Start recording":
        #         # recorder1.start()
        #         event.control.text = "Stop recording"
        #     else:
        #         # recorder1.stop()
        #         event.control.text = "Start recording"
        #     event.control.update()

        col = ft.Column([
            ft.Text("This is an app with audio recorder."),
            # ft.ElevatedButton("Start recording", on_click=toggle_recording),
            # ft.AnimatedButton(text="Abc"),
        ])

        return ft.Container(col, padding=ft.Padding(30, 30, 30, 30))

    def act_success(self, page):
        self.get_current_time()

        parent_name = list(self.parent_index.keys())[[page.route in list(r[1].values()) for r in list(self.parent_index.values())].index(True)]
        if not self.page_name.value in self.parent_index_states[parent_name][0]: self.parent_index_states[parent_name][0].append(self.page_name.value)
        self.parent_index_states[parent_name][1]["successes"].append(self.current_time.strftime("%d-%m-%Y"))
        page.client_storage.set("parent_index_states_dict", self.parent_index_states)
        
        page.dialog = self.success_modal
        self.success_modal.open = self.is_level_on(page)
        if self.is_level_on(page): 
            try: self.success_audio.play()
            except: pass

        try: page.update()
        except: pass

    def act_fail(self, page):
        page.dialog = self.fail_modal
        self.fail_modal.open = self.is_level_on(page)
        if self.is_level_on(page): 
            try: self.fail_audio.play()
            except: pass
        try: page.update()
        except: pass

    def get_current_time(self):
        self.current_time = datetime.now()
        self.day = self.days_en2tr[self.current_time.strftime("%A")]

    def main(self, page: ft.Page):
        self.haptic = ft.HapticFeedback()
        page.overlay.append(self.haptic)
        
        self.success_audio = ft.Audio(release_mode=ft.audio.ReleaseMode.STOP, src="https://github.com/durugezekli/project-down_up/blob/audio-assets/success.mp3?raw=true", volume=0.4)
        self.fail_audio = ft.Audio(release_mode=ft.audio.ReleaseMode.STOP, src="https://github.com/durugezekli/project-down_up/blob/audio-assets/fail.mp3?raw=true", volume=0.4)
        self.start_recording_audio = ft.Audio(release_mode=ft.audio.ReleaseMode.STOP, src="https://github.com/durugezekli/project-down_up/blob/audio-assets/start-recording.mp3?raw=true", volume=0.4)
        self.stop_recording_audio = ft.Audio(release_mode=ft.audio.ReleaseMode.STOP, src="https://github.com/durugezekli/project-down_up/blob/audio-assets/stop-recording.mp3?raw=true", volume=0.4)
        page.overlay.append(self.success_audio)
        page.overlay.append(self.fail_audio)
        page.overlay.append(self.start_recording_audio)
        page.overlay.append(self.stop_recording_audio)

        page.title = "Down Up"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.bgcolor = "#EBF2F7"
        page.padding = 0

        if "windows" in p.platform().lower():
            page.window_width = 460
            page.window_height = 900

        self.get_current_time()

        if page.client_storage.contains_key("parent_index_states_dict"):
            self.parent_index_states = page.client_storage.get("parent_index_states_dict")
        else:
            self.parent_index_states = {
                "Harfleri Öğren": [[], {"successes": []}], "Harfleri Çiz": [[], {"successes": []}], "Harfleri Oku": [[], {"successes": []}],
                "Şekilleri Öğren": [[], {"successes": []}], "Şekilleri Çiz": [[], {"successes": []}],
                "Sayıları Öğren": [[], {"successes": []}], "Sayı İşlemleri": [[], {"successes": []}],
            }

        self.container = ft.AnimatedSwitcher(
            None,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=350,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_OUT,
            expand=True
        )

        page_container = ft.AnimatedSwitcher(
            self.container,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=350,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_OUT,
            expand=True
        )
        page.add(page_container)

        self.success_modal = ft.AlertDialog(
            modal=True,
            content=ft.Container(ft.Image("success.gif")),
            actions=[
                ft.TextButton("Geri", on_click=self.go_to_prev_lesson, data=page),
                ft.TextButton("Tekrar", on_click=self.close_dialogs, data=page),
                ft.TextButton("İleri", on_click=self.go_to_next_lesson, data=page)
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            on_dismiss=self.close_dialogs,
            data=page,
        )

        self.fail_modal = ft.AlertDialog(
            modal=True,
            content=ft.Container(ft.Image("fail.gif")),
            actions=[
                ft.TextButton("Geri", on_click=self.go_to_prev_lesson, data=page),
                ft.TextButton("Tekrar", on_click=self.close_dialogs, data=page)
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            on_dismiss=self.close_dialogs,
            data=page,
        )

        self.bottom_progress = ft.BottomSheet(ft.Container(ft.Column([ft.ProgressRing()], tight=True), padding=10), dismissible=False)
        page.overlay.append(self.bottom_progress)

        def route_change(e: ft.RouteChangeEvent):
            for a in page.overlay:
                if type(a) == ft.Audio:
                    try: a.pause()
                    except: pass

            page.overlay.clear()
            page.overlay.append(self.haptic)
            page.overlay.append(self.success_audio)
            page.overlay.append(self.fail_audio)
            page.overlay.append(self.start_recording_audio)
            page.overlay.append(self.stop_recording_audio)
            page.overlay.append(self.bottom_progress)
            page.appbar = None
            page.navigation_bar = None

            # ANDROIDTEST -------> DELETE
            if page.route == "/androidtest":
                self.container.content = ft.Container(content=self.androidtest(page), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container
            
            # INTRO
            if page.route == "/intro":
                self.container.content = ft.Container(content=self.intro(page), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # REPORT
            if page.route == "/report":
                self.container.content = ft.Container(content=self.report(page), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # MAIN
            if page.route == "/ogren":
                self.container.content = ft.Container(content=self.ogren(page), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # LEARN_LETTER
            if page.route.startswith("/learn_letter_"):
                self.container.content = ft.Container(content=self.learn_letter(page, letter=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # DRAW_LETTER
            if page.route.startswith("/draw_letter_"):
                self.container.content = ft.Container(content=self.draw_letter(page, letter=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # LETTER_SEQUENCE
            if page.route.startswith("/letter_sequence_"):
                self.container.content = ft.Container(content=self.letter_sequence(page, letters=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # LEARN_SHAPE_2D
            if page.route.startswith("/learn_shape_2d_"):
                self.container.content = ft.Container(content=self.learn_shape_2d(page, shape_2d=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # DRAW_SHAPE_2D
            if page.route.startswith("/draw_shape_2d_"):
                self.container.content = ft.Container(content=self.draw_shape_2d(page, shape_2d=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # LEARN_SHAPE_3D
            if page.route.startswith("/learn_shape_3d_"):
                self.container.content = ft.Container(content=self.learn_shape_3d(page, shape_3d=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # LEARN_NUMBER
            if page.route.startswith("/learn_number_"):
                self.container.content = ft.Container(content=self.learn_number(page, number=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container
            
            # LEARN_SYMBOL
            if page.route.startswith("/learn_symbol_"):
                self.container.content = ft.Container(content=self.learn_symbol(page, symbol=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # MATH_OPERATION
            if page.route.startswith("/math_operation_"):
                self.container.content = ft.Container(content=self.math_operation(page, operation=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            # level_index
            if page.route.startswith("/level_index_"):
                self.container.content = ft.Container(content=self.level_index(page, index=page.route.split("_")[-1]), bgcolor="#EBF2F7", expand=True, width=float("inf"), padding=0)
                page_container.content = self.container

            try: page_container.update()
            except: pass

        page.on_route_change = route_change

        # page.client_storage.clear() # DELETE

        if page.client_storage.contains_key("needs_intro"):
            if page.client_storage.get("needs_intro") == True:
                page.client_storage.set("needs_intro", False)
                page.go("/intro")
            else:
                page.go("/ogren")
        else:
            page.client_storage.set("needs_intro", False)
            page.go("/intro")

app = MyApp()
ft.app(app.main, assets_dir="assets", name="Down Up")