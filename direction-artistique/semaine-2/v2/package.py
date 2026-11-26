# Range les créas v2 par jour et par heure, avec la légende du planning à côté de chaque visuel.
import os, glob, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'publication-v2')
shutil.rmtree(OUT, ignore_errors=True)
plan = json.load(open(os.path.join(HERE, 'planning.json'), encoding='utf-8'))
DAYS = [('2026-11-30', '01_lundi-30-novembre', 'lundi'), ('2026-12-01', '02_mardi-1er-decembre', 'mardi'),
        ('2026-12-02', '03_mercredi-2-decembre', 'mercredi'), ('2026-12-03', '04_jeudi-3-decembre', 'jeudi'),
        ('2026-12-04', '05_vendredi-4-decembre', 'vendredi'), ('2026-12-05', '06_samedi-5-decembre', 'samedi')]
PLAT = {'Facebook': 'Facebook', 'Instagram': 'Instagram', 'TikTok': 'TikTok'}
# index : (date, heure "08h00", plateforme) -> légende du planning
legend = {}
for p in plan:
    date = '-'.join(reversed(p['Date'].split('/')))
    h = p['Heure'].replace('h', 'h')
    legend[(date, h, p['Plateforme'])] = p['Légende proposée'] or p['Texte à intégrer / déroulé']
index = []
for date, folder, key in DAYS:
    base = os.path.join(OUT, folder)
    for f in sorted(glob.glob(os.path.join(HERE, 'png', f'{date}_*.png'))):
        name = os.path.basename(f)[:-4]
        rest = name.split('_', 1)[1]
        if rest.startswith('story'):
            dest = os.path.join(base, 'stories'); os.makedirs(dest, exist_ok=True)
            shutil.copy(f, dest); index.append((key, date, 'Story', 'à définir', os.path.basename(f), ''))
            continue
        hour = rest[:5]                      # 08h00
        plat = 'Facebook' if rest.endswith('_FB') or '_FB-' in rest else 'Instagram'
        sub = os.path.join(base, f"{hour.replace('h', 'h')}_{plat}"); os.makedirs(sub, exist_ok=True)
        shutil.copy(f, sub)
        leg = legend.get((date, hour.replace('h', 'h'), plat), '')
        if leg and not os.path.exists(os.path.join(sub, 'légende.txt')):
            open(os.path.join(sub, 'légende.txt'), 'w', encoding='utf-8').write(leg + '\n')
        index.append((key, date, plat, hour, os.path.basename(f), leg))
    for mp4 in glob.glob(os.path.join(HERE, 'tiktok', f'{key}.mp4')):
        sub = os.path.join(base, '19h00_TikTok'); os.makedirs(sub, exist_ok=True)
        shutil.copy(mp4, sub)
        leg = legend.get((date, '19h00', 'TikTok'), '')
        open(os.path.join(sub, 'légende.txt'), 'w', encoding='utf-8').write(leg + '\n')
        index.append((key, date, 'TikTok', '19h00', os.path.basename(mp4), leg))
md = ['# Créas semaine 2 (30 novembre au 5 décembre), par jour et par heure', '',
      'Planning : 42 publications (3 Facebook, 3 Instagram, 1 TikTok par jour) + 12 stories.', '',
      '| Jour | Heure | Plateforme | Fichier | Légende (planning) |', '|---|---|---|---|---|']
for key, date, plat, hour, fn, leg in index:
    md.append(f'| {key} | {hour} | {plat} | `{fn}` | {leg.replace(chr(10), " ")} |')
open(os.path.join(OUT, 'index.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print(len(index), 'fichiers classés')
