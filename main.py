import asyncio
import pygame
import sys
import random
import math
import webbrowser
from data1 import karakterler

# --- BURAYA KENDİ LİNKİNİ YAPIŞTIR ---
LINK_URL = "https://github.com/ErayG10"

# --- 1. SETTINGS & VISUALS ---
GENISLIK, YUKSEKLIK = 1200, 800
FPS = 60

# --- ÇİZGİ ROMAN RENK PALETİ ---
COMIC_PAPER = (245, 240, 225)
INK_BLACK = (20, 20, 25)
PANEL_LINE = (200, 195, 180)

SPIDEY_RED = (200, 30, 30)
SPIDEY_BLUE = (30, 60, 180)

# UI RENKLERİ
TEXT_INK = (10, 10, 15)
TEXT_PAPER = (245, 240, 225)

LINK_COLOR = SPIDEY_BLUE
LINK_HOVER = SPIDEY_RED

# Kutu Renkleri
CORRECT_BG = (46, 160, 67)
WRONG_BG = (200, 50, 50)
PARTIAL_BG = (220, 130, 20)
NEUTRAL_BG = (230, 230, 235)

# Arama Kutusu
INPUT_BG = (255, 255, 255)
INPUT_BORDER = INK_BLACK
INPUT_FOCUS = SPIDEY_BLUE
LIST_BG, LIST_HOVER = (240, 240, 245), (220, 220, 230)

pygame.init()

# --- TAM EKRAN AYARI (WEB İÇİN SCALED) ---
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK), pygame.SCALED)
pygame.display.set_caption("Spidey-Wordle Comic Edition")


# --- FONTS ---
def font_yukle(boyut):
    try:
        return pygame.font.SysFont("comic sans ms", boyut, bold=True)
    except:
        return pygame.font.SysFont("arial black", boyut, bold=True)


title_font = font_yukle(90)
header_font = font_yukle(20)
gui_font = font_yukle(18)
mini_font = font_yukle(12)
input_font = font_yukle(24)
warning_font = font_yukle(28)
footer_font = font_yukle(14)

# --- CHARACTER SELECTION ---
HEDEF = random.choice(karakterler)
print(f"\n[DEBUG] TARGET: {HEDEF['Ad']}\n")


# --- 2. THEME FUNCTIONS ---

# --- METİN SIĞDIRMA ---
def draw_text_fitted(surface, text, color, rect, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    padding = 8
    max_width = rect.width - padding
    if text_rect.width > max_width:
        scale_factor = max_width / text_rect.width
        new_width = int(text_rect.width * scale_factor)
        new_height = int(text_rect.height * scale_factor)
        text_surface = pygame.transform.smoothscale(text_surface, (new_width, new_height))
        text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# --- WEB & BG (GELİŞMİŞ EĞRİ AĞLAR) ---
background_surface = pygame.Surface((GENISLIK, YUKSEKLIK))
halftone_surface = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)


def draw_advanced_web(surface, cx, cy, max_radius, corner):
    if corner == "topleft":
        start_ang, end_ang = 0, 90
    elif corner == "topright":
        start_ang, end_ang = 90, 180
    elif corner == "bottomright":
        start_ang, end_ang = 180, 270
    elif corner == "bottomleft":
        start_ang, end_ang = 270, 360

    spokes = []
    num_spokes = 7
    angle_step = (end_ang - start_ang) / (num_spokes - 1)

    for i in range(num_spokes):
        angle_deg = start_ang + (i * angle_step)
        angle_rad = math.radians(angle_deg)
        end_x = cx + math.cos(angle_rad) * max_radius
        end_y = cy + math.sin(angle_rad) * max_radius
        pygame.draw.line(surface, INK_BLACK, (cx, cy), (end_x, end_y), 2)
        spokes.append((math.cos(angle_rad), math.sin(angle_rad)))

    web_layers = [0.15, 0.28, 0.42, 0.58, 0.75, 0.95]
    for r_factor in web_layers:
        current_r = max_radius * r_factor
        points = []
        for vec in spokes:
            px = cx + vec[0] * current_r
            py = cy + vec[1] * current_r
            points.append((px, py))
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            sag_amount = 0.15
            ctrl_x = mid_x + (cx - mid_x) * sag_amount
            ctrl_y = mid_y + (cy - mid_y) * sag_amount
            curve_points = [p1]
            steps = 5
            for t_step in range(1, steps):
                t = t_step / steps
                bx = (1 - t) ** 2 * p1[0] + 2 * (1 - t) * t * ctrl_x + t ** 2 * p2[0]
                by = (1 - t) ** 2 * p1[1] + 2 * (1 - t) * t * ctrl_y + t ** 2 * p2[1]
                curve_points.append((bx, by))
            curve_points.append(p2)
            pygame.draw.lines(surface, (40, 40, 50), False, curve_points, 1)


