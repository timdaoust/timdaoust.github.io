# -*- coding: utf-8 -*-
"""
Generate website based on contents of image directory

This examines given subdirectories, creates a page for each one, and constructs a gallery of all images

To change the website just change the contents of the directories and run 
 
"""
import os
import re
import sys


def mixedcase_to_title(name):
    """Convert mixedCase to Title Case

    Example:
        >>> mixedcase_to_title("mixedCase")
        'Mixed Case'
        >>> mixedcase_to_title("advancedAttributeName")
        'Advanced Attribute Name'

    """
    title_version =  re.sub("([a-z])([A-Z])", "\g<1> \g<2>", name).title()
    s = re.sub(r"[-_]", ' ', title_version)
    return s.upper()


def string_to_class(name):
    return name.replace(" ", "").lower()


def get_image_details(image_directory):
    images = []
    cd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cd)
    image_files = list()
    image_full_subdir = os.path.join(cd, "img", image_directory)

    for base, dirs, fnames in os.walk(image_full_subdir):
        for file in fnames:
            full_path = os.path.join(base, file)
            name, ext = os.path.splitext(file)
            title = mixedcase_to_title(name)
            if not ext in [".jpg", ".png"]:
                continue
            rel_path = os.path.relpath(full_path, cd)
            rel_path = rel_path.replace(os.sep, '/')
            entry = {"image": rel_path, "title": title}
            images.append(entry)
    return images

def on_heroarea(image_directory):
    hero_start = """\
    <section class="hero-area">
        <div class="hero-slides owl-carousel">
"""

    hero_item_text = """\
            <!-- Single Hero Slide -->
            <div class="single-hero-slide bg-img slide-background-overlay" style="background-image: url({image});">
                <div class="container h-100">
                    <div class="row h-100 align-items-end">
                        <div class="col-12">
                            <div class="hero-slides-content">
                                <div class="line"></div>
                                <h2>{title}</h2>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
"""
    hero_item = ""
    images = get_image_details(image_directory)
    for image_entry in images:
        hero_item = hero_item + hero_item_text.format(
            image= image_entry["image"],
            title= image_entry["title"]
        )

    hero_end = """\
        </div>
    </section>
"""
    return "\n\n".join([hero_start, hero_item, hero_end])

gallery_start = """\
    <section class="sonar-projects-area" id="projects">
        <div class="container-fluid">
            <div class="row sonar-portfolio">
"""

gallery_item_text = """\
                <!-- Single gallery Item -->
                <div class="col-12 col-sm-6 col-lg-3 single_gallery_item {category_class} wow fadeInUpBig" data-wow-delay="300ms">
                    <a class="gallery-img" href="{image}"><img src="{image}" alt=""></a>
                    <!-- Gallery Content -->
                    <div class="gallery-content">
                        <h4>{title}</h4>
                        <p>{category}</p>
                    </div>
                </div>	
"""
# Adding this to gallery end might allow more to load - the href is bad, so I'm not sure how
#
#            <div class="row">
#                <div class="col-12 text-center">
#                    <a href="#" class="btn sonar-btn">Load More</a>
#                </div>
#            </div>
gallery_end = """\
        </div>
    </section>
"""

def get_item_text_per_image(item_text, image_directory, category=""):
    gallery_item = ""
    images = get_image_details(image_directory)
    for image_entry in images:
        gallery_item = gallery_item + item_text.format(
            image=image_entry["image"],
            title=image_entry["title"],
            category=category,
            category_class=string_to_class(category)
        )
    return gallery_item

def on_portfolio(image_directory):
    gallery_item = get_item_text_per_image(gallery_item_text, image_directory)
    return "\n\n".join([gallery_start, gallery_item, gallery_end])

def get_subdir_categories(dir):
    cd = os.path.abspath(os.path.dirname(__file__))
    image_full_subdir = os.path.join(cd, "img", dir)
    categories = []
    for base, dirs, fnames in os.walk(image_full_subdir):
        for dir in dirs:
            categories.append(dir)
    return categories

def on_subdir_portfolio(image_directory):
    categories = get_subdir_categories(image_directory)
    gallery_item = ""
    for cat in categories:
        category_item = get_item_text_per_image(gallery_item_text,
                                                image_directory + "\\" + cat,
                                                mixedcase_to_title(cat))
        gallery_item = gallery_item + category_item

    return "\n\n".join([gallery_start, gallery_item, gallery_end])


