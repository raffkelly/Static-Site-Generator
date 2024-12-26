class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        formatted_props = []
        for prop in self.props:
            formatted_props.append(f'{prop}="{self.props[prop]}"')
        props_string = " " + " ".join(formatted_props)
        return props_string
    
    def __repr__(self):
        return (f"HTMLNode: Tag={self.tag} Value={self.value} Number of Children={len(self.children) if self.children else 0} Props={self.props}")