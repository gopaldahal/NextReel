"""
Generate 6 UML diagrams as a single black-and-white A4 Word document.
Sections:
  1 — Movie Recommendation System (1.1 Sequence, 1.2 State, 1.3 Activity)
  2 — Sentiment Analysis System   (2.1 Sequence, 2.2 State, 2.3 Activity)
"""

import os, io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.lines as mlines
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
BW = '#000000'
WHITE = '#ffffff'
GREY = '#cccccc'
LTGREY = '#f0f0f0'

def save_fig(fig, dpi=150):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    buf.seek(0)
    plt.close(fig)
    return buf

def arrow(ax, x0, y0, x1, y1, style='->', lw=1.0, color=BW, label=None,
          label_side='top', fontsize=8, dashed=False):
    ls = '--' if dashed else '-'
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, linestyle=ls))
    if label:
        mx, my = (x0+x1)/2, (y0+y1)/2
        dy = 0.18 if label_side == 'top' else -0.18
        ax.text(mx, my+dy, label, ha='center', va='center', fontsize=fontsize,
                color=BW, fontstyle='italic' if dashed else 'normal')

def hline(ax, x0, x1, y, lw=1.0, color=BW, dashed=False):
    ls = '--' if dashed else '-'
    ax.plot([x0, x1], [y, y], color=color, lw=lw, ls=ls)

def vline(ax, x, y0, y1, lw=1.0, color=BW, dashed=False):
    ls = '--' if dashed else '-'
    ax.plot([x, x], [y0, y1], color=color, lw=lw, ls=ls)

def box(ax, cx, cy, w, h, label, fontsize=8, fill=WHITE, edge=BW, lw=1.0,
        bold=False, rounded=False):
    style = 'round,pad=0.1' if rounded else 'square,pad=0'
    rect = FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                          boxstyle=style, linewidth=lw,
                          edgecolor=edge, facecolor=fill)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize,
            color=BW, fontweight=weight, wrap=True,
            multialignment='center')

def actor_head(ax, x, y, r=0.2):
    circle = plt.Circle((x, y), r, color=BW, fill=False, lw=1.2)
    ax.add_patch(circle)
    ax.plot([x, x], [y-r, y-r-0.5], color=BW, lw=1.2)
    ax.plot([x-0.3, x+0.3], [y-r-0.2, y-r-0.2], color=BW, lw=1.2)
    ax.plot([x, x-0.25], [y-r-0.5, y-r-0.9], color=BW, lw=1.2)
    ax.plot([x, x+0.25], [y-r-0.5, y-r-0.9], color=BW, lw=1.2)

def diamond(ax, cx, cy, w=0.6, h=0.35, fill=WHITE, edge=BW, lw=1.0):
    xs = [cx, cx+w/2, cx, cx-w/2, cx]
    ys = [cy+h/2, cy, cy-h/2, cy, cy+h/2]
    ax.fill(xs, ys, facecolor=fill, edgecolor=edge, linewidth=lw, zorder=3)

def rounded_rect(ax, cx, cy, w, h, label, fontsize=8, fill=WHITE, edge=BW, lw=1.0):
    rect = FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                          boxstyle='round,pad=0.08', linewidth=lw,
                          edgecolor=edge, facecolor=fill)
    ax.add_patch(rect)
    ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize, color=BW,
            multialignment='center')

