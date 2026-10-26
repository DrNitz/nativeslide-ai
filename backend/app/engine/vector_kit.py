"""
vector_kit.py - Native DrawingML toolkit for python-pptx.
Produces 100% editable PowerPoint shapes, text frames, connectors, groups, and charts.
No raster images, no SVG, no EMF. Standard ECMA-376 DrawingML.
"""
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.dml import MSO_LINE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn

# ---------- Core Palette ----------
NAVY      = RGBColor(0x0A, 0x19, 0x2F)
SLATE_900 = RGBColor(0x0F, 0x17, 0x2A)
SLATE_800 = RGBColor(0x1E, 0x29, 0x3B)
SLATE_700 = RGBColor(0x33, 0x41, 0x55)
SLATE_600 = RGBColor(0x47, 0x55, 0x69)
SLATE_500 = RGBColor(0x64, 0x74, 0x8B)
SLATE_400 = RGBColor(0x94, 0xA3, 0xB8)
SLATE_300 = RGBColor(0xCB, 0xD5, 0xE1)
SLATE_200 = RGBColor(0xE2, 0xE8, 0xF0)
SLATE_100 = RGBColor(0xF1, 0xF5, 0xF9)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

TEAL      = RGBColor(0x02, 0x84, 0xC7)
CYAN      = RGBColor(0x38, 0xBD, 0xF8)
SKY       = RGBColor(0x0E, 0xA5, 0xE9)
RED       = RGBColor(0xDC, 0x26, 0x26)
ROSE      = RGBColor(0xE1, 0x1D, 0x48)
ORANGE    = RGBColor(0xEA, 0x58, 0x0C)
AMBER     = RGBColor(0xD9, 0x77, 0x06)
GREEN     = RGBColor(0x10, 0xB9, 0x81)
EMERALD   = RGBColor(0x05, 0x96, 0x69)
VIOLET    = RGBColor(0x8B, 0x5C, 0xF6)
INDIGO    = RGBColor(0x4F, 0x46, 0xE5)

FONT = "Calibri"
FONT_LIGHT = "Calibri Light"

# ---------- DrawingML Injection ----------
def _spPr(shape):
    return shape._element.spPr

def set_gradient(shape, c1, c2, angle=2700000):
    spPr = _spPr(shape)
    for tag in ("a:noFill", "a:solidFill", "a:gradFill", "a:blipFill", "a:pattFill", "a:grpFill"):
        for e in spPr.findall(qn(tag)):
            spPr.remove(e)
    xml = (f'<a:gradFill {nsdecls("a")} rotWithShape="1"><a:gsLst>'
           f'<a:gs pos="0"><a:srgbClr val="{c1}"/></a:gs>'
           f'<a:gs pos="100000"><a:srgbClr val="{c2}"/></a:gs></a:gsLst>'
           f'<a:lin ang="{angle}" scaled="0"/></a:gradFill>')
    ln = spPr.find(qn("a:ln"))
    (ln.addprevious(parse_xml(xml)) if ln is not None else spPr.append(parse_xml(xml)))

def set_shadow(shape, blur=12, dist=6, alpha=26, direction=5400000):
    spPr = _spPr(shape)
    for e in spPr.findall(qn("a:effectLst")):
        spPr.remove(e)
    xml = (f'<a:effectLst {nsdecls("a")}><a:outerShdw blurRad="{int(blur*12700)}" '
           f'dist="{int(dist*12700)}" dir="{direction}" rotWithShape="0">'
           f'<a:srgbClr val="000000"><a:alpha val="{alpha*1000}"/></a:srgbClr>'
           f'</a:outerShdw></a:effectLst>')
    ln = spPr.find(qn("a:ln"))
    (ln.addnext(parse_xml(xml)) if ln is not None else spPr.append(parse_xml(xml)))

