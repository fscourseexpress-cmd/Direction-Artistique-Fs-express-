"""Génère creas.html : toutes les créas non vidéo de la semaine 1 (FS Express).

Usage : python3 build.py  puis  node export.js
Palette FS Express uniquement : bleu #1690C1, rouge #93241E, blanc et leurs nuances.
"""
import random

WA = "687 53 53 73"
CTA_WA = f"Envoyez votre première livraison sur WhatsApp : {WA}"

ICONS = {
    "phone-off": '<path d="M10.7 13.3a16 16 0 0 0 3.4 2.6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 3.1 4.2 2 2 0 0 1 5.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L9 9.9"/><path d="M23 1L1 23"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "id": '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="12" r="2.5"/><path d="M13 10h5M13 14h4"/>',
    "moto": '<circle cx="5.5" cy="16" r="3.5"/><circle cx="18.5" cy="16" r="3.5"/><path d="M5.5 16l4-7h5l4 7M14.5 9l1.5-3h3"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5z"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M3.3 7L12 12l8.7-5M12 22V12"/>',
    "x": '<circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/>',
    "alert": '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h16.9a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "check": '<path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="M22 4L12 14l-3-3"/>',
    "up": '<path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>',
    "store": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "zap": '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>',
    "send": '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/>',
    "map": '<path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4z"/><path d="M8 2v16M16 6v16"/>',
    "battery": '<rect x="1" y="6" width="18" height="12" rx="2"/><path d="M23 13v-2"/><rect x="4" y="9" width="3" height="6" fill="currentColor"/>',
    "frown": '<circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2M9 9h.01M15 9h.01"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "package-x": '<path d="M21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="M9 9l6 6M15 9l-6 6"/>',
    "repeat": '<path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
}

def defs():
    sy = "".join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
        for k, v in ICONS.items())
    return f'<svg class="defs" aria-hidden="true">{sy}</svg>'

def ico(name, cls=""):
    return f'<svg class="i {cls}"><use href="#i-{name}"/></svg>'

def logo(cls=""):
    return f'<div class="logo {cls}"><img src="assets/logo.jpg" alt="Logo FS Express"></div>'

def hdr(right=""):
    return f'<div class="hdr">{logo()}<div class="pg">{right}</div></div>'

def cta(text, v=""):
    return f'<div class="cta {v}">{text}</div>'

def torn(cx, cy, r, w, h, seed=7):
    rnd = random.Random(seed)
    def pts(r0, amp):
        out = []
        n = 120
        for i in range(n):
            import math
            t = i / n * 2 * math.pi
            rr = r0 + (rnd.random() - .5) * amp + (amp * .35 if i % 2 else -amp * .2)
            out.append(f"{cx + math.cos(t) * rr * 1.02:.1f},{cy + math.sin(t) * rr * 1.12:.1f}")
        return " ".join(out)
    return f'''<svg class="deco" style="left:0;top:0;width:{w}px;height:{h}px" viewBox="0 0 {w} {h}">
<defs><radialGradient id="hin{seed}" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#EAF6FC"/><stop offset="1" stop-color="#9FD3EC"/></radialGradient>
<filter id="hs{seed}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#3A0E0A" flood-opacity=".55"/></filter></defs>
<polygon points="{pts(r + 46, 60)}" fill="#C2463B" filter="url(#hs{seed})"/>
<polygon points="{pts(r + 20, 46)}" fill="#F4D9D5"/>
<polygon points="{pts(r, 36)}" fill="url(#hin{seed})"/></svg>'''

def rings(x, y, sizes=(820, 1040, 1240), disc=None):
    s = ""
    if disc:
        s += f'<div class="deco disc" style="left:{x - disc[0] // 2}px;top:{y - disc[0] // 2}px;width:{disc[0]}px;height:{disc[0]}px;background:{disc[1]}"></div>'
    for z in sizes:
        s += f'<div class="deco ring" style="left:{x - z // 2}px;top:{y - z // 2}px;width:{z}px;height:{z}px"></div>'
    return s

def num(n, cls=""):
    return f'<div class="num {cls}">{n}</div>'

def pbg(src, pos="center", ov="n"):
    return f'<div class="deco pbg" style="background-image:url(assets/{src});background-position:{pos}"></div><div class="deco ov ov-{ov}"></div>'

def poll(question, opts):
    o = "".join(f'<div class="opt"><span>{x}</span></div>' for x in opts)
    return f'<div class="poll"><div class="pq">{question}</div>{o}</div>'

def qsticker(label):
    return f'<div class="qs"><div class="qh">{label}</div><div class="qi">Votre réponse…</div></div>'

def linksticker(text):
    return f'<div class="lk">{ico("link")}<span>{text}</span></div>'

def mapdeco(w, h, pins=((.3, .35), (.62, .28), (.72, .62), (.4, .7), (.18, .58), (.55, .48))):
    roads = f'''<svg class="deco" style="left:0;top:0;width:{w}px;height:{h}px" viewBox="0 0 100 100" preserveAspectRatio="none">
<path d="M-5 30 C 20 25, 35 45, 55 40 S 85 20, 105 28" stroke="#7CCBEA" stroke-opacity=".35" stroke-width=".9" fill="none"/>
<path d="M10 -5 C 15 30, 30 50, 25 105" stroke="#7CCBEA" stroke-opacity=".3" stroke-width=".7" fill="none"/>
<path d="M60 -5 C 55 25, 70 55, 62 105" stroke="#7CCBEA" stroke-opacity=".3" stroke-width=".8" fill="none"/>
<path d="M-5 70 C 25 65, 45 80, 70 72 S 95 60, 105 66" stroke="#7CCBEA" stroke-opacity=".3" stroke-width=".7" fill="none"/>
<path d="M30 0 L 85 100 M0 50 L 100 52" stroke="#7CCBEA" stroke-opacity=".18" stroke-width=".5" fill="none"/></svg>'''
    p = "".join(f'<div class="deco mpin" style="left:{x * w - 30:.0f}px;top:{y * h - 70:.0f}px">{ico("pin")}</div>' for x, y in pins)
    return roads + p