# ─────────────────────────────────────────────────────────────
# DIAGRAM 1 — Sequence: Movie Recommendation System
# ─────────────────────────────────────────────────────────────
def diagram_rec_sequence():
    fig, ax = plt.subplots(figsize=(11, 14))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_facecolor('white')

    fig.suptitle('Figure 1.1 — Sequence Diagram: Movie Recommendation System',
                 fontsize=11, fontweight='bold', y=0.98)

    # Lifelines
    participants = ['User', 'Browser\n(Client)', 'Django\nView', 'SVD\nEngine', 'Database']
    xs = [1, 2.5, 4.5, 7, 9.5]
    top_y = 13.0
    bot_y = 0.5

    for lx, name in zip(xs, participants):
        box(ax, lx, top_y, 1.1, 0.55, name, fontsize=8, bold=True, fill=LTGREY)
        vline(ax, lx, top_y-0.28, bot_y, dashed=True, lw=0.8)

    # Activation bars
    def actbar(lx, y_top, y_bot, w=0.12):
        rect = mpatches.FancyBboxPatch((lx-w/2, y_bot), w, y_top-y_bot,
                                       boxstyle='square,pad=0', lw=0.8,
                                       edgecolor=BW, facecolor=GREY)
        ax.add_patch(rect)

    # Messages
    msgs = [
        # (y, x0, x1, label, dashed, style)
        (12.2, xs[0], xs[1], '1: GET /recommendations/', False, '->'),
        (11.5, xs[1], xs[2], '2: HTTP Request', False, '->'),
        (10.8, xs[2], xs[4], '3: fetch user ratings', False, '->'),
        (10.2, xs[4], xs[2], '4: ratings queryset', True, '->'),
        (9.5,  xs[2], xs[3], '5: get_recommendations(user_id)', False, '->'),
    ]
    for (y, x0, x1, lbl, dash, sty) in msgs:
        arrow(ax, x0, y, x1, y, style=sty, label=lbl, dashed=dash, fontsize=7.5)

    # Loop fragment
    loop_y_top = 9.1
    loop_y_bot = 7.0
    ax.add_patch(mpatches.FancyBboxPatch((xs[3]-0.8, loop_y_bot), 3.1, loop_y_top-loop_y_bot,
                                          boxstyle='square,pad=0', lw=1.2, edgecolor=BW,
                                          facecolor='none', linestyle='--'))
    ax.text(xs[3]-0.8, loop_y_top, 'loop [for each candidate movie]',
            fontsize=7, va='bottom', color=BW,
            bbox=dict(boxstyle='square,pad=0.1', facecolor=LTGREY, edgecolor=BW, lw=0.8))

    loop_msgs = [
        (8.7, xs[3], xs[4], '6: query movie features', False, '->'),
        (8.1, xs[4], xs[3], '7: movie data', True, '->'),
        (7.4, xs[3], xs[3], '8: compute SVD score', False, '->'),
    ]
    arrow(ax, xs[3]-0.05, 7.4, xs[3]+0.05, 7.4, style='->', label='8: compute SVD score', fontsize=7.5)
    arrow(ax, xs[3], 8.7, xs[4], 8.7, style='->', label='6: query movie features', fontsize=7.5)
    arrow(ax, xs[4], 8.1, xs[3], 8.1, style='->', label='7: movie data', dashed=True, fontsize=7.5)

    # Continue after loop
    post_loop = [
        (6.5, xs[3], xs[2], '9: ranked movie list', True, '->'),
        (5.8, xs[2], xs[4], '10: prefetch genres', False, '->'),
        (5.1, xs[4], xs[2], '11: genre data', True, '->'),
        (4.4, xs[2], xs[1], '12: render template', True, '->'),
        (3.7, xs[1], xs[0], '13: HTML Response', True, '->'),
    ]
    for (y, x0, x1, lbl, dash, sty) in post_loop:
        arrow(ax, x0, y, x1, y, style=sty, label=lbl, dashed=dash, fontsize=7.5)

    # Retrain note
    ax.text(4.5, 2.8, '[Every 50th rating: background\nthread retrains SVD model]',
            ha='center', fontsize=7.5, style='italic', color=BW,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LTGREY, edgecolor=BW, lw=0.8))

    actbar(xs[2], 11.5, 4.1)
    actbar(xs[3], 9.5, 6.5)
    actbar(xs[4], 10.8, 10.0)
    actbar(xs[4], 8.7, 7.9)

    return save_fig(fig)


