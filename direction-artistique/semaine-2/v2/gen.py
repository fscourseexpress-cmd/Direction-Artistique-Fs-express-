# Génère les créas de la semaine 2 selon le planning « FS Course Planning 42 publications ».
# Une page HTML par jour (lundi à samedi). export.js exporte chaque bloc [data-name] en PNG.
import os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
B, R, N, C, L, S, W = '#1690C1', '#93241E', '#0A3D57', '#FBFBF8', '#E8F6FC', '#7CCBEA', '#FFFFFF'
LOGO = '<div class="logo"><img src="../../../semaine-1/assets/logo.jpg" alt="Logo FS Express"></div>'
ICONS = open(os.path.join(HERE, 'icons-defs.html'), encoding='utf-8').read()


def ic(name, size=96, color=N):
    return f'<svg class="ic" width="{size}" height="{size}" style="color:{color}"><use href="#i-{name}"/></svg>'


def photo(src, h=560, pos='50% 50%'):
    return f'<img class="ph" src="../assets/{src}" alt="" style="height:{h}px;object-position:{pos}">'


def cards(items, cols=2, h=230):
    """items: (icône, libellé, fond, texte)"""
    out = [f'<div class="grid" style="grid-template-columns:repeat({cols},1fr)">']
    for icon, label, bg, fg in items:
        out.append(f'<div class="card" style="background:{bg};color:{fg};min-height:{h}px">'
                   f'{ic(icon, 84, fg) if icon else ""}<div>{label}</div></div>')
    out.append('</div>')
    return ''.join(out)


def bubbles(items, big=False):
    """items: (texte, 'l' pour reçu / 'r' pour envoyé)"""
    out = ['<div class="chat">']
    for text, side in items:
        cls = ('bub-r' if side == 'r' else 'bub-l') + (' big' if big else '')
        out.append(f'<div class="bub {cls}">{text}</div>')
    out.append('</div>')
    return ''.join(out)


def checks(items, color=B, tc=N):
    out = ['<div class="checks">']
    for t in items:
        out.append(f'<div class="chk"><span class="box" style="border-color:{color}"></span><span style="color:{tc}">{t}</span></div>')
    out.append('</div>')
    return ''.join(out)


def steps(items, color=B):
    out = ['<div class="steps">']
    for i, t in enumerate(items, 1):
        out.append(f'<div class="step"><span class="num" style="background:{color}">{i}</span><span>{t}</span></div>')
    out.append('</div>')
    return ''.join(out)


def stamp(text, color=R):
    return f'<div class="stamp" style="color:{color};border-color:{color}">{text}</div>'


def clock():
    return ('<svg class="clock" width="560" height="560" viewBox="0 0 400 400" fill="none">'
            '<circle cx="200" cy="200" r="180" fill="#FFFFFF" stroke="#0A3D57" stroke-width="10"/>'
            '<path d="M200 200 L200 20 A180 180 0 0 1 356 290 Z" fill="#1690C1"/>'
            '<path d="M200 200 L356 290 A180 180 0 0 1 44 290 Z" fill="#0A3D57"/>'
            '<path d="M200 200 L44 290 A180 180 0 0 1 200 20 Z" fill="#93241E"/>'
            '<circle cx="200" cy="200" r="22" fill="#FBFBF8"/>'
            '<text x="260" y="130" font-family="Archivo" font-weight="900" font-size="34" fill="#FBFBF8">Matin</text>'
            '<text x="120" y="330" font-family="Archivo" font-weight="900" font-size="34" fill="#FBFBF8">Après-midi</text>'
            '<text x="40" y="150" font-family="Archivo" font-weight="900" font-size="34" fill="#FBFBF8">Soirée</text>'
            '</svg>')