CREAS = []  # (id, size, bg, html, label)

def add(cid, size, bg, html, label):
    CREAS.append((cid, size, bg, html, label))

# ============================ LUNDI ============================
def car_3situations(prefix, size, platform):
    n = 5
    add(f"{prefix}-1", size, "n", pbg("dos-fs.jpg", "center 35%", "n2") + hdr("01 / 05") +
        '<div class="mid end"><div class="k">Vendeurs en ligne</div>'
        '<div class="t xl sh">3 situations qui font perdre <span class="hl r">une vente.</span></div>'
        '<div class="sub">Une vente conclue n\'est pas une vente encaissée.</div></div>'
        '<div class="ftr"><div class="k">Glissez →</div></div>', f"{platform} · Carrousel 1/5")
    data = [
        ("r", "1", "phone-off", "Le livreur injoignable.", "Le colis est parti. Le livreur ne répond plus."),
        ("b", "2", "clock", "Le retard qui s'allonge.", "Le client attend, relance, puis annule."),
        ("n", "3", "cash", "Le cash qui tarde à revenir.", "Vendu aujourd'hui. Encaissé… on ne sait pas quand."),
    ]
    for i, (bg, nn, ic, t, s) in enumerate(data, start=2):
        add(f"{prefix}-{i}", size, bg, rings(930, 160, (520, 720, 920)) + hdr(f"0{i} / 05") +
            f'<div class="mid"><div class="row">{num(nn)}<div class="bigic">{ico(ic)}</div></div>'
            f'<div class="t l sh">{t}</div><div class="sub">{s}</div></div>'
            '<div class="ftr"><div class="k">Glissez →</div></div>', f"{platform} · Carrousel {i}/5")
    last_cta = "Votez en commentaire : 1, 2 ou 3" if platform == "Facebook" else "Enregistrez ce post"
    add(f"{prefix}-5", size, "w", hdr('<span style="color:#0A3D57">05 / 05</span>') +
        '<div class="mid"><div class="t l" style="color:#0A3D57">Laquelle vous coûte <span class="hl r" style="color:#fff">le plus ?</span></div>'
        '<div class="choices"><div class="ch"><b>1</b>Le livreur injoignable</div><div class="ch"><b>2</b>Le retard</div><div class="ch"><b>3</b>Le cash qui tarde</div></div></div>'
        f'<div class="ftr">{cta(last_cta, "red")}</div>', f"{platform} · Carrousel 5/5")

car_3situations("LU-FB2", "sq", "Facebook")

add("LU-FB3", "p", "r", rings(540, 1000, (980, 1180)) + hdr() +
    '<div class="mid top"><div class="t xl sh">Vous vendez.</div>'
    '<div class="t xl"><span class="hl w">On livre.</span></div>'
    '<div class="sub" style="max-width:520px">Vous avez fait le plus dur : vendre. FS Express s\'occupe du reste.</div></div>'
    '<div class="deco cph" style="left:430px;top:560px;width:600px;height:600px;background-image:url(assets/remise-fs.jpg);background-size:1600px auto;background-position:-354px -921px"></div>'
    '<div class="deco cring" style="left:400px;top:530px;width:660px;height:660px"></div>'
    f'<div class="ftr">{cta(CTA_WA)}</div>', "Facebook · Affiche")

car_3situations("LU-IG2", "p", "Instagram")

add("LU-IG3", "s", "b", rings(900, 380, (600, 820, 1040), disc=(520, "#93241E")) + hdr() +
    '<div class="mid"><div class="t l sh">Quel est votre pire souvenir de livraison ?</div>'
    + poll("Sondage", ["Livreur injoignable", "Retard", "Cash qui tarde"]) +
    '</div><div class="ftr"><div class="k">Votez dans le sondage ↑</div></div>', "Instagram · Story sondage")

# ============================ MARDI ============================
add("MA-FB1", "p", "r", rings(980, 200, (520, 760, 980)) + hdr() +
    '<div class="mid"><div class="quote">“</div>'
    '<div class="t l sh" style="font-style:italic">Il va croire que je suis une arnaque.</div>'
    '<div class="sub">Quand un client relance pour la 3<sup>e</sup> fois, ce n\'est pas qu\'un retard : c\'est votre réputation en jeu.</div></div>'
    '<div class="ftr"><div class="pill w">On sait ce que ça fait.</div></div>', "Facebook · Visuel citation")

add("MA-FB3", "p", "n", hdr() +
    '<div class="mid top"><div class="t l sh">Le soir, on compte ce qui est <span class="hl r">vraiment rentré.</span></div></div>'
    '<div class="deco ledger"><div class="lh">Carnet de ventes</div>'
    '<div class="ll"><span>Robe wax</span><span>15 000</span></div>'
    '<div class="ll"><span>Sac à main</span><span class="ko">12 500</span></div>'
    '<div class="ll"><span>Chaussures</span><span>18 000</span></div>'
    '<div class="ll"><span>Parfum</span><span class="ko">9 000</span></div>'
    '<div class="ll tot"><span>Vendu</span><span>54 500</span></div>'
    '<div class="ll tot r"><span>Encaissé</span><span>33 000</span></div></div>'
    '<div class="ph3 deco" style="left:640px;top:760px;width:340px;height:520px"><div class="scr">'
    '<div class="bar">Paiements</div><div class="bub w" style="left:20px;top:110px">Cash en attente…</div>'
    '<div class="bub r" style="right:20px;top:230px">Toujours rien ?</div></div></div>'
    f'<div class="ftr">{cta("Répondez en commentaire", "red")}</div>', "Facebook · Post question (image)")

