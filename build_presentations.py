#!/usr/bin/env python3
"""
Triune Biblical University Global Extension USA
Bachelor of Artificial Intelligence and Robotics Engineering

Generates a premium, cinematic 6-hour orientation lecture PDF for every course subject.
Every slide footer carries: TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA
"""
import os
import re
from math import sin, cos, pi

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ----------------------------------------------------------------------------
# Fonts (registered TTFs for a premium serif/sans cinematic look)
# ----------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Serif", f"{FONT_DIR}/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", f"{FONT_DIR}/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))

DISPLAY = "Serif-B"      # premium cinematic display
DISPLAY_R = "Serif"      # serif regular
BODY = "Sans"            # clean body
BODY_B = "Sans-B"        # body bold

UNIVERSITY = "TRIUNE BIBLICAL UNIVERSITY GLOBAL EXTENSION USA"
UNIVERSITY_SHORT = "TRIUNE BIBLICAL UNIVERSITY"

# ----------------------------------------------------------------------------
# Palette — deep cinematic night + luxury gold
# ----------------------------------------------------------------------------
BG        = HexColor("#0A0E1A")   # near-black navy background
BG_PANEL  = HexColor("#12192E")   # panel slightly lighter
GOLD      = HexColor("#C9A227")   # luxury gold accent
GOLD_LT   = HexColor("#E3D49B")   # pale gold
GOLD_DK   = HexColor("#8F731E")   # dark gold
INK       = HexColor("#F4F6FA")   # off-white text
MUTED     = HexColor("#9FB0C4")   # muted slate
LINE      = HexColor("#2A3550")   # subtle divider
CREDIT    = HexColor("#7DD3FC")   # soft cyan for credits

# ----------------------------------------------------------------------------
# Geometry — 16:9 widescreen (points)
# ----------------------------------------------------------------------------
W, H = 960.0, 540.0
M = 60.0   # side margin

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def slugify(text):
    t = text.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t)
    t = re.sub(r"[\s]+", " ", t).strip().replace(" ", "_")
    return t[:60]

