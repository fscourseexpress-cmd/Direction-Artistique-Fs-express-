"""Semaine 1 — version 2 : chaque créa composée individuellement, avec photos.

Usage : python3 build_v2.py  puis  node export_v2.js   (PNG dans png-v2/)
Palette FS Express uniquement : bleu #1690C1, rouge #93241E, blanc et leurs nuances.
"""
import build as B   # icônes, déchirure, cercles, carte, sondage, autocollants et CSS de base

WA = "687 53 53 73"
CTA_WA = f"Envoyez votre première livraison sur WhatsApp : {WA}"
V2 = "assets/v2/"
SQ, P, ST = 1080, 1350, 1920
CREAS = []


def add(cid, size, bg, html, label):
    CREAS.append((cid, size, bg, html, label))


# ---------- briques ----------
def ph(src, x, y, w, h, pos="center", size="cover", rot=0, r=30, border=14, extra=""):
    return (f'<div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background-image:url({src});background-size:{size};background-position:{pos};'
            f'transform:rotate({rot}deg);border-radius:{r}px;border-width:{border}px;{extra}"></div>')

def circ(src, x, y, d, pos="center", size="cover", border=12, extra=""):
    return ph(src, x, y, d, d, pos, size, 0, d, border, extra)

def full(src, pos="center", filt="", size="cover"):
    return f'<div class="full" style="background-image:url({src});background-position:{pos};background-size:{size};filter:{filt}"></div>'

def grad(css):
    return f'<div class="full" style="background:{css};z-index:2"></div>'

def tb(html, x, y, w, style=""):
    return f'<div class="tb" style="left:{x}px;top:{y}px;width:{w}px;{style}">{html}</div>'

def logo(x=56, y=56, h=84):
    return f'<div class="logo abs" style="left:{x}px;top:{y}px"><img src="assets/logo.jpg" alt="Logo FS Express" style="height:{h}px"></div>'

def logo_low(right=56, top=1100, h=56):
    """Logo discret, posé en bas à droite."""
    return (f'<div class="logo abs" style="left:auto;right:{right}px;top:{top}px">'
            f'<img src="assets/logo.jpg" alt="Logo FS Express" style="height:{h}px"></div>')

def icon_disc(x, y, d, name, bg="#fff", fg="#1690C1"):
    """Pastille circulaire avec une icône (remplace une photo quand le planning demande une icône)."""
    return (f'<div class="idisc abs" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;'
            f'padding:{round(d * 0.24)}px;background:{bg};color:{fg}">{B.ico(name)}</div>')

def steps_list(items):
    """Rappel numéroté des étapes."""
    rows = "".join(f'<div class="srow"><b>{n}</b><span>{t}</span></div>' for n, t in enumerate(items, start=1))
    return f'<div class="slist">{rows}</div>'

def pg(text, color="#fff"):
    return f'<div class="pg abs" style="color:{color}">{text}</div>'

def cta(text, v="", bottom=50, fs=34, left=56, right=56):
    return f'<div class="cta abs {v}" style="left:{left}px;right:{right}px;bottom:{bottom}px;font-size:{fs}px">{text}</div>'

def glissez(color="#fff", bottom=60):
    return f'<div class="k abs" style="left:56px;bottom:{bottom}px;color:{color}">Glissez →</div>'

def numo(n, x, y, size=300, color="#fff"):
    return f'<div class="numo" style="left:{x}px;top:{y}px;font-size:{size}px;-webkit-text-stroke-color:{color}">{n}</div>'

def notif(title, sub, time, x, y, w=600, rot=0, icon="phone-off", avbg="#93241E"):
    return (f'<div class="notif" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
            f'<div class="av" style="background:{avbg}">{B.ico(icon)}</div><div class="nt"><b>{title}</b><span>{sub}</span></div>'
            f'<div class="tm">{time}</div></div>')

def bubble(text, x, y, w=None, kind="w", tail="bl", fs=40, rot=0):
    ww = f"width:{w}px;" if w else ""
    return f'<div class="bbl {kind} t-{tail}" style="left:{x}px;top:{y}px;{ww}font-size:{fs}px;transform:rotate({rot}deg)">{text}</div>'

def stk(text, x, y, rot=-4, kind="r", fs=30):
    return f'<div class="stk {kind}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);font-size:{fs}px">{text}</div>'

def ring_draw(x, y, w, h, color="#fff", sw=7, rot=0):
    return (f'<svg class="hd" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)" viewBox="0 0 200 120">'
            f'<path d="M20 64 C 10 22, 120 4, 176 34 C 204 52, 180 108, 100 112 C 40 114, 8 94, 22 60 M 30 44 C 70 16, 150 18, 186 50" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')

def arrow_draw(x, y, w, h, color="#fff", flip=False, rot=0):
    sx = -1 if flip else 1
    return (f'<svg class="hd" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:scaleX({sx}) rotate({rot}deg)" viewBox="0 0 200 120">'
            f'<path d="M10 20 C 70 10, 140 30, 170 96 M 140 86 L 172 100 L 182 64" fill="none" stroke="{color}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>')

def motion(x, y, w, h, op=.45):
    return (f'<svg class="hd" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:{op}" viewBox="0 0 400 200">'
            f'<path d="M0 40 H260 M40 100 H330 M10 160 H220" stroke="#fff" stroke-width="10" stroke-linecap="round" fill="none"/></svg>')

def cut(src, x, y, w, extra=""):
    return f'<img class="cut" src="{src}" style="left:{x}px;top:{y}px;width:{w}px;{extra}">'

def phone(x, y, w, h, inner, rot="rotateY(-16deg) rotateX(5deg) rotateZ(3deg)", bar="FS Express"):
    return (f'<div class="ph3" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:perspective(1200px) {rot}">'
            f'<div class="scr"><div class="bar">{bar}</div>{inner}</div></div>')

