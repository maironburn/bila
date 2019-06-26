from src.models import elemento


def get_type_from_filename(filename):
    '''extract name until first _ cause it defines class type'''
    return filename.split('_')[0].capitalize()


def get_element_name_from_filename(filename):
    '''element name without extension neither type'''
    return filename[0:filename.index('.')][filename.index('_') + 1:]


def dinamic_instance_elements(element_type, init_values):
    '''instantiating attending to element_type (inferred by the filename first _  )'''
    try:
        # getattr(module, class_name)
        element_type = getattr(elemento, element_type)
        return element_type(init_values)

    except Exception as e:
        pass
    return None
