from jinja2 import Template


def create_html(image_boxes: list, folder_link: str):
    # if the number of files its odd add empty one because table its 2 in each row
    if len(image_boxes) % 2 != 0:
        image_boxes.append('')
    # prepare the data to assume it into the html table by making list of lists, list for each row
    data_to_table = [[image_boxes[i], image_boxes[i+1]] for i in range(0, len(image_boxes), 2)]

    # create the html table
    with open('templates/table_image.html', 'r', encoding='utf-8') as f:
        html_template = Template(f.read())

    html_message = html_template.render(data=data_to_table, folder_link=folder_link)
    return html_message