def pbub(text, x, y, kind="w", fs=28, side="left"):
    return f'<div class="bub {kind}" style="{side}:{x}px;top:{y}px;font-size:{fs}px">{text}</div>'

def guide(x, y, w=520, h=690, rot="rotateY(-22deg) rotateZ(4deg)"):
    return (f'<div class="guide abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:perspective(1400px) {rot}">'
            f'<div class="gk">Guide gratuit</div><div class="gt" style="font-size:{int(w / 10.5)}px">5 erreurs qui font perdre des ventes aux vendeurs en ligne à Yaoundé</div>'
            '<div class="gl"><img src="assets/logo.jpg" alt=""></div></div>')

# =============================== LUNDI ===============================
def car_lu(prefix, H, platform):
    big = H > SQ
    # 1 — couverture : les 3 situations en photos (sans légende ni surtitre ajouté)
    d = 290 if big else 250
    yc = H - (430 if big else 380)
    trio = [("assets/dos-fs.jpg", "50% 28%", "cover"),
            ("assets/v2/livreur-au-telephone.jpg", "50% 30%", "cover"),
            ("assets/v2/vendeuse-cash@2x.jpg", "30% 92%", "230%")]
    xs = [60, 395, 730] if not big else [56, 395, 734]
    items = ""
    for i, ((src, pos, size), x) in enumerate(zip(trio, xs), start=1):
        items += circ(src, x, yc + (i % 2) * 24, d, pos, size)
        items += f'<div class="nb" style="left:{x + d - 86}px;top:{yc + (i % 2) * 24 - 10}px">{i}</div>'
    add(f"{prefix}-1", "sq" if not big else "p", "n",
        B.rings(950, 120, (520, 760)) + logo() + pg("01 / 05") +
        tb(f'<div class="t {"xl" if big else "l"} sh">3 situations qui font perdre <span class="hl r">une vente.</span></div>', 56, 255, 968) +
        tb('<div class="sub">Une vente conclue n\'est pas une vente encaissée.</div>', 56, 600 if big else 520, 900) + items,
        f"{platform} · Carrousel 1/5")
    # 2 — livreur injoignable : photo pleine page
    add(f"{prefix}-2", "sq" if not big else "p", "n",
        full("assets/dos-fs.jpg", "center 30%") +
        grad("linear-gradient(180deg,rgba(10,61,87,.55) 0%,rgba(10,61,87,.05) 30%,rgba(10,61,87,.25) 55%,rgba(10,61,87,.97) 85%)") +
        logo() + pg("02 / 05") + numo("1", 820, 150, 260) +
        tb('<div class="t l sh">Le livreur injoignable.</div>', 56, (930 if big else 700), 968) +
        tb('<div class="sub">Le colis est parti. Le livreur ne répond plus.</div>', 56, (1030 if big else 800), 968) +
        glissez(), f"{platform} · Carrousel 2/5")
    # 3 — retard : la photo et le titre, sans bulle ni sous-titre inventés
    cd = 600 if big else 520
    add(f"{prefix}-3", "sq" if not big else "p", "b",
        B.rings(760, 420, (700, 900)) + logo() + pg("03 / 05") + numo("2", 56, 190, 240) +
        circ("assets/v2/livreur-au-telephone.jpg", 1080 - cd - 40, 170, cd, "50% 25%", "cover", 14) +
        tb('<div class="t l sh">Le retard qui s\'allonge.</div>', 56, (860 if big else 735), 968) +
        glissez(), f"{platform} · Carrousel 3/5")
    # 4 — cash qui tarde : la photo et le titre, sans notification inventée
    add(f"{prefix}-4", "sq" if not big else "p", "r",
        B.rings(300, 900, (700, 900)) + logo() + pg("04 / 05") + numo("3", 56, 190, 240) +
        ph("assets/v2/vendeuse-cash@2x.jpg", 400, 160, 620, (560 if big else 470), "30% 95%", "185%", 4) +
        tb('<div class="t l sh">Le cash qui tarde à revenir.</div>', 56, (860 if big else 735), 968) +
        glissez(), f"{platform} · Carrousel 4/5")
    # 5 — la question, logo discret
    last = "Votez en commentaire : 1, 2 ou 3" if platform == "Facebook" else "Enregistrez ce post"
    rows = ""
    y0 = 420 if big else 400
    step = 175 if big else 150
    for i, ((src, pos, size), lab) in enumerate(zip(trio, ["Le livreur injoignable", "Le retard", "Le cash qui tarde"])):
        y = y0 + i * step
        rows += f'<div class="row-ch" style="top:{y}px;height:{step - 25}px"><b>{i + 1}</b><span>{lab}</span></div>'
        rows += circ(src, 1080 - 56 - (step - 25) - 6, y - 6, step - 13, pos, size, 6, "z-index:7")
    add(f"{prefix}-5", "sq" if not big else "p", "w",
        logo(56, 56, 56) + pg("05 / 05", "#0A3D57") +
        tb('<div class="t l" style="color:#0A3D57">Laquelle vous coûte <span class="hl r" style="color:#fff">le plus&nbsp;?</span></div>', 56, 200, 968) +
        rows + cta(last, "red"), f"{platform} · Carrousel 5/5")

car_lu("LU-FB2", SQ, "Facebook")

add("LU-FB3", "p", "r",
    full(V2 + "commercant-boutique@2x.jpg", "center 20%") +
    grad("linear-gradient(180deg,rgba(94,23,18,0) 38%,rgba(147,36,30,.85) 62%,rgba(94,23,18,.98) 100%)") +
    logo_low(56, 1100, 56) +
    tb('<div class="t xl sh">Vous vendez.</div><div class="t xl" style="margin-top:10px"><span class="hl w">On livre.</span></div>', 56, 800, 968) +
    tb('<div class="sub" style="font-size:38px">Vous avez fait le plus dur : vendre.</div>', 56, 1030, 968) +
    cta(CTA_WA, fs=32), "Facebook · Affiche")

