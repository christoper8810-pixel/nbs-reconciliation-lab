"""Start NBS Mapping Control with Mapping Studio (and the separate TB reconciliation) registered.

    python -m nbs_control.studio_app [--port 8765]

Works whether or not nbs_control/web.py registers the Studio itself (for example when the update could only
add files to a locally modified installation): the existing application is created unchanged and the Studio
routes are added only if they are not already present.
"""
from __future__ import annotations

import argparse


def build_app(service=None, export_dir=None):
    from . import EXPORT_DIR
    from .web import create_app
    if service is None:
        from .service import ControlService
        service = ControlService()
    app = create_app(service, export_dir or EXPORT_DIR)
    root = service.config_dir.parent
    if 'studio_home' not in app.view_functions:
        from .studio.web import register_studio_routes
        register_studio_routes(app, root)
    if 'tb_home' not in app.view_functions:
        from .tbrecon.web import register_tb_routes
        register_tb_routes(app, root)
    return app


def main(argv=None):
    ap = argparse.ArgumentParser(description='NBS Mapping Control with Mapping Studio')
    ap.add_argument('--port', type=int, default=8765)
    a = ap.parse_args(argv)
    app = build_app()
    print(f'Mapping Studio: http://127.0.0.1:{a.port}/studio  (local only, Ctrl+C to stop)')
    app.run(host='127.0.0.1', port=a.port, debug=False)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