def set_custom_geometry(shape, subpaths, w=1000, h=1000):
    spPr = _spPr(shape)
    for tag in ("a:prstGeom", "a:custGeom"):
        for e in spPr.findall(qn(tag)):
            spPr.remove(e)
    d = []
    for sp in subpaths:
        seg = []
        for cmd in sp:
            if cmd[0] == "M":
                seg.append(f'<a:moveTo><a:pt x="{int(cmd[1])}" y="{int(cmd[2])}"/></a:moveTo>')
            elif cmd[0] == "L":
                seg.append(f'<a:lnTo><a:pt x="{int(cmd[1])}" y="{int(cmd[2])}"/></a:lnTo>')
            elif cmd[0] == "C":
                seg.append('<a:cubicBezTo>' + "".join(
                    f'<a:pt x="{int(v[0])}" y="{int(v[1])}"/>' for v in cmd[1:]) + '</a:cubicBezTo>')
            elif cmd[0] == "Z":
                seg.append("<a:close/>")
        d.append(f'<a:path w="{w}" h="{h}">' + "".join(seg) + "</a:path>")
    xml = (f'<a:custGeom {nsdecls("a")}><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/>'
           f'<a:rect l="0" t="0" r="r" b="b"/><a:pathLst>' + "".join(d) + '</a:pathLst></a:custGeom>')
    spPr.insert(1, parse_xml(xml))

def set_line_cap(shape, cap="rnd"):
    ln = shape.line._get_or_add_ln()
    ln.set("cap", cap)

# ---------- Text Engine ----------
def text(shape, blocks, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, margins=(0.10, 0.05, 0.10, 0.05)):
    """
    Renders structured text runs into a shape text frame.
    blocks: list of dicts: {t, sz, bold, color, font, space_before, space_after, align, italic, line}
    """
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    for i, b in enumerate(blocks):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = b.get("align", align)
        if b.get("space_before") is not None: p.space_before = Pt(b["space_before"])
        if b.get("space_after") is not None: p.space_after = Pt(b["space_after"])
        if b.get("line") is not None: p.line_spacing = b["line"]
        r = p.add_run()
        r.text = b.get("t", "")
        f = r.font
        f.name = b.get("font", FONT)
        f.size = Pt(b.get("sz", 11))
        f.bold = b.get("bold", False)
        f.italic = b.get("italic", False)
        f.color.rgb = b.get("color", SLATE_900)
    return tf

# ---------- Reusable Native Components ----------
def card(parent, x, y, w, h, fill=WHITE, line=SLATE_200, radius=0.10,
         grad=None, shadow=None, line_w=1.0):
    shp = parent.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.adjustments[0] = radius / min(w, h)
    if grad:
        set_gradient(shp, grad[0], grad[1], grad[2] if len(grad) > 2 else 2700000)
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w)
    if shadow:
        set_shadow(shp, *shadow)
    shp.text_frame.word_wrap = True
    return shp

def pill(parent, x, y, w, h, fill, label, fg=WHITE, sz=8.5, bold=True):
    shp = parent.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.adjustments[0] = 0.5
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background()
    text(shp, [{"t": label, "sz": sz, "bold": bold, "color": fg, "align": PP_ALIGN.CENTER}],
         anchor=MSO_ANCHOR.MIDDLE, margins=(0.03, 0.0, 0.03, 0.0))
    return shp