car_lu("LU-IG2", P, "Instagram")

add("LU-IG3", "s", "r",
    B.rings(900, 200, (600, 820)) + logo(64, 120) +
    tb('<div class="t l sh">Quel est votre pire souvenir de livraison&nbsp;?</div>', 64, 430, 952) +
    tb(B.poll("Sondage", ["Livreur injoignable", "Retard", "Cash qui tarde"]), 64, 800, 952) +
    '<div class="k abs" style="left:64px;bottom:120px">Votez dans le sondage ↑</div>',
    "Instagram · Story sondage")

# =============================== MARDI ===============================
add("MA-FB1", "p", "r",
    B.rings(980, 160, (520, 760, 980)) + logo() +
    '<div class="bigquote">“</div>' +
    tb('<div class="t xl sh" style="font-style:italic">Il va croire que je suis une arnaque.</div>', 56, 320, 968) +
    tb('<div class="sub">Quand un client relance pour la 3<sup>e</sup> fois, ce n\'est pas qu\'un retard : c\'est votre réputation en jeu.</div>', 56, 740, 968) +
    '<div class="pill w abs" style="left:56px;bottom:56px">On sait ce que ça fait.</div>',
    "Facebook · Visuel citation")

add("MA-FB3", "p", "n",
    full(V2 + "tel-carnet-fs@2x.jpg", "center 40%") +
    grad("linear-gradient(180deg,rgba(10,61,87,.96) 0%,rgba(10,61,87,.75) 18%,rgba(10,61,87,0) 30%,rgba(10,61,87,0) 75%,rgba(10,61,87,.7) 100%)") +
    logo() +
    tb('<div class="t m sh">Le soir, on compte ce qui est <span class="hl r">vraiment rentré.</span></div>', 56, 180, 968) +
    cta("Répondez en commentaire", "red"), "Facebook · Post question (image)")

emo = [
    ("Angoisse", "Et s'il n'arrivait jamais ?", "r"),
    ("Honte", "Mon client va croire que je suis une arnaque.", "b"),
    ("Impuissance", "Je ne peux rien faire. Il ne répond pas.", "n"),
    ("Fatigue", "Vingt appels aujourd'hui. Pour un seul colis.", "r"),
]
add("MA-IG1-1", "p", "n",
    full(V2 + "vendeuse-emballe@2x.jpg", "center 30%") +
    grad("linear-gradient(180deg,rgba(10,61,87,.45) 0%,rgba(10,61,87,0) 25%,rgba(10,61,87,.2) 45%,rgba(10,61,87,.96) 78%)") +
    logo() + pg("01 / 06") +
    tb('<div class="t l sh">Ce que personne ne voit derrière une <span class="hl r">livraison ratée.</span></div>', 56, 860, 968) +
    glissez(), "Instagram · Carrousel 1/6")
# 2 — angoisse : le mot géant, l'horloge
add("MA-IG1-2", "p", "r",
    logo() + pg("02 / 06") +
    '<div class="wordo" style="top:250px">ANGOISSE</div>' +
    '<div class="clock abs" style="left:640px;top:470px">' + B.ico("clock") + '</div>' +
    tb('<div class="qcard">« Et s\'il n\'arrivait jamais ? »</div>', 56, 860, 968) +
    glissez(), "Instagram · Carrousel 2/6")
# 3 — honte : la phrase du vendeur (à valider)
add("MA-IG1-3", "p", "b",
    B.rings(900, 300, (560, 780)) + logo() + pg("03 / 06") +
    tb('<div class="word">Honte</div>', 56, 210, 968) +
    tb('<div class="qcard">« Mon client va croire que je suis une arnaque. »</div>', 56, 820, 968) +
    glissez(), "Instagram · Carrousel 3/6")
# 4 — impuissance : le livreur qui ne répond plus
add("MA-IG1-4", "p", "n",
    logo() + pg("04 / 06") +
    circ("assets/dos-fs.jpg", 560, 170, 460, "50% 30%", "cover", 12) +
    tb('<div class="word" style="font-size:132px">Impuissance</div>', 56, 690, 968) +
    tb('<div class="qcard">« Je ne peux rien faire. Il ne répond pas. »</div>', 56, 880, 968) +
    glissez(), "Instagram · Carrousel 4/6")
# 5 — fatigue : l'icône seule, sans compteur d'appels
add("MA-IG1-5", "p", "r",
    B.rings(800, 420, (560, 780)) + logo() + pg("05 / 06") +
    '<div class="bigic abs" style="left:56px;top:190px">' + B.ico("battery") + '</div>' +
    tb('<div class="word">Fatigue</div>', 56, 640, 968) +
    tb('<div class="qcard">« Vingt appels aujourd\'hui. Pour un seul colis. »</div>', 56, 860, 968) +
    glissez(), "Instagram · Carrousel 5/6")
add("MA-IG1-6", "p", "w",
    logo() + pg("06 / 06", "#0A3D57") +
    ph(V2 + "operatrice-tel@2x.jpg", 540, 250, 480, 640, "center 30%", "cover", 3) +
    tb('<div class="t xl" style="color:#0A3D57">On</div><div class="t xl"><span class="hl r">connaît.</span></div>', 56, 290, 470) +
    tb('<div class="sub" style="color:#0A3D57">Vous n\'êtes pas seul. Un commerçant devrait passer son temps à vendre, pas à courir après ses livraisons.</div>', 56, 560, 460) +
    cta("Enregistrez et envoyez à un vendeur qui en a besoin", "red", fs=30), "Instagram · Carrousel 6/6")