emotions = [
    ("Angoisse", "Et s'il n'arrivait jamais ?", "alert", "r"),
    ("Honte", "Mon client va croire que je suis une arnaque.", "frown", "b"),
    ("Impuissance", "Je ne peux rien faire. Il ne répond pas.", "phone-off", "n"),
    ("Fatigue", "Vingt appels aujourd'hui. Pour un seul colis.", "battery", "r"),
]
add("MA-IG1-1", "p", "n", pbg("dos-fs.jpg", "center 30%", "n2") + hdr("01 / 06") +
    '<div class="mid end"><div class="t xl sh">Ce que personne ne voit derrière une <span class="hl r">livraison ratée.</span></div></div>'
    '<div class="ftr"><div class="k">Glissez →</div></div>', "Instagram · Carrousel 1/6")
for i, (w, q, ic, bg) in enumerate(emotions, start=2):
    add(f"MA-IG1-{i}", "p", bg, rings(900, 260, (560, 780, 1000)) + hdr(f"0{i} / 06") +
        f'<div class="mid"><div class="bigic">{ico(ic)}</div><div class="word">{w}</div>'
        f'<div class="qcard">« {q} »</div></div>'
        '<div class="ftr"><div class="k">Glissez →</div></div>', f"Instagram · Carrousel {i}/6")
add("MA-IG1-6", "p", "w", hdr('<span style="color:#0A3D57">06 / 06</span>') +
    '<div class="mid"><div class="t xl" style="color:#0A3D57">On <span class="hl r" style="color:#fff">connaît.</span></div>'
    '<div class="sub" style="color:#0A3D57">Vous n\'êtes pas seul. Un commerçant devrait passer son temps à vendre, pas à courir après ses livraisons.</div></div>'
    f'<div class="ftr">{cta("Enregistrez et envoyez à un vendeur qui en a besoin", "red")}</div>', "Instagram · Carrousel 6/6")

add("MA-IG3", "s", "r", rings(850, 420, (600, 820, 1040)) + hdr() +
    '<div class="mid"><div class="k">Terminez la phrase</div>'
    '<div class="t l sh">Un commerçant devrait passer son temps à…</div>'
    + qsticker("Complétez la phrase") +
    '</div><div class="ftr"><div class="k">Répondez à la story ↑</div></div>', "Instagram · Story question")

# ============================ MERCREDI ============================
add("ME-FB3-1", "sq", "b", mapdeco(1080, 1080, ((.55, .22), (.85, .2), (.9, .75), (.7, .88), (.2, .88))) + hdr("01 / 04") +
    '<div class="mid"><div class="t l sh">Une commande à l\'autre bout de la ville ?</div>'
    '<div class="t l"><span class="hl r">Ne la refusez plus.</span></div></div>'
    '<div class="ftr"><div class="k">Glissez →</div></div>', "Facebook · Carrousel 1/4")
add("ME-FB3-2", "sq", "n", mapdeco(1080, 1080, ((.22, .4), (.5, .3), (.78, .36), (.3, .68), (.62, .62), (.84, .72), (.46, .5))) + hdr("02 / 04") +
    '<div class="mid end"><div class="t m sh">Nos livreurs partenaires couvrent les différentes zones de Yaoundé.</div>'
    '<div class="pill w" style="align-self:flex-start">[Liste des zones à compléter]</div></div>', "Facebook · Carrousel 2/4")
add("ME-FB3-3", "sq", "r", torn(790, 640, 270, 1080, 1080, seed=11) + hdr("03 / 04") +
    '<div class="mid top" style="max-width:520px"><div class="t xl sh">Vous vendez.</div><div class="t xl"><span class="hl w">On livre.</span></div></div>'
    '<img class="cut" src="assets/livreur-fs.png" style="left:470px;top:300px;width:760px">', "Facebook · Carrousel 3/4")
add("ME-FB3-4", "sq", "w", hdr('<span style="color:#0A3D57">04 / 04</span>') +
    '<div class="mid"><div class="t l" style="color:#0A3D57">Toute la ville. <span class="hl b" style="color:#fff">Un seul message.</span></div></div>'
    f'<div class="ftr">{cta("Demandez votre livraison sur WhatsApp : " + WA, "red")}</div>', "Facebook · Carrousel 4/4")

add("ME-IG3-1", "s", "r", torn(640, 1150, 380, 1080, 1920, seed=21) + hdr("1 / 3") +
    '<div class="mid top"><div class="k">Nos engagements</div><div class="t xl sh">Livreurs identifiés.</div>'
    '<div class="chips"><span>' + ico("id") + 'Permis</span><span>' + ico("shield") + 'Assurance</span><span>' + ico("moto") + 'Moto immatriculée</span></div></div>'
    '<img class="cut" src="assets/livreur-fs.png" style="left:180px;top:780px;width:1000px">', "Instagram · Story 1/3")
