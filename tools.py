def block(route):
    resource_type=route.request.resource_type
    if resource_type in ['image','font','media']:
        route.abort()
    else:
        route.continue_()

def cleanup(spec:str):
    words=['Gaming','Laptop','Notebook','GPU','RAM','Nvidia','SSD','Processor','Storage','GeForce','DDR5','NVIDIA','GDDR6','GDDR7','Graphics']
    if spec==None:
        return None
    for word in words:
        spec=spec.replace(word,'')
    return ' '.join(spec.split())
