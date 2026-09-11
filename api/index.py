import os
import sys
import traceback

# Ensure project root is on Python module search path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    # Import Starlette ASGI application from server
    from server import app
except Exception as exc:
    tb = traceback.format_exc()
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    async def init_error_handler(request):
        return JSONResponse(
            {
                "status": "error",
                "message": "AeroGuardian AI API initialization failed on Vercel.",
                "error": str(exc),
                "traceback": tb,
            },
            status_code=500,
        )

    app = Starlette(routes=[Route("/{rest_of_path:path}", init_error_handler)])