add("ME-IG3-2", "s", "b", rings(540, 1180, (900, 1100, 1300)) + hdr("2 / 3") +
    '<div class="mid top"><div class="k">Nos engagements</div><div class="t xl sh">Argent reversé <span class="hl r">vite.</span></div>'
    '<div class="sub">Cash plafonné par livreur, reversé rapidement.</div></div>'
    '<div class="deco cph" style="left:190px;top:880px;width:700px;height:700px;background-image:url(assets/remise-fs.jpg);background-size:1700px auto;background-position:-344px -945px"></div>'
    '<div class="deco cring" style="left:160px;top:850px;width:760px;height:760px"></div>', "Instagram · Story 2/3")
add("ME-IG3-3", "s", "n", rings(900, 500, (600, 820, 1040)) + hdr("3 / 3") +
    '<div class="mid"><div class="k">Nos engagements</div><div class="bigic">' + ico("phone") + '</div>'
    '<div class="t l sh">Un appel de validation avant chaque course.</div>'
    '<div class="sub">Et un interlocuteur dédié qui vous répond.</div>' + linksticker("Écrivez-nous sur WhatsApp · " + WA) +
    '</div>', "Instagram · Story 3/3")

# ============================ JEUDI ============================
steps = [
    ("chat", "Vous envoyez la commande sur WhatsApp et on la confirme."),
    ("moto", "Un livreur de votre zone vient la récupérer."),
    ("check", "Votre client est livré et vous recevez votre argent."),
]
add("JE-FB1-1", "sq", "b", rings(900, 200, (560, 780, 1000)) + hdr("01 / 05") +
    '<div class="mid"><div class="t xl sh">3 étapes,</div><div class="t xl"><span class="hl r">pas une de plus.</span></div>'
    '<div class="sub">Livrer avec FS Express, c\'est simple.</div></div>'
    '<div class="ftr"><div class="k">Glissez →</div></div>', "Facebook · Carrousel 1/5")
for i, (ic, t) in enumerate(steps, start=1):
    bg = ["r", "n", "b"][i - 1]
    add(f"JE-FB1-{i + 1}", "sq", bg, rings(900, 200, (560, 780, 1000)) + hdr(f"0{i + 1} / 05") +
        f'<div class="mid"><div class="row">{num(str(i))}<div class="bigic">{ico(ic)}</div></div><div class="t m sh">{t}</div></div>'
        '<div class="ftr"><div class="k">Glissez →</div></div>', f"Facebook · Carrousel {i + 1}/5")
add("JE-FB1-5", "sq", "w", hdr('<span style="color:#0A3D57">05 / 05</span>') +
    '<div class="mid"><div class="t l" style="color:#0A3D57">Prêt pour votre <span class="hl r" style="color:#fff">première livraison ?</span></div></div>'
    f'<div class="ftr">{cta(CTA_WA, "red")}</div>', "Facebook · Carrousel 5/5")

add("JE-FB3", "p", "b", hdr() +
    '<div class="mid top" style="max-width:560px"><div class="k">Question fréquente</div>'
    '<div class="t m sh">Qui me rappelle avant chaque course ?</div>'
    '<div class="sub">Votre interlocuteur dédié. Vous savez où est votre colis, sans relancer 20 fois.</div></div>'
    '<div class="ph3 deco" style="left:600px;top:250px;width:420px;height:860px"><div class="scr">'
    '<div class="bar">FS Express · Interlocuteur dédié</div>'
    '<div class="bub w" style="left:18px;top:110px">Bonjour ! Je confirme votre course : retrait à 14 h.</div>'
    '<div class="bub b" style="right:18px;top:270px">Parfait, merci !</div>'
    '<div class="bub w" style="left:18px;top:380px">Colis récupéré. Je vous préviens à la livraison.</div>'
    '<div class="bub w" style="left:18px;top:540px">Livré ! Votre client a bien reçu son colis.</div>'
    '<div class="bub b" style="right:18px;top:700px">Top 👍</div></div></div>'
    '<div class="deco note" style="left:600px;top:1125px">Exemple de conversation</div>'
    f'<div class="ftr">{cta("Une question ? Écrivez-nous sur WhatsApp : " + WA)}</div>', "Facebook · Post FAQ (image)")

pairs = [
    ("« Mon client attend et je ne sais rien. »", "Un interlocuteur dédié qui vous répond.", "Angoisse, honte"),
    ("« Je ne connais pas ce livreur. »", "Des livreurs identifiés, assurés, en règle.", "Méfiance"),
    ("« Et si mon argent disparaît ? »", "Cash plafonné par livreur et reversé vite.", "Cash"),
    ("« Je ne sais pas où est mon colis. »", "Un appel de validation avant chaque course.", "Perte de contrôle"),
    ("« Personne ne va là-bas. »", "Toute la ville couverte.", "Commandes refusées"),
]
add("JE-IG2-1", "p", "r", torn(620, 900, 330, 1080, 1350, seed=31) + hdr("01 / 06") +
    '<div class="mid top"><div class="t xl sh">Vos peurs,</div><div class="t xl"><span class="hl w">nos engagements.</span></div></div>'
    '<img class="cut" src="assets/livreur-fs.png" style="left:330px;top:620px;width:800px">', "Instagram · Carrousel 1/6")
for i, (fear, eng, lab) in enumerate(pairs, start=2):
    extra = f'<div class="ftr">{cta("Enregistrez ce post", "red")}</div>' if i == 6 else '<div class="ftr"><div class="k" style="color:#0A3D57">Glissez →</div></div>'
    add(f"JE-IG2-{i}", "p", "w", hdr(f'<span style="color:#0A3D57">0{i} / 06</span>') +
        f'<div class="mid"><div class="pair"><div class="pc fear"><div class="pl">Peur · {lab}</div><div class="pt">{fear}</div></div>'
        f'<div class="arrow">↓</div><div class="pc eng"><div class="pl">Engagement FS Express</div><div class="pt">{eng}</div></div></div></div>'
        + extra, f"Instagram · Carrousel {i}/6")