# ─────────────────────────────────────────────────────────────
# DIAGRAM 2 — State: Movie Recommendation System
# ─────────────────────────────────────────────────────────────
def diagram_rec_state():
    fig, ax = plt.subplots(figsize=(9, 13))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 13)
    ax.axis('off')
    ax.set_facecolor('white')

    fig.suptitle('Figure 1.2 — State Diagram: Movie Recommendation System',
                 fontsize=11, fontweight='bold', y=0.98)

    # States (cx, cy, label)
    states = [
        (4.5, 12.0, 'START'),
        (4.5, 10.5, 'User Visits\n/recommendations'),
        (4.5,  9.0, 'Checking\nUser History'),
        (2.0,  7.5, 'Cold Start\n(No History)'),
        (7.0,  7.5, 'Has\nRatings'),
        (7.0,  6.0, 'Loading\nSVD Model'),
        (7.0,  4.5, 'Generating\nCandidates'),
        (7.0,  3.0, 'Scoring &\nRanking'),
        (2.0,  6.0, 'Fetching\nTrending/Top Rated'),
        (4.5,  1.5, 'Displaying\nRecommendations'),
        (4.5,  0.3, 'END'),
    ]

    state_map = {lbl.split('\n')[0]: (cx, cy) for (cx, cy, lbl) in states}

    for (cx, cy, lbl) in states:
        if lbl == 'START':
            ax.add_patch(plt.Circle((cx, cy), 0.25, color=BW, zorder=3))
        elif lbl == 'END':
            ax.add_patch(plt.Circle((cx, cy), 0.25, color=BW, zorder=3))
            ax.add_patch(plt.Circle((cx, cy), 0.35, color=BW, fill=False, lw=2, zorder=3))
        else:
            rounded_rect(ax, cx, cy, 2.2, 0.75, lbl, fontsize=8, fill=LTGREY)

    def st(lbl):
        for (cx, cy, l) in states:
            if l == lbl:
                return cx, cy
        return 0, 0

    # Transitions
    transitions = [
        ('START', 'User Visits\n/recommendations', '', False),
        ('User Visits\n/recommendations', 'Checking\nUser History', 'load session', False),
        ('Checking\nUser History', 'Cold Start\n(No History)', 'no ratings found', False),
        ('Checking\nUser History', 'Has\nRatings', 'ratings ≥ 1', False),
        ('Cold Start\n(No History)', 'Fetching\nTrending/Top Rated', 'query DB', False),
        ('Has\nRatings', 'Loading\nSVD Model', 'load_svd_model()', False),
        ('Loading\nSVD Model', 'Generating\nCandidates', 'model ready', False),
        ('Generating\nCandidates', 'Scoring &\nRanking', 'predict ratings', False),
        ('Scoring &\nRanking', 'Displaying\nRecommendations', 'sort & group', False),
        ('Fetching\nTrending/Top Rated', 'Displaying\nRecommendations', 'results ready', False),
        ('Displaying\nRecommendations', 'END', 'render template', False),
    ]

    def get_xy(lbl):
        for (cx, cy, l) in states:
            if l == lbl:
                return cx, cy
        return 0, 0

    for (s0, s1, lbl, dash) in transitions:
        x0, y0 = get_xy(s0)
        x1, y1 = get_xy(s1)
        arrow(ax, x0, y0-0.38, x1, y1+0.38, label=lbl, dashed=dash, fontsize=7)

    # trainingError() back-transition on SVD
    ax.annotate('', xy=(7.0, 6.38), xytext=(8.3, 6.38),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1))
    ax.plot([8.3, 8.3], [5.62, 6.38], color=BW, lw=1)
    ax.annotate('', xy=(8.3, 5.62), xytext=(7.0+1.1, 5.62),
                arrowprops=dict(arrowstyle='-', color=BW, lw=1))
    ax.text(8.5, 6.0, 'trainingError()\n[retry]', fontsize=7, ha='left', va='center',
            color=BW, style='italic')

    return save_fig(fig)


