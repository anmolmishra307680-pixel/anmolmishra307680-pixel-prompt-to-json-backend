#!/usr/bin/env python3
"""Preview generation with Three.js viewer compatibility"""

import json
import base64
from typing import Dict, Any, List
from datetime import datetime
from src.storage.bucket_storage import bucket_storage

class PreviewGenerator:
    """Generate previews and Three.js compatible data"""
    
    def __init__(self):
        self.default_materials = {
            "wood": {"color": "#8B4513", "roughness": 0.8, "metalness": 0.0},
            "metal": {"color": "#C0C0C0", "roughness": 0.2, "metalness": 0.9},
            "glass": {"color": "#87CEEB", "roughness": 0.0, "metalness": 0.0, "transparent": True, "opacity": 0.3},
            "concrete": {"color": "#808080", "roughness": 0.9, "metalness": 0.0},
            "marble": {"color": "#F8F8FF", "roughness": 0.1, "metalness": 0.0},
            "fabric": {"color": "#DDA0DD", "roughness": 0.9, "metalness": 0.0},
            "plastic": {"color": "#FF6347", "roughness": 0.5, "metalness": 0.0}
        }
    
    async def generate_preview(self, spec_data: Dict[str, Any]) -> str:
        """Generate preview image and return signed URL"""
        spec_id = spec_data.get('spec_id', f"preview_{int(datetime.now().timestamp())}")
        
        # Generate mock preview image (in production, this would render actual 3D scene)
        preview_data = self._generate_mock_preview(spec_data)
        
        # Upload to bucket storage
        signed_url = await bucket_storage.upload_preview(spec_id, preview_data)
        
        return signed_url
    
    def _generate_mock_preview(self, spec_data: Dict[str, Any]) -> bytes:
        """Generate mock preview image data"""
        # Simple base64 encoded 1x1 pixel image for demo
        # In production, this would use a 3D rendering engine
        pixel_data = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77zgAAAABJRU5ErkJggg=="
        )
        return pixel_data
    
    def format_for_threejs(self, spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format specification data for Three.js viewer"""
        objects = spec_data.get('objects', [])
        
        # Convert objects to Three.js format
        threejs_objects = []
        for obj in objects:
            threejs_obj = self._convert_object_to_threejs(obj)
            threejs_objects.append(threejs_obj)
        
        # Create scene configuration
        scene_config = {
            "scene": {
                "background": "#f0f0f0",
                "fog": {"color": "#f0f0f0", "near": 1, "far": 1000}
            },
            "camera": {
                "type": "PerspectiveCamera",
                "fov": 75,
                "aspect": 16/9,
                "near": 0.1,
                "far": 1000,
                "position": {"x": 10, "y": 10, "z": 10},
                "lookAt": {"x": 0, "y": 0, "z": 0}
            },
            "lights": [
                {
                    "type": "AmbientLight",
                    "color": "#404040",
                    "intensity": 0.4
                },
                {
                    "type": "DirectionalLight",
                    "color": "#ffffff",
                    "intensity": 0.8,
                    "position": {"x": 10, "y": 10, "z": 5}
                }
            ],
            "objects": threejs_objects,
            "controls": {
                "type": "OrbitControls",
                "enableDamping": True,
                "dampingFactor": 0.05
            }
        }
        
        return scene_config
    
    def _convert_object_to_threejs(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Convert object to Three.js format"""
        obj_type = obj.get('type', 'box')
        material_type = obj.get('material', 'standard')
        
        # Get material properties
        material_props = self.default_materials.get(material_type, self.default_materials['wood'])
        
        # Override with object properties
        if 'properties' in obj:
            if 'color' in obj['properties']:
                material_props = material_props.copy()
                material_props['color'] = self._color_name_to_hex(obj['properties']['color'])
        
        # Determine geometry based on object type
        geometry = self._get_geometry_for_type(obj_type, obj.get('dimensions', {}))
        
        # Create Three.js object
        threejs_obj = {
            "id": obj.get('id', f"obj_{obj_type}"),
            "type": "Mesh",
            "geometry": geometry,
            "material": {
                "type": "MeshStandardMaterial",
                **material_props
            },
            "position": obj.get('position', {"x": 0, "y": 0, "z": 0}),
            "rotation": obj.get('rotation', {"x": 0, "y": 0, "z": 0}),
            "scale": obj.get('scale', {"x": 1, "y": 1, "z": 1}),
            "userData": {
                "editable": obj.get('editable', True),
                "originalType": obj_type,
                "materialType": material_type
            }
        }
        
        return threejs_obj
    
    def _get_geometry_for_type(self, obj_type: str, dimensions: Dict[str, Any]) -> Dict[str, Any]:
        """Get Three.js geometry for object type"""
        width = dimensions.get('width', 1)
        height = dimensions.get('height', 1)
        depth = dimensions.get('depth', 1)
        
        if obj_type in ['floor', 'wall', 'ceiling']:
            return {
                "type": "BoxGeometry",
                "parameters": [width, height, depth]
            }
        elif obj_type in ['window', 'door']:
            return {
                "type": "PlaneGeometry",
                "parameters": [width, height]
            }
        elif obj_type in ['chair', 'table']:
            return {
                "type": "BoxGeometry",
                "parameters": [width, height, depth]
            }
        elif obj_type == 'cushion':
            return {
                "type": "SphereGeometry",
                "parameters": [max(width, height, depth) / 2, 16, 16]
            }
        else:
            # Default to box
            return {
                "type": "BoxGeometry",
                "parameters": [width, height, depth]
            }
    
    def _color_name_to_hex(self, color_name: str) -> str:
        """Convert color name to hex code"""
        color_map = {
            "red": "#FF0000",
            "blue": "#0000FF",
            "green": "#00FF00",
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "purple": "#800080",
            "pink": "#FFC0CB",
            "brown": "#A52A2A",
            "black": "#000000",
            "white": "#FFFFFF",
            "gray": "#808080",
            "grey": "#808080"
        }
        return color_map.get(color_name.lower(), "#808080")
    
    def generate_viewer_html(self, spec_data: Dict[str, Any]) -> str:
        """Generate HTML for Three.js viewer"""
        threejs_data = self.format_for_threejs(spec_data)
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>BHIV 3D Viewer</title>
    <style>
        body {{ margin: 0; overflow: hidden; background: #f0f0f0; }}
        #viewer {{ width: 100vw; height: 100vh; }}
        #controls {{ position: absolute; top: 10px; left: 10px; z-index: 100; }}
        .control-btn {{ margin: 5px; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }}
    </style>
</head>
<body>
    <div id="viewer"></div>
    <div id="controls">
        <button class="control-btn" onclick="resetCamera()">Reset View</button>
        <button class="control-btn" onclick="toggleWireframe()">Wireframe</button>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <script>
        const sceneData = {json.dumps(threejs_data, indent=2)};
        
        // Initialize Three.js scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(sceneData.scene.background);
        
        // Camera
        const camera = new THREE.PerspectiveCamera(
            sceneData.camera.fov,
            window.innerWidth / window.innerHeight,
            sceneData.camera.near,
            sceneData.camera.far
        );
        camera.position.set(
            sceneData.camera.position.x,
            sceneData.camera.position.y,
            sceneData.camera.position.z
        );
        
        // Renderer
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.getElementById('viewer').appendChild(renderer.domElement);
        
        // Controls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = sceneData.controls.enableDamping;
        controls.dampingFactor = sceneData.controls.dampingFactor;
        
        // Lights
        sceneData.lights.forEach(lightData => {{
            let light;
            if (lightData.type === 'AmbientLight') {{
                light = new THREE.AmbientLight(lightData.color, lightData.intensity);
            }} else if (lightData.type === 'DirectionalLight') {{
                light = new THREE.DirectionalLight(lightData.color, lightData.intensity);
                if (lightData.position) {{
                    light.position.set(lightData.position.x, lightData.position.y, lightData.position.z);
                }}
                light.castShadow = true;
            }}
            if (light) scene.add(light);
        }});
        
        // Objects
        sceneData.objects.forEach(objData => {{
            const geometry = createGeometry(objData.geometry);
            const material = createMaterial(objData.material);
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.set(objData.position.x, objData.position.y, objData.position.z);
            mesh.rotation.set(objData.rotation.x, objData.rotation.y, objData.rotation.z);
            mesh.scale.set(objData.scale.x, objData.scale.y, objData.scale.z);
            mesh.userData = objData.userData;
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            
            scene.add(mesh);
        }});
        
        function createGeometry(geomData) {{
            switch(geomData.type) {{
                case 'BoxGeometry':
                    return new THREE.BoxGeometry(...geomData.parameters);
                case 'SphereGeometry':
                    return new THREE.SphereGeometry(...geomData.parameters);
                case 'PlaneGeometry':
                    return new THREE.PlaneGeometry(...geomData.parameters);
                default:
                    return new THREE.BoxGeometry(1, 1, 1);
            }}
        }}
        
        function createMaterial(matData) {{
            const material = new THREE.MeshStandardMaterial({{
                color: matData.color,
                roughness: matData.roughness || 0.5,
                metalness: matData.metalness || 0.0
            }});
            
            if (matData.transparent) {{
                material.transparent = true;
                material.opacity = matData.opacity || 1.0;
            }}
            
            return material;
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        
        function resetCamera() {{
            camera.position.set(10, 10, 10);
            camera.lookAt(0, 0, 0);
            controls.reset();
        }}
        
        function toggleWireframe() {{
            scene.traverse(child => {{
                if (child.isMesh) {{
                    child.material.wireframe = !child.material.wireframe;
                }}
            }});
        }}
        
        // Handle window resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
        
        animate();
    </script>
</body>
</html>
        """
        
        return html_template.strip()

# Global instance
preview_generator = PreviewGenerator()

# Legacy function for backward compatibility
def generate_preview(spec_data: Dict[str, Any]) -> str:
    """Legacy function for backward compatibility"""
    import asyncio
    return asyncio.run(preview_generator.generate_preview(spec_data))