add("JE-IG3", "s", "b", rings(540, 1450, (900, 1100, 1300), disc=(760, "#0E6A96")) + hdr() +
    '<div class="mid top"><div class="t l sh">Une commande à livrer demain ?</div>'
    '<div class="t l"><span class="hl r">Envoyez-la nous.</span></div>'
    '<div class="mini"><div><b>1</b>Message WhatsApp</div><div><b>2</b>On récupère</div><div><b>3</b>Client livré</div></div>'
    + linksticker("WhatsApp · " + WA) + '</div>'
    '<img class="cut" src="assets/livreur-fs.png" style="left:160px;top:1080px;width:900px">', "Instagram · Story lien")

# ============================ VENDREDI ============================
add("VE-IG2-MODELE", "p", "r", rings(900, 300, (560, 780, 1000)) + hdr("MODÈLE") +
    '<div class="mid"><div class="quote">“</div><div class="t l sh" style="font-style:italic">[Citation du commerçant]</div>'
    '<div class="row" style="gap:28px"><div class="phold">Photo du commerçant<br>(avec accord)</div>'
    '<div class="sub"><b>[Nom du commerçant]</b><br>[Activité]</div></div></div>'
    f'<div class="ftr">{cta(CTA_WA)}</div>', "Instagram · Affiche citation (modèle à compléter)")

# ============================ SAMEDI ============================
add("SA-FB1", "p", "n", rings(900, 300, (560, 780, 1000)) + hdr() +
    '<div class="mid"><div class="t l sh">Une livraison ratée coûte plus <span class="hl r">qu\'une vente.</span></div>'
    '<div class="costs"><div>' + ico("users") + 'Un client qui ne revient pas</div><div>' + ico("star") + 'Un avis négatif</div><div>' + ico("chat") + 'Une histoire racontée autour de lui</div></div></div>'
    f'<div class="ftr">{cta("Ne laissez pas un livreur décider si ça marche : WhatsApp " + WA)}</div>', "Facebook · Post image")

add("SA-FB3", "p", "b", mapdeco(1080, 1350, ((.9, .2), (.88, .4), (.62, .9), (.12, .9))) + hdr() +
    '<div class="mid top"><div class="t l sh">Vendez partout</div><div class="t l"><span class="hl r">à Yaoundé.</span></div>'
    '<div class="sub" style="max-width:430px">Acceptez enfin les commandes de toute la ville.</div></div>'
    '<img class="cut" src="assets/livreur-fs.png" style="left:470px;top:560px;width:720px">'
    f'<div class="ftr">{cta(CTA_WA)}</div>', "Facebook · Affiche")

ba = [("Débordé", "Chef d'entreprise"), ("Petit business", "Marque recommandée"),
      ("Vend dans son quartier", "Vend dans tout Yaoundé"), ("Subit", "Garde le contrôle")]
add("SA-IG1-1", "p", "b", rings(900, 260, (560, 780, 1000), disc=(420, "#93241E")) + hdr("01 / 05") +
    '<div class="mid"><div class="t xl sh">De vendeur débordé</div><div class="t xl"><span class="hl r">à chef d\'entreprise.</span></div></div>'
    '<div class="ftr"><div class="k">Glissez →</div></div>', "Instagram · Carrousel 1/5")
for i, (av, ap) in enumerate(ba, start=2):
    extra = f'<div class="ftr">{cta(CTA_WA, "red")}</div>' if i == 5 else '<div class="ftr"><div class="k" style="color:#0A3D57">Glissez →</div></div>'
    add(f"SA-IG1-{i}", "p", "w", hdr(f'<span style="color:#0A3D57">0{i} / 05</span>') +
        f'<div class="mid"><div class="ba"><div class="bb av"><div class="pl">Avant</div><div class="bt">{av}</div></div>'
        f'<div class="bb ap"><div class="pl">Après</div><div class="bt">{ap}</div></div></div></div>' + extra,
        f"Instagram · Carrousel {i}/5")

add("SA-IG3", "s", "b", rings(880, 480, (600, 820, 1040), disc=(420, "#93241E")) + hdr() +
    '<div class="mid"><div class="t l sh">Dans un an, votre boutique ressemble à quoi ?</div>'
    '<div class="sub">Une marque connue ? Une équipe ? Une boutique physique ?</div>'
    + qsticker("Dans un an, ma boutique…") + '</div>'
    '<div class="ftr"><div class="k">Répondez à la story ↑</div></div>', "Instagram · Story question")

# ============================ DIMANCHE ============================
add("DI-FB1", "p", "r", rings(780, 820, (760, 960, 1160)) + hdr() +
    '<div class="mid top"><div class="t m sh">Pas encore prêt à changer de livreur ?</div><div class="sub">Commencez par ne plus perdre de ventes.</div></div>'
    '<div class="deco guide"><div class="gk">Guide gratuit</div><div class="gt">5 erreurs qui font perdre des ventes aux vendeurs en ligne à Yaoundé</div>'
    '<div class="gl"><img src="assets/logo.jpg" alt=""></div></div>'
    f'<div class="ftr">{cta("Commentez « GUIDE » et on vous l\'envoie")}</div>', "Facebook · Post visuel (couverture du guide)")