def connector(parent, x1, y1, x2, y2, color=SLATE_400, width=1.5, dash=None,
              arrow=True, kind=MSO_CONNECTOR.STRAIGHT):
    c = parent.shapes.add_connector(kind, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = dash
    if arrow:
        ln = c.line._get_or_add_ln()
        for tag in ("a:headEnd", "a:tailEnd"):
            for e in ln.findall(qn(tag)):
                ln.remove(e)
        ln.append(parse_xml(f'<a:headEnd {nsdecls("a")} type="none" w="med" len="med"/>'))
        ln.append(parse_xml(f'<a:tailEnd {nsdecls("a")} type="triangle" w="med" len="med"/>'))
    return c

def line(parent, x1, y1, x2, y2, color=SLATE_200, width=1.0, dash=None):
    return connector(parent, x1, y1, x2, y2, color, width, dash, arrow=False)

# ---------- Native Vector Geometry Icons ----------
BRAIN_PATH = [[("M",500,110),
               ("C",(360,110),(270,190),(285,285)),
               ("C",(205,310),(190,420),(255,475)),
               ("C",(215,560),(280,650),(390,650)),
               ("C",(425,715),(575,715),(610,650)),
               ("C",(720,650),(785,560),(745,475)),
               ("C",(810,420),(795,310),(715,285)),
               ("C",(730,190),(640,110),(500,110)),("Z",)]]

KIDNEY_PATH = [[("M",560,140),
                ("C",(760,190),(865,380),(825,580)),
                ("C",(795,760),(640,870),(515,830)),
                ("C",(620,760),(685,620),(662,480)),
                ("C",(640,320),(600,200),(560,140)),("Z",)]]

EYE_OUTLINE = [[("M",80,500),("C",(250,270),(750,270),(920,500)),
               ("C",(750,730),(250,730),(80,500)),("Z",)]]

ARTERY_PATH = [[("M",80,720),("C",(260,720),(300,280),(500,280)),
                ("C",(700,280),(740,720),(920,720))]]

WAVE_PATH = [[("M",40,500),("L",170,500),("L",210,430),("L",250,600),("L",300,340),
              ("L",350,660),("L",395,470),("L",430,520),("L",960,520)]]

SHIELD_PATH = [[("M", 500, 80), ("C", (750, 80), (880, 150), (920, 220)),
                 ("C", (920, 620), (680, 840), (500, 940)),
                 ("C", (320, 840), (80, 620), (80, 220)),
                 ("C", (120, 150), (250, 80), (500, 80)), ("Z",)]]

FLASK_PATH = [[("M", 420, 100), ("L", 580, 100), ("L", 580, 320), ("L", 840, 800),
                ("C", (870, 860), (830, 920), (750, 920)), ("L", 250, 920),
                ("C", (170, 920), (130, 860), (160, 800)), ("L", 420, 320), ("Z",)]]

ALERT_PATH = [[("M", 500, 120), ("L", 920, 880), ("L", 80, 880), ("Z",)]]

def icon(parent, kind, x, y, size, color, accent=None):
    """Draw a native vector icon. Returns list of shapes."""
    out = []
    if kind == "heart":
        s = parent.shapes.add_shape(MSO_SHAPE.HEART, Inches(x), Inches(y), Inches(size), Inches(size))
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        out.append(s)
    elif kind == "brain":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size))
        set_custom_geometry(s, BRAIN_PATH)
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        out.append(s)
    elif kind == "kidney":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size))
        set_custom_geometry(s, KIDNEY_PATH)
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        out.append(s)
    elif kind == "eye":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size*0.62))
        set_custom_geometry(s, EYE_OUTLINE, h=620)
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        p = parent.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x+size*0.34), Inches(y+size*0.10),
                                     Inches(size*0.32), Inches(size*0.32))
        p.fill.solid(); p.fill.fore_color.rgb = accent or WHITE; p.line.fill.background()
        out += [s, p]
    elif kind == "artery":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size*0.7))
        set_custom_geometry(s, ARTERY_PATH, h=1000)
        s.fill.background()
        s.line.color.rgb = color; s.line.width = Pt(size*3.2); set_line_cap(s, "rnd")
        out.append(s)
    elif kind == "pulse":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size*0.42))
        set_custom_geometry(s, WAVE_PATH, h=1000)
        s.fill.background()
        s.line.color.rgb = color; s.line.width = Pt(2.2); set_line_cap(s, "rnd")
        out.append(s)
    elif kind == "shield":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size))
        set_custom_geometry(s, SHIELD_PATH)
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        out.append(s)
    elif kind == "flask":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size))
        set_custom_geometry(s, FLASK_PATH)
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        out.append(s)
    elif kind == "alert":
        s = parent.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(size), Inches(size*0.88))
        set_custom_geometry(s, ALERT_PATH, h=1000)
        s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
        # Exclamation dot and stem
        st = line(parent, x+size*0.5, y+size*0.38, x+size*0.5, y+size*0.62, accent or WHITE, width=2.4)
        dt = parent.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x+size*0.46), Inches(y+size*0.70), Inches(size*0.08), Inches(size*0.08))
        dt.fill.solid(); dt.fill.fore_color.rgb = accent or WHITE; dt.line.fill.background()
        out += [s, st, dt]
    return out

