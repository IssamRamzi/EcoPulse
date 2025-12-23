import dash
from dash import html
import dash_bootstrap_components as bsp


def create_header():
    
    nav_links = []
    for page in dash.page_registry.values():
        if page['path'] and page['name']:
            nav_links.append(
                bsp.NavLink(
                    page['name'], 
                    href=page['path'], 
                    active="exact", # met le label page en brillance si celle ci est activé
                    className="mx-2" 
                )
            )

    
    header = bsp.Navbar(
        bsp.Container(
            [
                # partie gauche de la navbar
                html.A(
                    
                    bsp.Row(
                        [
                            bsp.Col(bsp.NavbarBrand("Pollution Data Analysis", className="ms-2")),
                        ],
                        align="center",
                        className="g-0", 
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                
                # partie droite de la navbar
                bsp.Nav(
                    nav_links, 
                    navbar=True, 
                    className="ms-auto" 
                ),
            ],
            fluid=True 
        ),

        # params de la navbar
        color="dark",
        dark=True, 
        className="mb-4 shadow-sm", 
        sticky="top" 
    )
    
    return header
