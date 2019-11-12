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

def get_image_details(image_directory):
    images = []
    cd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cd)
    image_files = list()
    image_full_subdir = os.path.join(cd, "img", "portfolio-img",
                                     image_directory)

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
                                <p> Details about this image</p>
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


def on_portfolio(image_directory):

    gallery_start = """\
    <section class="sonar-projects-area" id="projects">
        <div class="container-fluid">
            <div class="row sonar-portfolio">
"""

    gallery_item_text = """\
                <!-- Single gallery Item -->
                <div class="col-12 col-sm-6 col-lg-3 single_gallery_item landscapes studio wow fadeInUpBig" data-wow-delay="300ms">
                    <a class="gallery-img" href="{image}"><img src="{image}" alt=""></a>
                    <!-- Gallery Content -->
                    <div class="gallery-content">
                        <h4>{title}</h4>
                        <p>Landscapes</p>
                    </div>
                </div>	
"""
    gallery_item = ""
    images = get_image_details(image_directory)
    for image_entry in images:
        gallery_item = gallery_item + gallery_item_text.format(
            image= image_entry["image"],
            title= image_entry["title"]
        )
    gallery_end = """\
            <div class="row">
                <div class="col-12 text-center">
                    <a href="#" class="btn sonar-btn">Load More</a>
                </div>
            </div>
        </div>
    </section>
"""
    return "\n\n".join([gallery_start, gallery_item, gallery_end])

def on_template(template):
    definition = template.strip("{{").rstrip().rstrip("}}")
    key, value = definition.split(":")

    if key == "heroarea":
        return on_heroarea(value)
    elif key == "portfolio":
        return on_portfolio(value)
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