# ─────────────────────────────────────────────────────────────
# DIAGRAM 3 — Activity: Movie Recommendation System (3 swimlanes)
# ─────────────────────────────────────────────────────────────
def diagram_rec_activity():
    fig, ax = plt.subplots(figsize=(13, 15))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 15)
    ax.axis('off')
    ax.set_facecolor('white')

    fig.suptitle('Figure 1.3 — Activity Diagram: Movie Recommendation System',
                 fontsize=11, fontweight='bold', y=0.98)

    # Swimlane boundaries
    lanes = [
        (0.0, 4.0, 'User'),
        (4.0, 8.5, 'Server (Django)'),
        (8.5, 13.0, 'SVD Model'),
    ]
    lane_tops = 14.5
    lane_bot  = 0.2

    for (lx, rx, name) in lanes:
        cx = (lx + rx) / 2
        ax.add_patch(mpatches.FancyBboxPatch((lx+0.05, lane_bot), rx-lx-0.1,
                                              lane_tops-lane_bot, boxstyle='square,pad=0',
                                              lw=1.0, edgecolor=BW, facecolor='none'))
        ax.add_patch(mpatches.FancyBboxPatch((lx+0.05, 13.8), rx-lx-0.1, 0.65,
                                              boxstyle='square,pad=0', lw=1.0,
                                              edgecolor=BW, facecolor=LTGREY))
        ax.text(cx, 14.12, name, ha='center', va='center', fontsize=9,
                fontweight='bold', color=BW)

    def lx_cx(lane_idx):
        l = lanes[lane_idx]
        return (l[0] + l[1]) / 2

    # Start node
    ax.add_patch(plt.Circle((lx_cx(0), 13.3), 0.22, color=BW, zorder=3))

    # Activities: (lane, cy, label)
    acts = [
        (0, 12.5, 'Open\n/recommendations'),
        (1, 11.5, 'Receive HTTP\nRequest'),
        (1, 10.5, 'Query User\nRating History'),
        (1,  9.3, 'Has Ratings?'),          # decision
        (0,  8.3, 'Display Trending\n& Top Rated'),
        (2,  9.3, 'Load SVD\nModel (cached)'),
        (2,  8.0, 'Compute Predicted\nRatings'),
        (2,  6.8, 'Sort & Group\nby Genre'),
        (1,  5.7, 'Fetch Movie\nMetadata\n(prefetch genres)'),
        (1,  4.4, 'Build Template\nContext'),
        (0,  3.2, 'Render\nRecommendations\nPage'),
        (0,  1.8, 'User Rates\na Movie'),
        (1,  1.8, 'Save Rating\nto DB'),
        (2,  1.8, 'Auto-retrain SVD\n(background thread)'),
    ]

    act_pos = {}
    for (lane, cy, lbl) in acts:
        cx = lx_cx(lane)
        act_pos[lbl] = (cx, cy)
        if lbl == 'Has Ratings?':
            diamond(ax, cx, cy, w=1.8, h=0.7)
            ax.text(cx, cy, lbl, ha='center', va='center', fontsize=7.5, color=BW)
        else:
            rounded_rect(ax, cx, cy, 2.8, 0.65, lbl, fontsize=7.5, fill=LTGREY)

    # Arrows
    flow = [
        ('Open\n/recommendations', 'Receive HTTP\nRequest'),
        ('Receive HTTP\nRequest', 'Query User\nRating History'),
        ('Query User\nRating History', 'Has Ratings?'),
    ]
    for (a, b) in flow:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7)

    # Decision branches
    hx, hy = act_pos['Has Ratings?']
    # No branch → left (User lane, cold start)
    ax.annotate('', xy=(lx_cx(0), 8.63), xytext=(hx-0.9, hy),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text((hx-0.9+lx_cx(0))/2, hy+0.18, 'No', ha='center', fontsize=7.5)
    # Yes branch → right (Model lane)
    ax.annotate('', xy=(lx_cx(2), 9.63), xytext=(hx+0.9, hy),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text((hx+0.9+lx_cx(2))/2, hy+0.18, 'Yes', ha='center', fontsize=7.5)

    # Model flow
    model_flow = [
        ('Load SVD\nModel (cached)', 'Compute Predicted\nRatings'),
        ('Compute Predicted\nRatings', 'Sort & Group\nby Genre'),
    ]
    for (a, b) in model_flow:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7)

    # Both paths converge to Fetch Metadata
    arrow(ax, lx_cx(2), 6.47, lx_cx(1), 6.03, label='results', fontsize=7)
    arrow(ax, lx_cx(0), 7.97, lx_cx(1), 6.03, label='results', fontsize=7)

    server_flow = [
        ('Fetch Movie\nMetadata\n(prefetch genres)', 'Build Template\nContext'),
        ('Build Template\nContext', 'Render\nRecommendations\nPage'),
        ('Render\nRecommendations\nPage', 'User Rates\na Movie'),
        ('User Rates\na Movie', 'Save Rating\nto DB'),
        ('Save Rating\nto DB', 'Auto-retrain SVD\n(background thread)'),
    ]
    for (a, b) in server_flow:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7)

    # End node
    end_x = lx_cx(1)
    end_y = 0.7
    ax.add_patch(plt.Circle((end_x, end_y), 0.22, color=BW, zorder=3))
    ax.add_patch(plt.Circle((end_x, end_y), 0.32, color=BW, fill=False, lw=2, zorder=3))
    arrow(ax, lx_cx(2), 1.47, end_x, end_y+0.32, fontsize=7)

    return save_fig(fig)