add("MA-IG3", "s", "r",
    B.rings(850, 380, (600, 820, 1040)) + logo(64, 120) +
    tb('<div class="k">Terminez la phrase</div>', 64, 330, 900) +
    tb('<div class="t l sh">Un commerçant devrait passer son temps à…</div>', 64, 390, 952) +
    arrow_draw(560, 760, 300, 180, "#fff", False, 8) +
    tb(B.qsticker("Complétez la phrase"), 64, 960, 952) +
    '<div class="k abs" style="left:64px;bottom:120px">Répondez à la story ↑</div>',
    "Instagram · Story question")

# =============================== MERCREDI ===============================
add("ME-FB3-1", "sq", "n",
    full(V2 + "rue-yaounde-fs@2x.jpg", "center 55%") +
    grad("linear-gradient(180deg,rgba(10,61,87,.95) 0%,rgba(10,61,87,.8) 32%,rgba(10,61,87,0) 60%,rgba(10,61,87,.6) 100%)") +
    logo() + pg("01 / 04") +
    tb('<div class="t m sh">Une commande à l\'autre bout de la ville&nbsp;?</div>', 56, 200, 968) +
    tb('<div class="t l"><span class="hl r">Ne la refusez plus.</span></div>', 56, 380, 968) +
    glissez(), "Facebook · Carrousel 1/4")
add("ME-FB3-2", "sq", "n",
    B.mapdeco(1080, 1080, ((.22, .42), (.5, .3), (.78, .36), (.3, .7), (.62, .62), (.84, .74), (.46, .52))) +
    logo() + pg("02 / 04") +
    tb('<div class="glass"><div class="t m sh">Nos livreurs partenaires couvrent les différentes zones de Yaoundé.</div>'
       '<div class="pill w" style="margin-top:26px">[Liste des zones à compléter]</div></div>', 56, 640, 968),
    "Facebook · Carrousel 2/4")
add("ME-FB3-3", "sq", "b",
    motion(-40, 520, 620, 300, .35) + logo() + pg("03 / 04") +
    cut(V2 + "livreur-scooter-detoure.png", 330, 260, 800) +
    tb('<div class="t xl sh">Vous vendez.</div><div class="t xl" style="margin-top:8px"><span class="hl r">On livre.</span></div>', 56, 190, 640),
    "Facebook · Carrousel 3/4")
add("ME-FB3-4", "sq", "w",
    logo() + pg("04 / 04", "#0A3D57") +
    '<div class="cta abs red" style="left:56px;right:56px;top:420px;bottom:auto;font-size:52px;padding:56px 44px">Demandez votre livraison sur WhatsApp : ' + WA + '</div>',
    "Facebook · Carrousel 4/4")

add("ME-IG3-1", "s", "r",
    B.torn(540, 1290, 400, 1080, 1920, seed=41) + logo(64, 120) + pg("1 / 3") +
    tb('<div class="k">Nos engagements</div>', 64, 300, 900) +
    tb('<div class="t xl sh">Livreurs identifiés.</div>', 64, 360, 952) +
    tb('<div class="chips"><span>' + B.ico("id") + 'Permis</span><span>' + B.ico("shield") + 'Assurance</span><span>' + B.ico("moto") + 'Moto immatriculée</span></div>', 64, 640, 952) +
    cut(V2 + "livreur-sac-repas-detoure.png", 150, 820, 780),
    "Instagram · Story 1/3")
add("ME-IG3-2", "s", "b",
    B.rings(540, 1240, (900, 1100, 1300)) + logo(64, 120) + pg("2 / 3") +
    tb('<div class="k">Nos engagements</div>', 64, 300, 900) +
    tb('<div class="t xl sh">Argent reversé <span class="hl r">vite.</span></div>', 64, 360, 952) +
    tb('<div class="sub">Cash plafonné par livreur, reversé rapidement.</div>', 64, 700, 952) +
    '<div class="cph abs" style="left:190px;top:900px;width:700px;height:700px;background-image:url(assets/remise-fs.jpg);background-size:1700px auto;background-position:-344px -945px"></div>' +
    '<div class="cring abs" style="left:160px;top:870px;width:760px;height:760px"></div>' +
    ring_draw(380, 1180, 300, 190, "#fff", 7, -8),
    "Instagram · Story 2/3")
add("ME-IG3-3", "s", "n",
    B.rings(900, 1300, (700, 900)) + logo(64, 120) + pg("3 / 3") +
    tb('<div class="k">Nos engagements</div>', 64, 300, 900) +
    tb('<div class="t l sh">Un appel de validation avant chaque course.</div>', 64, 360, 952) +
    tb('<div class="sub">Et un interlocuteur dédié qui vous répond.</div>', 64, 700, 952) +
    ph(V2 + "operatrice-tel@2x.jpg", 120, 840, 840, 760, "center 25%", "cover", -2) +
    tb(B.linksticker("Écrivez-nous sur WhatsApp · " + WA), 64, 1660, 952),
    "Instagram · Story 3/3")

# =============================== JEUDI ===============================
add("JE-FB1-1", "sq", "b",
    B.rings(260, 900, (600, 800)) + logo() + pg("01 / 05") +
    ph(V2 + "agent-pouce@2x.jpg", 540, 190, 480, 600, "center 20%", "cover", 4) +
    tb('<div class="t l sh" style="white-space:nowrap">3 étapes,</div><div class="t l" style="margin-top:12px"><span class="hl r">pas une de plus.</span></div>', 56, 220, 470) +
    tb('<div class="sub">Livrer avec FS Express, c\'est simple.</div>', 56, 640, 440) +
    glissez(), "Facebook · Carrousel 1/5")
add("JE-FB1-2", "sq", "r",
    logo() + pg("02 / 05") +
    icon_disc(56, 190, 470, "chat", "#fff", "#93241E") +
    numo("1", 640, 170, 280) +
    tb('<div class="t m sh">Vous envoyez la commande sur WhatsApp et on la confirme.</div>', 600, 480, 424) +
    glissez(), "Facebook · Carrousel 2/5")