# ---------- OpenXML Timing & Transitions ----------
class TimingBuilder:
    def __init__(self):
        self._id = 1
        self.effects = []

    def _n(self):
        self._id += 1
        return self._id

    def add(self, shape, trigger="click", delay=0, dur=450, effect="zoom"):
        self.effects.append((shape.shape_id, trigger, delay, dur, effect))

    def _effect_node(self, spid, delay, dur, effect):
        tn = self._n()
        if effect == "zoom":
            body = f'''
        <p:set><p:cBhvr><p:cTn id="{self._n()}" dur="1" fill="hold">
          <p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
          <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
        </p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
        <p:animEffect transition="in" filter="fade">
          <p:cBhvr><p:cTn id="{self._n()}" dur="{dur}"/>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
        <p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base">
          <p:cTn id="{self._n()}" dur="{dur}" fill="hold"/>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
          <p:attrNameLst><p:attrName>ppt_w</p:attrName><p:attrName>ppt_h</p:attrName></p:attrNameLst>
        </p:cBhvr>
        <p:tavLst>
          <p:tav tm="0"><p:val><p:strVal val="#ppt_w*0.55"/></p:val></p:tav>
          <p:tav tm="100000"><p:val><p:strVal val="#ppt_w"/></p:val></p:tav>
        </p:tavLst></p:anim>'''
            preset = ('presetID="23" presetClass="entr" presetSubtype="16"')
        else:  # fade
            body = f'''
        <p:set><p:cBhvr><p:cTn id="{self._n()}" dur="1" fill="hold">
          <p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
          <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
        </p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
        <p:animEffect transition="in" filter="fade">
          <p:cBhvr><p:cTn id="{self._n()}" dur="{dur}"/>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'''
            preset = ('presetID="10" presetClass="entr" presetSubtype="0"')

        return f'''<p:par><p:cTn id="{tn}" {preset} fill="hold" grpId="0" nodeType="clickEffect">
       <p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>
       <p:childTnLst>{body}
       </p:childTnLst></p:cTn></p:par>'''

    def xml(self):
        groups = []
        for spid, trigger, delay, dur, effect in self.effects:
            grp = self._n()
            wait = 'indefinite' if trigger == "click" else '0'
            groups.append(f'''<p:par><p:cTn id="{grp}" fill="hold">
      <p:stCondLst><p:cond delay="{wait}"/></p:stCondLst>
      <p:childTnLst>{self._effect_node(spid, delay, dur, effect)}</p:childTnLst>
     </p:cTn></p:par>''')
        return f'''<p:timing {nsdecls("p", "a")}>
 <p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
  <p:childTnLst><p:seq concurrent="1" nextAc="seek">
   <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
    <p:childTnLst>
     {''.join(groups)}
    </p:childTnLst>
   </p:cTn></p:seq></p:childTnLst>
  </p:cTn></p:par></p:tnLst>
</p:timing>'''

    def apply(self, slide):
        if not self.effects:
            return
        sld = slide._element
        for e in sld.findall(qn("p:timing")):
            sld.remove(e)
        sld.append(parse_xml(self.xml()))

def transition(slide, kind="fade", speed="med", direction=None):
    for e in slide._element.findall(qn("p:transition")):
        slide._element.remove(e)
    d = f' dir="{direction}"' if direction else ""
    if kind == "fade":
        inner = "<p:fade/>"
    elif kind == "push":
        inner = f"<p:push{d}/>"
    elif kind == "wipe":
        inner = f"<p:wipe{d}/>"
    else:
        inner = "<p:fade/>"
    xml = f'<p:transition {nsdecls("p")} spd="{speed}">{inner}</p:transition>'
    tr = parse_xml(xml)
    timing = slide._element.find(qn("p:timing"))
    if timing is not None:
        timing.addprevious(tr)
    else:
        slide._element.append(tr)