def mascots():
    cat = ('<svg width="200" height="200" viewBox="0 0 200 200"><path d="M40 90 L60 30 L90 75 L110 75 L140 30 L160 90 Q170 150 100 170 Q30 150 40 90 Z" fill="#0A3D57"/>'
           '<circle cx="78" cy="110" r="10" fill="#FBFBF8"/><circle cx="122" cy="110" r="10" fill="#FBFBF8"/>'
           '<path d="M92 132 L100 140 L108 132" stroke="#FBFBF8" stroke-width="6" fill="none"/></svg>')
    lion = ('<svg width="200" height="200" viewBox="0 0 200 200"><circle cx="100" cy="100" r="90" fill="#93241E"/>'
            '<circle cx="100" cy="100" r="60" fill="#FBFBF8"/><circle cx="78" cy="96" r="8" fill="#0A3D57"/>'
            '<circle cx="122" cy="96" r="8" fill="#0A3D57"/><path d="M84 124 Q100 138 116 124" stroke="#0A3D57" stroke-width="6" fill="none"/></svg>')
    bee = ('<svg width="200" height="200" viewBox="0 0 200 200"><ellipse cx="100" cy="110" rx="70" ry="60" fill="#1690C1"/>'
           '<rect x="52" y="90" width="96" height="18" fill="#0A3D57"/><rect x="52" y="122" width="96" height="18" fill="#0A3D57"/>'
           '<ellipse cx="60" cy="60" rx="26" ry="18" fill="#E8F6FC"/><ellipse cx="140" cy="60" rx="26" ry="18" fill="#E8F6FC"/></svg>')
    robot = ('<svg width="200" height="200" viewBox="0 0 200 200"><rect x="40" y="50" width="120" height="110" rx="24" fill="#0A3D57"/>'
             '<rect x="90" y="20" width="20" height="36" fill="#93241E"/><circle cx="100" cy="18" r="12" fill="#93241E"/>'
             '<circle cx="78" cy="100" r="16" fill="#1690C1"/><circle cx="122" cy="100" r="16" fill="#1690C1"/>'
             '<rect x="78" y="128" width="44" height="12" rx="6" fill="#FBFBF8"/></svg>')
    out = ['<div class="mascots">']
    for svg, lab in [(cat, 'Le chat'), (lion, 'Le lion'), (bee, 'L’abeille'), (robot, 'Le robot')]:
        out.append(f'<div class="mascot">{svg}<div>{lab}</div></div>')
    out.append('</div>')
    return ''.join(out)


def parcel(color=B, tape=R, w=520):
    return (f'<svg width="{w}" height="{int(w*0.7)}" viewBox="0 0 600 420" fill="none">'
            f'<polygon points="60,140 360,140 360,400 60,400" fill="{color}"/>'
            f'<polygon points="60,140 160,40 460,40 360,140" fill="{S}"/>'
            f'<polygon points="360,140 460,40 460,300 360,400" fill="{N}"/>'
            f'<rect x="60" y="250" width="300" height="44" fill="{tape}"/>'
            '<rect x="110" y="170" width="120" height="66" fill="#FBFBF8"/></svg>')


def wave():
    bars = [30, 60, 90, 130, 70, 110, 150, 90, 50, 120, 80, 40, 100, 60, 30]
    inner = ''.join(f'<span class="bar" style="height:{h}px"></span>' for h in bars)
    return f'<div class="wave">{inner}</div>'


def map_card():
    return ('<svg class="mapsvg" width="900" height="420" viewBox="0 0 900 420" fill="none">'
            '<rect x="10" y="10" width="880" height="400" rx="36" fill="#FFFFFF" stroke="#0A3D57" stroke-width="6"/>'
            '<path d="M0 120 H900 M0 300 H900 M200 0 V420 M520 0 V420 M740 0 V420" stroke="#7CCBEA" stroke-width="22"/>'
            '<path d="M120 260 L300 80" stroke="#1690C1" stroke-width="10" stroke-dasharray="4 26" stroke-linecap="round"/>'
            '<path d="M640 110 C600 110 580 140 580 165 C580 200 640 260 640 260 C640 260 700 200 700 165 C700 140 680 110 640 110 Z" fill="#93241E"/>'
            '<circle cx="640" cy="165" r="20" fill="#FBFBF8"/></svg>')


def avatar(color):
    return (f'<svg width="150" height="150" viewBox="0 0 150 150"><circle cx="75" cy="50" r="30" fill="{color}"/>'
            f'<path d="M20 145 Q20 92 75 92 Q130 92 130 145 Z" fill="{color}"/></svg>')


def people_grid():
    items = [('Allô, je suis prêt !', B, C), ('Vous êtes déjà où ?', R, C),
             ('Attendez, je cherche le numéro', N, C), ('Je descends !', S, N)]
    out = ['<div class="grid" style="grid-template-columns:1fr 1fr">']
    for q, bg, fg in items:
        out.append(f'<div class="card people" style="background:{bg};color:{fg}">{avatar(W if bg != S else N)}'
                   f'<div class="bubq" style="color:{N};background:{C}">{q}</div></div>')
    out.append('</div>')
    return ''.join(out)


