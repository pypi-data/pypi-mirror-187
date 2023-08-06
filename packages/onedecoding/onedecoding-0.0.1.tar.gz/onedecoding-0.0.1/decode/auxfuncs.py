def bitmap(struct_id, structs, dtypes, bit_sizes):
    if not isinstance(struct_id, str):
        struct_id = str(struct_id)

    variables = structs[struct_id]
    dt = [dtypes[v] for v in variables]
    bs = [bit_sizes[d] for d in dt]
    return {
        v: (d, b) for v, d, b in zip(variables, dt, bs)
    }
    

def create_values_dict(values, names):
    spl = {var: val for var, val in zip(names, values)}
    return spl