def subdir_portfolio_controls(image_directory):
    controls_text_header ="""
        <!-- Portfolio Menu -->
        <div class="sonar-portfolio-menu">
            <div class="text-center portfolio-menu">
                <button class="btn active" data-filter="*">All</button>
"""

    control_text_item = """\
                <button class="btn" data-filter=".{filter}">{filterText}</button>
"""
    categories = get_subdir_categories(image_directory)
    control_text_body = ""
    for cat in categories:
        control_text_body = control_text_body + control_text_item.format(
            filter=string_to_class(mixedcase_to_title(cat)),
            filterText=mixedcase_to_title(cat)
        )

    controls_text_footer ="""\
            </div>
        </div>  
"""
    return "\n\n".join([controls_text_header,
                        control_text_body, controls_text_footer])


def on_headerarea(unused):
    header_area_text = """
<header class="header-area">
        <div class="container-fluid">
            <div class="row">
                <div class="col-12">
                    <div class="menu-area d-flex justify-content-between">
                        <!-- Logo Area  -->
                        <div class="logo-area">
                            <a href="index.html">Tim Daoust</a>
                        </div>

                        <div class="menu-content-area d-flex align-items-center">
                            <!-- Header Social Area -->
                            <div class="header-social-area d-flex align-items-center">
                                <a href="https://www.instagram.com/digitalcoffeeink/" data-toggle="tooltip" data-placement="bottom" title="Instagram"><i class="fa fa-instagram" aria-hidden="true"></i></a>
                            </div>
                            <!-- Menu Icon -->
                            <span class="navbar-toggler-icon" id="menuIcon"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>    
"""
    return header_area_text

def on_menuarea(unused):
    menu_area_text = """
    <div class="mainMenu d-flex align-items-center justify-content-between">
        <!-- Close Icon -->
        <div class="closeIcon">
            <i class="ti-close" aria-hidden="true"></i>
        </div>
        <!-- Logo Area -->
        <div class="logo-area">
            <a href="index.html">Tim Daoust</a>
        </div>
        <!-- Nav -->
        <div class="sonarNav wow fadeInUp" data-wow-delay="1s">
            <nav>
                <ul>
                    <li class="nav-item active">
                        <a class="nav-link" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="about-me.html">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="services.html">Services</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="portfolio.html">Portfolio</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="contact.html">Contact</a>
                    </li>
                </ul>
            </nav>
        </div>
        <!-- Copwrite Text -->
        <div class="copywrite-text">
            <p><!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
 Site template by <a href="https://colorlib.com" target="_blank">Colorlib</a> under <a href="https://creativecommons.org/licenses/by-nc/3.0/us/" target="_blank">CC3</a>.  
<!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
</p>
        </div>
    </div>
    """
    return menu_area_text

def on_footer_area(unused):
    footer_area_text = """
    <footer class="footer-area">
        <!-- back end content -->
        <div class="backEnd-content">
            <img class="dots" src="img/core-img/dots.png" alt="">
        </div>
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <!-- Copywrite Text -->
                    <div class="copywrite-text">
                        <p><!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
Site template by <a href="https://colorlib.com" target="_blank">Colorlib</a> under <a href="https://creativecommons.org/licenses/by-nc/3.0/us/" target="_blank">CC3</a>.  
<!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
</p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
    """
    return footer_area_text

def on_template(template):
    definition = template.strip("{{").rstrip().rstrip("}}")
    try:
        key, value = definition.split(":")
    except ValueError:
        key = definition
        value = ""

    if key == "heroarea":
        return on_heroarea(value)
    elif key == "portfolio":
        return on_portfolio(value)
    elif key == "subdir_portfolio_controls":
        return subdir_portfolio_controls(value)
    elif key == "subdir_portfolio":
        return on_subdir_portfolio(value)
    elif key == "headerarea":
        return on_headerarea(value)
    elif key == "footerarea":
        return on_footer_area(value)
    elif key == "menuarea":
        return on_menuarea(value)
    else:
        raise ValueError("Unsupported template: %s" % key)

    return template


def parse(fname):
    parsed = list()

    with open(fname) as f:
        line_no = 0
        for line in f:
            line_no += 1

            if line_no == 1 and line.startswith("build: false"):
                print("Skipping '%s'.." % fname)
                parsed = f.read()
                break

            if line.startswith("{{"):
                line = on_template(line)
                parsed.append(line)
            else:
                parsed.append(line)

    return "".join(parsed)


if __name__ == '__main__':
    import os
    import argparse

    cd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cd)

    template_files = list()
    for base, dirs, fnames in os.walk("."):
        for fname in fnames:
            name, ext = os.path.splitext(fname)
            if ext != ".template":
                continue

            src = os.path.join(base, fname)

            template_files.append(src)

    results = list()
    for src in template_files:
        print("Building '%s'.." % src)
        dst = src.replace(".template", "")
        parsed = parse(src)
        with open(dst, "w") as f:
            f.write(parsed)
