# -*- coding: utf-8 -*-
"""Builds i18n.js from the translation chunks and FAILS if any string rendered
by the real page is neither translated nor explicitly kept in English."""
import json, os, re, sys, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LANGS = ['zh', 'ms', 'ar']

# Proper nouns stay as they are in every language: brands, residences, stations,
# roads, malls, hospitals, map attribution, Erican's own slogan, and the bare
# emoji that label a list item.
KEEP_ENGLISH = set("""
BeLive Erican College Erican College. M Vertica The Parc3 Meta City Nexus Residence
Maluri Taman Pertama Taman Equine Persiaran KLCC Tun Razak Exchange Kuala Lumpur
Avenue K Prince Court Leaflet OpenStreetMap GreenRE Gold yes, you can
Maluri MRT Taman Pertama MRT Taman Equine MRT KLCC & TRX
Suria KLCC · Tun Razak Exchange · KL Sentral
Meta City · Seri Kembangan
M Vertica · Taman Pertama, Cheras
The Parc3 · Taman Pudu Ulu, Cheras
Nexus Residence · Taman Pertama, Cheras
Avenue K · The Intermark Mall · Sunway Velocity Mall · MyTOWN & AEON Maluri
Prince Court · Hospital Kuala Lumpur · Sunway Velocity Medical Centre · KPJ Ampang Puteri
Erican College City Campus (★) · M Vertica · Nexus Residence · The Parc3 · Meta City
""".strip().split('\n'))
KEEP_ENGLISH |= {s.strip() for s in """
BeLive|Erican College|M Vertica|The Parc3|Meta City|Nexus Residence|Maluri|Taman Pertama
Taman Equine|Persiaran KLCC|Tun Razak Exchange|Kuala Lumpur|Avenue K|Prince Court|Leaflet
OpenStreetMap|GreenRE Gold|yes, you can|Maluri MRT|Taman Pertama MRT|Taman Equine MRT
KLCC & TRX|Kajang Line|Putrajaya Line|Erican College.|Erican College campus
Vertica|Nexus|Residence|Parc3|Meta|City|The|M
""".replace('\n', '|').split('|') if s.strip()}

def load_chunks():
    entries = {}
    for name in sorted(f for f in os.listdir(HERE) if f.startswith('chunk') and f.endswith('.json')):
        with io.open(os.path.join(HERE, name), encoding='utf-8') as fh:
            for k, v in json.load(fh).items():
                assert k not in entries, 'duplicate key %r in %s' % (k, name)
                assert len(v) == 3, 'key %r needs exactly zh/ms/ar' % k
                entries[k] = v
    return entries

def main():
    need = json.load(io.open(os.path.join(HERE, 'need.json'), encoding='utf-8'))
    # Strings the rendered-page sweep filtered out as numeric but which still
    # carry English words ('25-30 minutes'), plus the map popup bodies.
    for extra in ('leaked.json', 'popups.json'):
        fp = os.path.join(HERE, extra)
        if os.path.exists(fp):
            need = need + json.load(io.open(fp, encoding='utf-8'))
    entries = load_chunks()
    # emoji-only and pure-symbol strings never need a translation
    def trivial(s):
        return all(ord(c) > 0x2000 or c in ' ‍️' for c in s)
    phrases = json.load(io.open(os.path.join(HERE, 'phrases.json'), encoding='utf-8'))
    # longest key first, so "Single Room" cannot match inside a longer room name
    order = sorted(phrases, key=len, reverse=True)

    def phrase_covered(s):
        """A string assembled in JS has no single key. It counts as covered when
        the phrase pass plus the proper nouns we keep leaves no English behind."""
        out = s
        for k in order:
            out = out.replace(k, '\u0001')
        for name in sorted(KEEP_ENGLISH, key=len, reverse=True):
            out = out.replace(name, '\u0001')
        out = re.sub(r'RM\s?[\d,.]+', '\u0001', out)   # currency amounts are not copy
        return not re.search(r'[A-Za-z]{2,}', out)

    missing = [s for s in need
               if s not in entries and s not in KEEP_ENGLISH and not trivial(s)
               and not phrase_covered(s)]
    print('translated: %d   kept English: %d   MISSING: %d'
          % (len(entries), sum(1 for s in need if s in KEEP_ENGLISH), len(missing)))
    if missing:
        io.open(os.path.join(HERE, 'missing.json'), 'w', encoding='utf-8').write(
            json.dumps(sorted(missing, key=len), ensure_ascii=False, indent=1))
        print('  -> wrote missing.json (%d)' % len(missing))
    dict_by_lang = {L: {k: v[i] for k, v in entries.items()} for i, L in enumerate(LANGS)}
    out = {'dict': dict_by_lang, 'phrases': {L: {k: v[i] for k, v in phrases.items()}
                                             for i, L in enumerate(LANGS)}}
    return out, missing

if __name__ == '__main__':
    out, missing = main()
    sys.exit(1 if missing else 0)

def emit(path):
    out, missing = main()
    assert not missing, 'refusing to emit with %d untranslated strings' % len(missing)
    head = (
        "/* Generated — do not hand-edit. Source: scratchpad/i18n/chunk*.json +\n"
        "   phrases.json, built by build.py, which refuses to emit while any string\n"
        "   the live page renders is neither translated nor explicitly kept in\n"
        "   English. `dict` is keyed on the EXACT English string. `phrases` is the\n"
        "   substring pass for text assembled in JS, applied longest key first. */\n"
        "window.BELIVE_I18N = ")
    io.open(path, 'w', encoding='utf-8').write(
        head + json.dumps(out, ensure_ascii=False, indent=0, sort_keys=True) + ';\n')
    print('wrote %s (%d exact keys, %d phrases per language)'
          % (path, len(out['dict']['zh']), len(out['phrases']['zh'])))
