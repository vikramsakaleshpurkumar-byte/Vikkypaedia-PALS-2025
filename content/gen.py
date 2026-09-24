"""Tiny authoring layer: unit content in Python, Standard markup out.
Keeps the HTML structure identical across units so the engine never meets a surprise."""
import html as _h

LV = {"e": ("t-e", "UG"), "a": ("t-a", "UG/PG"), "x": ("t-x", "PG")}
TIER = {"must": ("tier-must", "t-must", "Must-know"),
        "good": ("tier-good", "t-good", "Good-to-know"),
        "nice": ("tier-nice", "t-nice", "Nice-to-know")}

PARTS_META = {}
UNITS = []


def part(key, title, units_label, lede):
    PARTS_META[key] = dict(title=title, label=units_label, lede=lede, units=[])


def box(kind, title, body):
    return '<div class="box %s">\n  <h5>%s</h5>\n  %s\n</div>' % (kind, title, body)


def india(body):   return box("india", "India lens", body)
def pearl(body, t="Pearl"):   return box("pearl", t, body)
def pitfall(body, t="The error clinicians actually make"): return box("pitfall", t, body)
def evidence(body, t="Evidence note"): return box("evidence", t, body)
def danger(body, t="Danger"): return box("danger", t, body)


ROLE_LABELS = [("ug", "Student"), ("nurse", "Nurse"), ("pg", "PG resident"), ("fac", "Faculty")]


def roles(d):
    """A 'Your role' box: what each of the four audiences should take from this unit."""
    rows = "".join('<li><b>%s.</b> %s</li>' % (lab, d[k]) for k, lab in ROLE_LABELS if d.get(k))
    return ('<div class="box roles">\n  <h5>Your role</h5>\n  <ul>%s</ul>\n'
            '  <p class="roles-note">Role notes say what to emphasise. They do not authorise any procedure beyond your training and local policy.</p>\n</div>') % rows


def tracks(ideal, rc):
    li = lambda xs: "".join("<li>%s</li>" % x for x in xs)
    return ('<div class="tracks">\n  <div class="track track-id">\n    <h5>Ideal setting</h5>\n    <ul>%s</ul>\n  </div>\n'
            '  <div class="track track-rc">\n    <h5>Resource-constrained setting</h5>\n    <ul>%s</ul>\n  </div>\n</div>') % (li(ideal), li(rc))


def algo(title, pre):
    return '<div class="algo">\n  <div class="algo-t">%s</div>\n<pre>%s</pre>\n</div>' % (title, _h.escape(pre, quote=False))


def fig(key, title, pre):
    return ('<figure class="fig">\n  <figcaption class="fig-t">%s</figcaption>\n  <div class="fig-svg" data-figspec="%s"></div>\n'
            '  <details class="fig-alt"><summary>Text version</summary>\n    <div class="algo"><pre>%s</pre></div>\n  </details>\n</figure>') % (title, key, _h.escape(pre, quote=False))


def table(head, rows, cls="reflow"):
    th = "".join("<th>%s</th>" % c for c in head)
    tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<div class="tw"><table class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, th, tr)


def sec(num, title, body, tier="must", lvl=None):
    tcls, tagc, tagt = TIER[tier]
    lvcls = (" lv-" + lvl) if lvl in ("a", "x") else ""
    lvtag = (' <span class="tag %s">%s</span>' % LV[lvl]) if lvl in ("a", "x") else ""
    return ('<div class="sec %s%s">\n  <h4>%s · %s <span class="tag %s">%s</span>%s</h4>\n  %s\n</div>'
            % (tcls, lvcls, num, title, tagc, tagt, lvtag, body))


class Q:
    def __init__(self, stem, opts, correct, nudge, hint, why, wrong, teach, remed, critical=False):
        assert len(opts) == 4 and 0 <= correct < 4
        self.__dict__.update(locals())


def unit(n, part_key, title, lede, los, sections, qs, must=True):
    assert len(qs) == 2, "every unit has exactly two checkpoints"
    UNITS.append(dict(n=n, part=part_key, title=title, lede=lede, los=los, sections=sections, qs=qs))
    PARTS_META[part_key]["units"].append(n)


def _q_html(n, i, q):
    opts = "\n".join('        <li><button class="opt"%s>%s</button></li>' % (' data-c="1"' if k == q.correct else "", o)
                     for k, o in enumerate(q.opts))
    crit = ' data-critical="1"' if getattr(q, "critical", False) else ""
    return ('''    <div class="q" data-q="%d.%d" data-unit="%d"''' + crit + ''' data-remed="%s">
      <div class="qh">Checkpoint %d of 2</div>
      <p class="stem">%s</p>
      <ol class="opts">
%s
      </ol>
      <div class="hintbar"><button class="btn ghost sm hint-btn" type="button">Need a hint?</button></div>
      <div class="hint"><h6>Nudge</h6><p>%s</p></div>
      <div class="hint"><h6>Structured hint</h6><p>%s</p></div>
      <div class="rationale" hidden>
        <h6>Why the answer is what it is</h6>
        <p>%s</p>
        <div class="why-wrong">%s</div>
        <div class="teach">%s</div>
      </div>
    </div><!--/q-->''') % (n, i, n, _h.escape(q.remed, quote=True), i, q.stem, opts, q.nudge, q.hint, q.why, q.wrong, q.teach)