def post(name, kicker, title, body, vis, cta, bg=C, fg=N, count=None, fs=None, story=False):
    """Un visuel 1080x1350 (feed) ou 1080x1920 (story)."""
    if fs is None:
        n = len(re.sub(r'<[^>]+>', '', title))
        fs = 104 if n < 34 else 92 if n < 60 else 78 if n < 100 else 66
        if story:
            fs = int(fs * 1.25)
    kick = f'<div class="kick" style="color:{S if bg in (N, B, R) else B}">{kicker}</div>' if kicker else ''
    bdy = f'<div class="body" style="color:{fg}">{body}</div>' if body else ''
    cls = 'story' if story else 'post'
    top_right = f'<div class="count" style="color:{fg}">{count}</div>' if count else f'<div class="tag" style="color:{S if fg == N else B}">FS Express</div>'
    footer = f'<div class="pill" style="background:{R if bg != R else N}">{cta}</div>' if cta else ''
    return (f'<section class="{cls}" data-name="{name}" style="background:{bg};color:{fg}">'
            f'<div class="top">{LOGO}{top_right}</div>'
            f'<div class="main">{kick}<div class="t" style="font-size:{fs}px;color:{fg}">{title}</div>{bdy}'
            f'<div class="vis">{vis}</div></div>{footer}</section>')


def carousel(prefix, slides, bg=C, fg=N):
    out = []
    for i, s in enumerate(slides, 1):
        out.append(post(f'{prefix}-{i}', s.get('kicker'), s['title'], s.get('body', ''), s.get('vis', ''),
                        s.get('cta') if i == len(slides) else s.get('cta', ''), bg=s.get('bg', bg), fg=s.get('fg', fg),
                        count=f'{i} / {len(slides)}', fs=s.get('fs')))
    return '\n'.join(out)


D = {'lundi': '2026-11-30', 'mardi': '2026-12-01', 'mercredi': '2026-12-02',
     'jeudi': '2026-12-03', 'vendredi': '2026-12-04', 'samedi': '2026-12-05'}


