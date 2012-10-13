
LEVEL = {
    'default'       : {
        'value'                 : 10,
        'cart'                  : False,
        'user_content'          : False,
        'blog'                  : False,
        'max_product_category'  : 1,
        'max_product'           : 5,
        'max_file_size'         : 100 * 1024,
        'max_files'             : 5,
    },
    
    'standard'      : {
        'value'                 : 50,
        'max_product_category'  : 3,
        'max_product'           : 15,
        'max_files'             : 20,        
    },
    
    'professional'  : {
        'value'                 : 100,
        'cart'                  : True, 
        'max_product_category'  : 10,
        'max_product'           : 50,
        'max_file_size'         : 300 * 1024,
        'max_files'             : 60,
    },
    
    'enterprise'    : {
        'value'                 : 200,
        'cart'                  : True,
        'user_content'          : True,
        'blog'                  : True,        
        'max_product_category'  : 100,
        'max_product'           : 500,
        'max_file_size'         : 600 * 1024,
        'max_files'             : 600,
    },
}

def res(level):
    if not level or level not in LEVEL.keys(): 
        lvl = 'default'
    else:
        lvl = level
    #
    try:
        ret = LEVEL[lvl]
    except:
        return None
    #
    default = LEVEL['default']
    for k in default.keys():
        if not ret.has_key(k):
            ret[k] = default[k]
    #
    return ret