def arkaplan_olustur():
    background_surface.fill(COMIC_PAPER)
    for _ in range(5):
        bx = random.randint(0, GENISLIK - 200)
        by = random.randint(0, YUKSEKLIK - 200)
        bw = random.randint(150, 400)
        bh = random.randint(100, 300)
        pygame.draw.rect(background_surface, PANEL_LINE, (bx, by, bw, bh), 3)

    for x in range(0, GENISLIK, 8):
        for y in range(0, YUKSEKLIK, 8):
            ox = random.randint(-1, 1)
            oy = random.randint(-1, 1)
            pygame.draw.circle(halftone_surface, (20, 20, 20, 15), (x + ox, y + oy), 1)

    background_surface.blit(halftone_surface, (0, 0))
    draw_advanced_web(background_surface, 0, 0, 220, "topleft")
    draw_advanced_web(background_surface, GENISLIK, 0, 220, "topright")
    draw_advanced_web(background_surface, 0, YUKSEKLIK, 180, "bottomleft")
    draw_advanced_web(background_surface, GENISLIK, YUKSEKLIK, 180, "bottomright")


arkaplan_olustur()


# --- COMIC BOX ---
def comic_kutu_ciz(rect, bg_color, text, f_tipi=gui_font, scale_y=1.0):
    if scale_y < 0.15: return
    target_width = rect.width
    current_height = int(rect.height * scale_y)
    target_x = rect.x
    target_y = int(rect.centery - (current_height / 2))
    anim_rect = pygame.Rect(target_x, target_y, target_width, current_height)

    border_thickness = 4
    shadow_offset = 5
    shadow_rect = anim_rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    pygame.draw.rect(ekran, INK_BLACK, shadow_rect)
    pygame.draw.rect(ekran, bg_color, anim_rect)

    if bg_color != NEUTRAL_BG and current_height > 20:
        dot_surf = pygame.Surface((anim_rect.width, anim_rect.height), pygame.SRCALPHA)
        for dx in range(2, anim_rect.width, 6):
            for dy in range(2, anim_rect.height, 6):
                dot_alpha = 40
                if bg_color == WRONG_BG: dot_alpha = 60
                pygame.draw.circle(dot_surf, (0, 0, 0, dot_alpha), (dx, dy), 1)
        ekran.blit(dot_surf, anim_rect.topleft)

    pygame.draw.rect(ekran, INK_BLACK, anim_rect, border_thickness)
    pygame.draw.circle(ekran, INK_BLACK, anim_rect.topleft, border_thickness - 1)
    pygame.draw.circle(ekran, INK_BLACK, anim_rect.topright, border_thickness - 1)
    pygame.draw.circle(ekran, INK_BLACK, anim_rect.bottomleft, border_thickness - 1)
    pygame.draw.circle(ekran, INK_BLACK, anim_rect.bottomright, border_thickness - 1)

    text_col = TEXT_PAPER if bg_color != NEUTRAL_BG else TEXT_INK
    if scale_y > 0.6:
        if "\n" in str(text):
            satirlar = str(text).split("\n")
            top_rect = pygame.Rect(anim_rect.x, anim_rect.centery - 18, anim_rect.w, 20)
            draw_text_fitted(ekran, satirlar[0], text_col, top_rect, f_tipi)
            t2_col = (text_col[0], text_col[1], text_col[2], 180) if len(text_col) > 3 else text_col
            t2 = mini_font.render(satirlar[1], True, t2_col)
            ekran.blit(t2, t2.get_rect(center=(anim_rect.centerx, anim_rect.centery + 14)))
        else:
            draw_text_fitted(ekran, str(text), text_col, anim_rect, f_tipi)


