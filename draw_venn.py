from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3, venn2_circles, venn3_circles
import traceback
import re
import warnings
warnings.filterwarnings("ignore")


def color_regions(venn_diagram, regions, color):
    for region in regions:
        venn_diagram.get_patch_by_id(region).set_color(color)

def _set_region_text(venn_diagram, region, elements):
    if elements:
        venn_diagram.get_label_by_id(region).set_text(str(elements))
    else:
        venn_diagram.get_label_by_id(region).set_text('')


def set_region_text(venn_diagram, region, text):
    venn_diagram.get_label_by_id(region).set_text(text)


def _get_arg_names(stack):
    _, _, _, code = stack[-2]
    args = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
    arg_names = tuple([x.strip() for x in args.split(',')])
    return arg_names

def draw_venn(s1, s2=None, s3=None):
    warnings.filterwarnings("ignore")
    stack = traceback.extract_stack()
    set_names = _get_arg_names(stack)
    
    if not s2:
        c = _draw_venn1(s1, set_names[0])
        return c
    i12 = s1 & s2
    
    if not s3:
        d12 = s1 - s2
        d21 = s2 - s1
        v = venn2([s1, s2], set_names)
        color_regions(v, ['10', '11', '01'], 'white')
        _set_region_text(v, '10', d12)
        _set_region_text(v, '01', d21)
        _set_region_text(v, '11', i12)
        venn2_circles([s1, s2], linestyle='solid')
    else:
        i23 = s2 & s3
        i13 = s1 & s3
        u12 = s1 | s2
        u23 = s2 | s3
        u13 = s1 | s3
        d123 = s1 - u23
        d213 = s2 - u13
        d312 = s3 - u12
        i123 = i12 & s3
        v = venn3([s1, s2, s3], set_names)
        regions = [
            '100',
            '110',
            '010',
            '010',
            '011',
            '001',
            '111',
            '101',
        ]
        color_regions(v, regions, 'white')
        _set_region_text(v, '100', d123)
        _set_region_text(v, '110', i12)
        _set_region_text(v, '111', i123)
        _set_region_text(v, '101', i13)
        _set_region_text(v, '011', i23)
        _set_region_text(v, '010', d213)
        _set_region_text(v, '001', d312)
        venn3_circles([s1, s2, s3], linestyle='solid')

    return v

def plot_venn(tittle):
    plt.title(tittle, fontsize=14)
    ax = plt.gca()
    ax.set_axis_on()
    ax.text(0.95, 0.95, r'$\mathbb{U}$',
        horizontalalignment='right',
        verticalalignment='top',
        transform=ax.transAxes)    
    plt.tight_layout()
    plt.show()




def _label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)

def _draw_venn1(set_values, set_name):
    ax = plt.gca()
    ax.set_xlim((0,1))
    ax.set_ylim((0,1))
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    circle1 = plt.Circle((.5,.5),.25,color='black',fill=False)
    _label( (0.5, .25), set_name)
    elements = str(set_values) if set_values else ""
    plt.text(0.5, 0.5, elements, ha="center", family='sans-serif', size=14)
    ax.add_artist(circle1)
    return circle1

if __name__ == '__main__':
    G = {r'$s_{11}$', r'$s_{12}$', r'$s_{13}$'}
    B = {r'$s_{21}$', r'$s_{22}$', r'$s_{13}$'}
    T = {r'$s_{31}$', r'$s_{13}$', r'$s_{22}$'}
    v = draw_venn(G, B, T)
    set_region_text(v, '111', r'$G \cap B \cap T = \{s_{13}\}$')
    set_region_text(v, '100', r'$G - B \cup T = \{s_{11}, s_{12}\}$')
    set_region_text(v, '010', r'$B - G \cup T = \{s_{21}\}$')
    set_region_text(v, '001', r'$T - G \cup B = \{s_{31}\}$')
    set_region_text(v, '101', r'$G \cap T = \{s_{13}\}$')
    set_region_text(v, '110', r'$G \cap B = \{s_{13}\}$')
    set_region_text(v, '011', r'$T \cap B = \{s_{13}, s_{22}\}$')
    plot_venn('')