def wrap(text, font, size, max_w):
    """Simple word-wrap returning list of lines."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_text(c, x, y, text, font=BODY, size=13, color=INK, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "right":
        c.drawRightString(x, y, text)
    elif align == "center":
        c.drawCentredString(x, y, text)
    else:
        c.drawString(x, y, text)
    return y

def draw_paragraph(c, x, y, text, font=BODY, size=12, color=INK, max_w=400, leading=16, bullet=False):
    """Draw wrapped paragraph, return new y (lower)."""
    lines = wrap(text, font, size, max_w)
    for i, ln in enumerate(lines):
        if bullet:
            c.setFillColor(GOLD)
            c.drawString(x - 14, y, "■")
            c.setFillColor(color)
        c.drawString(x, y, ln)
        y -= leading
    return y

def rect_round(c, x, y, w, h, r=8, fill=None, stroke=None, lw=1):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=bool(stroke), fill=bool(fill))

def spotlight(c, cx, cy, max_r, steps=18):
    """Soft radial spotlight (cinematic)."""
    for i in range(steps, 0, -1):
        t = i / steps
        r = max_r * t
        alpha = 0.06 * (1 - t)  # strongest at center, fades out
        c.setFillColor(Color(1, 0.82, 0.35, alpha=alpha))
        c.circle(cx, cy, r, stroke=0, fill=1)

def gradient_bg(c, top=HexColor("#0F172A"), bottom=HexColor("#0A0E1A")):
    """Subtle vertical gradient background."""
    import colorsys
    steps = 60
    band = H / steps
    r1, g1, b1 = top.red, top.green, top.blue
    r2, g2, b2 = bottom.red, bottom.green, bottom.blue
    for i in range(steps):
        t = i / (steps - 1)
        r = r1 + (r2 - r1) * t
        g = g1 + (g2 - g1) * t
        b = b1 + (b2 - b1) * t
        c.setFillColor(Color(r, g, b))
        c.rect(0, i * band, W, band + 0.5, stroke=0, fill=1)

def footer(c, page, course_code, course_title_short):
    """University footer on every slide."""
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(M, 40, W - M, 40)
    c.setFont(BODY, 9.5)
    c.setFillColor(MUTED)
    c.drawString(M, 28, UNIVERSITY)
    c.setFont(BODY_B, 9.5)
    c.setFillColor(GOLD_LT)
    c.drawRightString(W - M, 28, f"{course_code}  |  {page}")
    c.setFont(BODY, 8)
    c.setFillColor(HexColor("#5B6880"))
    c.drawCentredString(W / 2, 16, "Orientation Lecture  •  6 Hours  •  Bachelor of Artificial Intelligence and Robotics Engineering")

def header(c, course_code, course_title, section_tag):
    """Premium content-slide header."""
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.line(M, H - 46, W - M, H - 46)
    c.setFont(DISPLAY, 15)
    c.setFillColor(GOLD_LT)
    c.drawString(M, H - 38, course_code)
    c.setFont(BODY, 10.5)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, H - 38, section_tag)
    c.setFont(DISPLAY_R, 11.5)
    c.setFillColor(INK)
    # short title centered under rule
    c.drawCentredString(W / 2, H - 66, course_title.upper())

# ----------------------------------------------------------------------------
# Cover slide (cinematic, premium)
# ----------------------------------------------------------------------------
def draw_cover(c, course):
    gradient_bg(c, HexColor("#0E1426"), HexColor("#0A0E1A"))
    # Cinematic spotlight
    spotlight(c, W * 0.5, H * 0.62, W * 0.9)
    spotlight(c, W * 0.18, H * 0.85, W * 0.45)
    # Subtle horizon line
    c.setStrokeColor(Color(1, 0.78, 0.3, alpha=0.18))
    c.setLineWidth(1.2)
    c.line(M, H * 0.52, W - M, H * 0.52)

    # University wordmark (top)
    c.setFont(DISPLAY, 13)
    c.setFillColor(GOLD_LT)
    c.drawCentredString(W / 2, H - 78, UNIVERSITY.upper())
    c.setFont(BODY, 8.5)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, H - 94, "Bachelor of Artificial Intelligence and Robotics Engineering")

    # Gold divider
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    c.line(W / 2 - 90, H - 112, W / 2 + 90, H - 112)

    # Course code — big, gold
    c.setFont(DISPLAY, 44)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H - 176, course["code"])

    # Title — large serif
    for i, ln in enumerate(wrap(course["title"], DISPLAY_R, 23, W - 120)):
        c.setFont(DISPLAY_R, 23)
        c.setFillColor(INK)
        c.drawCentredString(W / 2, H - 218 - i * 40, ln)

    # Semester band
    band_w, band_h = 420, 44
    bx, by = W / 2 - band_w / 2, H - 330
    rect_round(c, bx, by, band_w, band_h, r=6, fill=BG_PANEL, stroke=GOLD, lw=1)
    c.setFont(BODY_B, 11)
    c.setFillColor(GOLD_LT)
    c.drawCentredString(W / 2, by + band_h / 2 - 7, course["semester"].upper())

    # 6-hour callout
    c.setFont(DISPLAY_B if False else DISPLAY, 16)
    c.setFillColor(GOLD_LT)
    c.drawCentredString(W / 2, H - 372, "ORIENTATION LECTURE  •  6 CONTACT HOURS")

    c.setFont(BODY, 9.5)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, H - 390, f"Credit: {course['credits']}   |   Orientation · Foundation Module")

    # Description panel (lower)
    py = 150
    rect_round(c, M, py, W - 2 * M, 110, r=10, fill=BG_PANEL, stroke=LINE, lw=0.8)
    c.setFont(DISPLAY_R, 11.5)
    c.setFillColor(INK)
    c.drawString(M + 28, py + 86, "COURSE OVERVIEW")
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(M + 28, py + 80, M + 150, py + 80)
    dy = py + 56
    for ln in wrap(course["description"], BODY, 11.5, W - 2 * M - 56):
        c.setFont(BODY, 11.5)
        c.setFillColor(MUTED)
        c.drawString(M + 28, dy, ln)
        dy -= 17

    # Footer
    footer(c, 1, course["code"], course["title"])
    c.showPage()

# ----------------------------------------------------------------------------
# Content slide
# ----------------------------------------------------------------------------
def draw_content(c, page, course, session):
    gradient_bg(c, HexColor("#0E1426"), HexColor("#0A0E1A"))
    header(c, course["code"], course["title"], session["tag"] or course["code"])

    # Left column: session identity
    lx = M
    # Session chip
    chip_w, chip_h = 78, 78
    rect_round(c, lx, H - 130 - chip_h, chip_w, chip_h, r=10, fill=BG_PANEL, stroke=GOLD, lw=1.2)
    c.setFont(DISPLAY, 24)
    c.setFillColor(GOLD)
    c.drawCentredString(lx + chip_w / 2, H - 130 - chip_h / 2 + 6, session["num"])
    c.setFont(BODY, 8.5)
    c.setFillColor(MUTED)
    c.drawCentredString(lx + chip_w / 2, H - 130 - chip_h / 2 - 24, "SESSION")

    # Time chip
    tw, th = 150, 36
    tx = lx
    ty = H - 130 - chip_h - th - 14
    rect_round(c, tx, ty, tw, th, r=6, fill=GOLD_DK)
    c.setFont(BODY_B, 11.5)
    c.setFillColor(INK)
    c.drawCentredString(tx + tw / 2, ty + th / 2 - 7, f"⏱  {session['minutes']} MINUTES")

    # Session title
    sy = ty - 34
    c.setFont(DISPLAY_R, 15.5)
    c.setFillColor(GOLD_LT)
    c.drawString(lx, sy, session["title"].upper())
    c.setStrokeColor(LINE); c.setLineWidth(0.8)
    c.line(lx, sy - 8, lx + 300, sy - 8)

    # Topics
    ty2 = sy - 46
    c.setFont(BODY_B, 10)
    c.setFillColor(MUTED)
    c.drawString(lx, ty2, "KEY TOPICS")
    yy = ty2 - 24
    max_w = 330
    for top in session["topics"]:
        lines = wrap("• " + top, BODY, 11, max_w)
        c.setFont(BODY, 11)
        c.setFillColor(INK)
        c.drawString(lx, yy, lines[0])
        yy -= 15
        for extra in lines[1:]:
            c.setFont(BODY, 10.5)
            c.setFillColor(MUTED)
            c.drawString(lx + 18, yy, extra)
            yy -= 14
        yy -= 9  # gap between topics

    # Right panel: Teaching focus & takeaway
    px = W - M - 360
    pw = 360
    ph = H - 150 - 90
    py2 = 90
    rect_round(c, px, py2, pw, ph, r=12, fill=BG_PANEL, stroke=LINE, lw=0.8)
    # inner gold top edge
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(px + 16, py2 + ph - 22, px + pw - 16, py2 + ph - 22)
    c.setFont(BODY_B, 11.5)
    c.setFillColor(GOLD_LT)
    c.drawString(px + 24, py2 + ph - 32, "TEACHING FOCUS")
    c.setFont(BODY, 10.5)
    c.setFillColor(INK)
    fy = py2 + ph - 58
    for ln in wrap(session["focus"], BODY, 10.5, pw - 48):
        c.drawString(px + 24, fy, ln)
        fy -= 15

    # Takeaway strip
    tyaw = py2 - 46
    rect_round(c, px, tyaw, pw, 34, r=6, fill=GOLD_DK)
    c.setFont(BODY_B, 10)
    c.setFillColor(INK)
    c.drawString(px + 16, tyaw + 10, "▲  KEY TAKEAWAY")
    c.setFont(BODY, 9.5)
    c.setFillColor(GOLD_LT)
    c.drawString(px + 160, tyaw + 10, session["takeaway"][:60])

    footer(c, page, course["code"], course["title"])
    c.showPage()

# ----------------------------------------------------------------------------
# Build one course PDF
# ----------------------------------------------------------------------------
def build_course(course, out_path):
    c = canvas.Canvas(out_path, pagesize=(W, H))
    c.setTitle(f"{course['code']} — {course['title']}")
    c.setAuthor(UNIVERSITY)
    c.setSubject("Orientation Lecture — 6 Hours")

    draw_cover(c, course)                       # page 1
    page = 2
    for session in course["sessions"]:
        draw_content(c, page, course, session)  # one slide per session
        page += 1
    c.save()
    return page - 1  # total slides

# ----------------------------------------------------------------------------
# Course data — 43 subjects (42 courses + 1 project)
# Each session: ~60 minutes, 6 sessions = 6 hours.
# ----------------------------------------------------------------------------
def course(code, title, semester, description, sessions):
    return {
        "code": code,
        "title": title,
        "semester": semester,
        "credits": "2.70",
        "description": description,
        "sessions": sessions,
    }

def S(num, title, topics, focus, takeaway, minutes=60, tag=None):
    return {"num": num, "title": title, "topics": topics,
            "focus": focus, "takeaway": takeaway, "minutes": minutes, "tag": tag}

ALL_COURSES = []

# ---------------- YEAR 1 SEMESTER 1 ----------------
YS1 = "YEAR 1 · SEMESTER 1"
ALL_COURSES += [
course("AI.101", "Introduction to Artificial Intelligence", YS1,
 "Origins, definitions, and the landscape of artificial intelligence; how AI perceives, reasons, learns, and acts, and its role in modern engineering.",
 [S("1", "Orientation: What Is AI?", ["Defining AI: narrow vs. general vs. super", "A brief history of AI and robotics", "AI in everyday systems", "Course scope and learning path"],
   "Situate AI within engineering and society; set expectations for the 6-hour orientation.", "AI = machines that perceive, reason, learn, act."),
  S("2", "Intelligent Agents & Environments", ["Agent architecture: sensors, actuators, effectors", "Rational agents and performance measures", "Environment types: observable, deterministic, episodic", "PEAS framework in robotics"],
   "Model an intelligent agent and its operating environment.", "Every intelligent system is an agent in an environment."),
  S("3", "Problem Solving & Search", ["Uninformed search: BFS, DFS, UCS", "Informed search: greedy, A*, heuristics", "Adversarial search: minimax, alpha-beta", "Constraint satisfaction intro"],
   "Apply classical search to robot path and puzzle problems.", "Search is the engine of automated reasoning."),
  S("4", "Knowledge Representation & Logic", ["Propositional and first-order logic", "Semantic networks and frames", "Ontologies for robotics domains", "Reasoning under uncertainty"],
   "Encode domain knowledge so machines can infer.", "Knowledge plus inference equals intelligence."),
  S("5", "Planning & Decision Making", ["STRIPS and classical planning", "State-space vs. plan-space planning", "Decision trees and utility", "Introduction to Markov decision processes"],
   "Generate action sequences to achieve robot goals.", "Planning turns goals into action sequences."),
  S("6", "AI Applications, Ethics & Review", ["AI in industry, healthcare, transport", "Bias, transparency, and accountability", "Course recap and assessment", "Next steps in the degree"],
   "Connect foundations to real-world impact and responsibility.", "Intelligent systems must be built responsibly.")],
),
course("AI.102", "Robotics Fundamentals", YS1,
 "Core robotics concepts: robot anatomy, kinematics basics, sensors, actuators, and the integrate sense-plan-act cycle.",
 [S("1", "Orientation: The Robot as a System", ["What defines a robot", "Sense–plan–act cycle", "Robot vs. automaton", "Applications across sectors"],
   "Establish a unified view of a robot as an integrated system.", "A robot senses, plans, and acts in the physical world."),
  S("2", "Robot Anatomy & Classification", ["Links, joints, and degrees of freedom", "Serial vs. parallel manipulators", "Mobile, humanoid, and industrial robots", "Specification and workspaces"],
   "Classify robots by structure and intended workspace.", "Structure determines capability."),
  S("3", "Actuators & Drive Systems", ["Electric motors: DC, stepper, servo", "Hydraulic and pneumatic actuators", "Transmission: gears, belts, harmonic drives", "Actuator selection criteria"],
   "Match actuators to motion and force requirements.", "Actuators are the muscles of a robot."),
  S("4", "Sensors & Perception Basics", ["Proprioceptive vs. exteroceptive sensors", "Encoders, IMUs, LiDAR, cameras", "Sensor characteristics: noise, range, resolution", "Sensor fusion introduction"],
   "Choose and interpret the robot's senses.", "Sensors convert the physical world into data."),
  S("5", "Control Basics for Robotics", ["Open-loop vs. closed-loop control", "Feedback and error signals", "P, PI, PID concepts", "Set-point tracking in motion"],
   "Regulate robot motion with feedback control.", "Feedback closes the sense–plan–act loop."),
  S("6", "Integration, Safety & Review", ["Hardware–software integration", "Robot safety standards and E-stops", "Course recap and assessment", "Path toward robotics design"],
   "Integrate knowledge with safety-first engineering practice.", "Safe integration is the mark of a professional.")],
),
course("AI.103", "Machine Learning", YS1,
 "Foundations of machine learning: supervised, unsupervised, and reinforcement learning; data, models, training, and evaluation.",
 [S("1", "Orientation: Machines That Learn", ["AI vs. ML vs. deep learning", "The learning problem: data → model", "Training, validation, test splits", "Types of ML: supervised, unsupervised, RL"],
   "Define machine learning and its place in AI.", "Learning is improving performance through experience."),
  S("2", "Supervised Learning — Regression", ["Linear regression and least squares", "Polynomial features and overfitting", "Gradient descent optimization", "Evaluating regression models"],
   "Fit continuous-output models to data.", "Predict numbers from features."),
  S("3", "Supervised Learning — Classification", ["Logistic regression", "Decision trees and random forests", "k-Nearest neighbors", "Support vector machines"],
   "Assign inputs to discrete classes.", "Draw boundaries that separate classes."),
  S("4", "Unsupervised Learning", ["k-Means clustering", "Hierarchical clustering", "Principal Component Analysis (PCA)", "Dimensionality reduction and visualization"],
   "Discover hidden structure without labels.", "Find patterns where labels do not exist."),
  S("5", "Model Evaluation & Selection", ["Accuracy, precision, recall, F1", "Confusion matrix", "Cross-validation", "Bias–variance tradeoff"],
   "Choose models that generalize, not memorize.", "Generalization is the true test of learning."),
  S("6", "ML in Robotics & Ethics", ["ML for perception and control", "Data bias and fairness", "Course recap and assessment", "Preparation for neural networks"],
   "Apply ML responsibly to robotic systems.", "Data-driven robots must be fair and robust.")],
),
course("AI.104", "Computer Vision", YS1,
 "How machines see: image formation, filtering, feature detection, and introductory object recognition.",
 [S("1", "Orientation: The Machine Eye", ["Image formation and the camera model", "Pixels, color spaces, and digital images", "The computer vision pipeline", "Vision in robotics and AI"],
   "Understand how images become machine-readable data.", "Seeing begins with light, lenses, and sensors."),
  S("2", "Image Processing & Filtering", ["Point operations: brightness, contrast", "Convolution and spatial filtering", "Smoothing: Gaussian and median", "Edge detection: Sobel, Canny"],
   "Enhance and extract structure from images.", "Filters reveal what the eye may miss."),
  S("3", "Features & Keypoints", ["Corners: Harris and Shi-Tomasi", "SIFT and ORB descriptors", "Feature matching and tracking", "Template matching"],
   "Identify stable points across views.", "Keypoints anchor vision to the world."),
  S("4", "Image Segmentation", ["Thresholding and Otsu", "Region growing and watershed", "Contour detection", "Semantic vs. instance segmentation"],
   "Partition an image into meaningful regions.", "Segmentation separates object from background."),
  S("5", "Object Recognition Basics", ["Sliding-window detection", "Histogram of oriented gradients", "Intro to deep vision", "Face and object recognition"],
   "Name and locate things in images.", "Recognition answers 'what is where?'."),
  S("6", "Vision for Robots & Review", ["Visual servoing and motion", "Camera calibration", "Course recap and assessment", "Toward machine vision (AI.307)"],
   "Connect vision to robot action.", "Robots act on what they see.")],
),
course("AI.105", "Natural Language Processing", YS1,
 "Computational processing of human language: text representation, linguistic structure, and introductory language understanding.",
 [S("1", "Orientation: Language for Machines", ["What is NLP", "Tokenization, stemming, lemmatization", "Corpus and text preprocessing", "NLP in AI assistants and robots"],
   "Turn raw text into structured linguistic data.", "Language is data with structure and meaning."),
  S("2", "Text Representation", ["Bag-of-words and n-grams", "TF-IDF weighting", "One-hot encoding", "Intro to word embeddings"],
   "Represent words and documents numerically.", "Meaning can be represented as vectors."),
  S("3", "Linguistic Structure", ["Part-of-speech tagging", "Named entity recognition", "Parsing and syntax trees", "Morphology basics"],
   "Analyze the grammar of sentences.", "Structure disambiguates meaning."),
  S("4", "Language Modeling", ["N-gram language models", "Probability of word sequences", "Perplexity and smoothing", "Neural language models intro"],
   "Predict what word comes next.", "Modeling sequences models language."),
  S("5", "NLP Applications", ["Machine translation", "Sentiment analysis", "Chatbots and dialogue", "Speech recognition intro"],
   "Deploy language understanding in products.", "NLP powers human–machine conversation."),
  S("6", "NLP for Robotics & Ethics", ["Human–robot dialogue", "Bias in language models", "Course recap and assessment", "Toward HRI (AI.110)"],
   "Enable robots to understand and speak.", "Robots must understand humans, not just commands.")],
),
course("AI.106", "Control Systems", YS1,
 "Classical control theory: modeling dynamic systems, feedback, stability, and PID—foundations for robotic motion.",
 [S("1", "Orientation: Why Control Matters", ["Open-loop vs. closed-loop", "Control objectives: regulate and track", "Examples in robotics and AI", "Course roadmap"],
   "Motivate feedback control as the regulator of behavior.", "Control makes behavior stable and predictable."),
  S("2", "Modeling Dynamic Systems", ["Differential equations and state space", "Transfer functions and Laplace", "Mechanical and electrical examples", "Block diagrams"],
   "Describe a system mathematically before controlling it.", "A model is the controller's blueprint."),
  S("3", "Time-Domain Analysis", ["Step response and transient specs", "Rise time, settling time, overshoot", "Steady-state error", "First- and second-order systems"],
   "Predict how a system responds over time.", "Transient behavior reveals system character."),
  S("4", "Stability & Frequency Response", ["Routh–Hurwitz stability", "Bode plots and gain/phase margins", "Nyquist criterion intro", "Root locus basics"],
   "Guarantee a controller will not diverge.", "Stability is non-negotiable."),
  S("5", "PID Control", ["Proportional, integral, derivative actions", "PID tuning: Ziegler–Nichols", "PID for motor position and speed", "Anti-windup and limits"],
   "Implement the most-used controller in robotics.", "PID is the workhorse of motion control."),
  S("6", "Control in Robotics & Review", ["Cascade and feedforward control", "Digital control and sampling", "Course recap and assessment", "Toward intelligent control (AI.308)"],
   "Apply control to real robotic platforms.", "Control turns intent into motion.")],
),
]

# ---------------- YEAR 1 SEMESTER 2 ----------------
YS2 = "YEAR 1 · SEMESTER 2"
ALL_COURSES += [
course("AI.107", "Data Structures and Algorithms", YS2,
 "Organizing data and analyzing algorithms: arrays, lists, trees, graphs, sorting, searching, and complexity.",
 [S("1", "Orientation: Data + Algorithms", ["Why data structures matter", "Abstract data types", "Algorithm analysis motivation", "Course scope"],
   "Frame computing as data organization plus stepwise logic.", "The right structure makes the algorithm efficient."),
  S("2", "Complexity Analysis", ["Big O, Big Omega, Big Theta", "Time vs. space complexity", "Analyzing loops and recursion", "Best/average/worst case"],
   "Quantify algorithm cost before coding.", "Complexity predicts scalability."),
  S("3", "Linear Structures", ["Arrays and dynamic arrays", "Linked lists: singly, doubly", "Stacks and queues", "Applications: undo, BFS"],
   "Choose and implement linear collections.", "Order defines access pattern."),
  S("4", "Sorting & Searching", ["Bubble, insertion, selection", "Merge sort and quick sort", "Binary search", "Hashing and hash tables"],
   "Order and retrieve data efficiently.", "Sorting is the prerequisite for fast search."),
  S("5", "Trees & Graphs", ["Binary trees and BSTs", "Tree traversals", "Graph representations", "BFS/DFS and shortest path intro"],
   "Model relationships and networks.", "Graphs model everything from circuits to cities."),
  S("6", "Algorithms for AI & Robotics", ["A* and graph search in navigation", "Algorithm selection for embedded", "Course recap and assessment", "Toward embedded systems (AI.109)"],
   "Use algorithms to make robots think fast.", "Efficient algorithms enable real-time robots.")],
),
course("AI.108", "Digital Signal Processing", YS2,
 "Representing and manipulating signals in discrete time: sampling, filtering, transforms, and spectral analysis.",
 [S("1", "Orientation: Signals in Machines", ["Continuous vs. discrete signals", "Sampling and the Nyquist theorem", "Quantization and digital audio", "DSP in robotics and AI"],
   "Convert the analog world into numbers.", "Digital signals are sampled slices of reality."),
  S("2", "Discrete-Time Systems", ["Difference equations", "Linear time-invariant (LTI) systems", "Impulse response and convolution", "System stability"],
   "Model systems that process sequences.", "LTI systems are analyzable and composable."),
  S("3", "The z-Transform", ["z-transform definition", "Region of convergence", "Transfer functions in z", "Poles and zeros"],
   "Analyze discrete systems in the z-domain.", "The z-domain is to discrete what s-domain is to continuous."),
  S("4", "Digital Filtering", ["FIR vs. IIR filters", "Filter design: windowing method", "Low-pass, high-pass, band-pass", "Filtering sensor data"],
   "Remove noise and extract bands of interest.", "Filters shape a signal's frequency content."),
  S("5", "Spectral Analysis", ["Discrete Fourier Transform (DFT)", "FFT algorithm", "Spectral leakage and windowing", "Frequency-domain interpretation"],
   "Reveal the frequencies inside a signal.", "The spectrum shows what a signal is made of."),
  S("6", "DSP in Perception & Review", ["Audio and sensor signal processing", "Real-time DSP on embedded", "Course recap and assessment", "Toward machine vision and perception"],
   "DSP cleans the raw signals robots rely on.", "Good perception starts with clean signals.")],
),
course("AI.109", "Embedded Systems", YS2,
 "Computing on constrained hardware: microcontrollers, I/O, interrupts, and real-time considerations for robotics.",
 [S("1", "Orientation: Computers in Things", ["Embedded vs. general-purpose systems", "Microcontroller architecture", "The embedded software stack", "Role in robotics"],
   "Understand computing inside physical devices.", "Embedded systems are computers that interact with the world."),
  S("2", "Microcontroller Internals", ["CPU, memory, and buses", "GPIO and digital I/O", "Timers and counters", "Interrupts and ISRs"],
   "Program the processor and respond to events.", "Interrupts make embedded systems responsive."),
  S("3", "Analog & Communication", ["ADC and DAC", "PWM for motor control", "UART, I2C, SPI protocols", "Sensor interfacing"],
   "Bridge the digital processor and analog world.", "Protocols let chips talk to sensors and actuators."),
  S("4", "Real-Time Concepts", ["Determinism and latency", "Task scheduling basics", "RTOS introduction", "Deadlines and jitter"],
   "Guarantee timing-critical robot behavior.", "In robotics, late answers can be wrong answers."),
  S("5", "Power & Hardware Integration", ["Power budgets and regulators", "PCB layout basics", "Debugging embedded systems", "Hardware–software co-design"],
   "Build reliable embedded hardware.", "Power and layout determine reliability."),
  S("6", "Embedded AI & Review", ["TinyML and on-device inference", "Course recap and assessment", "Toward IoT (AI.201)", "Final project preview"],
   "Run intelligence on the edge.", "AI on the edge means intelligence wherever the robot is.")],
),
course("AI.110", "Human-Robot Interaction", YS2,
 "Designing robots that communicate and collaborate with people: interfaces, social cues, and trust.",
 [S("1", "Orientation: Robots Among People", ["What is HRI", "Why human-centered design matters", "Domains: assistive, service, collaborative", "Course roadmap"],
   "Put the human at the center of robot design.", "A robot's user is usually a person."),
  S("2", "Communication Modalities", ["Speech and natural language", "Gestures and body language", "Facial expression and gaze", "Haptics and touch"],
   "Give robots multiple ways to express intent.", "Communication is multimodal, not just words."),
  S("3", "Social Cues & Proxemics", ["Personal space and distance", "Turn-taking and attention", "Joint attention", "Social norms for robots"],
   "Make robots behave socially appropriately.", "Respecting space builds trust."),
  S("4", "Trust & Acceptance", ["Factors influencing trust", "Anthropomorphism and uncanny valley", "Transparency and explainability", "User studies and evaluation"],
   "Design robots people will trust and use.", "Trust is earned through predictable behavior."),
  S("5", "Collaborative & Assistive Robots", ["Cobots in industry", "Assistive robots for disabilities", "Teleoperation and shared control", "Safety in close interaction"],
   "Build robots that work beside people.", "Collaboration requires shared understanding."),
  S("6", "HRI Ethics & Review", ["Privacy and surveillance", "Dependency and manipulation", "Course recap and assessment", "Toward social robotics (AI.312)"],
   "Interact ethically with vulnerable users.", "Respecting persons is the foundation of HRI.")],
),
course("AI.111", "Neural Networks", YS2,
 "Artificial neural networks: perceptrons, multilayer networks, backpropagation, and training deep models.",
 [S("1", "Orientation: Brains in Silicon", ["Biological inspiration", "The perceptron", "Multilayer perceptrons", "Neural networks in AI"],
   "Introduce the neuron as a computational unit.", "Networks of simple units compute complex functions."),
  S("2", "Activation & Forward Pass", ["Sigmoid, tanh, ReLU activations", "Forward propagation", "Loss functions", "Output layers for regression/classification"],
   "Compute predictions from inputs through layers.", "The forward pass turns data into predictions."),
  S("3", "Backpropagation", ["Chain rule and gradients", "Computing gradients backward", "Weight updates", "Stochastic gradient descent"],
   "Train networks by propagating error.", "Backpropagation is how networks learn from mistakes."),
  S("4", "Training Dynamics", ["Learning rate and momentum", "Batch vs. mini-batch", "Overfitting and regularization", "Dropout and early stopping"],
   "Train models that generalize.", "Training well is harder than training fast."),
  S("5", "Network Architectures", ["Feedforward networks", "Convolutional networks intro", "Recurrent networks intro", "Autoencoders"],
   "Match architecture to data type.", "Architecture encodes inductive bias."),
  S("6", "Neural Networks in Robotics & Review", ["Perception and control networks", "Deployment on embedded", "Course recap and assessment", "Toward deep learning (AI.210)"],
   "Deploy learned models on robots.", "Learned models give robots adaptive behavior.")],
),
course("AI.112", "Computer Graphics", YS2,
 "Generating synthetic images: geometry, transformations, lighting, rendering, and visualization for simulation.",
 [S("1", "Orientation: Pixels from Math", ["Raster vs. vector graphics", "The graphics pipeline", "Coordinate systems", "Graphics in simulation and VR"],
   "Create images algorithmically rather than capturing them.", "Graphics synthesize reality from geometry."),
  S("2", "2D & 3D Transformations", ["Translation, rotation, scaling", "Homogeneous coordinates", "Composite transformations", "Viewing and projection"],
   "Move and shape objects in virtual space.", "Transformations place objects in a scene."),
  S("3", "Geometric Modeling", ["Polygon meshes", "Curves and surfaces", "Scene graphs", "Modeling for robot simulation"],
   "Represent shape digitally.", "Meshes are the skin of virtual objects."),
  S("4", "Lighting & Shading", ["Light sources and materials", "Phong and Gouraud shading", "Shadows", "Global illumination intro"],
   "Make virtual scenes look physical.", "Lighting gives form its presence."),
  S("5", "Rendering & Visualization", ["Rasterization and ray tracing basics", "Textures and mapping", "Real-time rendering", "Visualizing sensor data"],
   "Produce the final image from a scene.", "Rendering is the last step of the pipeline."),
  S("6", "Graphics for Robotics & Review", ["Robot simulation environments", "Visualizing point clouds", "Course recap and assessment", "Toward VR (AI.301)"],
   "Use graphics to simulate and test robots.", "Simulation lets robots practice before they move.")],
),
]

# ---------------- YEAR 2 SEMESTER 1 ----------------
Y2S1 = "YEAR 2 · SEMESTER 1"
ALL_COURSES += [
course("AI.201", "Internet of Things", Y2S1,
 "Networked physical devices: sensors, connectivity, cloud integration, and edge computing for smart systems.",
 [S("1", "Orientation: The Connected World", ["What is IoT", "Sensors, actuators, and things", "Connectivity options", "IoT architecture"],
   "See the world as a network of sensing devices.", "IoT is the internet extended to physical things."),
  S("2", "Protocols & Connectivity", ["MQTT, CoAP, HTTP", "Wi-Fi, Bluetooth, Zigbee, LoRaWAN", "IPv6 and 6LoWPAN", "Gateway and edge devices"],
   "Choose the right network for each device.", "Connectivity is chosen by range, power, and bandwidth."),
  S("3", "Cloud & Edge Platforms", ["Cloud IoT platforms", "Edge computing and fog", "Data ingestion and storage", "Dashboards and visualization"],
   "Process data where it makes sense.", "The cloud stores; the edge acts fast."),
  S("4", "Security & Privacy", ["Device authentication", "Encryption in transit and at rest", "Firmware updates", "Privacy by design"],
   "Secure devices from chip to cloud.", "A chain is only as strong as its weakest node."),
  S("5", "IoT in Robotics", ["Connected robots and fleets", "Telemetry and remote monitoring", "Over-the-air updates", "Case studies"],
   "Network robots for fleet intelligence.", "Connected robots learn from each other."),
  S("6", "IoT Project & Review", ["Mini IoT prototype", "Course recap and assessment", "Toward CPS (AI.302)", "Design review"],
   "Build a small connected sensing system.", "Prototyping turns concepts into working things.")],
),
course("AI.202", "Robotic Perception", Y2S1,
 "Fusing sensor data to understand the world: vision, LiDAR, depth, and multimodal perception for robots.",
 [S("1", "Orientation: Perceiving the World", ["Perception pipeline", "Uncertainty in sensing", "Modality trade-offs", "Perception in autonomy"],
   "Give robots a model of their surroundings.", "Perception turns raw signals into world models."),
  S("2", "Visual Perception", ["Camera models and calibration", "Stereo vision and depth", "Optical flow", "Object detection for robots"],
   "Extract 3D structure from 2D images.", "Stereo and flow reveal distance and motion."),
  S("3", "Range Sensing", ["LiDAR and point clouds", "Depth cameras", "Ultrasonic and infrared", "Point-cloud registration (ICP)"],
   "Measure distance and shape directly.", "Range sensors give precise spatial answers."),
  S("4", "Sensor Fusion", ["Why fuse sensors", "Kalman filter introduction", "Extended Kalman filter", "Complementary filtering"],
   "Combine sensors for a better estimate.", "Fused sensors see more clearly than any alone."),
  S("5", "Perception for Navigation", ["Obstacle detection", "Free-space segmentation", "Place recognition", "Semantic mapping"],
   "Support safe robot motion.", "Perception answers 'where can I go?'."),
  S("6", "Perception Systems & Review", ["Real-time perception on robots", "Course recap and assessment", "Toward localization (AI.310)", "System integration"],
   "Integrate perception into a robot loop.", "Perception closes the loop with action.")],
),
course("AI.203", "Ethics in AI and Robotics", Y2S1,
 "Moral and societal dimensions of intelligent machines: bias, safety, accountability, and responsible design.",
 [S("1", "Orientation: Why Ethics Now", ["Ethics vs. law vs. policy", "AI and robotics impact", "Responsible innovation", "Course framework"],
   "Treat ethics as a core engineering constraint.", "Building smart is not enough; it must be right."),
  S("2", "Bias & Fairness", ["Sources of bias in data and algorithms", "Fairness metrics", "Mitigation strategies", "Case studies"],
   "Detect and reduce unfair outcomes.", "Data reflects history—including its injustices."),
  S("3", "Safety & Risk", ["Functional safety", "Risk assessment", "Fail-safe design", "Autonomous weapons debate"],
   "Design systems that fail safely.", "Safety must be engineered in, not bolted on."),
  S("4", "Accountability & Transparency", ["Explainable AI (XAI)", "Who is responsible", "Auditability", "Regulatory landscape"],
   "Make decisions traceable and justifiable.", "If a robot harms, someone must answer."),
  S("5", "Privacy & Autonomy", ["Surveillance and data collection", "Human autonomy and consent", "Workplace automation", "Digital rights"],
   "Respect persons and their data.", "Technology should serve human agency, not replace it."),
  S("6", "Ethical Practice & Review", ["Ethical design frameworks", "Course recap and assessment", "Toward robot ethics (AI.402)", "Ethics pledge"],
   "Adopt a personal code of responsible engineering.", "Engineers are stewards of trust.")],
),
course("AI.204", "Autonomous Systems", Y2S1,
 "Systems that operate without continuous human input: autonomy levels, decision making, and self-management.",
 [S("1", "Orientation: Toward Autonomy", ["Levels of autonomy", "Sense–plan–act autonomy", "Benefits and risks", "Autonomy in AI and robotics"],
   "Define what it means for a machine to act alone.", "Autonomy is delegated decision-making."),
  S("2", "Autonomy Architecture", ["Hierarchical vs. reactive", "Behavior trees", "Finite state machines", "Supervisory control"],
   "Structure autonomous decision-making.", "Architecture determines how autonomously a system acts."),
  S("3", "Mission & Task Planning", ["Mission specification", "Task decomposition", "Contingency handling", "Replanning"],
   "Turn goals into executable missions.", "Planning under autonomy must anticipate surprises."),
  S("4", "Decision Making Under Uncertainty", ["POMDPs introduction", "Belief states", "Policy and value", "Online decision making"],
   "Choose actions when the world is unclear.", "Uncertainty is the rule, not the exception."),
  S("5", "Safety in Autonomy", ["Safe autonomy envelopes", "Monitoring and fallback", "Human-in-the-loop", "Validation of autonomous systems"],
   "Keep autonomous systems within safe bounds.", "Autonomy without safety is dangerous."),
  S("6", "Autonomous Systems & Review", ["Case studies: self-driving, drones", "Course recap and assessment", "Toward mobile robotics (AI.207)", "Autonomy demo"],
   "Operate a system with minimal supervision.", "True autonomy earns human trust.")],
),
course("AI.205", "Reinforcement Learning", Y2S1,
 "Learning from interaction: agents, rewards, policies, and value-based methods for sequential decision making.",
 [S("1", "Orientation: Learning by Doing", ["RL vs. supervised learning", "Agent–environment loop", "Rewards and returns", "Applications in robotics"],
   "Learn optimal behavior from trial and error.", "Reinforcement learning learns from consequences."),
  S("2", "Markov Decision Processes", ["States, actions, transitions", "Rewards and discounting", "Policies and value functions", "Bellman equation"],
   "Model sequential decisions formally.", "MDPs are the mathematical heart of RL."),
  S("3", "Dynamic Programming", ["Policy evaluation and improvement", "Policy iteration", "Value iteration", "Model-based planning"],
   "Solve MDPs when the model is known.", "Dynamic programming computes optimal policies exactly."),
  S("4", "Model-Free RL", ["Monte Carlo methods", "Temporal difference learning", "Q-learning", "SARSA"],
   "Learn without a model of the world.", "Model-free agents learn from experience alone."),
  S("5", "Deep RL", ["Deep Q-networks (DQN)", "Policy gradients", "Actor–critic", "RL in continuous control"],
   "Scale RL to high-dimensional robot tasks.", "Deep RL lets robots learn complex skills."),
  S("6", "RL for Robots & Review", ["Sim-to-real transfer", "Safe exploration", "Course recap and assessment", "Toward robot learning (AI.403)"],
   "Deploy learned policies on real robots.", "Simulation trains; reality tests.")],
),
course("AI.206", "Computer Architecture", Y2S1,
 "How computers are built: processors, memory hierarchy, I/O, and performance—basis for embedded AI hardware.",
 [S("1", "Orientation: Machines That Compute", ["Von Neumann architecture", "Instruction cycle", "CPU vs. GPU vs. TPU", "Architecture and AI workloads"],
   "Understand the machine that runs the software.", "Architecture determines what software can do."),
  S("2", "Processor Design", ["Datapath and control", "Pipelining", "Superscalar and out-of-order", "Instruction sets (RISC/CISC)"],
   "Execute instructions efficiently.", "Pipelining lets many instructions overlap."),
  S("3", "Memory Hierarchy", ["Cache levels and locality", "Virtual memory", "RAM and storage", "Memory bandwidth"],
   "Feed the processor fast enough.", "Memory is the bottleneck of modern computing."),
  S("4", "I/O & Interconnects", ["Buses and interfaces", "DMA", "Interrupts vs. polling", "GPU interconnects"],
   "Move data between processor and devices.", "Fast processors need fast I/O."),
  S("5", "Performance & Parallelism", ["Amdahl's law", "Multi-core and many-core", "SIMD and vectorization", "Benchmarking"],
   "Measure and improve system speed.", "Parallelism is the path to performance."),
  S("6", "Architecture for AI & Review", ["AI accelerators and TPUs", "Edge AI hardware", "Course recap and assessment", "Toward robot design (AI.411)"],
   "Match hardware to intelligent workloads.", "AI needs specialized silicon.")],
),
]

# ---------------- YEAR 2 SEMESTER 2 ----------------
Y2S2 = "YEAR 2 · SEMESTER 2"
ALL_COURSES += [
course("AI.207", "Mobile Robotics", Y2S2,
 "Robots that move: locomotion, wheeled and legged platforms, navigation, and mobile manipulation.",
 [S("1", "Orientation: Robots That Move", ["Locomotion types", "Wheeled vs. legged vs. aerial", "Mobile robot applications", "Challenges of mobility"],
   "Survey how robots get from place to place.", "Mobility expands a robot's reach."),
  S("2", "Wheeled Locomotion", ["Differential drive", "Ackermann steering", "Omnidirectional and mecanum", "Odometry"],
   "Model and control wheeled motion.", "Wheels are efficient on structured floors."),
  S("3", "Legged Locomotion", ["Bipedal, quadruped, hexapod", "Gaits and walking", "Balance and ZMP", "Boston-dynamics-style platforms"],
   "Achieve stable walking on legs.", "Legs go where wheels cannot."),
  S("4", "Mobile Navigation", ["Waypoint following", "Obstacle avoidance", "Potential fields", "Vector field histograms"],
   "Move safely toward a goal.", "Navigation is motion with awareness."),
  S("5", "Manipulation on the Move", ["Mobile bases with arms", "Coordination of base and manipulator", "Whole-body control", "Case studies"],
   "Combine movement with manipulation.", "Mobile manipulators do work across spaces."),
  S("6", "Mobile Robotics & Review", ["Platform demo and assessment", "Course recap", "Toward AI for robotics (AI.208)", "Field trial"],
   "Operate a mobile robot end-to-end.", "A mobile robot must go, sense, and act.")],
),
course("AI.208", "AI for Robotics", Y2S2,
 "Integrating AI methods—perception, planning, learning—into embodied robotic systems.",
 [S("1", "Orientation: Embodied AI", ["AI in the robot loop", "Embodiment and situatedness", "Perception–action coupling", "Course roadmap"],
   "Put intelligence inside a body.", "Embodied AI acts in the world it perceives."),
  S("2", "Perception for Action", ["Vision for grasping", "Tactile and force sensing", "Multimodal fusion", "Perception–action loop"],
   "Let perception guide immediate action.", "Seeing is for doing."),
  S("3", "Learning for Control", ["Imitation learning", "Reinforcement learning for control", "Sim-to-real", "Skill acquisition"],
   "Teach robots skills rather than code them.", "Robots learn best by doing."),
  S("4", "Task & Motion Planning", ["Task planning", "Motion planning integration", "Symbolic and geometric reasoning", "Manipulation planning"],
   "Plan both what to do and how to move.", "Tasks give purpose; motion gives movement."),
  S("5", "Human-in-the-Loop AI", ["Teleoperation and shared autonomy", "Robot learning from humans", "Interactive learning", "Trust and transparency"],
   "Blend human and machine intelligence.", "Humans and robots learn together."),
  S("6", "AI for Robotics & Review", ["Integrated robot demo", "Course recap and assessment", "Toward swarm robotics (AI.303)", "Capstone preview"],
   "Run a full AI–robot pipeline.", "Embodied intelligence is the sum of perception, planning, and action.")],
),
course("AI.209", "Fuzzy Logic", Y2S2,
 "Reasoning with imprecision: fuzzy sets, linguistic variables, and fuzzy control for uncertain systems.",
 [S("1", "Orientation: Reasoning with Vagueness", ["Crisp vs. fuzzy sets", "Why classical logic is not enough", "Fuzzy logic in control", "Applications"],
   "Model concepts that admit degrees.", "Many real-world properties are a matter of degree."),
  S("2", "Fuzzy Sets & Membership", ["Membership functions", "Linguistic variables", "Fuzzy operators: AND, OR, NOT", "Fuzzification"],
   "Quantify partial truth.", "Fuzzy logic computes with words."),
  S("3", "Fuzzy Inference", ["Rule base: IF–THEN rules", "Mamdani and Sugeno inference", "Defuzzification", "Fuzzy rule design"],
   "Derive crisp actions from fuzzy inputs.", "Rules plus inference make decisions."),
  S("4", "Fuzzy Control", ["Fuzzy PID", "Fuzzy control of nonlinear plants", "Tuning membership functions", "Stability considerations"],
   "Control systems without precise models.", "Fuzzy control works where models fail."),
  S("5", "Fuzzy in Robotics", ["Fuzzy obstacle avoidance", "Fuzzy navigation", "Fuzzy sensor fusion", "Case studies"],
   "Handle noisy, uncertain robot data.", "Robots live in a fuzzy world."),
  S("6", "Fuzzy Logic & Review", ["Fuzzy controller implementation", "Course recap and assessment", "Toward deep learning (AI.210)", "Fuzzy vs. PID comparison"],
   "Embrace uncertainty in control.", "Precision is not always possible—or necessary.")],
),
course("AI.210", "Deep Learning", Y2S2,
 "Deep neural networks: CNNs, RNNs, transformers, and modern architectures for perception and sequence tasks.",
 [S("1", "Orientation: The Deep Revolution", ["From shallow to deep", "Why depth matters", "Data and compute needs", "Deep learning in AI and robotics"],
   "Enter the era of deep representations.", "Depth learns hierarchy."),
  S("2", "Convolutional Networks", ["Convolution operation", "CNN architectures", "Pooling and normalization", "Transfer learning"],
   "Process images and spatial data.", "CNNs see patterns across space."),
  S("3", "Recurrent Networks", ["RNNs and LSTMs", "Sequence modeling", "GRUs", "Time-series forecasting"],
   "Handle data that unfolds over time.", "Sequences carry memory."),
  S("4", "Attention & Transformers", ["Attention mechanism", "Transformer architecture", "Self-attention", "Language and vision transformers"],
   "Focus on what matters.", "Attention weights relevance dynamically."),
  S("5", "Training Deep Networks", ["Backprop through depth", "Optimizers: Adam, RMSprop", "Batch normalization", "Regularization"],
   "Train very deep models reliably.", "Depth brings power and training challenges."),
  S("6", "Deep Learning for Robots & Review", ["Deep perception and control", "Deployment on edge", "Course recap and assessment", "Toward pattern recognition (AI.211)"],
   "Deploy deep models on embodied agents.", "Deep learning gives robots rich perception.")],
),
course("AI.211", "Pattern Recognition", Y2S2,
 "Classifying and clustering patterns: feature extraction, classifiers, and evaluation for perception and diagnostics.",
 [S("1", "Orientation: Seeing Patterns", ["What is pattern recognition", "Feature extraction and selection", "Supervised vs. unsupervised", "Applications"],
   "Recognize structure in data.", "Patterns are the signature of meaning."),
  S("2", "Classical Classifiers", ["Nearest neighbor", "Linear discriminant analysis", "Naive Bayes", "Support vector machines"],
   "Assign patterns to categories.", "Classifiers draw boundaries in feature space."),
  S("3", "Feature Engineering", ["Descriptors and histograms", "Dimensionality reduction", "Feature selection", "Domain-specific features"],
   "Represent patterns compactly.", "Good features make classification easy."),
  S("4", "Clustering", ["k-means and variants", "Gaussian mixture models", "DBSCAN", "Cluster evaluation"],
   "Group similar patterns together.", "Clustering finds categories without labels."),
  S("5", "Evaluation", ["Confusion matrix", "ROC and AUC", "Cross-validation", "Precision-recall"],
   "Judge a recognizer honestly.", "Accuracy alone can mislead."),
  S("6", "Pattern Recognition in AI & Review", ["Speech, vision, and sensor patterns", "Course recap and assessment", "Toward robot kinematics (AI.212)", "Recognizer demo"],
   "Build a pattern recognizer end-to-end.", "Recognition turns raw data into categories.")],
),
course("AI.212", "Robot Kinematics", Y2S2,
 "Describing robot motion mathematically: forward and inverse kinematics, Jacobians, and manipulator control.",
 [S("1", "Orientation: Motion in Math", ["Why kinematics matters", "Robot links and joints", "Degrees of freedom", "Workspace"],
   "Describe robot geometry precisely.", "Kinematics is the language of robot motion."),
  S("2", "Representations", ["Rotation matrices", "Homogeneous transforms", "Euler angles and quaternions", "Denavit–Hartenberg convention"],
   "Represent position and orientation.", "Transforms move frames through space."),
  S("3", "Forward Kinematics", ["Computing end-effector pose", "DH parameters", "Serial-chain FK", "Examples: 2-link, 6-DOF arm"],
   "Find where the tool is from joint angles.", "Forward kinematics answers 'where am I?'."),
  S("4", "Inverse Kinematics", ["IK problem", "Analytical vs. numerical IK", "Multiple solutions", "Jacobian-based IK"],
   "Find joint angles for a desired pose.", "Inverse kinematics answers 'how do I get there?'."),
  S("5", "Jacobians & Velocities", ["Jacobian matrix", "Velocity kinematics", "Singularities", "Manipulability"],
   "Relate joint speeds to tool speed.", "The Jacobian maps motion spaces."),
  S("6", "Kinematics in Control & Review", ["Kinematic control of manipulators", "Course recap and assessment", "Toward mobile robotics (AI.207)", "IK lab"],
   "Use kinematics to command robot arms.", "Control without kinematics is blind.")],
),
]

# ---------------- YEAR 3 SEMESTER 1 ----------------
Y3S1 = "YEAR 3 · SEMESTER 1"
ALL_COURSES += [
course("AI.301", "Virtual Reality", Y3S1,
 "Immersive synthetic environments: displays, tracking, interaction, and VR for training and simulation.",
 [S("1", "Orientation: Stepping Inside", ["What is VR", "Immersion vs. presence", "VR hardware: HMDs, controllers", "VR in training and robotics"],
   "Define virtual presence.", "VR replaces the physical with the synthetic."),
  S("2", "VR Hardware & Displays", ["Head-mounted displays", "Lenses and distortion", "Tracking systems", "Input devices"],
   "Build the sensory interface.", "Presence begins with the display."),
  S("3", "3D Interaction", ["Selection and manipulation", "Wayfinding and navigation", "Gestures in VR", "Haptic feedback"],
   "Let users act inside virtual worlds.", "Interaction makes VR participatory."),
  S("4", "Rendering for VR", ["Stereo rendering", "Latency and frame rate", "Distortion correction", "Performance budgets"],
   "Render two views fast enough.", "VR demands low latency and high frame rates."),
  S("5", "VR for Robotics", ["Robot telepresence", "VR training environments", "Sim-to-real VR", "Human-in-the-loop simulation"],
   "Train and operate robots in VR.", "VR is a safe training ground for robots."),
  S("6", "VR Systems & Review", ["VR prototype demo", "Course recap and assessment", "Toward CPS (AI.302)", "User study"],
   "Build and evaluate a VR experience.", "Presence is measured by the user.")],
),
course("AI.302", "Cyber-Physical Systems", Y3S1,
 "Integrating computation, networking, and physical processes: CPS architecture, real-time coordination, and safety.",
 [S("1", "Orientation: The Cyber-Physical Merge", ["What is CPS", "Computation + networking + physics", "CPS vs. IoT", "Applications"],
   "Blend the digital with the physical.", "CPS are systems where software moves matter."),
  S("2", "CPS Architecture", ["Sensors, controllers, actuators", "Networked control", "Real-time operating systems", "System-of-systems"],
   "Architect tight cyber–physical loops.", "Architecture binds computation to physics."),
  S("3", "Real-Time Coordination", ["Time-triggered vs. event-triggered", "Synchronization", "Scheduling", "Determinism"],
   "Coordinate actions across time.", "Time is the glue of cyber–physical systems."),
  S("4", "Safety & Reliability", ["Fault tolerance", "Redundancy", "Fail-operational design", "Safety standards"],
   "Keep physical processes safe.", "Physical stakes demand high reliability."),
  S("5", "CPS in Robotics", ["Robotic CPS examples", "Smart manufacturing", "Autonomous vehicles", "Medical robotics"],
   "Apply CPS to embodied systems.", "Modern robots are quintessential CPS."),
  S("6", "CPS Design & Review", ["CPS prototype", "Course recap and assessment", "Toward swarm robotics (AI.303)", "System validation"],
   "Design a cyber–physical system end-to-end.", "CPS must be safe by design.")],
),
course("AI.303", "Swarm Robotics", Y3S1,
 "Collective robotics: decentralized coordination, emergence, and scalable multi-robot behaviors.",
 [S("1", "Orientation: Strength in Numbers", ["What is swarm robotics", "Decentralization and emergence", "Bio-inspiration: ants, bees", "Swarm advantages"],
   "Many simple robots can do complex things.", "Collective intelligence beats individual complexity."),
  S("2", "Swarm Behaviors", ["Aggregation and dispersion", "Flocking and alignment", "Foraging", "Synchronization"],
   "Program collective motion.", "Simple local rules yield global patterns."),
  S("3", "Local Communication", ["Direct and indirect communication", "Stigmergy", "Local sensing", "Limited-range interaction"],
   "Coordinate with only local knowledge.", "Locality scales to large swarms."),
  S("4", "Task Allocation", ["Dynamic task partitioning", "Market-based and threshold methods", "Adaptivity", "Load balancing"],
   "Divide work among robots.", "Tasks should find the right robot."),
  S("5", "Swarm Intelligence Algorithms", ["Ant colony optimization", "Particle swarm optimization", "Swarm applications", "Optimization"],
   "Solve problems with swarms.", "Swarm intelligence optimizes through collective search."),
  S("6", "Swarm Systems & Review", ["Swarm demo (simulation)", "Course recap and assessment", "Toward ROS (AI.304)", "Scalability discussion"],
   "Coordinate many robots as one system.", "A swarm is more than the sum of its robots.")],
),
course("AI.304", "Robot Operating Systems", Y3S1,
 "The ROS ecosystem: nodes, topics, services, actions, launch files, and middleware for robot software.",
 [S("1", "Orientation: The Robot OS", ["What is ROS", "ROS architecture", "Why ROS dominates robotics", "ROS1 vs ROS2"],
   "Learn the middleware of modern robots.", "ROS is the shared language of robot software."),
  S("2", "Nodes & Communication", ["ROS nodes", "Topics and publishers/subscribers", "Services", "Messages and parameters"],
   "Build modular robot software.", "Nodes talk through topics and services."),
  S("3", "Tools & Workflow", ["roscore, rosrun, roslaunch", "rviz and gazebo", "rosbag", "Catkin/colcon build"],
   "Develop, visualize, and log robot software.", "Tools make ROS development tractable."),
  S("4", "Actions & Coordination", ["Actionlib and action servers", "Goal feedback and preemption", "Complex robot behaviors", "State machines (SMACH)"],
   "Manage long-running robot tasks.", "Actions coordinate multi-step behavior."),
  S("5", "ROS in Practice", ["Integrating drivers", "Multi-robot namespaces", "Real-time considerations", "Debugging ROS"],
   "Deploy ROS on real robots.", "ROS must run reliably on hardware."),
  S("6", "ROS Project & Review", ["ROS-based robot demo", "Course recap and assessment", "Toward cognitive robotics (AI.305)", "Code review"],
   "Build a complete ROS robot system.", "ROS integrates perception, planning, and action.")],
),
course("AI.305", "Cognitive Robotics", Y3S1,
 "Robots with reasoning, memory, and awareness: knowledge, planning, and metacognition in embodied agents.",
 [S("1", "Orientation: Thinking Robots", ["What is cognitive robotics", "Cognition vs. reactivity", "Architectures: Soar, ACT-R", "Course roadmap"],
   "Give robots knowledge and reasoning.", "Cognitive robots understand what they do."),
  S("2", "Knowledge & Reasoning", ["Knowledge representation", "Automated reasoning", "Belief revision", "Commonsense reasoning"],
   "Let robots reason about their world.", "Reasoning turns data into understanding."),
  S("3", "Memory & Learning", ["Episodic and semantic memory", "Lifelong learning", "Memory consolidation", "Robot autobiographical memory"],
   "Remember and learn over time.", "Cognition needs memory across experiences."),
  S("4", "Metacognition & Awareness", ["Self-monitoring", "Error detection", "Confidence and uncertainty", "Robot self-awareness intro"],
   "Robots that know what they know.", "Metacognition enables self-improvement."),
  S("5", "Human-like Interaction", ["Theory of mind for robots", "Collaborative reasoning", "Explainable robot behavior", "Social cognition"],
   "Interact as a cognitive partner.", "Partners understand each other's minds."),
  S("6", "Cognitive Robotics & Review", ["Cognitive robot demo", "Course recap and assessment", "Toward bio-inspired robotics (AI.306)", "Reasoning eval"],
   "Integrate reasoning into a robot.", "Cognition closes the loop from perception to purpose.")],
),
course("AI.306", "Biologically Inspired Robotics", Y3S1,
 "Robots modeled on nature: locomotion, sensing, and control principles from animals and plants.",
 [S("1", "Orientation: Learning from Life", ["Bio-inspiration vs. biomimetics", "Why nature is a good teacher", "Organisms as models", "Course scope"],
   "Mine biology for robot design ideas.", "Evolution has already solved mobility."),
  S("2", "Bio-Inspired Locomotion", ["Snake, fish, and insect gaits", "Muscle-like actuators", "Compliant mechanisms", "Soft robotics"],
   "Move like living organisms.", "Nature's movers are efficient and adaptable."),
  S("3", "Bio-Inspired Sensing", ["Vision systems: insect eyes", "Whiskers and tactile", "Echolocation and lateral line", "Chemical sensing"],
   "Sense like animals do.", "Biological sensors are tuned and efficient."),
  S("4", "Neuromorphic Control", ["Spiking neural networks", "Central pattern generators", "Reflexes and reflexes", "Bio-control architectures"],
   "Control like a nervous system.", "Brains control bodies efficiently."),
  S("5", "Swarm & Social Biology", ["Ant colonies and bee swarms", "Flocking and schooling", "Territoriality", "Collective behavior"],
   "Coordinate like social animals.", "Biology excels at decentralized coordination."),
  S("6", "Bio-Robotics & Review", ["Bio-robot prototype", "Course recap and assessment", "Toward machine vision (AI.307)", "Design review"],
   "Build robots inspired by life.", "Nature is the ultimate robotics lab.")],
),
]

# ---------------- YEAR 3 SEMESTER 2 ----------------
Y3S2 = "YEAR 3 · SEMESTER 2"
ALL_COURSES += [
course("AI.307", "Machine Vision", Y3S2,
 "Advanced machine vision: 3D reconstruction, object tracking, and vision systems for industrial and robotic inspection.",
 [S("1", "Orientation: Vision for Machines", ["Machine vision vs. computer vision", "Industrial vision systems", "Vision pipeline", "Applications"],
   "Engineer vision for inspection and guidance.", "Machine vision measures and decides."),
  S("2", "3D Vision", ["Structured light and stereo", "Time-of-flight", "3D reconstruction", "Point clouds"],
   "Recover 3D from 2D images.", "Depth makes vision spatial."),
  S("3", "Object Tracking", ["Tracking by detection", "Kalman filter tracking", "Optical flow tracking", "Occlusion handling"],
   "Follow objects over time.", "Tracking links frames into stories."),
  S("4", "Inspection & Gauging", ["Defect detection", "Measurement and gauging", "Barcode and OCR", "Vision-guided robotics"],
   "Automate quality inspection.", "Vision inspects faster and more reliably than people."),
  S("5", "Vision Systems Design", ["Lighting and optics", "Camera selection", "Real-time constraints", "Integration"],
   "Build a complete vision system.", "Lighting and optics determine image quality."),
  S("6", "Machine Vision & Review", ["Vision system demo", "Course recap and assessment", "Toward intelligent control (AI.308)", "Inspection task"],
   "Deploy vision on the factory floor.", "Good vision makes good products.")],
),
course("AI.308", "Intelligent Control Systems", Y3S2,
 "Modern control: adaptive, robust, and intelligent control for uncertain robotic plants.",
 [S("1", "Orientation: Beyond PID", ["Limitations of classical control", "Intelligent control", "Adaptive and robust control", "Applications"],
   "Control systems that adapt to change.", "Intelligent control handles uncertainty."),
  S("2", "Adaptive Control", ["Model-reference adaptive control", "Self-tuning regulators", "Parameter estimation", "Gain scheduling"],
   "Adjust the controller as the plant changes.", "Adaptation keeps performance as plants drift."),
  S("3", "Robust Control", ["H-infinity and mu-synthesis", "Uncertainty modeling", "Robust stability", "Loop shaping"],
   "Guarantee performance under uncertainty.", "Robustness is control for the unknown."),
  S("4", "Intelligent Control Methods", ["Fuzzy control", "Neural control", "Genetic-algorithm-based tuning", "Hybrid intelligent control"],
   "Combine learning and control.", "Learning + control = intelligent control."),
  S("5", "Control for Robotics", ["Impedance and admittance control", "Force control", "Whole-body control", "Physical human–robot interaction"],
   "Control robots that touch the world.", "Intelligent control enables safe contact."),
  S("6", "Intelligent Control & Review", ["Controller implementation", "Course recap and assessment", "Toward multi-robot systems (AI.309)", "Control lab"],
   "Tune an adaptive controller on hardware.", "The best controllers learn as they act.")],
),
course("AI.309", "Multi-Robot Systems", Y3S2,
 "Coordinating teams of robots: task allocation, consensus, communication, and collective decision-making.",
 [S("1", "Orientation: Teams of Robots", ["Multi-robot vs. swarm", "Coordination challenges", "Centralized vs. decentralized", "Applications"],
   "Make robots work as a team.", "Teams outperform individuals on complex tasks."),
  S("2", "Communication & Coordination", ["Inter-robot communication", "Consensus algorithms", "Leader election", "Formation control"],
   "Align robots on shared goals.", "Coordination requires shared information."),
  S("3", "Task Allocation", ["Contract net protocol", "Auction-based allocation", "Optimization methods", "Dynamic repartitioning"],
   "Assign tasks to the right robots.", "Efficient allocation maximizes team performance."),
  S("4", "Cooperative Manipulation", ["Joint carrying", "Coordination of multiple arms", "Force synchronization", "Case studies"],
   "Move large objects together.", "Cooperation handles heavy or awkward loads."),
  S("5", "Decentralized Decision Making", ["Distributed optimization", "Game theory for robots", "Voting and consensus", "Scalable protocols"],
   "Decide without a central commander.", "Decentralized teams are resilient."),
  S("6", "Multi-Robot Systems & Review", ["Team demo", "Course recap and assessment", "Toward localization (AI.310)", "Team performance eval"],
   "Evaluate a robot team end-to-end.", "A team is judged by its collective result.")],
),
course("AI.310", "Robot Localization and Mapping", Y3S2,
 "Knowing where you are and what is around you: localization, mapping, and SLAM.",
 [S("1", "Orientation: Where Am I?", ["Localization vs. mapping", "The localization problem", "Map representations", "SLAM overview"],
   "Ground the robot in its environment.", "Navigation starts with knowing where you are."),
  S("2", "Localization", ["Monte Carlo localization", "Particle filters", "EKF localization", "Global vs. local localization"],
   "Estimate robot pose from sensors.", "Filters track pose over time."),
  S("3", "Mapping", ["Occupancy grid maps", "Feature maps", "Topological maps", "Map building"],
   "Represent the world for a robot.", "Maps are the robot's memory of space."),
  S("4", "SLAM", ["Simultaneous localization and mapping", "EKF SLAM", "FastSLAM", "Graph-based SLAM"],
   "Build a map while locating in it.", "SLAM solves the chicken-and-egg problem."),
  S("5", "Loop Closure & Relocalization", ["Detecting revisited places", "Loop closure", "Kidnapped robot problem", "Global localization"],
   "Correct drift and recover from loss.", "Loop closure keeps maps consistent."),
  S("6", "Localization & Mapping & Review", ["SLAM demo", "Course recap and assessment", "Toward robotics planning (AI.311)", "Mapping exercise"],
   "Run SLAM on a mobile robot.", "A mapped world is a navigable world.")],
),
course("AI.311", "Robotics Planning", Y3S2,
 "Deliberative planning for robots: task, motion, and manipulation planning under constraints.",
 [S("1", "Orientation: Planning to Act", ["Task vs. motion planning", "Why deliberate", "Planning in robotics", "Course roadmap"],
   "Decide what to do before moving.", "Planning prevents costly mistakes."),
  S("2", "Task Planning", ["HTN and STRIPS planning", "Goal decomposition", "Plan execution and monitoring", "Replanning"],
   "Structure complex missions.", "Task planning gives a robot purpose."),
  S("3", "Motion Planning", ["Configuration space", "Roadmaps and PRM", "RRT and RRT*", "Optimal planning"],
   "Find collision-free paths.", "Motion planning finds the way."),
  S("4", "Manipulation Planning", ["Grasp planning", "Pick-and-place", "Two-arm coordination", "Constrained manipulation"],
   "Plan physical interaction with objects.", "Manipulation planning moves things intentionally."),
  S("5", "Planning Under Uncertainty", ["Contingent planning", "Belief-space planning", "Online replanning", "Robust plans"],
   "Plan when outcomes are uncertain.", "Good plans anticipate failure."),
  S("6", "Robotics Planning & Review", ["Planning demo on robot", "Course recap and assessment", "Toward social robotics (AI.312)", "Planning competition"],
   "Execute a full task–motion plan.", "Plans turn goals into robot motion.")],
),
course("AI.312", "Social Robotics", Y3S2,
 "Robots in society: social norms, long-term interaction, ethics, and robots as companions and collaborators.",
 [S("1", "Orientation: Robots in Society", ["What is social robotics", "Social robots vs. industrial robots", "Roles: companion, tutor, caregiver", "Course roadmap"],
   "Design robots for social worlds.", "Social robots relate, not just perform."),
  S("2", "Social Cognition", ["Joint attention", "Turn-taking", "Empathy and rapport", "Social intelligence"],
   "Read and respond to social cues.", "Social skill is interaction skill."),
  S("3", "Long-Term Interaction", ["Relationship building", "Adaptation over time", "User modeling", "Engagement"],
   "Sustain interaction across encounters.", "Trust grows over repeated encounters."),
  S("4", "Ethics of Social Robots", ["Attachment and dependency", "Deception and authenticity", "Privacy in the home", "Vulnerable populations"],
   "Protect users in intimate settings.", "Social robots must respect dignity."),
  S("5", "Applications", ["Education robots", "Healthcare and elder care", "Retail and hospitality", "Therapeutic robots"],
   "Deploy robots in social institutions.", "Social robots serve people in context."),
  S("6", "Social Robotics & Review", ["Social robot demo", "Course recap and assessment", "Toward evolutionary robotics (AI.401)", "Ethical reflection"],
   "Evaluate a robot's social impact.", "A social robot is measured by human well-being.")],
),
]

# ---------------- YEAR 4 SEMESTER 1 ----------------
Y4S1 = "YEAR 4 · SEMESTER 1"
ALL_COURSES += [
course("AI.401", "Evolutionary Robotics", Y4S1,
 "Evolutionary algorithms for robot design and behavior: morphology, control co-optimization, and artificial life.",
 [S("1", "Orientation: Evolving Robots", ["Evolutionary computation", "Evolutionary robotics", "Morphology and control co-design", "Artificial life"],
   "Let robots design themselves.", "Evolution discovers designs humans miss."),
  S("2", "Genetic Algorithms", ["Encoding and genomes", "Selection, crossover, mutation", "Fitness functions", "GA for robotics"],
   "Search design spaces with evolution.", "Genetic algorithms optimize by breeding solutions."),
  S("3", "Evolving Morphology", ["Evolving robot bodies", "Sim-to-real bodies", "Modular and soft robots", "Embodied evolution"],
   "Design bodies and brains together.", "Body and mind evolve as one."),
  S("4", "Evolving Control", ["Evolving neural controllers", "Behavioral diversity", "Novelty search", "Open-endedness"],
   "Evolve robot behavior directly.", "Evolution can invent unexpected behaviors."),
  S("5", "Evolutionary Multi-Objective", ["Pareto optimization", "Trade-offs in design", "NSGA-II", "Conflicting objectives"],
   "Balance competing design goals.", "Good design balances trade-offs."),
  S("6", "Evolutionary Robotics & Review", ["Evolution demo", "Course recap and assessment", "Toward robot ethics (AI.402)", "Evolved robot showcase"],
   "Evolve a robot in simulation.", "Evolution is creativity with selection.")],
),
course("AI.402", "Robot Ethics", Y4S1,
 "Ethics specific to robots: autonomy, responsibility, harm, and robot–human moral relationships.",
 [S("1", "Orientation: Ethics of Robots", ["Robot ethics vs. AI ethics", "Moral agency of robots", "Responsibility gaps", "Course framework"],
   "Ask what robots ought to do.", "Robots act in the world; their actions have moral weight."),
  S("2", "Autonomy & Responsibility", ["Moral responsibility", "Command responsibility", "Autonomous weapons", "Accountability chains"],
   "Assign responsibility for robot acts.", "When robots err, humans answer."),
  S("3", "Harm & Safety", ["Physical harm", "Psychological harm", "Risk-benefit analysis", "Safe robot design"],
   "Prevent robots from causing harm.", "Safety is an ethical obligation."),
  S("4", "Robot Rights & Status", ["Robot personhood debate", "Moral status of machines", "Property vs. person", "Legal perspectives"],
   "Decide how the law sees robots.", "Robots are tools—until society says otherwise."),
  S("5", "Human–Robot Moral Relations", ["Trust and deception", "Emotional attachment", "Care robots and dignity", "Robot nudging"],
   "Respect human–robot bonds.", "Relationships with robots shape human behavior."),
  S("6", "Robot Ethics & Review", ["Case studies", "Course recap and assessment", "Toward AI ethics (AI.404)", "Ethics panel"],
   "Apply ethical reasoning to robotics.", "Ethical robots serve humanity.")],
),
course("AI.403", "Robot Learning", Y4S1,
 "Robots that improve with experience: imitation, reinforcement, meta-learning, and lifelong learning on hardware.",
 [S("1", "Orientation: Robots That Improve", ["Robot learning vs. general ML", "Learning on physical robots", "Sample efficiency", "Course roadmap"],
   "Let robots get better with practice.", "Experience is the best teacher for robots."),
  S("2", "Imitation Learning", ["Learning from demonstration", "Behavior cloning", "Inverse reinforcement learning", "DAgger"],
   "Teach robots by showing them.", "Demonstration is an efficient teacher."),
  S("3", "Reinforcement Learning on Robots", ["RL on hardware", "Safe exploration", "Sim-to-real", "Reward shaping"],
   "Learn policies through interaction.", "Hardware teaches grounding."),
  S("4", "Lifelong & Meta-Learning", ["Continual learning", "Catastrophic forgetting", "Meta-learning", "Few-shot robot learning"],
   "Learn to learn, and never stop.", "Lifelong learners adapt forever."),
  S("5", "Skill Generalization", ["Generalizing across tasks", "Transfer learning", "Domain adaptation", "Reusable skills"],
   "Apply one skill to many situations.", "Generalization is the mark of real learning."),
  S("6", "Robot Learning & Review", ["Learning robot demo", "Course recap and assessment", "Toward AI ethics (AI.404)", "Skill showcase"],
   "Demonstrate a robot learning a skill.", "Learning robots grow with use.")],
),
course("AI.404", "AI Ethics", Y4S1,
 "Ethics of artificial intelligence: fairness, transparency, accountability, and the societal impact of AI systems.",
 [S("1", "Orientation: Ethics of AI", ["AI ethics landscape", "Values in technology", "Ethical AI principles", "Course framework"],
   "Align AI with human values.", "AI reflects the values of its builders."),
  S("2", "Fairness & Discrimination", ["Algorithmic bias", "Fairness definitions", "Disparate impact", "Mitigation"],
   "Build fair algorithms.", "Unfair AI harms the vulnerable most."),
  S("3", "Transparency & Explainability", ["Black-box problem", "XAI methods", "Right to explanation", "Interpretability"],
   "Make AI decisions understandable.", "People deserve to know why AI decided."),
  S("4", "Accountability & Governance", ["Responsibility for AI", "AI governance", "Audit trails", "Regulation"],
   "Hold AI creators accountable.", "Powerful AI needs clear accountability."),
  S("5", "Societal Impact", ["Employment and automation", "AI and inequality", "Environmental cost of AI", "AI for social good"],
   "Assess AI's broad effects.", "AI reshapes labor, equity, and the planet."),
  S("6", "AI Ethics & Review", ["Case studies", "Course recap and assessment", "Toward capstone project (AI.450)", "Ethics commitment"],
   "Practice responsible AI engineering.", "Ethical AI earns public trust.")],
),
course("AI.405", "Robot Manipulation", Y4S1,
 "Robot grasping and manipulation: grippers, grasp planning, dexterous manipulation, and contact.",
 [S("1", "Orientation: Grasping the World", ["Manipulation in robotics", "Grasp types", "Contact mechanics", "Applications"],
   "Let robots hold and move objects.", "Manipulation is physical intelligence."),
  S("2", "Grippers & End-Effectors", ["Parallel-jaw grippers", "Vacuum and adhesive", "Multi-fingered hands", "End-effector selection"],
   "Choose the right hand for the task.", "The gripper is the robot's hand."),
  S("3", "Grasp Planning", ["Grasp taxonomy", "Force-closure and form-closure", "Grasp quality metrics", "Grasp synthesis"],
   "Plan stable and effective grasps.", "A good grasp resists disturbance."),
  S("4", "Dexterous Manipulation", ["In-hand manipulation", "Finger gaiting", "Tactile feedback", "Dexterous control"],
   "Manipulate objects skillfully.", "Dexterity turns grasping into tool use."),
  S("5", "Contact & Interaction", ["Contact modeling", "Impedance control", "Slip detection", "Safe physical interaction"],
   "Manage contact safely.", "Contact is where manipulation happens."),
  S("6", "Robot Manipulation & Review", ["Manipulation demo", "Course recap and assessment", "Toward robot perception (AI.406)", "Grasp challenge"],
   "Pick, place, and manipulate reliably.", "Manipulation is the robot's handiwork.")],
),
course("AI.406", "Robot Perception", Y4S1,
 "Advanced robot perception: multimodal fusion, deep perception, and perception for autonomous operation.",
 [S("1", "Orientation: Seeing to Act", ["Robot perception stack", "Multimodal perception", "Perception under uncertainty", "Applications"],
   "Fuse senses into understanding.", "Robots perceive with many senses at once."),
  S("2", "Deep Perception", ["CNNs for robot vision", "3D deep learning", "Perception networks", "Real-time deep perception"],
   "Use deep networks to perceive.", "Deep perception sees richly and quickly."),
  S("3", "Tactile & Force Sensing", ["Tactile sensors", "Force-torque sensing", "Slip and texture", "Tactile servoing"],
   "Feel what the robot touches.", "Touch completes vision."),
  S("4", "Perception for Autonomy", ["Obstacle and free space", "Semantic perception", "Human detection", "Perception–action loop"],
   "Perceive to navigate and act.", "Autonomous perception drives action."),
  S("5", "Perception Systems", ["Sensor calibration", "Data association", "Real-time pipelines", "Perception validation"],
   "Engineer robust perception systems.", "Perception must work in the wild."),
  S("6", "Robot Perception & Review", ["Perception demo", "Course recap and assessment", "Toward robot navigation (AI.407)", "Perception eval"],
   "Integrate perception on a robot.", "Perception closes the loop to action.")],
),
]

# ---------------- YEAR 4 SEMESTER 2 ----------------
Y4S2 = "YEAR 4 · SEMESTER 2"
ALL_COURSES += [
course("AI.407", "Robot Navigation", Y4S2,
 "Moving safely through space: global and local path planning, obstacle avoidance, and navigation stacks.",
 [S("1", "Orientation: Getting There", ["Navigation problem", "Global vs. local navigation", "Navigation stack", "Applications"],
   "Guide robots from start to goal.", "Navigation moves robots purposefully."),
  S("2", "Global Path Planning", ["Graph search: Dijkstra, A*", "D* lite", "Roadmaps", "Optimal paths"],
   "Plan routes over known maps.", "Global planning finds the best route."),
  S("3", "Local Navigation & Obstacle Avoidance", ["Dynamic window approach", "Potential fields", "Vector fields", "Reactive avoidance"],
   "Avoid obstacles in real time.", "Local planning reacts to the now."),
  S("4", "Navigation Stacks", ["ROS navigation", "Costmaps", "Global and local planners", "Recovery behaviors"],
   "Assemble a full navigation system.", "Stacks integrate planning, control, and sensing."),
  S("5", "Navigation in Dynamic Worlds", ["Moving obstacles", "Human-aware navigation", "Social navigation", "Crowd navigation"],
   "Navigate among people and robots.", "Social robots move with people."),
  S("6", "Robot Navigation & Review", ["Navigation demo", "Course recap and assessment", "Toward path planning (AI.408)", "Obstacle course"],
   "Demonstrate autonomous navigation.", "A robot that cannot navigate is not autonomous.")],
),
course("AI.408", "Robot Path Planning", Y4S2,
 "Computing collision-free paths: configuration spaces, sampling, optimization, and kinodynamic planning.",
 [S("1", "Orientation: The Path Problem", ["Path vs. trajectory", "Configuration space", "Obstacles as C-obstacles", "Planning queries"],
   "Compute where a robot may move.", "Path planning finds feasible motion."),
  S("2", "Classical Planners", ["Visibility graphs", "Cell decomposition", "Voronoi diagrams", "Exact cell decomposition"],
   "Solve planning with geometry.", "Geometry defines the free space."),
  S("3", "Sampling-Based Planners", ["PRM", "RRT and RRT*", "BIT*", "Informed sampling"],
   "Plan in high-dimensional spaces.", "Sampling tames high dimensions."),
  S("4", "Optimization-Based Planning", ["Trajectory optimization", "CHMP", "Convex optimization", "Smooth paths"],
   "Refine paths for quality and dynamics.", "Optimization polishes raw paths."),
  S("5", "Kinodynamic & Constrained Planning", ["Dynamics constraints", "Kinodynamic planning", "State lattices", "Time-parameterization"],
   "Plan physically feasible motion.", "Feasible paths respect the robot's body."),
  S("6", "Path Planning & Review", ["Planner comparison", "Course recap and assessment", "Toward simulation (AI.409)", "Planning race"],
   "Implement and compare planners.", "The right planner fits the robot and task.")],
),
course("AI.409", "Robot Simulation", Y4S2,
 "Virtual robotics: simulators, physics engines, digital twins, and sim-to-real transfer.",
 [S("1", "Orientation: Virtual Robots", ["Why simulate", "Simulators vs. real robots", "Digital twins", "Sim-to-real gap"],
   "Test robots without risk.", "Simulation is the robot's practice ground."),
  S("2", "Physics Engines", ["Rigid-body dynamics", "Contact and collision", "Actuator models", "Gazebo, PyBullet, MuJoCo"],
   "Simulate physics faithfully.", "Physics engines make virtual motion real."),
  S("3", "Simulation Workflow", ["URDF/SDF models", "Worlds and environments", "Sensors in sim", "Logging and replay"],
   "Build simulation scenes.", "Models and worlds define the sim."),
  S("4", "Sim-to-Real Transfer", ["Domain randomization", "System identification", "Transfer learning", "Hardware validation"],
   "Move from sim to real reliably.", "The sim–real gap must be bridged."),
  S("5", "Simulation for AI & Robotics", ["Training RL in sim", "Testing perception", "Regression testing", "CI for robotics"],
   "Develop and test in simulation.", "Simulation accelerates development."),
  S("6", "Robot Simulation & Review", ["Simulation project", "Course recap and assessment", "Toward robot vision (AI.410)", "Sim showcase"],
   "Validate a robot in simulation first.", "Fail in sim, not in the field.")],
),
course("AI.410", "Robot Vision", Y4S2,
 "Vision integrated with robot action: visual servoing, hand-eye coordination, and vision-based manipulation.",
 [S("1", "Orientation: Vision in Action", ["Robot vision vs. machine vision", "Hand–eye coordination", "Vision–action loop", "Applications"],
   "Let vision guide robot motion.", "Vision directs the hand."),
  S("2", "Visual Servoing", ["Image-based vs. position-based", "Visual servo control", "Camera calibration", "Eye-in-hand vs. eye-to-hand"],
   "Close the loop through the camera.", "Visual servoing moves by what it sees."),
  S("3", "Vision-Based Navigation", ["Visual odometry", "SLAM with cameras", "Monocular and stereo", "Loop closure"],
   "Navigate using vision alone.", "Cameras are lightweight eyes."),
  S("4", "Vision-Based Manipulation", ["Guided grasping", "Object tracking for manipulation", "Vision-tactile fusion", "Assembly by vision"],
   "Manipulate with visual feedback.", "Vision guides manipulation precisely."),
  S("5", "Robot Vision Systems", ["Pipeline design", "Real-time constraints", "Calibration and maintenance", "Evaluation metrics"],
   "Integrate vision on robots.", "Robot vision must be fast and robust."),
  S("6", "Robot Vision & Review", ["Vision–robot demo", "Course recap and assessment", "Toward robot design (AI.411)", "Vision task"],
   "Combine sight and motion on a robot.", "Sight plus action equals robot vision.")],
),
course("AI.411", "Robot Design", Y4S2,
 "Designing complete robots: requirements, concept design, prototyping, and integration.",
 [S("1", "Orientation: Designing Robots", ["The design process", "Requirements and constraints", "Concept generation", "Robot design disciplines"],
   "Create robots from first principles.", "Design begins with purpose."),
  S("2", "Mechanical Design", ["Kinematic design", "Structure and materials", "Actuator integration", "CAD and prototyping"],
   "Design the robot's body.", "The body enables the behavior."),
  S("3", "Electrical & Electronics", ["Power systems", "Wiring and sensors", "Microcontroller selection", "PCB design"],
   "Power and wire the machine.", "Electronics are the robot's nervous system."),
  S("4", "Software Architecture", ["Robot software stack", "Middleware choice", "Concurrency", "Modularity"],
   "Architect robot software.", "Software coordinates the whole robot."),
  S("5", "Integration & Testing", ["System integration", "Testing and validation", "Failure modes", "Iteration"],
   "Assemble and verify the robot.", "Integration reveals the real design."),
  S("6", "Robot Design & Review", ["Design review and demo", "Course recap and assessment", "Toward capstone (AI.450)", "Portfolio"],
   "Present a complete robot design.", "A robot is judged as a whole system.")],
),
course("AI.450", "Project", Y4S2,
 "Capstone project: students design, build, and document an AI/robotics project from concept to demonstration.",
 [S("1", "Orientation: The Capstone", ["Project scope and deliverables", "Team formation", "Timeline and milestones", "Assessment criteria"],
   "Plan a major AI/robotics project.", "A capstone synthesizes the degree."),
  S("2", "Problem Definition & Requirements", ["Choosing a problem", "Stakeholder needs", "Functional and non-functional requirements", "Success criteria"],
   "Define what the project must achieve.", "Clear requirements drive good projects."),
  S("3", "Design & Architecture", ["System design", "Hardware/software split", "Architecture diagrams", "Design review"],
   "Architect the solution.", "Design before implementation."),
  S("4", "Implementation", ["Prototyping", "Iterative development", "Version control", "Documentation"],
   "Build the system incrementally.", "Implementation turns design into reality."),
  S("5", "Testing & Evaluation", ["Test plan", "Performance evaluation", "User testing", "Iteration"],
   "Verify the system works.", "Testing proves the project works."),
  S("6", "Demonstration & Report", ["Final demo", "Project report", "Presentation", "Reflection and future work"],
   "Show and explain the completed project.", "Communication completes engineering.")],
),
]

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    base_out = "/home/user/allnew/output"
    os.makedirs(base_out, exist_ok=True)

    total_slides = 0
    manifest_lines = ["# Course Orientation Presentations\n",
                      "Triune Biblical University Global Extension USA — Bachelor of Artificial Intelligence and Robotics Engineering\n",
                      "Each PDF is a premium cinematic 6-hour orientation lecture. Every slide footer carries the university name.\n\n"]

    for course in ALL_COURSES:
        sem_folder = course["semester"].replace(" · ", "_").replace(" ", "_")
        out_dir = os.path.join(base_out, sem_folder)
        os.makedirs(out_dir, exist_ok=True)

        safe = f"{slugify(course['code'])}_-_{slugify(course['title'])}.pdf"
        out_path = os.path.join(out_dir, safe)

        slides = build_course(course, out_path)
        total_slides += slides
        manifest_lines.append(f"- **{course['code']}** — {course['title']}  ({course['semester']}, {course['credits']} cr) → `{out_path}`  ({slides} slides)")

    manifest_path = os.path.join(base_out, "MANIFEST.md")
    with open(manifest_path, "w") as f:
        f.write("\n".join(manifest_lines))

    print(f"Generated {len(ALL_COURSES)} course PDFs, {total_slides} total slides.")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