def karsilastir(t_k):
    sonuc, dogru = {}, 0
    for oz in ["Cinsiyet", "Tur", "Tip", "Kaynak"]:
        bg = CORRECT_BG if t_k[oz] == HEDEF[oz] else WRONG_BG
        if bg == CORRECT_BG: dogru += 1
        sonuc[oz] = (t_k[oz], bg)
    fark = abs(t_k["Yil"] - HEDEF["Yil"])
    y_bg = CORRECT_BG if fark == 0 else (PARTIAL_BG if fark <= 2 else WRONG_BG)
    if y_bg == CORRECT_BG: dogru += 1
    yil_ok = " ^" if t_k["Yil"] < HEDEF["Yil"] else (" v" if t_k["Yil"] > HEDEF["Yil"] else "")
    sonuc["Yil"] = (f"{t_k['Yil']}{yil_ok}\n{t_k.get('Comic', '')}", y_bg)
    sonuc["_anim_index"] = 0
    sonuc["_anim_timer"] = 0
    sonuc["_dogru_sayisi"] = dogru
    sonuc["Ad"] = (t_k["Ad"], NEUTRAL_BG)
    return sonuc


# --- MAIN ASYNC LOOP ---
async def main():
    global HEDEF

    tahminler = []
    kullanici_yazisi = ""
    oneri_listesi = []
    oyun_bitti = False
    input_aktif = True
    animasyon_oynuyor = False
    uyari_mesaji = ""
    uyari_sayaci = 0
    link_rect = pygame.Rect(0, 0, 0, 0)

    clock = pygame.time.Clock()

    base_ix = GENISLIK // 2 - 250
    base_iy = YUKSEKLIK - 120
    i_rect = pygame.Rect(base_ix, base_iy, 500, 60)

    while True:
        ekran.blit(background_surface, (0, 0))
        m_pos = pygame.mouse.get_pos()

        # FOOTER
        text_static = "Fan Game. Made by "
        text_link = "Eray Gürbüz"
        surf_static = footer_font.render(text_static, True, INK_BLACK)
        is_hovering_link = link_rect.collidepoint(m_pos)
        link_col = LINK_HOVER if is_hovering_link else LINK_COLOR
        surf_link = footer_font.render(text_link, True, link_col)
        total_width = surf_static.get_width() + surf_link.get_width()
        start_x = (GENISLIK - total_width) // 2
        footer_y = YUKSEKLIK - 30
        ekran.blit(surf_static, (start_x, footer_y))
        link_rect = ekran.blit(surf_link, (start_x + surf_static.get_width(), footer_y))
        if is_hovering_link:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # TITLE (Çakışma Önleyici & Negatif Tire)
        s_text = title_font.render("SPIDEY", True, SPIDEY_RED)
        d_text = title_font.render("-", True, COMIC_PAPER)  # Tire: Arka plan rengi
        w_text = title_font.render("WORDLE", True, SPIDEY_BLUE)
        s_out = title_font.render("SPIDEY", True, INK_BLACK)
        d_out = title_font.render("-", True, INK_BLACK)
        w_out = title_font.render("WORDLE", True, INK_BLACK)

        gap = 10
        total_w = s_text.get_width() + d_text.get_width() + w_text.get_width() + (gap * 2)
        start_x = (GENISLIK - total_w) // 2
        base_y = 20
        s_pos = (start_x, base_y)
        d_pos = (start_x + s_text.get_width() + gap, base_y)
        w_pos = (d_pos[0] + d_text.get_width() + gap, base_y)

        for dx, dy in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
            ekran.blit(s_out, (s_pos[0] + dx, s_pos[1] + dy))
            ekran.blit(d_out, (d_pos[0] + dx, d_pos[1] + dy))
            ekran.blit(w_out, (w_pos[0] + dx, w_pos[1] + dy))
        ekran.blit(s_text, s_pos)
        ekran.blit(d_text, d_pos)
        ekran.blit(w_text, w_pos)

        # LOGIC
        if tahminler:
            son_tahmin = tahminler[0]
            if son_tahmin["_anim_index"] < 6:
                animasyon_oynuyor = True
                input_aktif = False

                # --- HIZ AYARI: 0.3 (Orijinal Hızlı) ---
                son_tahmin["_anim_timer"] += 0.05

                if son_tahmin["_anim_timer"] >= 10:
                    son_tahmin["_anim_index"] += 1
                    son_tahmin["_anim_timer"] = 0
            else:
                if animasyon_oynuyor:
                    animasyon_oynuyor = False
                    tahmin_edilen_ad = son_tahmin["Ad"][0]
                    if tahmin_edilen_ad == HEDEF["Ad"]:
                        son_tahmin["Ad"] = (tahmin_edilen_ad, CORRECT_BG)
                        oyun_bitti = True
                    elif son_tahmin["_dogru_sayisi"] == 5:
                        uyari_mesaji = "Wrong character!"
                        uyari_sayaci = 180
                    if not oyun_bitti: input_aktif = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if link_rect.collidepoint(event.pos): webbrowser.open(LINK_URL)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

            if not animasyon_oynuyor:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not oyun_bitti:
                        input_aktif = True if i_rect.collidepoint(m_pos) else False
                        for i, oneri in enumerate(oneri_listesi):
                            r = pygame.Rect(i_rect.x, i_rect.y - ((i + 1) * 50), 500, 50)
                            if r.collidepoint(m_pos):
                                t_ad = oneri["Ad"]
                                bulunan = next((k for k in karakterler if k["Ad"] == t_ad), None)
                                if bulunan:
                                    tahminler.insert(0, karsilastir(bulunan))
                                    animasyon_oynuyor = True  # FIX
                                    kullanici_yazisi, oneri_listesi = "", []
                    else:
                        if pygame.Rect(GENISLIK // 2 - 120, YUKSEKLIK // 2 + 110, 240, 60).collidepoint(m_pos):
                            HEDEF = random.choice(karakterler)
                            print(f"NEW TARGET: {HEDEF['Ad']}")
                            tahminler, kullanici_yazisi, oyun_bitti, input_aktif = [], "", False, True

                if event.type == pygame.KEYDOWN and input_aktif and not oyun_bitti:
                    if event.key == pygame.K_RETURN:
                        t_ad = oneri_listesi[0]["Ad"] if oneri_listesi else kullanici_yazisi
                        bulunan = next((k for k in karakterler if k["Ad"].lower() == t_ad.lower()), None)
                        if bulunan:
                            tahminler.insert(0, karsilastir(bulunan))
                            animasyon_oynuyor = True  # FIX
                            kullanici_yazisi, oneri_listesi = "", []
                    elif event.key == pygame.K_BACKSPACE:
                        kullanici_yazisi = kullanici_yazisi[:-1]
                    else:
                        kullanici_yazisi += event.unicode
                    oneri_listesi = [k for k in karakterler if kullanici_yazisi.lower() in k["Ad"].lower()][
                                    :5] if kullanici_yazisi else []

        # HEADERS
        headers = ["Character", "Gender", "Species", "Role", "Origin", "Year"]
        for i, b in enumerate(headers):
            t = header_font.render(b.upper(), True, INK_BLACK)
            ekran.blit(t, t.get_rect(center=(80 + i * 180 + 80, 140)))

        # DRAW BOXES
        for r, satir in enumerate(tahminler[:8]):
            ozellikler_listesi = ["Ad", "Cinsiyet", "Tur", "Tip", "Kaynak", "Yil"]
            current_anim_idx = satir.get("_anim_index", 6)
            for c, oz in enumerate(ozellikler_listesi):
                val, bg = satir[oz]
                kutu_rect = pygame.Rect(80 + c * 180, 170 + r * 70, 160, 55)
                if r == 0 and animasyon_oynuyor:
                    if c < current_anim_idx:
                        comic_kutu_ciz(kutu_rect, bg, val, scale_y=1.0)
                    elif c == current_anim_idx:
                        progress = min(1.0, satir["_anim_timer"] / 10)
                        comic_kutu_ciz(kutu_rect, bg, val, scale_y=progress)
                else:
                    comic_kutu_ciz(kutu_rect, bg, val, scale_y=1.0)

        # INPUT UI
        if not animasyon_oynuyor:
            for i, o in enumerate(oneri_listesi):
                r = pygame.Rect(i_rect.x, i_rect.y - ((i + 1) * 50), 500, 50)
                is_hov = r.collidepoint(m_pos)
                pygame.draw.rect(ekran, LIST_HOVER if is_hov else LIST_BG, r)
                pygame.draw.rect(ekran, INK_BLACK, r, 2)
                ekran.blit(input_font.render(o["Ad"], True, INK_BLACK), (r.x + 20, r.y + 10))

        pygame.draw.rect(ekran, INK_BLACK, (i_rect.x + 4, i_rect.y + 4, i_rect.w, i_rect.h), border_radius=20)
        pygame.draw.rect(ekran, INPUT_BG, i_rect, border_radius=20)
        border_col = INPUT_FOCUS if input_aktif else INPUT_BORDER
        pygame.draw.rect(ekran, border_col, i_rect, 4, border_radius=20)

        t_disp = "Analyzing..." if animasyon_oynuyor else (
            kullanici_yazisi if kullanici_yazisi or input_aktif else "Spidey-Sense tingling... (Type here)")
        text_col = WRONG_BG if animasyon_oynuyor else (INK_BLACK if kullanici_yazisi else (100, 100, 110))
        ekran.blit(input_font.render(t_disp, True, text_col), (i_rect.x + 25, i_rect.y + 15))

        if uyari_sayaci > 0 and not animasyon_oynuyor:
            msg_bg = pygame.Rect(GENISLIK // 2 - 150, i_rect.y - 50, 300, 40)
            pygame.draw.rect(ekran, WRONG_BG, msg_bg)
            pygame.draw.rect(ekran, INK_BLACK, msg_bg, 3)
            msg = warning_font.render(uyari_mesaji.upper(), True, TEXT_PAPER)
            ekran.blit(msg, msg.get_rect(center=msg_bg.center))
            uyari_sayaci -= 1

        if oyun_bitti and not animasyon_oynuyor:
            overlay = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
            overlay.fill((20, 20, 25, 200))
            ekran.blit(overlay, (0, 0))
            win_r = pygame.Rect(GENISLIK // 2 - 300, YUKSEKLIK // 2 - 150, 600, 300)
            pygame.draw.rect(ekran, INK_BLACK, (win_r.x + 8, win_r.y + 8, win_r.w, win_r.h))
            pygame.draw.rect(ekran, COMIC_PAPER, win_r)
            pygame.draw.rect(ekran, INK_BLACK, win_r, 6)
            t_con = title_font.render("AMAZING!", True, CORRECT_BG)
            t_con_out = title_font.render("AMAZING!", True, INK_BLACK)
            ekran.blit(t_con_out, t_con_out.get_rect(center=(win_r.centerx + 3, win_r.y + 63)))
            ekran.blit(t_con, t_con.get_rect(center=(win_r.centerx, win_r.y + 60)))
            t_targ = input_font.render(f"It was: {HEDEF['Ad']}", True, INK_BLACK)
            ekran.blit(t_targ, t_targ.get_rect(center=(win_r.centerx, win_r.y + 150)))
            btn_r = pygame.Rect(GENISLIK // 2 - 120, YUKSEKLIK // 2 + 110, 240, 60)
            comic_kutu_ciz(btn_r, CORRECT_BG, "PLAY AGAIN", scale_y=1.0)

        pygame.display.flip()
        await asyncio.sleep(0)


# OYUNU BAŞLAT
asyncio.run(main())