add("JE-FB1-3", "sq", "n",
    B.rings(760, 560, (640, 860)) + motion(240, 560, 400, 200, .3) + logo() + pg("03 / 05") +
    icon_disc(480, 560, 470, "moto") +
    tb('<div class="t m sh">Un livreur de votre zone vient la récupérer.</div>', 56, 200, 430) +
    numo("2", 56, 640, 280), "Facebook · Carrousel 3/5")
add("JE-FB1-4", "sq", "b",
    logo() + pg("04 / 05") +
    icon_disc(520, 180, 440, "cash", "#fff", "#93241E") +
    numo("3", 56, 190, 280) +
    '<div class="band abs" style="left:40px;right:40px;top:810px">Votre client est livré et vous recevez votre argent.</div>',
    "Facebook · Carrousel 4/5")
add("JE-FB1-5", "sq", "w",
    logo() + pg("05 / 05", "#0A3D57") +
    '<div class="cta abs red" style="left:56px;right:56px;top:420px;bottom:auto;font-size:52px;padding:56px 44px">' + CTA_WA + '</div>',
    "Facebook · Carrousel 5/5")

add("JE-FB3", "p", "b",
    B.rings(250, 1100, (600, 800)) + logo() +
    tb('<div class="k">Question fréquente</div>', 56, 200, 900) +
    tb('<div class="t m sh">Qui me rappelle avant chaque course&nbsp;?</div>', 56, 250, 968) +
    ph(V2 + "operatrice-colis@2x.jpg", 56, 440, 500, 620, "center 25%", "cover", -3) +
    stk("Votre interlocuteur dédié", 70, 1000, -3, "r", 32) +
    phone(600, 400, 400, 700,
          pbub("Bonjour ! Je confirme votre course : retrait à 14 h.", 16, 110, "w", 24) +
          pbub("Parfait, merci !", 16, 270, "b", 24, "right") +
          pbub("Colis récupéré. Je vous préviens à la livraison.", 16, 360, "w", 24) +
          pbub("Livré ! Votre client a bien reçu son colis.", 16, 520, "w", 24), bar="FS Express · Interlocuteur dédié") +
    '<div class="note abs" style="left:640px;top:1120px">Exemple de conversation</div>' +
    cta("Une question ? Écrivez-nous sur WhatsApp : " + WA, fs=30), "Facebook · Post FAQ (image)")

pairs = [
    ("Angoisse, honte", "« Mon client attend et je ne sais rien. »", "Un interlocuteur dédié qui vous répond.", "chat"),
    ("Méfiance", "« Je ne connais pas ce livreur. »", "Des livreurs identifiés, assurés, en règle.", "shield"),
    ("Cash", "« Et si mon argent disparaît ? »", "Cash plafonné par livreur et reversé vite.", "cash"),
    ("Perte de contrôle", "« Je ne sais pas où est mon colis. »", "Un appel de validation avant chaque course.", "phone"),
    ("Commandes refusées", "« Personne ne va là-bas. »", "Toute la ville couverte.", "pin"),
]
add("JE-IG2-1", "p", "r",
    full(V2 + "agent-telephone@2x.jpg", "center 25%") +
    grad("linear-gradient(180deg,rgba(94,23,18,.4) 0%,rgba(94,23,18,0) 25%,rgba(147,36,30,.3) 50%,rgba(94,23,18,.97) 80%)") +
    logo() + pg("01 / 06") +
    tb('<div class="t xl sh">Vos peurs,</div><div class="t xl" style="margin-top:10px"><span class="hl w">nos engagements.</span></div>', 56, 890, 968) +
    glissez(), "Instagram · Carrousel 1/6")
# Les citations de peur ne viennent pas du planning : seul le nom de la peur est affiché (variable « fear » non utilisée).
for i, (lab, fear, eng, icn) in enumerate(pairs, start=2):
    end = cta("Enregistrez ce post", "red") if i == 6 else glissez("#0A3D57")
    add(f"JE-IG2-{i}", "p", "w",
        logo() + pg(f"0{i} / 06", "#0A3D57") +
        '<div class="fcol"></div><div class="ecol"></div>' +
        tb(f'<div class="pl" style="color:#93241E">Peur</div><div class="fname">{lab}</div>', 96, 380, 390) +
        icon_disc(596, 380, 170, icn, "#fff", "#1690C1") +
        tb(f'<div class="pl" style="color:#fff">Engagement FS Express</div><div class="engt2">{eng}</div>', 596, 600, 390) +
        end, f"Instagram · Carrousel {i}/6")

add("JE-IG3", "s", "b",
    B.rings(900, 350, (600, 820)) + logo(64, 120) +
    tb('<div class="t l sh">Vous avez une commande à livrer demain&nbsp;?</div>', 64, 250, 952) +
    tb('<div class="t l"><span class="hl r">Envoyez-la nous sur WhatsApp.</span></div>', 64, 600, 952) +
    tb(B.linksticker("WhatsApp · " + WA), 64, 820, 952) +
    tb(steps_list(["Vous envoyez la commande sur WhatsApp et on la confirme.",
                   "Un livreur de votre zone vient la récupérer.",
                   "Votre client est livré et vous recevez votre argent."]), 64, 930, 952) +
    ph(V2 + "colis-palette-fs@2x.jpg", 100, 1420, 880, 300, "center 40%", "cover", 2),
    "Instagram · Story lien")

# =============================== VENDREDI ===============================
add("VE-IG2-MODELE", "p", "r",
    B.rings(900, 300, (560, 780, 1000)) + logo() + pg("MODÈLE") +
    '<div class="bigquote">“</div>' +
    tb('<div class="t l sh" style="font-style:italic">[Citation du commerçant]</div>', 56, 360, 968) +
    '<div class="phold abs" style="left:56px;top:640px">Photo du commerçant<br>(avec accord)</div>' +
    tb('<div class="sub"><b>[Nom du commerçant]</b><br>[Activité]</div>', 330, 700, 700) +
    cta(CTA_WA, fs=32), "Instagram · Affiche citation (modèle à compléter)")