def unit_html(u):
    los = "\n".join('        <li><span class="tag %s">%s</span> %s</li>' % (LV[l][0], LV[l][1], t) for l, t in u["los"])
    body = "\n\n".join("    " + s for s in u["sections"])
    qs = "\n\n".join(_q_html(u["n"], i + 1, q) for i, q in enumerate(u["qs"]))
    return '''<!-- ======================================================= UNIT %(n)d -->
<section class="unit" id="u%(n)d" data-unit="%(n)d" data-part="%(p)s" data-title="%(ta)s">
  <h3 class="unit-head">
    <span class="caret">▸</span><span class="un">Unit %(n)d</span>
    <span class="ut">%(t)s</span>
    <span class="ubadge" data-s="not">Not attempted</span>
  </h3>
  <div class="unit-body">
    <p class="lede">%(lede)s</p>

    <div class="box lo">
      <h5>Learning outcomes</h5>
      <ul>
%(los)s
      </ul>
    </div>

%(body)s

%(qs)s

    <div class="mastery-badge" data-s="not"></div>
  </div>
</section>
''' % dict(n=u["n"], p=u["part"], t=u["title"], ta=_h.escape(_h.unescape(u["title"]), quote=True), lede=u["lede"], los=los, body=body, qs=qs)


def part_html(key):
    m = PARTS_META[key]
    head = '''<section class="part" id="part%s" data-part="%s" data-title="%s">
  <div class="part-head">
    <div>
      <span class="pk">Part %s</span>
      <h2>%s</h2>
    </div>
    <span class="part-meta">%s</span>
  </div>
  <p class="part-lede">%s</p>
''' % (key, key, _h.escape(_h.unescape(m["title"]), quote=True), key, m["title"], m["label"], m["lede"])
    units = "\n".join(unit_html(u) for u in UNITS if u["part"] == key)
    return head + "\n" + units + "\n</section>\n"


def move_answer(n, qi, target):
    """Swap the correct option with the option at `target`, keeping the
    why-wrong letters consistent. Used to balance the answer key."""
    import re as _re
    u = [x for x in UNITS if x["n"] == n][0]
    q = u["qs"][qi]
    a, b = q.correct, target
    if a == b:
        return
    q.opts[a], q.opts[b] = q.opts[b], q.opts[a]
    la, lb = "ABCD"[a], "ABCD"[b]
    swap = {la: lb, lb: la}
    for f in ("wrong", "why", "nudge", "hint", "teach"):
        setattr(q, f, _re.sub(r"<b>([A-D])</b>", lambda m: "<b>%s</b>" % swap.get(m.group(1), m.group(1)), getattr(q, f)))
    q.correct = b
    # keep the why-wrong list in letter order
    grp = r"<b>[A-D]</b>(?:(?:, | and | or |, and )<b>[A-D]</b>)* &mdash;"
    parts = _re.split(r"(?<!and )(?<!, )(?<!or )(?=" + grp + ")", q.wrong)

    def _order(seg):  # sort letters inside a grouped label such as "<b>D</b> and <b>A</b>"
        m = _re.match(grp, seg)
        if not m:
            return seg
        lab = m.group(0)
        ls = sorted(_re.findall(r"<b>([A-D])</b>", lab))
        it = iter(ls)
        return _re.sub(r"<b>[A-D]</b>", lambda _m: "<b>%s</b>" % next(it), lab) + seg[m.end():]
    head, items = parts[0], sorted((_order(x) for x in parts[1:]), key=lambda s: s[3])
    q.wrong = head + " ".join(p.strip() for p in items)


SITE = "https://vikramsakaleshpurkumar-byte.github.io/"
MODS = {"oxy": ("Vikkypaedia-OxyVent-Module/", "OxyVent"),
        "sc": ("Vikkypaedia-Module-Approach-to-a-Sick-child/", "Approach to the Sick Child"),
        "nrp": ("Vikkypaedia-NRP-2025/", "Neonatal Resuscitation 2025"),
        "met": ("Vikkypaedia-Metabolic-Child-MOOC/", "The Metabolic Child")}


def deeper(links):
    """'Go deeper' box: links into other Vikkypaedia modules. links = [(mod, unit_or_None, label)]."""
    li = []
    for mod, u, label in links:
        path, name = MODS[mod]
        href = SITE + path + (("#u%d" % u) if u else "")
        li.append('<li><a href="%s" target="_blank" rel="noopener">%s%s</a> &mdash; %s</li>'
                  % (href, name, (" &middot; Unit %d" % u) if u else "", label))
    return ('<div class="box deeper">\n  <h5>Go deeper in another module</h5>\n  <ul>%s</ul>\n'
            '  <p class="roles-note">Opens in a new tab. Units there unlock by mastery, as here.</p>\n</div>') % "".join(li)