# ─────────────────────────────────────────────────────────────
# DIAGRAM 4 — Sequence: Sentiment Analysis System
# ─────────────────────────────────────────────────────────────
def diagram_sent_sequence():
    fig, ax = plt.subplots(figsize=(11, 14))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_facecolor('white')

    fig.suptitle('Figure 2.1 — Sequence Diagram: Sentiment Analysis System',
                 fontsize=11, fontweight='bold', y=0.98)

    participants = ['User', 'Browser\n(Client)', 'Review\nView', 'Sentiment\nModel', 'Database']
    xs = [1, 2.5, 4.5, 7, 9.5]
    top_y = 13.0

    for lx, name in zip(xs, participants):
        box(ax, lx, top_y, 1.2, 0.55, name, fontsize=8, bold=True, fill=LTGREY)
        vline(ax, lx, top_y-0.28, 0.5, dashed=True, lw=0.8)

    def actbar(lx, y_top, y_bot, w=0.12):
        rect = mpatches.FancyBboxPatch((lx-w/2, y_bot), w, y_top-y_bot,
                                       boxstyle='square,pad=0', lw=0.8,
                                       edgecolor=BW, facecolor=GREY)
        ax.add_patch(rect)

    msgs_top = [
        (12.2, xs[0], xs[1], '1: Write review text', False, '->'),
        (11.5, xs[1], xs[2], '2: POST /reviews/add/<movie_id>/', False, '->'),
        (10.8, xs[2], xs[2], '3: validate form', False, '->'),
    ]
    arrow(ax, xs[2]-0.05, 10.8, xs[2]+0.05, 10.8, label='3: validate form', fontsize=7.5)
    arrow(ax, xs[0], 12.2, xs[1], 12.2, label='1: Write review text', fontsize=7.5)
    arrow(ax, xs[1], 11.5, xs[2], 11.5, label='2: POST /reviews/add/<movie_id>/', fontsize=7.5)

    # alt fragment
    alt_y_top = 10.3
    alt_y_bot = 7.8
    ax.add_patch(mpatches.FancyBboxPatch((xs[3]-0.8, alt_y_bot), 4.1, alt_y_top-alt_y_bot,
                                          boxstyle='square,pad=0', lw=1.2, edgecolor=BW,
                                          facecolor='none', linestyle='--'))
    ax.text(xs[3]-0.8, alt_y_top, 'alt',
            fontsize=7, va='bottom', color=BW,
            bbox=dict(boxstyle='square,pad=0.1', facecolor=LTGREY, edgecolor=BW, lw=0.8))

    # divider in alt
    hline(ax, xs[3]-0.8, xs[3]+3.3, 9.0, lw=0.7, dashed=True)
    ax.text(xs[3]-0.75, 10.1, '[model file exists]', fontsize=7, color=BW, style='italic')
    ax.text(xs[3]-0.75, 8.8, '[no model file]', fontsize=7, color=BW, style='italic')

    alt_msgs = [
        (9.7, xs[2], xs[3], '4: analyze(review_text)', False, '->'),
        (9.1, xs[3], xs[3], '5: load from cache / mtime check', False, '->'),
        (8.5, xs[3], xs[2], '6: sentiment label + confidence', True, '->'),
        (7.5, xs[2], xs[3], "4': load_sentiment_model()", False, '->'),
        (7.0, xs[3], xs[3], "5': read .pkl from disk", False, '->'),
        (6.5, xs[3], xs[2], "6': model instance", True, '->'),
    ]
    arrow(ax, xs[2], 9.7, xs[3], 9.7, label='4: analyze(review_text)', fontsize=7.5)
    arrow(ax, xs[3]-0.05, 9.1, xs[3]+0.05, 9.1, label='5: load from cache / mtime check', fontsize=7.5)
    arrow(ax, xs[3], 8.5, xs[2], 8.5, label='6: sentiment label + confidence', dashed=True, fontsize=7.5)
    arrow(ax, xs[2], 7.5, xs[3], 7.5, label="4': load_sentiment_model()", fontsize=7.5)
    arrow(ax, xs[3]-0.05, 7.0, xs[3]+0.05, 7.0, label="5': read .pkl from disk", fontsize=7.5)
    arrow(ax, xs[3], 6.5, xs[2], 6.5, label="6': model instance", dashed=True, fontsize=7.5)

    post = [
        (5.8, xs[2], xs[4], '7: save review + sentiment', False, '->'),
        (5.1, xs[4], xs[2], '8: saved OK', True, '->'),
        (4.4, xs[2], xs[1], '9: JSON {message, sentiment}', True, '->'),
        (3.7, xs[1], xs[0], '10: show toast + update UI', True, '->'),
    ]
    for (y, x0, x1, lbl, dash, sty) in post:
        arrow(ax, x0, y, x1, y, label=lbl, dashed=dash, fontsize=7.5)

    # every 50 retrain note
    ax.text(4.5, 2.8, '[Every 50th review: background\nthread retrains Naive Bayes model]',
            ha='center', fontsize=7.5, style='italic', color=BW,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LTGREY, edgecolor=BW, lw=0.8))

    actbar(xs[2], 11.5, 3.8)
    actbar(xs[3], 9.7, 6.3)
    actbar(xs[4], 5.8, 5.0)

    return save_fig(fig)


