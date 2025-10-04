"""Frontend Integration Endpoints - Three.js and React Integration"""

from fastapi import APIRouter, HTTPException, Depends, Request
from src.api.contract_v2 import load_spec, generate_preview_url
from src.api.threejs_integration import transform_to_three_js, generate_react_three_fiber_code
from src.services.preview_manager_v2 import preview_manager
from src.core.auth import get_current_user
from datetime import datetime, timezone
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/api/v1/three-js/{spec_id}")
@limiter.limit("20/minute")
async def get_three_js_data(request: Request, spec_id: str, user=Depends(get_current_user)):
    """Get Three.js compatible JSON data for frontend rendering"""
    try:
        # Load spec data
        spec_data = await load_spec(spec_id)
        if not spec_data:
            raise HTTPException(status_code=404, detail="Spec not found")
        
        # Transform to Three.js format
        three_js_data = transform_to_three_js(spec_data)
        
        # Get current preview URL
        preview_url = await generate_preview_url(spec_id)
        
        return {
            "success": True,
            "spec_id": spec_id,
            "three_js_data": three_js_data,
            "preview_url": preview_url,
            "last_updated": spec_data.get('version', {}).get('modified_at'),
            "message": "Three.js data ready for frontend"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Three.js data generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/react-three-fiber/{spec_id}")
@limiter.limit("10/minute")
async def get_react_three_fiber_code(request: Request, spec_id: str, user=Depends(get_current_user)):
    """Generate React Three Fiber component code"""
    try:
        # Load spec and transform to Three.js
        spec_data = await load_spec(spec_id)
        if not spec_data:
            raise HTTPException(status_code=404, detail="Spec not found")
        
        three_js_data = transform_to_three_js(spec_data)
        
        # Generate React component code
        component_code = generate_react_three_fiber_code(spec_id, three_js_data)
        
        return {
            "success": True,
            "spec_id": spec_id,
            "component_code": component_code,
            "dependencies": [
                "@react-three/fiber",
                "@react-three/drei",
                "three"
            ],
            "message": "React Three Fiber component generated"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/preview/refresh")
@limiter.limit("10/minute")
async def refresh_preview_and_threejs(request: Request, refresh_data: dict, user=Depends(get_current_user)):
    """Force refresh preview and Three.js data after spec changes"""
    try:
        spec_id = refresh_data.get('spec_id')
        if not spec_id:
            raise HTTPException(status_code=400, detail="spec_id required")
        
        # Get updated spec data
        spec_data = await load_spec(spec_id)
        if not spec_data:
            raise HTTPException(status_code=404, detail="Spec not found")
        
        # Refresh preview URL
        new_preview_url = await preview_manager.refresh_preview(spec_id, spec_data)
        
        # Generate fresh Three.js data
        three_js_data = transform_to_three_js(spec_data)
        
        return {
            "success": True,
            "spec_id": spec_id,
            "preview_url": new_preview_url,
            "three_js_data": three_js_data,
            "refreshed_at": datetime.now(timezone.utc).isoformat(),
            "message": "Preview and Three.js data refreshed"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Preview refresh failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/viewer/{spec_id}")
async def get_html_viewer(spec_id: str):
    """Get HTML viewer for spec preview"""
    try:
        # Load spec data
        spec_data = await load_spec(spec_id)
        if not spec_data:
            raise HTTPException(status_code=404, detail="Spec not found")
        
        # Generate HTML viewer
        viewer_html = preview_manager.generate_viewer_html(spec_data)
        
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=viewer_html)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))