def car_erreurs(prefix, size, platform):
    add(f"{prefix}-1", size, "n", rings(900, 200, (560, 780, 1000)) + hdr("01 / 05") +
        '<div class="mid"><div class="k">Avant-goût du guide</div><div class="t xl sh">3 erreurs à éviter</div>'
        '<div class="t l"><span class="hl r">quand on vend en ligne.</span></div></div>'
        '<div class="ftr"><div class="k">Glissez →</div></div>', f"{platform} · Carrousel 1/5")
    err = [("Des délais de livraison flous.", "« Bientôt » ne rassure personne.", "clock", "r"),
           ("Un emballage négligé.", "Un colis abîmé, c'est votre image qui arrive.", "box", "b"),
           ("Aucun suivi après l'achat.", "Un message après la livraison fidélise.", "chat", "n")]
    for i, (t, s, ic, bg) in enumerate(err, start=2):
        add(f"{prefix}-{i}", size, bg, rings(900, 200, (560, 780, 1000)) + hdr(f"0{i} / 05") +
            f'<div class="mid"><div class="row">{num(str(i - 1))}<div class="bigic">{ico(ic)}</div></div>'
            f'<div class="t l sh">{t}</div><div class="sub">{s}</div></div>'
            '<div class="ftr"><div class="k">Glissez →</div></div>', f"{platform} · Carrousel {i}/5")
    add(f"{prefix}-5", size, "w", hdr('<span style="color:#0A3D57">05 / 05</span>') +
        '<div class="mid"><div class="t l" style="color:#0A3D57">Les 2 autres sont <span class="hl r" style="color:#fff">dans le guide.</span></div></div>'
        f'<div class="ftr">{cta("Commentez « GUIDE » pour recevoir les 5 erreurs", "red")}</div>', f"{platform} · Carrousel 5/5")

car_erreurs("DI-FB2", "sq", "Facebook")

add("DI-FB3", "p", "b", hdr() +
    '<div class="mid top"><div class="t l sh">Merci pour cette semaine !</div>'
    '<div class="sub">Livreur injoignable, honte, cash qui tarde : merci pour vos réponses.</div></div>'
    '<div class="deco thumb" style="left:120px;top:545px;width:300px;transform:rotate(-5deg)"><img src="png/LU-FB1.png"></div>'
    '<div class="deco thumb" style="left:640px;top:540px;width:300px;transform:rotate(4deg)"><img src="png/MA-FB1.png"></div>'
    '<div class="deco thumb" style="left:260px;top:780px;width:300px;transform:rotate(3deg)"><img src="png/ME-FB1.png"></div>'
    '<div class="deco thumb" style="left:570px;top:785px;width:300px;transform:rotate(-3deg)"><img src="png/JE-FB2.png"></div>'
    f'<div class="ftr">{cta("Dites-nous ce que vous voulez voir")}</div>', "Facebook · Post récap (image)")

car_erreurs("DI-IG1", "p", "Instagram")

add("DI-IG3-1", "s", "n", rings(880, 420, (600, 820, 1040)) + hdr("1 / 2") +
    '<div class="mid"><div class="k">Récap de la semaine</div><div class="t l sh">Votre semaine en 4 mots.</div>'
    '<div class="words"><span>Livreur injoignable</span><span>Honte</span><span>Fatigue</span><span>Cash qui tarde</span></div>'
    '<div class="sub">Merci pour toutes vos réponses.</div></div>', "Instagram · Story récap 1/2")