# ─────────────────────────────────────────────────────────────
# DIAGRAM 5 — State: Sentiment Analysis System
# ─────────────────────────────────────────────────────────────
def diagram_sent_state():
    fig, ax = plt.subplots(figsize=(9, 13))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 13)
    ax.axis('off')
    ax.set_facecolor('white')

    fig.suptitle('Figure 2.2 — State Diagram: Sentiment Analysis System',
                 fontsize=11, fontweight='bold', y=0.98)

    states_list = [
        (4.5, 12.3, 'START'),
        (4.5, 11.2, 'Review\nForm Displayed'),
        (4.5, 10.0, 'User Typing\nReview Text'),
        (4.5,  8.8, 'Form\nSubmitted'),
        (4.5,  7.6, 'Validating\nInput'),
        (2.0,  6.4, 'Validation\nFailed'),
        (4.5,  6.4, 'Loading\nSentiment Model'),
        (4.5,  5.2, 'Analysing\nSentiment'),
        (4.5,  4.0, 'Saving Review\nto Database'),
        (2.5,  2.8, 'Positive\nReview Saved'),
        (6.5,  2.8, 'Negative\nReview Saved'),
        (4.5,  1.6, 'Response\nReturned to User'),
        (4.5,  0.35, 'END'),
    ]

    def get_xy2(lbl):
        for (cx, cy, l) in states_list:
            if l == lbl:
                return cx, cy
        return 0, 0

    for (cx, cy, lbl) in states_list:
        if lbl == 'START':
            ax.add_patch(plt.Circle((cx, cy), 0.22, color=BW, zorder=3))
        elif lbl == 'END':
            ax.add_patch(plt.Circle((cx, cy), 0.22, color=BW, zorder=3))
            ax.add_patch(plt.Circle((cx, cy), 0.32, color=BW, fill=False, lw=2, zorder=3))
        else:
            rounded_rect(ax, cx, cy, 2.2, 0.65, lbl, fontsize=8, fill=LTGREY)

    main_flow = [
        ('START', 'Review\nForm Displayed'),
        ('Review\nForm Displayed', 'User Typing\nReview Text'),
        ('User Typing\nReview Text', 'Form\nSubmitted'),
        ('Form\nSubmitted', 'Validating\nInput'),
    ]
    for (a, b) in main_flow:
        x0, y0 = get_xy2(a)
        x1, y1 = get_xy2(b)
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7.5)

    # validation branches
    vx, vy = get_xy2('Validating\nInput')
    # fail → left
    ax.annotate('', xy=(get_xy2('Validation\nFailed')[0], 6.72), xytext=(vx-0.9, vy),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(3.0, 7.2, 'invalid', fontsize=7.5, ha='center')
    # pass → down
    ax.annotate('', xy=(4.5, 6.72), xytext=(vx, vy-0.33),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(4.9, 7.1, 'valid', fontsize=7.5)

    # invalidText() back-transition
    ax.annotate('', xy=(4.5, 10.33), xytext=(1.2, 6.72),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0,
                                connectionstyle='arc3,rad=0.4'))
    ax.text(1.0, 8.5, 'invalidText()\n[re-enter]', fontsize=7, ha='center',
            color=BW, style='italic')

    model_flow = [
        ('Loading\nSentiment Model', 'Analysing\nSentiment'),
        ('Analysing\nSentiment', 'Saving Review\nto Database'),
    ]
    for (a, b) in model_flow:
        x0, y0 = get_xy2(a)
        x1, y1 = get_xy2(b)
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7.5)

    # Saving → two outcomes
    sx, sy = get_xy2('Saving Review\nto Database')
    # positive
    ax.annotate('', xy=(2.5, 3.12), xytext=(sx-0.8, sy-0.33),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(2.8, 3.5, 'positive', fontsize=7.5, ha='center')
    # negative
    ax.annotate('', xy=(6.5, 3.12), xytext=(sx+0.8, sy-0.33),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(6.2, 3.5, 'negative', fontsize=7.5, ha='center')

    # both → response
    rx, ry = get_xy2('Response\nReturned to User')
    ax.annotate('', xy=(rx-0.8, ry+0.33), xytext=(2.5, 2.47),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.annotate('', xy=(rx+0.8, ry+0.33), xytext=(6.5, 2.47),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))

    # response → end
    x0, y0 = get_xy2('Response\nReturned to User')
    x1, y1 = get_xy2('END')
    arrow(ax, x0, y0-0.33, x1, y1+0.32, fontsize=7.5)

    return save_fig(fig)


# ─────────────────────────────────────────────────────────────
# DIAGRAM 6 — Activity: Sentiment Analysis System (3 swimlanes)
# ─────────────────────────────────────────────────────────────
def diagram_sent_activity():
    fig, ax = plt.subplots(figsize=(13, 15))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 15)
    ax.axis('off')
    ax.set_facecolor('white')

    fig.suptitle('Figure 2.3 — Activity Diagram: Sentiment Analysis System',
                 fontsize=11, fontweight='bold', y=0.98)

    lanes = [
        (0.0, 4.0, 'User'),
        (4.0, 8.5, 'Web Server (Django)'),
        (8.5, 13.0, 'Analysis Model'),
    ]
    lane_tops = 14.5
    lane_bot  = 0.2

    for (lx, rx, name) in lanes:
        cx = (lx + rx) / 2
        ax.add_patch(mpatches.FancyBboxPatch((lx+0.05, lane_bot), rx-lx-0.1,
                                              lane_tops-lane_bot,
                                              boxstyle='square,pad=0', lw=1.0,
                                              edgecolor=BW, facecolor='none'))
        ax.add_patch(mpatches.FancyBboxPatch((lx+0.05, 13.8), rx-lx-0.1, 0.65,
                                              boxstyle='square,pad=0', lw=1.0,
                                              edgecolor=BW, facecolor=LTGREY))
        ax.text(cx, 14.12, name, ha='center', va='center', fontsize=9,
                fontweight='bold', color=BW)

    def lc(i): return (lanes[i][0] + lanes[i][1]) / 2

    # Start
    ax.add_patch(plt.Circle((lc(0), 13.3), 0.22, color=BW, zorder=3))
    arrow(ax, lc(0), 13.08, lc(0), 12.68, fontsize=7)

    acts = [
        (0, 12.35, 'Navigate to\nMovie Detail Page'),
        (0, 11.35, 'Fill in Review\nForm'),
        (0, 10.35, 'Click "Submit\nReview"'),
        (1, 10.35, 'Receive POST\nRequest'),
        (1,  9.35, 'Validate\nForm Data'),
        (1,  8.35, 'Valid?'),  # decision
        (0,  7.55, 'Show\nValidation Errors'),
        (2,  8.35, 'Tokenise &\nPreprocess Text'),
        (2,  7.1, 'Load Naive Bayes\nModel (cached)'),
        (2,  5.9, 'Compute Class\nProbabilities'),
        (2,  4.7, 'Return Label +\nConfidence Score'),
        (1,  4.7, 'Save Review &\nSentiment to DB'),
        (1,  3.5, 'Trigger Auto-Retrain?\n[every 50th]'),  # decision
        (2,  3.5, 'Retrain Naive Bayes\n(background thread)'),
        (0,  2.5, 'Display\nSentiment Badge\n& Toast'),
    ]

    act_pos = {}
    for (lane, cy, lbl) in acts:
        cx = lc(lane)
        act_pos[lbl] = (cx, cy)
        if lbl in ('Valid?', 'Trigger Auto-Retrain?\n[every 50th]'):
            diamond(ax, cx, cy, w=2.2, h=0.7)
            ax.text(cx, cy, lbl.split('\n')[0], ha='center', va='center', fontsize=7.5, color=BW)
            if '\n' in lbl:
                ax.text(cx, cy-0.22, lbl.split('\n')[1], ha='center', va='center', fontsize=6.5, color=BW)
        else:
            rounded_rect(ax, cx, cy, 2.8, 0.65, lbl, fontsize=7.5, fill=LTGREY)

    # Flows
    user_top = [
        ('Navigate to\nMovie Detail Page', 'Fill in Review\nForm'),
        ('Fill in Review\nForm', 'Click "Submit\nReview"'),
    ]
    for (a, b) in user_top:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7)

    # cross-lane: click → receive
    arrow(ax, act_pos['Click "Submit\nReview"'][0], act_pos['Click "Submit\nReview"'][1],
          act_pos['Receive POST\nRequest'][0], act_pos['Receive POST\nRequest'][1]+0.33, fontsize=7)

    server_early = [
        ('Receive POST\nRequest', 'Validate\nForm Data'),
        ('Validate\nForm Data', 'Valid?'),
    ]
    for (a, b) in server_early:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.35, fontsize=7)

    # Valid? → No (left to User errors)
    vx, vy = act_pos['Valid?']
    ax.annotate('', xy=(lc(0), 7.88), xytext=(vx-1.1, vy),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(2.5, 8.1, 'No', fontsize=7.5, ha='center')

    # Show errors → re-fill (loop back)
    ax.annotate('', xy=(lc(0), 11.02), xytext=(lc(0), 7.22),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0,
                                connectionstyle='arc3,rad=-0.5'))
    ax.text(0.3, 9.1, 're-enter', fontsize=7, ha='left', style='italic')

    # Valid? → Yes (right to Model)
    ax.annotate('', xy=(lc(2), 8.68), xytext=(vx+1.1, vy),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(7.5, 8.1, 'Yes', fontsize=7.5, ha='center')

    model_flow = [
        ('Tokenise &\nPreprocess Text', 'Load Naive Bayes\nModel (cached)'),
        ('Load Naive Bayes\nModel (cached)', 'Compute Class\nProbabilities'),
        ('Compute Class\nProbabilities', 'Return Label +\nConfidence Score'),
    ]
    for (a, b) in model_flow:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.33, fontsize=7)

    # JOIN BAR — both "Return Label" and a flow from server converge
    join_y = 5.15
    join_x0 = lc(1) - 0.1
    join_x1 = lc(2) + 0.1
    ax.plot([join_x0, join_x1], [join_y, join_y], color=BW, lw=3, zorder=4)
    # Return Label → join
    arrow(ax, lc(2), 4.37, lc(2), join_y, fontsize=7)
    # join → Save Review
    arrow(ax, (join_x0+join_x1)/2, join_y, lc(1), 5.03, fontsize=7)

    server_late = [
        ('Save Review &\nSentiment to DB', 'Trigger Auto-Retrain?\n[every 50th]'),
    ]
    for (a, b) in server_late:
        x0, y0 = act_pos[a]
        x1, y1 = act_pos[b]
        arrow(ax, x0, y0-0.33, x1, y1+0.35, fontsize=7)

    # Trigger → No → Display (cross to user)
    tx, ty = act_pos['Trigger Auto-Retrain?\n[every 50th]']
    ax.annotate('', xy=(lc(0), 2.83), xytext=(tx-1.1, ty),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(3.0, 3.15, 'No', fontsize=7.5, ha='center')

    # Trigger → Yes → retrain
    ax.annotate('', xy=(lc(2), 3.83), xytext=(tx+1.1, ty),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0))
    ax.text(8.7, 3.15, 'Yes', fontsize=7.5, ha='center')

    # Retrain → Display
    ax.annotate('', xy=(lc(0), 2.83), xytext=(lc(2), 3.17),
                arrowprops=dict(arrowstyle='->', color=BW, lw=1.0,
                                connectionstyle='arc3,rad=0.2'))

    # End
    end_x = lc(0)
    end_y = 0.65
    ax.add_patch(plt.Circle((end_x, end_y), 0.22, color=BW, zorder=3))
    ax.add_patch(plt.Circle((end_x, end_y), 0.32, color=BW, fill=False, lw=2, zorder=3))
    arrow(ax, lc(0), act_pos['Display\nSentiment Badge\n& Toast'][1]-0.33, end_x, end_y+0.32, fontsize=7)

    return save_fig(fig)