# =============================== SAMEDI ===============================
add("SA-FB1", "p", "n",
    full("assets/dos-fs.jpg", "center 35%", "grayscale(.75) brightness(.55)") +
    grad("linear-gradient(180deg,rgba(10,61,87,.7) 0%,rgba(10,61,87,.35) 45%,rgba(10,61,87,.9) 100%)") +
    logo() +
    tb('<div class="t l sh">Une livraison ratée coûte plus <span class="hl r">qu\'une vente.</span></div>', 56, 230, 968) +
    cta("Ne laissez pas un livreur décider si ça marche : WhatsApp " + WA, fs=30), "Facebook · Post image")

add("SA-FB3", "p", "b",
    full(V2 + "rue-yaounde-fs@2x.jpg", "center 60%") +
    grad("linear-gradient(180deg,rgba(14,106,150,.97) 0%,rgba(14,106,150,.85) 36%,rgba(14,106,150,0) 58%,rgba(10,61,87,.4) 100%)") +
    tb('<div class="t xl sh">Vendez partout</div><div class="t xl" style="margin-top:8px"><span class="hl r">à Yaoundé.</span></div>', 56, 190, 968) +
    tb('<div class="sub">Acceptez enfin les commandes de toute la ville.</div>', 56, 470, 968) +
    circ(V2 + "commercant-boutique@2x.jpg", 200, 580, 600, "center 30%", "cover", 14) +
    logo_low(56, 1100, 56) +
    cta(CTA_WA, fs=32), "Facebook · Affiche")

ba = [("Débordé", "Chef d'entreprise", "users"), ("Petit business", "Marque recommandée", "star"),
      ("Vend dans son quartier", "Vend dans tout Yaoundé", "pin"), ("Subit", "Garde le contrôle", "lock")]
add("SA-IG1-1", "p", "b",
    '<div class="split-l abs" style="background-image:url(assets/v2/vendeuse-cash@2x.jpg)"></div>' +
    '<div class="split-r abs" style="background-image:url(assets/v2/commercant-boutique@2x.jpg)"></div>' +
    '<div class="split-cut abs"></div>' +
    stk("Avant", 60, 230, -4, "w", 36) + stk("Après", 830, 230, 4, "r", 36) +
    logo() + pg("01 / 05") +
    '<div class="titleband abs"><div class="t l">De vendeur débordé <span class="hl r">à chef d\'entreprise.</span></div></div>',
    "Instagram · Carrousel 1/5")
for i, (av, ap, icn) in enumerate(ba, start=2):
    end = cta(CTA_WA, "red", fs=30) if i == 5 else glissez("#0A3D57")
    add(f"SA-IG1-{i}", "p", "w",
        logo() + pg(f"0{i} / 05", "#0A3D57") +
        tb(f'<div class="bb av" style="transform:rotate(-2deg)"><div class="pl">Avant</div><div class="bt">{av}</div></div>', 56, 240, 968) +
        f'<div class="engicon abs" style="top:560px;background:#93241E">{B.ico(icn)}</div>' +
        tb(f'<div class="bb ap" style="transform:rotate(1.5deg)"><div class="pl">Après</div><div class="bt">{ap}</div></div>', 56, 720, 968) +
        end, f"Instagram · Carrousel {i}/5")

add("SA-IG3", "s", "b",
    B.rings(900, 300, (600, 820, 1040)) + logo(64, 120) +
    tb(B.qsticker("Dans un an, votre boutique ressemble à quoi&nbsp;?"), 64, 760, 952),
    "Instagram · Story question")

# =============================== DIMANCHE ===============================
add("DI-FB1", "p", "r",
    B.rings(760, 820, (760, 960, 1160)) + logo() +
    tb('<div class="t m sh">Pas encore prêt à changer de livreur&nbsp;?</div>', 56, 210, 968) +
    guide(380, 500) + stk("Gratuit", 800, 470, 8, "w", 40) +
    arrow_draw(80, 560, 280, 200, "#fff", False, 10) +
    cta("Commentez « GUIDE » et on vous l'envoie", fs=34), "Facebook · Post visuel (couverture du guide)")

def car_di(prefix, H, platform):
    big = H > SQ
    s = "p" if big else "sq"
    add(f"{prefix}-1", s, "n",
        logo() + pg("01 / 05") +
        ph(V2 + "vendeuse-emballe@2x.jpg", 560, 190, 460, (640 if big else 560), "35% 70%", "cover", 3) +
        tb('<div class="k">Avant-goût du guide</div>', 56, 220, 480) +
        tb('<div class="t l sh">3 erreurs à éviter</div><div class="t m" style="margin-top:14px"><span class="hl r">quand on vend en ligne.</span></div>', 56, 280, 480) +
        glissez(), f"{platform} · Carrousel 1/5")
    add(f"{prefix}-2", s, "r",
        logo() + pg("02 / 05") + numo("1", 760, 140, 260) +
        tb('<div class="t l sh">Des délais de livraison flous.</div>', 56, (720 if big else 580), 968) +
        glissez(), f"{platform} · Carrousel 2/5")
    add(f"{prefix}-3", s, "b",
        logo() + pg("03 / 05") + numo("2", 56, 170, 260) +
        circ(V2 + "vendeuse-emballe@2x.jpg", 540, 150, (480 if big else 420), "40% 85%", "190%", 12) +
        tb('<div class="t l sh">Un emballage négligé.</div>', 56, (720 if big else 610), 968) +
        glissez(), f"{platform} · Carrousel 3/5")
    add(f"{prefix}-4", s, "n",
        logo() + pg("04 / 05") + numo("3", 56, 170, 260) +
        circ(V2 + "agent-telephone@2x.jpg", 540, 150, (480 if big else 420), "50% 25%", "cover", 12) +
        tb('<div class="t l sh">Aucun suivi après l\'achat.</div>', 56, (780 if big else 640), 968) +
        glissez(), f"{platform} · Carrousel 4/5")
    add(f"{prefix}-5", s, "w",
        logo() + pg("05 / 05", "#0A3D57") +
        tb('<div class="t l" style="color:#0A3D57">Les 2 autres sont <span class="hl r" style="color:#fff">dans le guide.</span></div>', 56, 200, (560 if not big else 968)) +
        guide((600 if not big else 330), (180 if not big else 470), (400 if not big else 460), (540 if not big else 620)) +
        cta("Commentez « GUIDE » pour recevoir les 5 erreurs", "red", fs=30), f"{platform} · Carrousel 5/5")

