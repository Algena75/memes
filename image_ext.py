import mimetypes


def main():
    """files_ext.txt creation"""
    types_map = mimetypes.types_map
    image_ext = list()
    for item in types_map.items():
        ext, descr = tuple(item)
        descr = descr.split('/')[0]
        if descr == 'image':
            image_ext.append(ext[1:])
    print(image_ext)


if __name__ == '__main__':
    main()