# ─────────────────────────────────────────────────────────────
# ASSEMBLE WORD DOCUMENT
# ─────────────────────────────────────────────────────────────
def set_a4(doc):
    for section in doc.sections:
        section.page_width  = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin    = Cm(1.5)
        section.bottom_margin = Cm(1.5)
        section.left_margin   = Cm(2.0)
        section.right_margin  = Cm(2.0)

def add_section_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.font.bold = True
    return p

def add_caption(doc, text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.runs[0]
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0, 0, 0)

def add_page_break(doc):
    doc.add_page_break()

def build_docx(diagrams):
    doc = Document()
    set_a4(doc)

    # Cover / title
    t = doc.add_heading('NextReel — UML Diagrams', level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in t.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)

    sub = doc.add_paragraph('Movie Recommendation & Sentiment Analysis System')
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].font.size = Pt(12)
    sub.runs[0].font.color.rgb = RGBColor(0, 0, 0)

    add_page_break(doc)

    entries = [
        ('1  Movie Recommendation System', None),
        ('1.1  Sequence Diagram', 'rec_seq'),
        ('1.2  State Diagram',    'rec_state'),
        ('1.3  Activity Diagram', 'rec_act'),
        ('2  Sentiment Analysis System', None),
        ('2.1  Sequence Diagram', 'sent_seq'),
        ('2.2  State Diagram',    'sent_state'),
        ('2.3  Activity Diagram', 'sent_act'),
    ]

    captions = {
        'rec_seq':   'Figure 1.1 — Sequence Diagram: Movie Recommendation System',
        'rec_state': 'Figure 1.2 — State Diagram: Movie Recommendation System',
        'rec_act':   'Figure 1.3 — Activity Diagram: Movie Recommendation System',
        'sent_seq':  'Figure 2.1 — Sequence Diagram: Sentiment Analysis System',
        'sent_state':'Figure 2.2 — State Diagram: Sentiment Analysis System',
        'sent_act':  'Figure 2.3 — Activity Diagram: Sentiment Analysis System',
    }

    first_diagram = True
    for (heading, key) in entries:
        if key is None:
            # Section heading page (shared with next diagram)
            add_section_heading(doc, heading, level=1)
        else:
            if not first_diagram:
                add_page_break(doc)
            first_diagram = False
            add_section_heading(doc, heading, level=2)
            buf = diagrams[key]
            doc.add_picture(buf, width=Inches(6.2))
            last_para = doc.paragraphs[-1]
            last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_caption(doc, captions[key])

    out_path = r'e:\Projects\Manoj\NextReel\NextReel_UML_Diagrams.docx'
    doc.save(out_path)
    print(f'Saved: {out_path}')
    return out_path


if __name__ == '__main__':
    print('Generating diagram 1/6: Sequence - Recommendation...')
    d1 = diagram_rec_sequence()
    print('Generating diagram 2/6: State - Recommendation...')
    d2 = diagram_rec_state()
    print('Generating diagram 3/6: Activity - Recommendation...')
    d3 = diagram_rec_activity()
    print('Generating diagram 4/6: Sequence - Sentiment...')
    d4 = diagram_sent_sequence()
    print('Generating diagram 5/6: State - Sentiment...')
    d5 = diagram_sent_state()
    print('Generating diagram 6/6: Activity - Sentiment...')
    d6 = diagram_sent_activity()

    diagrams = {
        'rec_seq':   d1,
        'rec_state': d2,
        'rec_act':   d3,
        'sent_seq':  d4,
        'sent_state':d5,
        'sent_act':  d6,
    }

    print('Assembling Word document...')
    path = build_docx(diagrams)
    print('Done.')