car_di("DI-FB2", SQ, "Facebook")

add("DI-FB3", "p", "b",
    logo() +
    '<div class="thumb abs" style="left:120px;top:400px;width:280px;transform:rotate(-5deg)"><img src="png-v2/LU-FB3.png"></div>'
    '<div class="thumb abs" style="left:660px;top:395px;width:280px;transform:rotate(4deg)"><img src="png-v2/MA-FB1.png"></div>'
    '<div class="thumb abs" style="left:270px;top:640px;width:280px;transform:rotate(3deg)"><img src="png-v2/MA-FB3.png"></div>'
    '<div class="thumb abs" style="left:570px;top:645px;width:280px;transform:rotate(-3deg)"><img src="png-v2/SA-FB3.png"></div>' +
    cta("Dites-nous ce que vous voulez voir", fs=34), "Facebook · Post récap (image)")

car_di("DI-IG1", P, "Instagram")

add("DI-IG3-1", "s", "n",
    logo(64, 120) + pg("1 / 2") +
    ph(V2 + "agent-pouce@2x.jpg", 120, 260, 840, 760, "center 25%", "cover", -2) +
    tb('<div class="k">Récap de la semaine</div>', 64, 1080, 900) +
    tb('<div class="t l sh">[Contenu du récap à fournir]</div>', 64, 1130, 952),
    "Instagram · Story récap 1/2")
add("DI-IG3-2", "s", "r",
    B.rings(880, 420, (600, 820, 1040)) + logo(64, 120) + pg("2 / 2") +
    tb('<div class="t l sh">Quel sujet pour la semaine prochaine&nbsp;?</div>', 64, 420, 952) +
    tb(B.poll("Sondage", ["[Sujet 1 à confirmer]", "[Sujet 2 à confirmer]"]), 64, 820, 952) +
    '<div class="k abs" style="left:64px;bottom:120px">Votez dans le sondage ↑</div>',
    "Instagram · Story sondage 2/2")