def page(title, sections):
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400..900&family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="../style-v2.css"></head><body>
<div style="position:absolute;width:0;height:0;overflow:hidden">{ICONS}</div>
{sections}
</body></html>'''


# ------------------------------------------------------------------ LUNDI 30
def lundi():
    d = D['lundi']
    s = []
    s.append(post(f'{d}_08h00_FB', 'Visuel participatif',
                  f'Le panier est plein…<br>mais vous n’avez pas <span class="hl">encore commandé ?</span>', '',
                  bubbles([('Le prix de la livraison ?', 'l'), ('Est-ce que ça va arriver ?', 'l'), ('Je commande demain', 'r')]),
                  'Répondez en commentaire.', count=None))
    s.append(carousel(f'{d}_09h00_IG', [
        dict(kicker='Messages WhatsApp', title='Les 5 messages qui annoncent une commande <span class="hl">mouvementée</span>', vis=''),
        dict(kicker='Message 1 / 5', title='« Bonjour, c’est disponible ? »', vis=bubbles([('Bonjour, c’est disponible ?', 'l')], big=True), fs=86),
        dict(kicker='Message 2 / 5', title='« Inbox svp »', vis=bubbles([('Inbox svp', 'l')], big=True), fs=86),
        dict(kicker='Message 3 / 5', title='« Le dernier prix ? »', vis=bubbles([('Le dernier prix ?', 'l')], big=True), fs=86),
        dict(kicker='Message 4 / 5', title='« Je confirme tout à l’heure »', vis=bubbles([('Je confirme tout à l’heure', 'l')], big=True), fs=80),
        dict(kicker='Message 5 / 5', title='« Vous êtes situé où ? »', vis=bubbles([('Vous êtes situé où ?', 'l')], big=True), fs=86,
             cta='Un message oublié ? Dites-le en commentaire.'),
    ]))
    s.append(post(f'{d}_13h00_FB', 'Conversation fictive',
                  '« Je suis au carrefour »… <span class="hl">mais lequel ?</span>', '',
                  bubbles([('Je suis au carrefour', 'r'), ('Lequel ?', 'l'), ('Celui près de la boutique', 'r'), ('Quelle boutique ?', 'l')]),
                  'Vous êtes où quand on vous dit ça ? En commentaire.'))
    s.append(carousel(f'{d}_13h00_IG', [
        dict(kicker='Culture de la livraison', title='Le dictionnaire non officiel de la <span class="hl">livraison</span>',
             body='Une expression par slide. Lesquelles reconnaissez-vous ?', vis=''),
        dict(kicker='Expression · 1 / 3', title='« JE SUIS <span class="hl">EN BAS</span> »', body='Expression qui peut désigner plusieurs endroits différents.', vis=''),
        dict(kicker='Expression · 2 / 3', title='« ÇA <span class="hl">ARRIVE</span> »', body='Notion de temps parfois mystérieuse.', vis=''),
        dict(kicker='Expression · 3 / 3', title='« ENVOYEZ LA <span class="hl">LOCALISATION</span> »', body='Phrase qui peut sauver une livraison.', vis=''),
        dict(kicker='À vous de jouer', title='Quelle expression avons-nous <span class="hl">oubliée ?</span>', vis='',
             cta='Ajoutez la vôtre en commentaire.'),
    ]))
    s.append(post(f'{d}_17h00_IG', 'Question',
                  'Vous commandez après avoir vu le statut WhatsApp, ou après avoir demandé « inbox » ?', '',
                  cards([('chat', 'Une réponse à un statut WhatsApp', B, C), ('send', 'Un message privé direct', N, C)], cols=2, h=320),
                  'Répondez A ou B en commentaire.', fs=76))
    s.append(post(f'{d}_18h00_FB', 'Post participatif',
                  'Le produit camerounais que vous recommandez <span class="hl">les yeux fermés</span>', '',
                  f'<div class="grid" style="grid-template-columns:1fr 1fr">'
                  f'<div class="ph-tile">{photo("tshirt.jpg", 220, "50% 60%")}<div class="lab">Mode</div></div>'
                  f'<div class="card" style="background:{S};color:{N};min-height:200px">{ic("star",70,N)}<div>Beauté</div></div>'
                  f'<div class="card" style="background:{R};color:{C};min-height:130px">{ic("zap",60,C)}<div>Gourmandises</div></div>'
                  f'<div class="card" style="background:{N};color:{C};min-height:130px">{ic("box",60,C)}<div>Artisanat</div></div>'
                  f'<div class="card" style="background:{L};color:{N};min-height:130px">{ic("id",60,N)}<div>Accessoires</div></div></div>',
                  'Recommandez un produit en commentaire.', fs=66))
    s.append(story_pair(d, [
        dict(kicker='On vous demande', title='Vous avez déjà abandonné un panier ?', bg=N, fg=C, zone='Sondage : Oui / Non'),
        dict(kicker='Votre réponse', title='Pourquoi ?', bg=B, fg=C, zone='Boîte à questions'),
    ]))
    return page('Lundi 30 novembre', '\n'.join(s))


def story_pair(d, items):
    out = []
    for i, st in enumerate(items, 1):
        out.append(story_block(f'{d}_story-{i}', st))
    return '\n'.join(out)


def story_block(name, st):
    fg = st.get('fg', C)
    bg = st['bg']
    zone = f'<div class="zone">{H.escape(st["zone"])}</div>' if st.get('zone') else ''
    kick = f'<div class="kick" style="color:{S}">{st["kicker"]}</div>' if st.get('kicker') else ''
    fs = st.get('fs', 150)
    vis = st.get('vis', '')
    return (f'<section class="story" data-name="{name}" style="background:{bg};color:{fg}">'
            f'<div class="top story-top">{LOGO}</div>'
            f'<div class="main story-main">{kick}<div class="t" style="font-size:{fs}px;color:{fg}">{st["title"]}</div>'
            f'<div class="vis">{vis}</div>{zone}</div></section>')


# ------------------------------------------------------------------ MARDI 1er
def mardi():
    d = D['mardi']
    s = []
    s.append(post(f'{d}_08h00_FB', 'Question du jour',
                  'Vous préférez commander <span class="hl">le matin</span> ou le soir ?', '',
                  cards([('clock', 'Team matin<br><span class="sub">Au petit-déjeuner</span>', B, C),
                         ('clock', 'Team soir<br><span class="sub">Une fois la journée finie</span>', N, C)], cols=2, h=360),
                  'Répondez « matin » ou « soir » en commentaire.'))
    s.append(post(f'{d}_13h00_FB', 'Débat',
                  'Paiement à la livraison ou paiement avant l’expédition : <span class="hl">tu préfères quoi ?</span>', '',
                  cards([('cash', 'Régler avant l’envoi', B, C), ('box', 'Payer à la réception, quand le vendeur le propose', N, C)], cols=2, h=360),
                  'Expliquez vos raisons en commentaire.'))
    s.append(post(f'{d}_18h00_FB', 'Mini-quiz',
                  'Quel repère aide le mieux à <span class="hl">retrouver une adresse</span> ?', '',
                  cards([('pin', 'A · Un nom de rue', L, N), ('pin', 'B · Un lieu connu à proximité', B, C),
                         ('pin', 'C · Une position partagée et un repère clair', N, C)], cols=1, h=170),
                  'Réponse et explication en commentaire.'))
    s.append(carousel(f'{d}_09h00_IG', [
        dict(kicker='Vendre sur WhatsApp', title='Les infos à envoyer <span class="hl">avant de confirmer</span>', body='Une commande, quatre points à vérifier.', vis=''),
        dict(kicker='1 · Le produit', title='Produit et quantité', vis=checks(['Le produit concerné', 'La quantité', 'La taille ou le modèle'])),
        dict(kicker='2 · Le prix', title='Le prix total', vis=checks(['Le prix total affiché', 'Les frais éventuels annoncés']) ),
        dict(kicker='3 · La réception', title='Les informations de réception', body='À confirmer en privé, jamais en public.', vis=checks(['Le lieu de remise', 'Un numéro joignable', 'Les modalités convenues'])),
    ], ))
    s.append(carousel(f'{d}_13h00_IG', [
        dict(kicker='Avant l’envoi', title='Votre colis est-il <span class="hl">prêt à voyager ?</span>', vis=photo('cartons-sol.jpg', 620, '50% 60%')),
        dict(kicker='Étape 1 · 4', title='L’emballage est <span class="hl">bien fermé</span>', body='Un carton solide, fermé sur tous les côtés.', vis=photo('pyramide.jpg', 620, '50% 50%')),
        dict(kicker='Étape 2 · 4', title='Les informations sont <span class="hl">vérifiées</span>', body='Vérifiées en privé, sans les afficher publiquement.',
             vis=checks(['Le nom et le lieu de remise', 'Le numéro joignable'], R)),
        dict(kicker='Étape 3 · 4', title='Le colis est <span class="hl">prêt à être remis</span>', vis=photo('livreur-remise.jpg', 620, '50% 40%'),
             cta='Enregistrez ce carrousel.'),
    ]))
    s.append(post(f'{d}_17h00_IG', 'Reel photo',
                  'Les différents types de personnes <span class="hl">quand le livreur appelle</span>', '',
                  people_grid(), 'Lequel vous ressemble ?', fs=84))
    s.append(story_pair(d, [
        dict(kicker='Team commande', title='Vous commandez le matin ou le soir ?', bg=B, fg=C, zone='Sondage : Matin / Soir'),
        dict(kicker='La communauté', title='Votre réponse la plus drôle ?', bg=N, fg=C, zone='Boîte à questions'),
    ]))
    return page('Mardi 1er décembre', '\n'.join(s))


# ------------------------------------------------------------------ MERCREDI 2
def mercredi():
    d = D['mercredi']
    s = []
    s.append(post(f'{d}_08h00_FB', 'Mini-sondage',
                  'Le détail qui vous rassure <span class="hl">le plus</span> quand vous commandez en ligne', '',
                  cards([('star', 'Les avis clients', B, C), ('eye', 'Les vraies photos', N, C),
                         ('chat', 'Une réponse rapide', R, C), ('box', 'Des infos claires sur la livraison', L, N)], cols=2, h=300),
                  'Lequel compte le plus pour vous ?'))
    s.append(post(f'{d}_13h00_FB', 'Question',
                  'Commerçants : à quelle heure vos clients <span class="hl">écrivent-ils le plus ?</span>', '',
                  f'<div class="center">{clock()}</div>', 'Dites-nous la plage qui reçoit le plus de messages.'))
    s.append(post(f'{d}_18h00_FB', 'Post communautaire',
                  'Quel marché ou quelle boutique te fait <span class="hl">toujours revenir ?</span>', '',
                  photo('vendeuse-rose.jpg', 640, '50% 35%'), 'Dites-nous lequel, et pourquoi.'))
    s.append(carousel(f'{d}_09h00_IG', [
        dict(kicker='Storytelling', title='Le parcours d’un colis <span class="hl">avant qu’il arrive chez vous</span>', vis=''),
        dict(kicker='Étape 1 · 4', title='La commande est confirmée', vis=parcel(B, R, 460)),
        dict(kicker='Étape 2 · 4', title='Le colis est préparé', vis=parcel(N, R, 460)),
        dict(kicker='Étape 3 · 4', title='Les informations sont vérifiées', vis=cards([('shield', 'Adresse et numéro vérifiés en privé', L, N)], cols=1, h=380)),
        dict(kicker='Étape 4 · 4', title='Prise en charge et remise', vis=photo('livreur-remise.jpg', 620, '50% 45%'),
             cta='Et vous, à quelle étape êtes-vous le plus attentif ?'),
    ]))
    s.append(post(f'{d}_13h00_IG', 'Affiche · mythe ou réalité',
                  'Mythe ou réalité : une livraison, c’est <span class="hl">juste transporter un colis ?</span>', '',
                  f'<div class="steps-row">{steps(["Vérifier les informations", "Coordonner les personnes", "Organiser le trajet", "Assurer la remise"], R)}</div>'
                  f'<div class="center">{stamp("RÉALITÉ : TOUT UN PARCOURS", R)}</div>',
                  'Enregistrez cette affiche.', fs=84))
    s.append(post(f'{d}_17h00_IG', 'Visuel interactif',
                  'Vous faites confiance à une boutique en ligne <span class="hl">grâce à quoi ?</span>', '',
                  cards([('star', 'Les avis', B, C), ('eye', 'Les photos réelles', N, C),
                         ('chat', 'Les réponses', R, C), ('box', 'Les informations claires', L, N)], cols=2, h=300),
                  'Quel critère compte le plus ?'))
    s.append(story_pair(d, [
        dict(kicker='Quiz', title='Le transport est-il la seule étape d’une livraison ?', bg=B, fg=C, zone='Quiz : Oui / Non', fs=120),
        dict(kicker='La réponse', title='Non. Il y a aussi préparer, vérifier et remettre.', bg=N, fg=C, fs=120),
    ]))
    return page('Mercredi 2 décembre', '\n'.join(s))


# ------------------------------------------------------------------ JEUDI 3
def jeudi():
    d = D['jeudi']
    s = []
    s.append(post(f'{d}_08h00_FB', 'Post participatif',
                  'Si votre boutique avait une mascotte, <span class="hl">ce serait quoi ?</span>', '',
                  mascots(), 'Votre boutique aurait quelle mascotte ? Dites-le en commentaire.'))
    s.append(post(f'{d}_13h00_FB', 'Anecdote · question',
                  'Le message vocal de 2 minutes pour <span class="hl">expliquer une adresse</span>', '',
                  f'{wave()}{bubbles([("Après le garage… non, avant… attendez, la pharmacie…", "l")])}',
                  'Quelle indication est la plus mémorable ? En commentaire.'))
    s.append(post(f'{d}_18h00_FB', 'Conseil express',
                  'Un petit réflexe pour éviter <span class="hl">les commandes incomplètes</span>', '',
                  '<div class="recap"><div class="rrow"><span>Produit</span><b>Exemple à compléter</b></div>'
                  '<div class="rrow"><span>Quantité</span><b>À confirmer</b></div>'
                  '<div class="rrow"><span>Montant</span><b>À confirmer</b></div>'
                  '<div class="rrow"><span>Modalités</span><b>Convenues ensemble</b></div></div>',
                  'Vérifiez le récapitulatif avant de confirmer.'))
    s.append(carousel(f'{d}_09h00_IG', [
        dict(kicker='Humour', title='Quand on vous dit « je suis à côté » : <span class="hl">4 interprétations</span>', vis=''),
        dict(kicker='Interprétation 1 · 4', title='Près du carrefour', vis=cards([('pin', 'Le grand carrefour, après le feu', B, C)], cols=1, h=400)),
        dict(kicker='Interprétation 2 · 4', title='Derrière la boutique', vis=cards([('store', 'La porte à côté de la boutique', N, C)], cols=1, h=400)),
        dict(kicker='Interprétation 3 · 4', title='Après le snack', vis=cards([('zap', 'Le snack du coin, à gauche', R, C)], cols=1, h=400)),
        dict(kicker='Interprétation 4 · 4', title='Près du portail', vis=cards([('lock', 'Le portail bleu, le deuxième', L, N)], cols=1, h=400)),
        dict(kicker='À vous de jouer', title='Quelle expression <span class="hl">avons-nous oubliée ?</span>', cta='Ajoutez la vôtre en commentaire.'),
    ]))
    s.append(carousel(f'{d}_13h00_IG', [
        dict(kicker='5 détails', title='5 détails qui rendent une boutique en ligne <span class="hl">plus rassurante</span>', vis=''),
        dict(kicker='Détail 1 · 5', title='Des photos fidèles au produit', vis=photo('tshirt.jpg', 620, '50% 50%')),
        dict(kicker='Détail 2 · 5', title='Des prix faciles à trouver', vis=cards([('cash', 'Le prix visible avant de payer', B, C)], cols=1, h=400)),
        dict(kicker='Détail 3 · 5', title='Des réponses claires', vis=cards([('chat', 'Une question, une réponse précise', N, C)], cols=1, h=400)),
        dict(kicker='Détail 4 · 5', title='Des conditions de commande compréhensibles', vis=cards([('shield', 'Ce qui est convenu, écrit noir sur blanc', L, N)], cols=1, h=400)),
        dict(kicker='Détail 5 · 5', title='Des informations de livraison annoncées sans ambiguïté', vis=cards([('box', 'Le délai et les conditions indiqués', R, C)], cols=1, h=400),
             cta='Et vous, quel détail comptez-vous ?'),
    ]))
    s.append(post(f'{d}_17h00_IG', 'Portrait',
                  'Le visage derrière <span class="hl">la petite boutique en ligne</span>', 'Portrait d’un commerçant partenaire : son activité, son produit phare et son défi du quotidien.',
                  photo('commercante-boutique.jpg', 520, '50% 30%'), 'Quel est votre défi du quotidien ?'))
    s.append(story_pair(d, [
        dict(kicker='Boîte à questions', title='Quelle est la meilleure astuce pour une boutique en ligne ?', bg=B, fg=C, zone='Boîte à questions', fs=110),
        dict(kicker='Repartage', title='Une réponse à repartager ?', bg=N, fg=C, zone='Repartage avec accord de l’auteur', fs=130),
    ]))
    return page('Jeudi 3 décembre', '\n'.join(s))


# ------------------------------------------------------------------ VENDREDI 4
def vendredi():
    d = D['vendredi']
    s = []
    s.append(post(f'{d}_08h00_FB', 'Vrai ou faux',
                  'Vrai ou faux : une adresse avec un repère <span class="hl">suffit toujours ?</span>', '',
                  map_card() + '<div class="vf"><div class="btnv" style="background:#1690C1">VRAI</div><div class="btnv" style="background:#93241E">FAUX</div></div>',
                  'Réponse dans les commentaires.'))
    s.append(post(f'{d}_13h00_FB', 'Débat · situation',
                  'Un client dit « je suis intéressé » : vous bloquez le produit <span class="hl">ou vous attendez ?</span>', '',
                  bubbles([('Je suis intéressé !', 'l'), ('Je le mets de côté ?', 'r')]) +
                  cards([('lock', 'Je bloque le produit', B, C), ('clock', 'J’attends la confirmation', N, C)], cols=2, h=260),
                  'Dites-nous votre pratique en commentaire.', fs=78))
    s.append(post(f'{d}_18h00_FB', 'Quiz · vrai ou faux',
                  'Vrai ou faux : les informations de livraison peuvent <span class="hl">attendre la dernière minute ?</span>', '',
                  steps(['Confirmer le numéro joignable', 'Vérifier le lieu de remise', 'Préparer le colis'], N),
                  'Vrai ou faux ? Votre réponse en commentaire.', fs=78))
    s.append(carousel(f'{d}_09h00_IG', [
        dict(kicker='Mini-guide', title='Avant de faire un dépôt pour une commande : <span class="hl">les vérifications utiles</span>', vis=''),
        dict(kicker='1 · La page du vendeur', title='Vérifier la page du vendeur', vis=cards([('store', 'Le nom et les informations de la boutique', B, C)], cols=1, h=400)),
        dict(kicker='2 · Le produit', title='Relire les détails du produit', vis=cards([('box', 'Taille, couleur, caractéristiques', N, C)], cols=1, h=400)),
        dict(kicker='3 · Le montant', title='Confirmer le montant total', vis=cards([('cash', 'Le total avant de payer', R, C)], cols=1, h=400)),
        dict(kicker='4 · Les conditions', title='Clarifier les conditions de vente et de livraison', vis=cards([('shield', 'Par écrit, avant la commande', L, N)], cols=1, h=400),
             cta='Une question sur un dépôt ? En commentaire.'),
    ]))
    s.append(carousel(f'{d}_13h00_IG', [
        dict(kicker='Checklist', title='Avant de valider une commande, <span class="hl">vérifiez ces 4 choses</span>', vis=''),
        dict(kicker='1 · Le prix', title='Le prix total', vis=f'<div class="center">{ic('cash',230,R)}</div>'+checks(['Le total est affiché avant de payer'], R)),
        dict(kicker='2 · Le produit', title='Les détails du produit', vis=f'<div class="center">{ic('box',230,R)}</div>'+checks(['Les caractéristiques sont claires'], R)),
        dict(kicker='3 · Le vendeur', title='Les informations du vendeur', vis=f'<div class="center">{ic('store',230,R)}</div>'+checks(['Un contact est indiqué'], R)),
        dict(kicker='4 · La livraison', title='Les conditions de livraison', vis=f'<div class="center">{ic('shield',230,R)}</div>'+checks(['Les conditions sont écrites'], R),
             cta='Enregistrez cette checklist.'),
    ], bg=C))
    s.append(post(f'{d}_17h00_IG', 'Sondage',
                  'Quel est votre réflexe quand vous attendez <span class="hl">une livraison ?</span>', '',
                  cards([('chat', 'Je vérifie WhatsApp', B, C), ('box', 'Je prépare la réception', N, C),
                         ('clock', 'J’attends sans regarder', R, C)], cols=1, h=170),
                  'Votez puis répondez en commentaire.'))
    s.append(story_pair(d, [
        dict(kicker='Quiz', title='Vrai ou faux sur les indications d’adresse', bg=B, fg=C, zone='Quiz : Vrai / Faux', fs=120),
        dict(kicker='À enregistrer', title='Checklist avant de commander', bg=N, fg=C,
             vis=checks(['Le total', 'Les détails du produit', 'Le vendeur', 'La livraison'], S, C), zone='Enregistrez'),
    ]))
    return page('Vendredi 4 décembre', '\n'.join(s))


# ------------------------------------------------------------------ SAMEDI 5
def samedi():
    d = D['samedi']
    s = []
    s.append(post(f'{d}_08h00_FB', 'Post reconnaissance',
                  'Les commerçants <span class="hl">qui font vivre nos timelines</span>',
                  'Derrière chaque page, il y a une personne qui crée, vend, répond et prépare des commandes.',
                  f'<div class="grid" style="grid-template-columns:1fr 1fr">'
                  f'<div class="ph-tile">{photo("vendeuse-telephone.jpg", 380, "50% 30%")}</div>'
                  f'<div class="ph-tile">{photo("commercante-boutique.jpg", 380, "50% 30%")}</div>'
                  f'<div class="ph-tile">{photo("tshirt.jpg", 260, "50% 50%")}</div>'
                  f'<div class="card" style="background:{N};color:{C};min-height:260px">{ic("star",70,C)}<div>Mode · Beauté · Gourmandises</div></div></div>',
                  'Taguez le commerçant que vous suivez.', fs=80))
    s.append(post(f'{d}_13h00_FB', 'Post valorisation',
                  'Un samedi pour soutenir <span class="hl">les petits commerces de Yaoundé</span>', 'Découvrez, recommandez, partagez une petite entreprise locale.',
                  photo('vendeuse-rose.jpg', 600, '50% 35%'), 'Recommandez une petite boutique en commentaire.', fs=80))
    s.append(post(f'{d}_18h00_FB', 'Question bilan',
                  'Cette semaine, quelle situation de livraison <span class="hl">vous a fait rire ?</span>', '',
                  bubbles([('Il a sonné… à la mauvaise porte', 'l'), ('Le colis était chez la voisine !', 'r')]) +
                  f'<div class="center">{parcel(B, R, 300)}</div>',
                  'Racontez-la en commentaire.', fs=78))
    s.append(carousel(f'{d}_09h00_IG', [
        dict(kicker='Boutique mémorable', title='Les petites choses qui rendent une boutique <span class="hl">mémorable</span>', vis=''),
        dict(kicker='1 · La présentation', title='Une présentation cohérente', vis=photo('pyramide.jpg', 560, '50% 50%')),
        dict(kicker='2 · La communication', title='Une communication claire', vis=cards([('chat', 'Des messages simples et précis', B, C)], cols=1, h=380)),
        dict(kicker='3 · L’attention', title='Une attention personnalisée', vis=photo('tshirt.jpg', 560, '50% 50%')),
        dict(kicker='4 · Le suivi', title='Un suivi après achat', vis=photo('cartons-sol.jpg', 560, '50% 60%'),
             cta='Quelle petite chose vous a marqué ?'),
    ]))
    s.append(carousel(f'{d}_13h00_IG', [
        dict(kicker='Votre choix', title='Quel colis <span class="hl">choisirais-tu ?</span>', vis=f'<div class="center" style="gap:30px">{parcel(B,R,300)}{parcel(N,R,300)}</div>'),
        dict(kicker='Les indices', title='Chaque colis a son univers', vis=
             cards([('star', '1 · Le colis mode', B, C), ('star', '2 · Le colis beauté', R, C),
                    ('zap', '3 · Le colis gourmand', N, C), ('lock', '4 · Le colis mystère', L, N)], cols=2, h=380)),
        dict(kicker='Votre choix', title='Lequel choisissez-vous ?', vis='',
             cta='Répondez 1, 2, 3 ou 4 en commentaire.'),
    ]))
    s.append(post(f'{d}_17h00_IG', 'Visuel · question',
                  'Si vous deviez décrire Yaoundé <span class="hl">en un seul repère</span>, lequel choisiriez-vous ?', '',
                  photo('monument.jpg', 560, '50% 50%'), 'Dites-le en commentaire.', fs=78))
    s.append(story_pair(d, [
        dict(kicker='Votre choix', title='Quel colis choisissez-vous ?', bg=R, fg=C, zone='Sondage : Colis A / Colis B', fs=130),
        dict(kicker='La communauté', title='Commerçants : montrez votre packaging', bg=N, fg=C,
             zone='Envoyez votre clip en message privé', fs=120),
    ]))
    return page('Samedi 5 décembre', '\n'.join(s))


PAGES = {'lundi': lundi, 'mardi': mardi, 'mercredi': mercredi, 'jeudi': jeudi, 'vendredi': vendredi, 'samedi': samedi}

if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'html'), exist_ok=True)
    for k, fn in PAGES.items():
        open(os.path.join(HERE, 'html', f'{k}.html'), 'w', encoding='utf-8').write(fn())
        print('ok', k)
