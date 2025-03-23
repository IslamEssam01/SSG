from generate_website import copy_dir_to, generate_pages


def main():
    copy_dir_to("static", "public")
    generate_pages("content", "template.html", "public")


if __name__ == "__main__":
    main()