CSS2 = """
.crea.free{display:block;padding:0;position:relative}
.abs{position:absolute}
.logo.abs{z-index:20}
.pg.abs{right:60px;top:84px;z-index:20}
.cta.abs{z-index:20}
.k.abs{z-index:20}
.full{position:absolute;inset:0;background-repeat:no-repeat;z-index:1}
.ph{position:absolute;background-repeat:no-repeat;border:14px solid #fff;box-shadow:0 30px 60px rgba(0,0,0,.4);z-index:4}
.tb{position:absolute;z-index:8}
.hd{position:absolute;z-index:9;overflow:visible}
.numo{position:absolute;font-family:Archivo,sans-serif;font-weight:900;line-height:.85;color:transparent;-webkit-text-stroke:5px #fff;letter-spacing:-.04em;z-index:6}
.nb{position:absolute;width:76px;height:76px;border-radius:50%;background:#93241E;color:#fff;font:900 44px Archivo,sans-serif;display:flex;align-items:center;justify-content:center;z-index:7;box-shadow:0 10px 20px rgba(0,0,0,.35)}
.cap{position:absolute;text-align:center;font:800 30px Archivo,sans-serif;z-index:7}
.notif{position:absolute;background:rgba(255,255,255,.96);color:#0A3D57;border-radius:30px;padding:20px 24px;display:flex;align-items:center;gap:18px;z-index:12;box-shadow:0 20px 40px rgba(0,0,0,.35)}
.notif .av{width:64px;height:64px;border-radius:18px;display:flex;align-items:center;justify-content:center;flex:0 0 64px;color:#fff;padding:14px}
.notif .nt b{display:block;font:800 30px Archivo,sans-serif}
.notif .nt span{font:600 26px Inter;color:#93241E}
.notif .tm{margin-left:auto;font:600 24px Inter;color:#5B6B76;white-space:nowrap}
.bbl{position:absolute;border-radius:36px;padding:26px 32px;font-family:Archivo,sans-serif;font-weight:800;line-height:1.15;z-index:12;box-shadow:0 20px 40px rgba(0,0,0,.3)}
.bbl.w{background:#fff;color:#0A3D57}.bbl.b{background:#1690C1;color:#fff}.bbl.r{background:#93241E;color:#fff}
.bbl::after{content:"";position:absolute;width:0;height:0;border:18px solid transparent}
.bbl.t-bl::after{left:36px;bottom:-30px;border-top-color:inherit}
.bbl.w.t-bl::after,.bbl.w.t-tr::after,.bbl.w.t-br::after{border-top-color:#fff}
.bbl.b.t-br::after{border-top-color:#1690C1}
.bbl.t-br::after{right:36px;bottom:-30px}
.bbl.t-tr::after{right:40px;bottom:-30px}
.stk{position:absolute;border-radius:999px;padding:14px 26px;font-family:Archivo,sans-serif;font-weight:900;z-index:13;box-shadow:0 12px 24px rgba(0,0,0,.35);white-space:nowrap}
.stk.r{background:#93241E;color:#fff}.stk.w{background:#fff;color:#93241E}
.row-ch{position:absolute;left:56px;right:56px;display:flex;align-items:center;gap:26px;background:#EAF6FC;border-radius:30px;padding:0 30px;font:800 46px Archivo,sans-serif;color:#0A3D57;z-index:5}
.row-ch b{width:84px;height:84px;border-radius:50%;background:#1690C1;color:#fff;display:flex;align-items:center;justify-content:center;flex:0 0 84px}
.bigquote{position:absolute;left:40px;top:120px;font:900 420px/1 Archivo,sans-serif;opacity:.22;z-index:2}
.wordo{position:absolute;left:40px;right:40px;font:900 176px/1 Archivo,sans-serif;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:4px #fff;z-index:3}
.clock{width:360px;height:360px;border-radius:50%;background:#fff;color:#93241E;padding:70px;box-shadow:0 30px 60px rgba(0,0,0,.35);z-index:5}
.counter{font:900 330px/0.85 Archivo,sans-serif;letter-spacing:-.05em;z-index:5;text-shadow:0 14px 34px rgba(0,0,0,.3)}
.counter span{display:block;font-size:64px;letter-spacing:.02em;margin-top:10px}
.bigic.abs{width:190px;height:190px;padding:44px;z-index:5}
.glass{background:rgba(10,61,87,.82);border:2px solid rgba(255,255,255,.2);border-radius:36px;padding:40px;box-shadow:0 24px 50px rgba(0,0,0,.35)}
.sugg{display:flex;flex-wrap:wrap;gap:16px}
.sugg span{border:3px dashed rgba(255,255,255,.75);border-radius:999px;padding:16px 26px;font:800 36px Archivo,sans-serif}
.band{background:#93241E;border-radius:36px;padding:36px 40px;font:900 50px/1.15 Archivo,sans-serif;box-shadow:0 24px 50px rgba(0,0,0,.35);z-index:8}
.steps3{display:flex;gap:20px}
.steps3 div{flex:1;background:#EAF6FC;color:#0A3D57;border-radius:30px;padding:28px 20px;font:800 34px Archivo,sans-serif;text-align:center}
.steps3 b{display:flex;margin:0 auto 14px;width:76px;height:76px;border-radius:50%;background:#93241E;color:#fff;align-items:center;justify-content:center;font-size:42px}
.fearzone{left:0;right:0;top:0;height:640px;background:radial-gradient(700px 400px at 80% 20%,#FBEAE8 0%,#F6E3E1 60%);z-index:1}
.fearq{font:900 74px/1.1 Archivo,sans-serif;font-style:italic;color:#5E1712;letter-spacing:-.02em}
.engicon{left:450px;top:560px;width:180px;height:180px;border-radius:50%;background:#1690C1;color:#fff;padding:44px;box-shadow:0 20px 40px rgba(10,61,87,.35);z-index:6;border:8px solid #fff}
.engt{font:900 76px/1.08 Archivo,sans-serif;color:#0A3D57;letter-spacing:-.02em}
.split-l,.split-r{top:0;bottom:0;width:50%;background-size:cover;background-position:center 25%;z-index:1}
.split-l{left:0;filter:grayscale(1) brightness(.8)}
.split-r{right:0}
.split-cut{left:calc(50% - 9px);top:0;bottom:0;width:18px;background:#93241E;transform:skewX(-6deg);z-index:2}
.titleband{left:0;right:0;bottom:0;background:linear-gradient(180deg,rgba(14,106,150,.0) 0%,rgba(14,106,150,.92) 22%,#0E6A96 100%);padding:140px 56px 90px;z-index:5}
.cph.abs{border-radius:50%;background-repeat:no-repeat;box-shadow:0 40px 70px rgba(0,0,0,.45);z-index:3}
.cring.abs{border-radius:50%;border:6px dashed rgba(255,255,255,.7);z-index:3}
.guide.abs{z-index:3}
.phold.abs{width:240px;height:240px}
.thumb.abs{z-index:3}
.note.abs{z-index:6}
.idisc{border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.35);z-index:6;border:10px solid #fff}
.idisc svg{width:100%;height:100%}
.fcol,.ecol{position:absolute;top:300px;width:470px;height:800px;border-radius:44px;z-index:2}
.fcol{left:56px;background:#FBEAE8}
.ecol{left:554px;background:#1690C1}
.fname{font:900 70px/1.02 Archivo,sans-serif;color:#5E1712;letter-spacing:-.03em;font-style:italic}
.engt2{font:900 62px/1.1 Archivo,sans-serif;color:#fff;letter-spacing:-.02em}
.slist{display:flex;flex-direction:column;gap:18px}
.srow{display:flex;align-items:center;gap:24px;background:#EAF6FC;color:#0A3D57;border-radius:30px;padding:22px 28px;font:800 36px/1.2 Archivo,sans-serif}
.srow b{width:76px;height:76px;flex:0 0 76px;border-radius:50%;background:#93241E;color:#fff;display:flex;align-items:center;justify-content:center;font-size:42px}
"""


def main():
    body = B.defs() + "".join(
        f'<div class="wrap"><h4>{cid} · {label}</h4><div class="crea free {size} {bg}" id="{cid}">{html}</div></div>'
        for cid, size, bg, html, label in CREAS)
    for a, b in ((' ?', '&nbsp;?'), (' !', '&nbsp;!'), (' :', '&nbsp;:'), (' ;', '&nbsp;;'), (' »', '&nbsp;»'), ('« ', '«&nbsp;')):
        body = body.replace(a, b)
    page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>FS Express · Semaine 1 · v2</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,700;0,800;0,900;1,900&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>{B.CSS}{CSS2}</style></head><body>{body}</body></html>'''
    open("creas-v2.html", "w", encoding="utf-8").write(page)
    print(len(CREAS), "visuels")


if __name__ == "__main__":
    main()
