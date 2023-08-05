import streamlit.components.v1 as components
import os

_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_ant_tree",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_ant_tree", path=build_dir)

def st_ant_tree(treeData:list = [], allowClear:bool = True, bordered:bool = True, max_height:int = 400, width_dropdown: str = "90%", disabled:bool = False, 
    	dropdownStyle: str = "{}", filterTreeNode: bool = True, multiple: bool = False, placeholder: str = "Choose an option",
        placement: str  = "bottomLeft",showArrow: bool = True, showSearch: bool = True, treeCheckable: bool = True, treeDefaultExpandAll: bool = False,
        treeDefaultExpandedKeys: list = [], treeLine: bool = True, onChange: str = "", onSelect: str = "", onSearch: str = "", defaultValue = None, onTreeExpand: str = "", onTreeLoad:str = "", min_height_dropdown: int = 100,
        maxTagCount:int= False, key = "first_tree") -> int:
    """

    Parameters
    ----------
    treeData : list of dict (default = [])
        The data of the tree. The data should be in the form of a list of dictionaries.
    allowClear : bool (default = True)
        Whether allow clear.
    bordered : bool (default = True)
        Whether show border.
    max_height : int (default = 400)
        The max height of the dropdown.
    width_dropdown : int (default = "100%")
        The width of the dropdown.
    disabled : bool (default = False)
        Whether the dropdown is disabled.
    dropdownStyle : str (default = "{}")
        The style of the dropdown.
    filterTreeNode : bool (default = True)
        Whether filter tree node.
    multiple : bool (default = False)  
        Whether allow multiple selection. --> Immer True wenn checkable = True
    placeholder : str (default = "Choose an option")
        The placeholder of the dropdown.
    placement : str (default = "bottomLeft")
        The placement of the dropdown.
    showArrow : bool (default = True)
        Whether show arrow.
    showSearch : bool (default = True)
        Whether show search.
    treeCheckable : bool (default = True)
        Whether tree node can be checked.
    treeDefaultExpandAll : bool (default = False)
        Whether default expand all tree nodes.
    treeDefaultExpandedKeys : list (default = [])
        The keys of the default expanded tree nodes.
    treeLine : bool (default = True)
        Whether show tree node line.
    onChange : str (default = "")
        The callback function when the value of the dropdown changes.
    onSelect : str (default = "")
        The callback function when a tree node is selected.
    onSearch : str (default = "")
        The callback function when the search input changes.
    defaultValue : str (default = None)
        The default value of the dropdown.
    onTreeExpand : str (default = "")
        The callback function when a tree node is expanded.
    onTreeLoad : str (default = "")
        The callback function when a tree node is loaded.
    min_height_dropdown : int (default = 100)
        The min height of the dropdown.
    key : str (default = "first_tree")
        The key of the dropdown.






        


    """

    component_value = _component_func(treeData = treeData, allowClear = allowClear, bordered = bordered, max_height = max_height, width_dropdown = width_dropdown, disabled = disabled,
        dropdownStyle = dropdownStyle, filterTreeNode = filterTreeNode, multiple = multiple, placeholder = placeholder,
        placement = placement, showArrow = showArrow, showSearch = showSearch, treeCheckable = treeCheckable, treeDefaultExpandAll = treeDefaultExpandAll,
        treeDefaultExpandedKeys = treeDefaultExpandedKeys, treeLine = treeLine, on_change = onChange, on_celect = onSelect, on_search = onSearch, default= defaultValue, defaultValue = defaultValue, min_height_dropdown = min_height_dropdown, onTreeExpand = onTreeExpand,
        onTreeLoad = onTreeLoad, maxTagCount = maxTagCount,key = key)

    return component_value
