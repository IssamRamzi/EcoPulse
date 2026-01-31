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
                    active="exact",
                    className="mx-2 px-3 py-2 rounded-pill",
                    style={
                        "transition": "all 0.2s ease",
                    }
                )
            )

    header = bsp.Navbar(
        bsp.Container(
            [
                # Left side
                html.A(
                    bsp.Row(
                        [
                            bsp.Col(
                                bsp.NavbarBrand(
                                    "Air Pollution Dashboard",
                                    className="fw-semibold"
                                )
                            )
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),

                # Right side - nav links
                bsp.Collapse(
                    bsp.Nav(
                        nav_links, 
                        navbar=True, 
                        className="ms-auto"
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
            fluid=True
        ),
        color="dark",
        dark=True,
        className="mb-4 shadow-sm",
        sticky="top",
        style={"borderBottom": "2px solid #6c757d"}
    )
    
    return header