add("DI-IG3-2", "s", "r", rings(880, 420, (600, 820, 1040)) + hdr("2 / 2") +
    '<div class="mid"><div class="t l sh">Quel sujet pour la semaine prochaine ?</div>'
    + poll("Sondage", ["L'emballage", "Les retours clients", "La fidélisation"]) +
    '</div><div class="ftr"><div class="k">Votez dans le sondage ↑</div></div>', "Instagram · Story sondage 2/2")

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#EEF6FA;font-family:Inter,sans-serif;padding:24px;display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
body.export{background:none;padding:0;display:block}
body.export .crea{zoom:1}
body:not(.export) .crea{zoom:.3}
.wrap h4{font:700 13px Inter;color:#0A3D57;padding:6px 0}
.defs{position:absolute;width:0;height:0;overflow:hidden}
.crea{position:relative;overflow:hidden;color:#fff;display:flex;flex-direction:column;padding:56px;gap:36px}
.sq{width:1080px;height:1080px}.p{width:1080px;height:1350px}.s{width:1080px;height:1920px;padding:120px 64px 150px}
.r{background:radial-gradient(900px 800px at 75% 25%,#C2463B 0%,#93241E 45%,#5E1712 100%)}
.b{background:radial-gradient(900px 800px at 80% 20%,#3BB0E0 0%,#1690C1 40%,#0E6A96 75%,#0A4E70 100%)}
.n{background:radial-gradient(900px 700px at 20% 10%,#1B6C92 0%,rgba(27,108,146,0) 60%),linear-gradient(170deg,#0A3D57 0%,#06283A 100%)}
.w{background:radial-gradient(800px 600px at 90% 10%,#D6EEF9 0%,rgba(214,238,249,0) 60%),#fff;color:#0A3D57}
.deco{position:absolute;z-index:1;pointer-events:none}
.ring{border-radius:50%;border:3px solid rgba(255,255,255,.18)}
.w .ring{border-color:rgba(22,144,193,.2)}
.disc{border-radius:50%}
.pbg{inset:0;background-size:cover}
.ov{inset:0}
.ov-n{background:linear-gradient(180deg,rgba(10,61,87,.2) 0%,rgba(10,61,87,.5) 45%,rgba(10,61,87,.95) 100%)}
.ov-n2{background:linear-gradient(180deg,rgba(10,61,87,.55) 0%,rgba(10,61,87,.35) 35%,rgba(10,61,87,.92) 75%,rgba(10,61,87,.98) 100%)}
.hdr,.mid,.ftr{position:relative;z-index:5}
.hdr{display:flex;justify-content:space-between;align-items:center}
.logo{background:#fff;border-radius:22px;padding:12px 18px;box-shadow:0 14px 30px rgba(0,0,0,.25)}
.logo img{height:84px;display:block}
.pg{font:800 32px Archivo,sans-serif;opacity:.9}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px;min-height:0}
.mid.top{justify-content:flex-start;padding-top:30px}
.mid.end{justify-content:flex-end}
.t{font-family:Archivo,sans-serif;font-weight:900;letter-spacing:-.035em;line-height:.95}
.xl{font-size:112px}.l{font-size:88px}.m{font-size:66px}
.s .xl{font-size:128px}.s .l{font-size:100px}
.sh{text-shadow:0 10px 30px rgba(0,0,0,.3)}
.hl{display:inline-block;padding:.03em .18em .08em;border-radius:.14em;box-shadow:0 12px 26px rgba(0,0,0,.25)}
.hl.r{background:#93241E;color:#fff}.hl.w{background:#fff;color:#93241E}.hl.b{background:#1690C1;color:#fff}
.k{font:800 30px Inter;letter-spacing:.18em;text-transform:uppercase;opacity:.92}
.sub{font:500 40px/1.35 Inter;max-width:900px}
.s .sub{font-size:46px}
.cta{background:#fff;color:#93241E;border-radius:999px;padding:26px 40px;font:900 34px/1.2 Archivo,sans-serif;text-align:center;box-shadow:0 20px 44px rgba(0,0,0,.3)}
.cta.red{background:#93241E;color:#fff}
.pill{display:inline-block;border-radius:999px;padding:20px 34px;font:800 34px Archivo,sans-serif}
.pill.w{background:#fff;color:#93241E}
.i{width:100%;height:100%}
.row{display:flex;align-items:center;gap:40px}
.num{font:900 260px/0.85 Archivo,sans-serif;color:transparent;-webkit-text-stroke:5px #fff;letter-spacing:-.04em}
.bigic{width:150px;height:150px;border-radius:50%;background:#fff;color:#1690C1;padding:36px;box-shadow:0 18px 36px rgba(0,0,0,.3)}
.r .bigic{color:#93241E}
.quote{font:900 260px/0.6 Archivo,sans-serif;opacity:.35;height:120px}
.word{font:900 150px/1 Archivo,sans-serif;letter-spacing:-.04em;text-shadow:0 10px 30px rgba(0,0,0,.3)}
.qcard{background:#fff;color:#0A3D57;border-radius:36px;padding:40px 44px;font:800 54px/1.2 Archivo,sans-serif;font-style:italic;box-shadow:0 24px 50px rgba(0,0,0,.3)}
.choices{display:flex;flex-direction:column;gap:22px}
.ch{display:flex;align-items:center;gap:26px;background:#EAF6FC;border-radius:30px;padding:26px 30px;font:800 46px Archivo,sans-serif;color:#0A3D57}
.ch b{width:84px;height:84px;border-radius:50%;background:#1690C1;color:#fff;display:flex;align-items:center;justify-content:center;flex:0 0 84px}
.poll{background:#fff;color:#0A3D57;border-radius:40px;padding:40px;display:flex;flex-direction:column;gap:22px;box-shadow:0 30px 60px rgba(0,0,0,.3)}
.pq{font:800 32px Inter;letter-spacing:.16em;text-transform:uppercase;color:#1690C1}
.opt{border:3px solid #CDE7F3;border-radius:26px;padding:30px 34px;font:800 52px Archivo,sans-serif}
.qs{background:#fff;color:#0A3D57;border-radius:40px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.3)}
.qh{background:#93241E;color:#fff;font:800 44px/1.2 Archivo,sans-serif;padding:34px 40px}
.b .qh{background:#0A3D57}
.qi{padding:40px;font:600 44px Inter;color:#8AA3B0}
.lk{display:inline-flex;align-items:center;gap:20px;background:#fff;color:#1690C1;border-radius:999px;padding:26px 40px;font:900 40px Archivo,sans-serif;align-self:flex-start;box-shadow:0 20px 40px rgba(0,0,0,.3)}
.lk .i{width:48px;height:48px;flex:0 0 48px}
.cut{position:absolute;z-index:4;filter:drop-shadow(0 40px 50px rgba(0,0,0,.45))}
.cph{border-radius:50%;background-repeat:no-repeat;box-shadow:0 40px 70px rgba(0,0,0,.45);z-index:3}
.cring{border-radius:50%;border:6px dashed rgba(255,255,255,.7);z-index:3}
.mpin{width:60px;height:70px;color:#fff;filter:drop-shadow(0 8px 12px rgba(0,0,0,.35))}
.chips{display:flex;flex-wrap:wrap;gap:18px}
.chips span{display:inline-flex;align-items:center;gap:14px;background:#fff;color:#93241E;border-radius:999px;padding:18px 28px;font:800 38px Archivo,sans-serif}
.chips .i{width:42px;height:42px}
.mini{display:flex;flex-direction:column;gap:18px}
.mini div{display:flex;align-items:center;gap:20px;font:800 46px Archivo,sans-serif}
.mini b{width:74px;height:74px;border-radius:50%;background:#93241E;display:flex;align-items:center;justify-content:center;flex:0 0 74px}
.ledger{left:70px;top:560px;width:560px;background:#FBF7EE;color:#2A2A2A;border-radius:18px;padding:34px 36px;transform:rotate(-4deg);box-shadow:0 30px 60px rgba(0,0,0,.45);z-index:3;background-image:repeating-linear-gradient(180deg,transparent 0 63px,#D6E6EE 63px 65px)}
.lh{font:800 34px Archivo,sans-serif;color:#0A3D57;margin-bottom:12px}
.ll{display:flex;justify-content:space-between;font:600 34px/65px Inter}
.ll .ko{color:#93241E;text-decoration:line-through}
.ll.tot{font-weight:800;border-top:3px solid #0A3D57}
.ll.tot.r{color:#93241E;border-top:0;background:none}
.ph3{position:absolute;z-index:4;border-radius:56px;background:linear-gradient(150deg,#1D2F3A,#070F14);padding:16px;box-shadow:0 50px 80px rgba(0,0,0,.45),inset 0 0 0 3px #3A4E5A;transform:perspective(1200px) rotateY(-16deg) rotateX(5deg) rotateZ(3deg)}
.ph3 .scr{width:100%;height:100%;border-radius:42px;background:linear-gradient(180deg,#EAF7FD,#CFEAF7);position:relative;overflow:hidden}
.ph3 .bar{height:84px;background:#0A3D57;color:#fff;font:700 24px Inter;display:flex;align-items:center;padding:0 26px}
.bub{position:absolute;padding:20px 24px;border-radius:26px;font:700 28px/1.25 Inter;max-width:80%;box-shadow:0 8px 18px rgba(10,61,87,.18)}
.bub.w{background:#fff;color:#0A3D57;border-bottom-left-radius:8px}
.bub.r{background:#93241E;color:#fff;border-bottom-right-radius:8px}
.bub.b{background:#1690C1;color:#fff;border-bottom-right-radius:8px}
.note{font:600 24px Inter;color:#fff;opacity:.85;z-index:5}
.pair{display:flex;flex-direction:column;gap:20px}
.pc{border-radius:36px;padding:40px 44px;box-shadow:0 24px 50px rgba(10,61,87,.18)}
.pc.fear{background:#F6E3E1;color:#5E1712}
.pc.eng{background:#1690C1;color:#fff}
.pl{font:800 28px Inter;letter-spacing:.14em;text-transform:uppercase;opacity:.85;margin-bottom:14px}
.pt{font:900 62px/1.12 Archivo,sans-serif;letter-spacing:-.02em}
.fear .pt{font-style:italic}
.arrow{font:900 80px/1 Archivo,sans-serif;color:#93241E;text-align:center}
.ba{display:flex;flex-direction:column;gap:24px}
.bb{border-radius:36px;padding:44px}
.bb.av{background:#EEF2F4;color:#5B6B76}
.bb.av .bt{text-decoration:line-through;text-decoration-color:#93241E;text-decoration-thickness:8px}
.bb.ap{background:#93241E;color:#fff;box-shadow:0 24px 50px rgba(147,36,30,.35)}
.bt{font:900 86px/1.05 Archivo,sans-serif;letter-spacing:-.03em}
.phold{width:240px;height:240px;border-radius:50%;border:5px dashed rgba(255,255,255,.8);display:flex;align-items:center;justify-content:center;text-align:center;font:700 26px Inter;flex:0 0 240px}
.costs{display:flex;flex-direction:column;gap:20px}
.costs div{display:flex;align-items:center;gap:24px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.2);border-radius:30px;padding:26px 30px;font:800 44px Archivo,sans-serif}
.costs .i{width:64px;height:64px;flex:0 0 64px;color:#7CCBEA}
.guide{left:330px;top:500px;width:560px;height:740px;background:linear-gradient(160deg,#1690C1,#0A3D57);border-radius:18px 34px 34px 18px;padding:56px 50px;transform:perspective(1400px) rotateY(-22deg) rotateZ(4deg);box-shadow:-24px 0 0 #0A2C40,0 50px 80px rgba(0,0,0,.5);z-index:3;color:#fff;display:flex;flex-direction:column;gap:30px}
.gk{display:inline-block;align-self:flex-start;background:#93241E;border-radius:999px;padding:12px 24px;font:800 28px Inter;letter-spacing:.12em;text-transform:uppercase}
.gt{font:900 64px/1.02 Archivo,sans-serif;letter-spacing:-.02em}
.gl{margin-top:auto;background:#fff;border-radius:16px;padding:10px 14px;align-self:flex-start}
.gl img{height:60px;display:block}
.thumb{width:420px;background:#fff;padding:12px;border-radius:20px;box-shadow:0 30px 60px rgba(0,0,0,.4);z-index:3}
.thumb img{width:100%;display:block;border-radius:12px}
.words{display:flex;flex-wrap:wrap;gap:20px}
.words span{background:#fff;color:#0A3D57;border-radius:999px;padding:22px 34px;font:900 48px Archivo,sans-serif}
.words span:nth-child(2n){background:#93241E;color:#fff}
"""

def main():
    body = defs() + "".join(
        f'<div class="wrap"><h4>{cid} · {label}</h4><div class="crea {size} {bg}" id="{cid}">{html}</div></div>'
        for cid, size, bg, html, label in CREAS)
    for a, b in ((' ?', '&nbsp;?'), (' !', '&nbsp;!'), (' :', '&nbsp;:'), (' ;', '&nbsp;;'), (' »', '&nbsp;»'), ('« ', '«&nbsp;')):
        body = body.replace(a, b)
    page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>FS Express · Semaine 1</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,700;0,800;0,900;1,900&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{body}</body></html>'''
    open("creas.html", "w", encoding="utf-8").write(page)
    print(len(CREAS), "créas")

if __name__ == "__main__":
    main()
